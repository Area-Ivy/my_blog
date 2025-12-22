import logging
import os
import re
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Sequence
from urllib.parse import urlparse

from opensearchpy import OpenSearch, RequestsHttpConnection, helpers

try:
    # When backend is a package
    from .models import Article as ArticleModel
except ImportError:  # pragma: no cover
    from models import Article as ArticleModel


logger = logging.getLogger(__name__)

ARTICLES_INDEX = os.getenv("ES_ARTICLES_INDEX", "articles")
ES_URL = os.getenv("ES_URL")
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


class SearchNotConfiguredError(RuntimeError):
    """Raised when ES_URL is missing and search should be treated as disabled."""


def _parse_es_url(url: str) -> Dict[str, Any]:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("ES_URL must include scheme and hostname, e.g. https://user:pass@host:port")

    use_ssl = parsed.scheme == "https"
    port = parsed.port or (443 if use_ssl else 80)

    http_auth: Optional[Sequence[str]] = None
    if parsed.username:
        http_auth = (parsed.username, parsed.password or "")

    return {
        "hosts": [{"host": parsed.hostname, "port": port}],
        "http_auth": http_auth,
        "use_ssl": use_ssl,
        "verify_certs": os.getenv("ES_VERIFY_CERTS", "true").lower() == "true",
        "ssl_assert_hostname": os.getenv("ES_ASSERT_HOSTNAME", "false").lower() == "true",
        "ca_certs": os.getenv("ES_CA_CERT"),
        "connection_class": RequestsHttpConnection,
    }


@lru_cache(maxsize=1)
def get_search_client() -> OpenSearch:
    if not ES_URL:
        raise SearchNotConfiguredError("ES_URL is not configured; skipping search integration.")

    kwargs = _parse_es_url(ES_URL)
    # Remove None values (e.g., no auth or ca cert provided)
    clean_kwargs = {k: v for k, v in kwargs.items() if v not in (None, (), [], "")}
    return OpenSearch(**clean_kwargs)


def article_to_doc(article: ArticleModel) -> Dict[str, Any]:
    tags = article.tags or ""
    content_plain = markdown_to_plain_text(article.content or "")
    return {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "summary": article.summary or "",
        "content": content_plain,
        "tags": tags,
        "created_at": (article.created_at.isoformat() if article.created_at else None),
        "updated_at": (article.updated_at.isoformat() if article.updated_at else None),
    }


def ensure_article_index() -> None:
    """
    Create the articles index with a sensible mapping if it doesn't exist yet.
    Safe to call multiple times.
    """
    client = get_search_client()
    if client.indices.exists(index=ARTICLES_INDEX):
        return

    body = {
        "settings": {
            "analysis": {
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 2,
                        "max_gram": 3,
                        "token_chars": ["letter", "digit", "punctuation", "symbol"],
                    }
                },
                "analyzer": {
                    "text_zh": {
                        "type": "custom",
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"],
                    },
                    "text_zh_search": {
                        "type": "custom",
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"],
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "analyzer": "text_zh",
                    "search_analyzer": "text_zh_search",
                    "fields": {"raw": {"type": "keyword", "ignore_above": 256}},
                },
                "summary": {
                    "type": "text",
                    "analyzer": "text_zh",
                    "search_analyzer": "text_zh_search",
                },
                "content": {
                    "type": "text",
                    "analyzer": "text_zh",
                    "search_analyzer": "text_zh_search",
                },
                "tags": {
                    "type": "text",
                    "analyzer": "text_zh",
                    "search_analyzer": "text_zh_search",
                    "fields": {"raw": {"type": "keyword", "ignore_above": 256}},
                },
                "slug": {"type": "keyword"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
            }
        },
    }

    client.indices.create(index=ARTICLES_INDEX, body=body)
    logger.info("Created OpenSearch index '%s'", ARTICLES_INDEX)


def search_articles(query: str, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []

    client = get_search_client()
    size = min(max(page_size, 1), MAX_PAGE_SIZE)
    
    # Use bool query with relaxed matching for ngram tokens
    # Since ngram creates many tokens, we use a more lenient matching strategy
    body = {
        "query": {
            "bool": {
                "should": [
                    # Phrase query with larger slop: allows more words between phrase terms
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^5", "summary^3", "content^2", "tags^2"],
                            "type": "phrase",
                            "slop": 10,  # Allow up to 10 words between phrase terms
                        }
                    },
                    # Cross fields query: matches query terms across all fields
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^5", "summary^3", "content^2", "tags^2"],
                            "type": "cross_fields",
                            "operator": "or",
                            "minimum_should_match": 2,  # Fixed number: only need 2 tokens to match (very lenient)
                        }
                    },
                    # Best fields with fixed minimum (works better than percentage for ngram)
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^4", "summary^3", "content", "tags"],
                            "type": "best_fields",
                            "operator": "or",
                            "minimum_should_match": 2,  # Fixed number: only need 2 tokens to match
                        }
                    }
                ],
                "minimum_should_match": 1,  # At least one of the queries must match
            }
        },
        "from": (page - 1) * size,
        "size": size,
        "highlight": {
            "fields": {
                "title": {},
                "summary": {},
                "content": {},
            },
            "fragment_size": 150,
            "number_of_fragments": 2,
        },
    }

    response = client.search(index=ARTICLES_INDEX, body=body)
    hits = response.get("hits", {}).get("hits", [])

    results: List[Dict[str, Any]] = []
    for hit in hits:
        source = hit.get("_source", {})
        if not source:
            continue
        highlight = hit.get("highlight") or {}
        highlight_parts = []
        for key in ("title", "summary", "content"):
            fragments = highlight.get(key) or []
            highlight_parts.extend(fragments)
        highlight_text = " ... ".join(highlight_parts)
        tags = source.get("tags")
        if isinstance(tags, list):
            tags = ",".join(tags)
        results.append(
            {
                "id": source.get("id"),
                "title": source.get("title") or "",
                "slug": source.get("slug") or "",
                "summary": source.get("summary") or "",
                "tags": tags or "",
                "created_at": source.get("created_at"),
                "updated_at": source.get("updated_at"),
                "highlight": highlight_text or None,
            }
        )
    return results


def index_article(article: ArticleModel) -> bool:
    """
    Index a single Article SQLAlchemy model into OpenSearch.
    Returns True if successful, False otherwise.
    """
    try:
        client = get_search_client()
        doc = article_to_doc(article)
        response = client.index(
            index=ARTICLES_INDEX,
            id=article.id,
            body=doc,
        )
        return response.get("result") in ("created", "updated")
    except SearchNotConfiguredError:
        logger.debug("ES_URL not configured; skipping article index.")
        return False
    except Exception as exc:
        logger.exception("Failed to index article %s: %s", article.id, exc)
        return False


def delete_article_from_index(article_id: int) -> bool:
    """
    Delete an article from OpenSearch by ID.
    Returns True if successful or if article doesn't exist, False on error.
    """
    try:
        client = get_search_client()
        response = client.delete(
            index=ARTICLES_INDEX,
            id=article_id,
            ignore=[404],  # Ignore if document doesn't exist
        )
        return True
    except SearchNotConfiguredError:
        logger.debug("ES_URL not configured; skipping article deletion.")
        return False
    except Exception as exc:
        logger.exception("Failed to delete article %s from index: %s", article_id, exc)
        return False


def get_all_indexed_article_ids() -> List[int]:
    """
    Get all article IDs currently indexed in OpenSearch.
    Returns an empty list if ES is not configured or on error.
    """
    try:
        client = get_search_client()
    except SearchNotConfiguredError:
        logger.debug("ES_URL not configured; cannot get indexed article IDs.")
        return []

    try:
        # Use scroll API to get all document IDs
        article_ids = []
        response = client.search(
            index=ARTICLES_INDEX,
            body={
                "size": 1000,  # Initial batch size
                "_source": False,  # Only return IDs, not full documents
            },
            scroll="2m",
        )

        scroll_id = response.get("_scroll_id")
        hits = response.get("hits", {}).get("hits", [])

        # Process initial batch
        for hit in hits:
            try:
                article_ids.append(int(hit["_id"]))
            except (ValueError, KeyError):
                logger.warning("Invalid article ID in ES: %s", hit.get("_id"))

        # Continue scrolling through remaining documents
        while scroll_id and hits:
            response = client.scroll(scroll_id=scroll_id, scroll="2m")
            scroll_id = response.get("_scroll_id")
            hits = response.get("hits", {}).get("hits", [])
            for hit in hits:
                try:
                    article_ids.append(int(hit["_id"]))
                except (ValueError, KeyError):
                    logger.warning("Invalid article ID in ES: %s", hit.get("_id"))

        # Clear scroll context
        if scroll_id:
            try:
                client.clear_scroll(scroll_id=scroll_id)
            except Exception:
                pass  # Ignore errors when clearing scroll

        return article_ids
    except Exception as exc:
        logger.exception("Failed to get indexed article IDs: %s", exc)
        return []


def bulk_delete_articles(article_ids: List[int]) -> int:
    """
    Delete multiple articles from OpenSearch by IDs.
    Returns the number of successfully deleted documents.
    """
    if not article_ids:
        return 0

    try:
        client = get_search_client()
    except SearchNotConfiguredError:
        logger.debug("ES_URL not configured; skipping bulk delete.")
        return 0

    actions = [
        {
            "_op_type": "delete",
            "_index": ARTICLES_INDEX,
            "_id": article_id,
        }
        for article_id in article_ids
    ]

    success, _ = helpers.bulk(client, actions, raise_on_error=False)
    return success


def bulk_index_articles(articles: Iterable[ArticleModel]) -> int:
    """
    Index a batch of Article SQLAlchemy models into OpenSearch.
    Returns the number of successfully indexed documents.
    """
    docs = list(articles)
    if not docs:
        return 0

    try:
        client = get_search_client()
    except SearchNotConfiguredError:
        logger.debug("ES_URL not configured; skipping bulk index.")
        return 0

    actions = [
        {
            "_op_type": "index",
            "_index": ARTICLES_INDEX,
            "_id": article.id,
            "_source": article_to_doc(article),
        }
        for article in docs
    ]

    success, _ = helpers.bulk(client, actions, raise_on_error=False)
    return success


CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^\)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
LIST_RE = re.compile(r"^\s*[\*\-\+]\s+", re.MULTILINE)
ORDERED_LIST_RE = re.compile(r"^\s*\d+\.\s+", re.MULTILINE)
BLOCKQUOTE_RE = re.compile(r"^>\s+", re.MULTILINE)
STRONG_EM_RE = re.compile(r"(\*\*|__)(.*?)\1")
EM_RE = re.compile(r"(\*|_)(.*?)\1")


def markdown_to_plain_text(text: str) -> str:
    """
    Convert markdown content into plain text while preserving punctuation.
    """
    if not text:
        return ""

    cleaned = CODE_BLOCK_RE.sub(" ", text)
    cleaned = INLINE_CODE_RE.sub(r"\1", cleaned)
    cleaned = IMAGE_RE.sub(r"\1", cleaned)
    cleaned = LINK_RE.sub(r"\1", cleaned)
    cleaned = HEADING_RE.sub("", cleaned)
    cleaned = LIST_RE.sub("", cleaned)
    cleaned = ORDERED_LIST_RE.sub("", cleaned)
    cleaned = BLOCKQUOTE_RE.sub("", cleaned)
    cleaned = STRONG_EM_RE.sub(r"\2", cleaned)
    cleaned = EM_RE.sub(r"\2", cleaned)
    cleaned = HTML_TAG_RE.sub(" ", cleaned)

    # Remove horizontal rules and extra hyphen lines
    cleaned = re.sub(r"^-{3,}$", " ", cleaned, flags=re.MULTILINE)
    # Collapse multiple whitespace into single spaces, but keep punctuation.
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned




import argparse
import logging

from sqlalchemy import select

try:
    from .database import SessionLocal
    from .models import Article as ArticleModel
    from .search import (
        SearchNotConfiguredError,
        bulk_index_articles,
        bulk_delete_articles,
        get_all_indexed_article_ids,
        ensure_article_index,
    )
except ImportError:  # pragma: no cover
    from database import SessionLocal
    from models import Article as ArticleModel
    from search import (
        SearchNotConfiguredError,
        bulk_index_articles,
        bulk_delete_articles,
        get_all_indexed_article_ids,
        ensure_article_index,
    )


logger = logging.getLogger(__name__)


def reindex(batch_size: int = 200, cleanup: bool = True) -> None:
    """
    Reindex all articles from database to OpenSearch.
    
    Args:
        batch_size: Number of articles to index per bulk request
        cleanup: If True, delete articles from ES that no longer exist in database
    """
    try:
        ensure_article_index()
    except SearchNotConfiguredError as exc:
        raise RuntimeError("ES_URL is not configured; cannot reindex articles.") from exc

    # Step 1: Get all article IDs from database
    db_article_ids = set()
    with SessionLocal() as session:
        stmt = select(ArticleModel.id)
        result = session.execute(stmt).scalars().all()
        db_article_ids = set(result)

    logger.info("Found %s articles in database", len(db_article_ids))

    # Step 2: Cleanup - delete articles from ES that don't exist in database
    if cleanup:
        try:
            es_article_ids = set(get_all_indexed_article_ids())
            logger.info("Found %s articles in Elasticsearch", len(es_article_ids))
            
            # Find articles in ES but not in database
            to_delete = es_article_ids - db_article_ids
            if to_delete:
                logger.info("Deleting %s articles from Elasticsearch that no longer exist in database", len(to_delete))
                deleted = bulk_delete_articles(list(to_delete))
                logger.info("Deleted %s articles from Elasticsearch", deleted)
                print(f"Deleted {deleted} articles from Elasticsearch that no longer exist in database.")
            else:
                logger.info("No articles to delete from Elasticsearch")
        except Exception as exc:
            logger.warning("Failed to cleanup deleted articles from Elasticsearch: %s", exc)
            print(f"Warning: Failed to cleanup deleted articles: {exc}")

    # Step 3: Index all articles from database
    total = 0
    with SessionLocal() as session:
        stmt = select(ArticleModel).order_by(ArticleModel.id)
        result = session.execute(stmt).scalars().yield_per(batch_size)
        batch = []
        for article in result:
            batch.append(article)
            if len(batch) >= batch_size:
                total += bulk_index_articles(batch)
                batch.clear()
        if batch:
            total += bulk_index_articles(batch)

    logger.info("Reindexed %s articles into OpenSearch.", total)
    print(f"Indexed {total} articles into OpenSearch.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reindex all articles into OpenSearch.")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=200,
        help="Number of articles to index per bulk request (default: 200).",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Skip cleanup: don't delete articles from ES that no longer exist in database.",
    )
    args = parser.parse_args()
    reindex(batch_size=max(1, args.batch_size), cleanup=not args.no_cleanup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()




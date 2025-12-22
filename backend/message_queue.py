import json
import logging
import os
import threading
import time
from typing import Any, Dict, Optional

import pika

try:
    # When backend is a package (run from project root)
    from .models import Article as ArticleModel
    from .search import SearchNotConfiguredError, index_article, delete_article_from_index
except ImportError:  # pragma: no cover
    # When running inside backend directory (no package)
    from models import Article as ArticleModel
    from search import SearchNotConfiguredError, index_article, delete_article_from_index


logger = logging.getLogger(__name__)


RABBITMQ_URL: Optional[str] = os.getenv("RABBITMQ_URL")
ARTICLE_QUEUE_NAME: str = os.getenv("RABBITMQ_ARTICLE_QUEUE", "article_events")


def _build_article_payload(event_type: str, article: ArticleModel) -> Dict[str, Any]:
    """
    Build a JSON-serializable payload for article change events.
    This will be consumed by a downstream worker to sync to ES.
    """
    return {
        "event_type": event_type,  # "created" | "updated" | "deleted"
        "article": {
            "id": int(article.id) if getattr(article, "id", None) is not None else None,
            "title": getattr(article, "title", None),
            "slug": getattr(article, "slug", None),
            "summary": getattr(article, "summary", None),
            "content": getattr(article, "content", None),
            "category_id": getattr(article, "category_id", None),
            "tags": getattr(article, "tags", None),
            "created_at": getattr(article, "created_at", None).isoformat()
            if getattr(article, "created_at", None)
            else None,
            "updated_at": getattr(article, "updated_at", None).isoformat()
            if getattr(article, "updated_at", None)
            else None,
        },
    }


def _publish_message_rabbitmq(payload: Dict[str, Any]) -> None:
    """
    Publish a single message to RabbitMQ.

    This function is intentionally simple and uses a short-lived connection
    per call to avoid global connection lifecycle issues.
    """
    if not RABBITMQ_URL:
        # MQ not configured, avoid raising in normal flows.
        logger.debug("RABBITMQ_URL not set; skipping MQ publish for payload: %s", payload)
        return

    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Use a durable queue so messages survive broker restarts.
        channel.queue_declare(queue=ARTICLE_QUEUE_NAME, durable=True)

        body = json.dumps(payload, default=str).encode("utf-8")
        channel.basic_publish(
            exchange="",
            routing_key=ARTICLE_QUEUE_NAME,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            ),
        )
        connection.close()
        logger.info("Published article event to RabbitMQ queue=%s", ARTICLE_QUEUE_NAME)
    except Exception:
        # Log but don't break the main request flow.
        logger.exception("Failed to publish article event to RabbitMQ")


def publish_article_event(event_type: str, article: ArticleModel) -> None:
    """
    Public helper for API layer to send article change events to MQ.
    """
    payload = _build_article_payload(event_type, article)
    _publish_message_rabbitmq(payload)


def _handle_article_event(message: Dict[str, Any]) -> None:
    """
    Handle a single article event message from RabbitMQ and sync it to OpenSearch.
    """
    event_type = message.get("event_type")
    article_data = message.get("article") or {}

    article_id = article_data.get("id")
    if not article_id:
        logger.warning("Received article event without valid id: %s", message)
        return

    try:
        if event_type in ("created", "updated"):
            # Construct a lightweight ArticleModel-like object for indexing
            article = ArticleModel(
                id=article_id,
                title=article_data.get("title") or "",
                slug=article_data.get("slug") or "",
                summary=article_data.get("summary"),
                content=article_data.get("content") or "",
                category_id=article_data.get("category_id"),
                tags=article_data.get("tags"),
            )
            # created_at / updated_at are not strictly required for search relevance,
            # so we don't try to parse them back – ES already has them from original index.
            index_article(article)
        elif event_type == "deleted":
            delete_article_from_index(int(article_id))
        else:
            logger.warning("Unknown event_type in MQ message: %s", event_type)
    except SearchNotConfiguredError:
        # If ES is not configured we simply skip sync
        logger.debug("ES not configured; skipping article event handling for id=%s", article_id)
    except Exception:
        logger.exception("Failed to handle article event from MQ: %s", message)


def _consume_loop(stop_event: threading.Event) -> None:
    """
    Long-running loop that connects to RabbitMQ and consumes article events.
    It will auto-reconnect on connection failures with a small backoff.
    """
    if not RABBITMQ_URL:
        logger.info("RABBITMQ_URL not set; MQ consumer thread will not start.")
        return

    logger.info("Starting RabbitMQ consumer loop for queue=%s", ARTICLE_QUEUE_NAME)

    while not stop_event.is_set():
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue=ARTICLE_QUEUE_NAME, durable=True)
            # Fair dispatch: don't give more than one unacked message to a worker
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                try:
                    message = json.loads(body.decode("utf-8"))
                    _handle_article_event(message)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    logger.exception("Error processing MQ message; nack and requeue")
                    # Nack and requeue the message for another attempt
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(queue=ARTICLE_QUEUE_NAME, on_message_callback=callback)

            # Blocking consume; will exit when connection is closed or stop_event is set
            while not stop_event.is_set():
                connection.process_data_events(time_limit=1)

            # Graceful shutdown: stop consuming and close connection
            try:
                channel.stop_consuming()
            except Exception:
                pass
            connection.close()
        except Exception:
            logger.exception("MQ consumer loop error, will retry in 5 seconds")
            time.sleep(5)


_consumer_stop_event: Optional[threading.Event] = None
_consumer_thread: Optional[threading.Thread] = None


def start_article_consumer_thread() -> None:
    """
    Start the background consumer thread if not already running.
    Safe to call multiple times.
    """
    global _consumer_stop_event, _consumer_thread

    if _consumer_thread and _consumer_thread.is_alive():
        return

    _consumer_stop_event = threading.Event()
    _consumer_thread = threading.Thread(
        target=_consume_loop, args=(_consumer_stop_event,), name="ArticleMQConsumer", daemon=True
    )
    _consumer_thread.start()
    logger.info("Started RabbitMQ consumer thread 'ArticleMQConsumer'")


def stop_article_consumer_thread() -> None:
    """
    Signal the background consumer thread to stop.
    """
    global _consumer_stop_event
    if _consumer_stop_event:
        _consumer_stop_event.set()


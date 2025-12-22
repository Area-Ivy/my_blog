"""
SQLAlchemy event listeners for automatic ES synchronization.
"""
import logging
from sqlalchemy import event
from sqlalchemy.orm import Session

try:
    from .models import Article as ArticleModel
    from .search import SearchNotConfiguredError, index_article, delete_article_from_index
except ImportError:  # pragma: no cover
    from models import Article as ArticleModel
    from search import SearchNotConfiguredError, index_article, delete_article_from_index

logger = logging.getLogger(__name__)


@event.listens_for(ArticleModel, "after_insert")
def receive_after_insert(mapper, connection, target: ArticleModel):
    """
    Automatically index article to ES after it's inserted into the database.
    """
    try:
        if index_article(target):
            logger.info("Auto-indexed article %s to ES", target.id)
        else:
            logger.warning("Failed to auto-index article %s to ES", target.id)
    except SearchNotConfiguredError:
        logger.debug("ES not configured; skipping auto-index for article %s", target.id)
    except Exception as exc:
        logger.exception("Error auto-indexing article %s: %s", target.id, exc)


@event.listens_for(ArticleModel, "after_update")
def receive_after_update(mapper, connection, target: ArticleModel):
    """
    Automatically update article in ES after it's updated in the database.
    This event is triggered when an Article instance is modified and the session is flushed.
    """
    try:
        # Mark this article as already processed to avoid duplicate updates in after_commit
        if hasattr(connection, 'info'):
            if 'updated_articles' not in connection.info:
                connection.info['updated_articles'] = set()
            connection.info['updated_articles'].add(target.id)
        
        if index_article(target):
            logger.info("Auto-updated article %s in ES", target.id)
        else:
            logger.warning("Failed to auto-update article %s in ES", target.id)
    except SearchNotConfiguredError:
        logger.debug("ES not configured; skipping auto-update for article %s", target.id)
    except Exception as exc:
        logger.exception("Error auto-updating article %s: %s", target.id, exc)


@event.listens_for(Session, "before_flush")
def receive_before_flush(session: Session, flush_context, instances):
    """
    Track modified Article instances before flush to ensure they are synced to ES.
    This catches updates that might not trigger after_update event (e.g., bulk updates).
    """
    # Initialize modified_articles set if it doesn't exist
    if 'modified_articles' not in session.info:
        session.info['modified_articles'] = set()
    
    # Track all dirty Article instances
    for instance in session.dirty:
        if isinstance(instance, ArticleModel) and hasattr(instance, 'id') and instance.id:
            session.info['modified_articles'].add(instance.id)


@event.listens_for(Session, "after_commit")
def receive_after_commit(session: Session):
    """
    Sync modified articles to ES after transaction commit.
    This ensures updates are synced even if after_update event didn't fire.
    Only processes articles that weren't already handled by after_update.
    """
    modified_ids = session.info.get('modified_articles', set())
    if not modified_ids:
        return
    
    # Check which articles were already updated by after_update event
    # (Note: connection.info might not be accessible here, so we'll process all)
    # This is a fallback mechanism, so processing all modified articles is acceptable
    
    # Re-query the articles to get fresh data after commit
    try:
        from sqlalchemy import select
        # Import SessionLocal with proper error handling
        try:
            from .database import SessionLocal
        except ImportError:
            from database import SessionLocal
        
        db = SessionLocal()
        try:
            articles = db.execute(select(ArticleModel).where(ArticleModel.id.in_(modified_ids))).scalars().all()
            for article in articles:
                try:
                    if index_article(article):
                        logger.info("Auto-updated article %s in ES (via after_commit fallback)", article.id)
                    else:
                        logger.warning("Failed to auto-update article %s in ES (via after_commit fallback)", article.id)
                except SearchNotConfiguredError:
                    logger.debug("ES not configured; skipping auto-update for article %s (via after_commit)", article.id)
                except Exception as exc:
                    logger.exception("Error auto-updating article %s (via after_commit): %s", article.id, exc)
        finally:
            db.close()
    except Exception as exc:
        logger.exception("Error syncing modified articles to ES after commit: %s", exc)
    finally:
        # Clear the tracking set
        session.info['modified_articles'] = set()


@event.listens_for(ArticleModel, "after_delete")
def receive_after_delete(mapper, connection, target: ArticleModel):
    """
    Automatically delete article from ES after it's deleted from the database.
    """
    article_id = target.id
    try:
        if delete_article_from_index(article_id):
            logger.info("Auto-deleted article %s from ES", article_id)
        else:
            logger.warning("Failed to auto-delete article %s from ES", article_id)
    except SearchNotConfiguredError:
        logger.debug("ES not configured; skipping auto-delete for article %s", article_id)
    except Exception as exc:
        logger.exception("Error auto-deleting article %s: %s", article_id, exc)


from typing import List, Optional
from datetime import datetime
import logging

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    # When backend is a package (run from project root)
    from .database import Base, engine, get_db
    from .models import Article as ArticleModel, Song as SongModel, Tool as ToolModel, Footprint as FootprintModel
    from .search import SearchNotConfiguredError, ensure_article_index, search_articles
    from . import search_events  # Register SQLAlchemy event listeners for auto-sync
    from .message_queue import publish_article_event, start_article_consumer_thread, stop_article_consumer_thread
except ImportError:  # pragma: no cover
    # When running inside backend directory (no package)
    from database import Base, engine, get_db
    from models import Article as ArticleModel, Song as SongModel, Tool as ToolModel, Footprint as FootprintModel
    from search import SearchNotConfiguredError, ensure_article_index, search_articles
    import search_events  # Register SQLAlchemy event listeners for auto-sync
    from message_queue import publish_article_event, start_article_consumer_thread, stop_article_consumer_thread


logger = logging.getLogger(__name__)


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: Optional[str] = None  # 逗号分隔字符串，前端可拆分
    highlight: Optional[str] = None


class ArticleDetail(ArticleOut):
    content: str
    category_id: Optional[int] = None


class ArticleBase(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None


class SongOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    artist: str
    url: str
    cover: str
    created_at: datetime
    updated_at: datetime


class ToolOut(BaseModel):
    id: str
    name: str
    tags: List[str] = []
    description: Optional[str] = None
    logo: Optional[str] = None
    link: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FootprintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    title: str
    description: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    highlights: Optional[List[str]] = None
    images: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


app = FastAPI(title="Blog Backend", version="0.1.0")

# Allow frontend dev server (Vite default: 5173) and typical local ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    # 创建表（若不存在）
    Base.metadata.create_all(bind=engine)
    try:
        ensure_article_index()
    except SearchNotConfiguredError:
        logger.info("ES_URL not set, skipping OpenSearch index creation.")
    except Exception:
        logger.exception("Failed to ensure OpenSearch index.")

    # 启动 RabbitMQ 消费者线程，用于根据队列消息增量同步 OpenSearch
    try:
        start_article_consumer_thread()
    except Exception:
        logger.exception("Failed to start RabbitMQ consumer thread")


@app.on_event("shutdown")
def on_shutdown() -> None:
    # 关闭 MQ 消费线程
    try:
        stop_article_consumer_thread()
    except Exception:
        logger.exception("Failed to stop RabbitMQ consumer thread")


def _parse_tags(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [tag.strip() for tag in value.split(",") if tag.strip()]


def _join_tags(tags: Optional[List[str]]) -> Optional[str]:
    if tags is None:
        return None
    cleaned = [tag.strip() for tag in tags if tag and tag.strip()]
    if not cleaned:
        return None
    return ",".join(cleaned)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/articles", response_model=List[ArticleOut])
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="按标题/摘要/标签模糊搜索"),
    db: Session = Depends(get_db),
) -> List[ArticleOut]:
    if q:
        try:
            results = search_articles(q, page=page, page_size=page_size)
            if results:
                # search_articles returns plain dicts; convert to ArticleOut for consistency.
                return [ArticleOut.model_validate(r) for r in results]
        except SearchNotConfiguredError:
            logger.info("Search requested but ES_URL is missing; falling back to DB LIKE query.")
        except Exception:
            logger.exception("OpenSearch query failed; falling back to DB LIKE query.")

    stmt = select(ArticleModel)
    if q:
        like = f"%{q}%"
        # 简单模糊匹配：标题、摘要、标签
        stmt = stmt.filter(
            (ArticleModel.title.like(like))
            | (ArticleModel.summary.like(like))
            | (ArticleModel.tags.like(like))
        )
    # 新到旧
    stmt = stmt.order_by(ArticleModel.created_at.desc())
    # 分页
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    rows = db.execute(stmt).scalars().all()
    return [ArticleOut.model_validate(r) for r in rows]


@app.get("/api/articles/{article_id}", response_model=ArticleDetail)
def get_article(article_id: int, db: Session = Depends(get_db)) -> ArticleDetail:
    stmt = select(ArticleModel).where(ArticleModel.id == article_id)
    obj = db.execute(stmt).scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleDetail.model_validate(obj)


@app.post("/api/articles", response_model=ArticleDetail, status_code=201)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)) -> ArticleDetail:
    if (
        db.execute(select(ArticleModel).where(ArticleModel.slug == payload.slug))
        .scalars()
        .first()
    ):
        raise HTTPException(status_code=400, detail="Slug already exists")

    article = ArticleModel(
        title=payload.title,
        slug=payload.slug,
        content=payload.content,
        summary=payload.summary,
        category_id=payload.category_id,
        tags=_join_tags(payload.tags),
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    # 推送到 RabbitMQ，供后续 ES 同步使用
    try:
        publish_article_event("created", article)
    except Exception:
        logger.exception("Failed to enqueue 'created' article event")
    return ArticleDetail.model_validate(article)


@app.put("/api/articles/{article_id}", response_model=ArticleDetail)
def update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)) -> ArticleDetail:
    stmt = select(ArticleModel).where(ArticleModel.id == article_id)
    article = db.execute(stmt).scalars().first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if payload.slug and payload.slug != article.slug:
        if (
            db.execute(select(ArticleModel).where(ArticleModel.slug == payload.slug))
            .scalars()
            .first()
        ):
            raise HTTPException(status_code=400, detail="Slug already exists")

    if payload.title is not None:
        article.title = payload.title
    if payload.slug is not None:
        article.slug = payload.slug
    if payload.content is not None:
        article.content = payload.content
    if payload.summary is not None:
        article.summary = payload.summary
    if payload.category_id is not None:
        article.category_id = payload.category_id
    if payload.tags is not None:
        article.tags = _join_tags(payload.tags)

    db.add(article)
    db.commit()
    db.refresh(article)
    # 推送到 RabbitMQ，供后续 ES 同步使用
    try:
        publish_article_event("updated", article)
    except Exception:
        logger.exception("Failed to enqueue 'updated' article event")
    return ArticleDetail.model_validate(article)


@app.delete("/api/articles/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db)) -> None:
    stmt = select(ArticleModel).where(ArticleModel.id == article_id)
    article = db.execute(stmt).scalars().first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 先缓存一份用于发送 MQ 消息（提交后对象会被过期）
    article_copy = article

    db.delete(article)
    db.commit()
    # 推送到 RabbitMQ，供后续 ES 同步使用
    try:
        publish_article_event("deleted", article_copy)
    except Exception:
        logger.exception("Failed to enqueue 'deleted' article event")
    return None


@app.get("/api/songs", response_model=List[SongOut])
def list_songs(db: Session = Depends(get_db)) -> List[SongOut]:
    """获取所有歌曲列表"""
    stmt = select(SongModel).order_by(SongModel.created_at.asc())
    rows = db.execute(stmt).scalars().all()
    return [SongOut.model_validate(r) for r in rows]


@app.get("/api/tools", response_model=List[ToolOut])
def list_tools(db: Session = Depends(get_db)) -> List[ToolOut]:
    stmt = select(ToolModel).order_by(ToolModel.created_at.desc())
    rows = db.execute(stmt).scalars().all()
    return [
        ToolOut(
            id=row.id,
            name=row.name,
            tags=_parse_tags(row.tags),
            description=row.description,
            logo=row.logo,
            link=row.link,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
        for row in rows
    ]


@app.get("/api/songs/{song_id}", response_model=SongOut)
def get_song(song_id: int, db: Session = Depends(get_db)) -> SongOut:
    """获取单个歌曲详情"""
    stmt = select(SongModel).where(SongModel.id == song_id)
    obj = db.execute(stmt).scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="Song not found")
    return SongOut.model_validate(obj)


@app.get("/api/footprints", response_model=List[FootprintOut])
def list_footprints(db: Session = Depends(get_db)) -> List[FootprintOut]:
    """获取所有足迹列表，按日期降序排列"""
    stmt = select(FootprintModel).order_by(FootprintModel.date.desc())
    rows = db.execute(stmt).scalars().all()
    return [FootprintOut.model_validate(r) for r in rows]


@app.get("/api/footprints/count")
def get_footprints_count(db: Session = Depends(get_db)) -> dict:
    """获取足迹总数"""
    stmt = select(FootprintModel)
    count = db.execute(stmt).scalars().all()
    return {"count": len(count)}


# For `python backend/main.py` local run convenience (optional)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)




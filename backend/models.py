from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Text, DateTime, JSON

try:
    # When backend is a package (run from project root)
    from .database import Base
except ImportError:  # pragma: no cover
    # When running inside backend directory (no package)
    from database import Base


class Article(Base):
    __tablename__ = "blog_posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    title = Column(String(255), nullable=False, comment="文章标题")
    slug = Column(String(255), nullable=False, unique=True, comment="URL别名（SEO友好）")
    content = Column(Text, nullable=False, comment="文章正文（支持 Markdown 或 HTML）")
    summary = Column(Text, nullable=True, comment="文章摘要")
    category_id = Column(BigInteger, nullable=True, comment="分类ID（关联分类表）")
    tags = Column(String(255), nullable=True, comment="逗号分隔的标签（如 AI,生活）")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后更新时间"
    )


class Song(Base):
    __tablename__ = "songs"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), nullable=False, comment="歌曲名称")
    artist = Column(String(255), nullable=False, comment="艺术家")
    url = Column(String(500), nullable=False, comment="歌曲文件地址")
    cover = Column(String(500), nullable=False, comment="封面图片地址")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后更新时间"
    )


class Tool(Base):
    __tablename__ = "tools"

    id = Column(String(50), primary_key=True, comment="工具唯一ID")
    name = Column(String(100), nullable=False, comment="工具名称")
    tags = Column(String(255), nullable=True, comment="逗号分隔标签")
    description = Column(Text, nullable=True, comment="工具描述")
    logo = Column(String(255), nullable=True, comment="LOGO地址")
    link = Column(String(255), nullable=True, comment="工具链接")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后更新时间"
    )


class Footprint(Base):
    __tablename__ = "footprints"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    date = Column(DateTime, nullable=False, comment="足迹日期")
    title = Column(String(255), nullable=False, comment="足迹标题")
    description = Column(Text, nullable=True, comment="足迹描述")
    type = Column(String(50), nullable=True, comment="足迹类型（如：项目、设计、学习等）")
    location = Column(String(255), nullable=True, comment="位置信息")
    highlights = Column(JSON, nullable=True, comment="高亮列表（JSON数组）")
    images = Column(JSON, nullable=True, comment="图片列表（JSON数组，存储图片URL）")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后更新时间"
    )



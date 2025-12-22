from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

try:
    # When backend is a package (run from project root)
    from .settings import get_database_url, get_mysql_ssl_connect_args
except ImportError:  # pragma: no cover
    # When running inside backend directory (no package)
    from settings import get_database_url, get_mysql_ssl_connect_args

# Build engine args based on DB driver and SSL needs
DATABASE_URL = get_database_url()
engine_args = {}

# SQLite specific
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

# MySQL SSL (optional)
if DATABASE_URL.startswith("mysql+pymysql"):
    ssl_args = get_mysql_ssl_connect_args()
    if ssl_args:
        engine_args["connect_args"] = {**engine_args.get("connect_args", {}), **ssl_args}

engine = create_engine(DATABASE_URL, echo=False, future=True, **engine_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



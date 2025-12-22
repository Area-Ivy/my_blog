import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv


def _load_env_files() -> None:
    """
    Load .env from project root and backend/.env if present.
    This makes running from either project root or backend directory work.
    """
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # 1) project root .env
    root_env = project_root / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env, override=False)

    # 2) backend/.env
    backend_env = current_dir / ".env"
    if backend_env.exists():
        load_dotenv(dotenv_path=backend_env, override=False)

    # 3) fallback: default .env in CWD (if neither above found but user relies on auto-discovery)
    load_dotenv(override=False)


_load_env_files()


def get_database_url() -> str:
    """
    DATABASE_URL, default to local SQLite file for out-of-the-box dev.
    For MySQL (LAS), example:
      mysql+pymysql://user:password@host:3306/dbname?charset=utf8mb4
    """
    return os.getenv("DATABASE_URL", "sqlite:///./backend/blog.db")


def get_mysql_ssl_connect_args() -> Optional[Dict[str, dict]]:
    """
    Optional SSL support for PyMySQL:
      DB_SSL_CA, DB_SSL_CERT, DB_SSL_KEY
    Returns a dict suitable to merge into SQLAlchemy create_engine(..., connect_args=...).
    Only applied when DATABASE_URL startswith mysql+pymysql and any SSL var is set.
    """
    ssl_ca = os.getenv("DB_SSL_CA")
    ssl_cert = os.getenv("DB_SSL_CERT")
    ssl_key = os.getenv("DB_SSL_KEY")
    if not any([ssl_ca, ssl_cert, ssl_key]):
        return None

    ssl_dict = {}
    if ssl_ca:
        ssl_dict["ca"] = ssl_ca
    if ssl_cert:
        ssl_dict["cert"] = ssl_cert
    if ssl_key:
        ssl_dict["key"] = ssl_key

    return {"ssl": ssl_dict}








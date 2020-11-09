from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@postgresserver/db"

# connect_args is ONLY for sqlite, remove if using PostgreSQL or other.
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

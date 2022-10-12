from contextvars import ContextVar

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

session_factory = sessionmaker(bind=engine)
session_var: ContextVar = ContextVar("db_session")
session = session_var.get

Base = declarative_base()

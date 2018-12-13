from typing import List, Set

from fastapi import Body, FastAPI, Path, Query, Depends, Cookie
from pydantic import BaseModel
from pydantic.types import UrlStr
from starlette.status import HTTP_201_CREATED
from starlette.responses import HTMLResponse
from random import choice

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr


# SQLAlchemy specific code, as with any other app


SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

# By creating this a CustomBase class and inheriting from it, your models will have
# automatic __tablename__ attributes. So you don't have to declare them.
# So, your models will behave very similarly to, for example, Flask-SQLAlchemy

class CustomBase:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


class User(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_user(username, db_session):
    return db_session.query(User).filter(User.id == username).first()

# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}")
def read_user(username: str):
    user = get_user(username, db_session)
    return user

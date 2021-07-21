from contextlib import contextmanager
from typing import Generator

from fastapi import Depends, FastAPI
from pydantic import BaseSettings


class Database:

    def __init__(self, hostname: str) -> None:
        ...

    @contextmanager
    def connect(self):
        yield



class AppConfig(BaseSettings):
    database_hostname: str = "localhost"


def Config() -> AppConfig:
    return AppConfig()


@contextmanager
def DBConnection(config: AppConfig = Depends(Config)) -> Generator[Database, None, None]:
    print("Creating DB connection!")
    db = Database(hostname=config.database_hostname)
    with db.connect():
        yield db


app = FastAPI()


@app.get("/")
def root(conn: Database = Depends(DBConnection, cache_lifespan="app")):
    ...

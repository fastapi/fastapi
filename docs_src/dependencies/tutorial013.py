from contextlib import contextmanager

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


def DBConnection(config: AppConfig = Depends(Config)) -> Database:
    print("Creating DB connection!")
    db = Database(hostname=config.database_hostname)
    with db.connect():
        yield db


app = FastAPI()


@app.get("/")
def root(conn: Database = Depends(DBConnection, lifespan="app")):
    ...

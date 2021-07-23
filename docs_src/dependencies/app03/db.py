from typing import AsyncGenerator

import sqlalchemy
from databases import Database
from fastapi import Depends

from .config import Settings, get_config
from .schemas import metadata


def run_migrations(config: Settings = Depends(get_config)) -> None:
    engine = sqlalchemy.create_engine(
        config.db_url, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)


async def get_db(
    config: Settings = Depends(get_config), migrations: None = Depends(run_migrations)
) -> AsyncGenerator[Database, None]:
    async with Database(config.db_url) as db:
        yield db

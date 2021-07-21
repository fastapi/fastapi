from typing import AsyncGenerator

from databases import Database
import sqlalchemy
from fastapi import Depends

from .config import get_config, Settings
from .schemas import metadata


def run_migrations(config: Settings = Depends(get_config)) -> None:
    engine = sqlalchemy.create_engine(
        config.db_url, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)


async def get_db(
    config: Settings = Depends(get_config),
    migrations: None = Depends(run_migrations)
) -> AsyncGenerator[Database, None]:
    database = Database(config.db_url)
    await database.connect()
    yield database
    await database.disconnect()

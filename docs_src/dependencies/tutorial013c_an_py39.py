from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI, Path
from typing_extensions import Self


@dataclass
class MyDatabaseConnection:
    """
    This is a mock just for example purposes.
    """

    connection_string: str

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_record(self, table_name: str, record_id: str) -> dict:
        pass


app = FastAPI()


async def get_configuration() -> dict:
    return {
        "database_url": "sqlite:///database.db",
    }


GlobalConfiguration = Annotated[
    dict, Depends(get_configuration, scope="lifespan")
]


async def get_database_connection(configuration: GlobalConfiguration):
    async with MyDatabaseConnection(configuration["database_url"]) as connection:
        yield connection


GlobalDatabaseConnection = Annotated[
    get_database_connection,
    Depends(get_database_connection, scope="lifespan"),
]


@app.get("/users/{user_id}")
async def read_user(
    database_connection: GlobalDatabaseConnection, user_id: Annotated[str, Path()]
):
    return await database_connection.get_record("users", user_id)

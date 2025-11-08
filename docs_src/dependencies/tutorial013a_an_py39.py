from typing import Annotated

from fastapi import Depends, FastAPI
from typing_extensions import Self


class MyDatabaseConnection:
    """
    This is a mock just for example purposes.
    """

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_records(self, table_name: str) -> list[dict]:
        pass


app = FastAPI()


async def get_database_connection():
    async with MyDatabaseConnection() as connection:
        yield connection


GlobalDatabaseConnection = Annotated[
    MyDatabaseConnection, Depends(get_database_connection, scope="lifespan")
]


@app.get("/users/")
async def read_users(database_connection: GlobalDatabaseConnection):
    return await database_connection.get_records("users")


@app.get("/items/")
async def read_items(database_connection: GlobalDatabaseConnection):
    return await database_connection.get_records("items")

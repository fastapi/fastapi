from typing import List

from fastapi import Depends, FastAPI, Path
from typing_extensions import Self


class MyDatabaseConnection:
    """
    This is a mock just for example purposes.
    """

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_records(self, table_name: str) -> List[dict]:
        pass

    async def get_record(self, table_name: str, record_id: str) -> dict:
        pass


app = FastAPI()


async def get_database_connection():
    async with MyDatabaseConnection() as connection:
        yield connection


GlobalDatabaseConnection = Depends(get_database_connection, scope="lifespan")
DedicatedDatabaseConnection = Depends(
    get_database_connection, scope="lifespan", use_cache=False
)


@app.get("/groups/")
async def read_groups(
    database_connection: MyDatabaseConnection = DedicatedDatabaseConnection,
):
    return await database_connection.get_records("groups")


@app.get("/users/")
async def read_users(
    database_connection: MyDatabaseConnection = DedicatedDatabaseConnection,
):
    return await database_connection.get_records("users")


@app.get("/items/")
async def read_items(
    database_connection: MyDatabaseConnection = GlobalDatabaseConnection,
):
    return await database_connection.get_records("items")


@app.get("/items/{item_id}")
async def read_item(
    item_id: str = Path(),
    database_connection: MyDatabaseConnection = GlobalDatabaseConnection,
):
    return await database_connection.get_record("items", item_id)

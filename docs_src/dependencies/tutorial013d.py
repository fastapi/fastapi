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

    async def get_record(self, table_name: str, record_id: str) -> dict:
        pass


app = FastAPI()


async def get_database_connection():
    async with MyDatabaseConnection() as connection:
        yield connection


GlobalDatabaseConnection = Depends(get_database_connection, scope="lifespan")


async def get_user_record(
    database_connection: MyDatabaseConnection = GlobalDatabaseConnection,
    user_id: str = Path(),
) -> dict:
    return await database_connection.get_record("users", user_id)


@app.get("/users/{user_id}")
async def read_user(user_record: dict = Depends(get_user_record)):
    return user_record

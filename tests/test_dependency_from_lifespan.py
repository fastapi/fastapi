from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

import pytest
from fastapi import Depends, FastAPI, FromLifespan
from fastapi.testclient import TestClient
from typing_extensions import Annotated


def test_app_extract_from_lifespan() -> None:
    class DatabaseConnection:
        def __init__(self, expected: int) -> None:
            self.expected = expected

        async def query(self, __query: str) -> Any:
            assert __query == f"SELECT {self.expected}"
            return self.expected

    class DatabaseConnectionPool:
        def __init__(self, expected: int) -> None:
            self.expected = expected

        @asynccontextmanager
        async def acquire(self) -> AsyncIterator[DatabaseConnection]:
            yield DatabaseConnection(self.expected)

    @asynccontextmanager
    async def connect(expected: int) -> AsyncIterator[DatabaseConnectionPool]:
        yield DatabaseConnectionPool(expected)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[Dict[str, Any]]:
        async with connect(42) as db:
            yield {"db": db}

    app = FastAPI(lifespan=lifespan)

    async def get_connection(
        db: FromLifespan[DatabaseConnectionPool],
    ) -> AsyncIterator[DatabaseConnection]:
        async with db.acquire() as conn:
            yield conn

    DbConnection = Annotated[DatabaseConnection, Depends(get_connection)]

    @app.get("/")
    async def endpoint(conn: DbConnection) -> int:
        return await conn.query("SELECT 42")

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == 42


def test_app_extract_from_lifespan_not_found() -> None:
    class Foo:
        pass

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[Dict[str, Any]]:
        yield {}

    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    async def endpoint(foo: FromLifespan[Foo]) -> Any:
        raise AssertionError("Should not be called")  # pragma: no cover

    with TestClient(app) as client:
        with pytest.raises(RuntimeError, match="not found"):
            client.get("/")

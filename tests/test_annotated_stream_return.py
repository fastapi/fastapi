from collections.abc import AsyncGenerator, AsyncIterator
from typing import Annotated

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str


def test_annotated_async_iterator_stream() -> None:
    app = FastAPI()

    @app.get("/items")
    async def stream_items() -> Annotated[AsyncIterator[int], "stream-meta"]:
        yield 1
        yield 2

    client = TestClient(app)
    response = client.get("/items")
    assert response.status_code == 200
    assert response.text == "1\n2\n"

    openapi = app.openapi()
    schema = openapi["paths"]["/items"]["get"]["responses"]["200"]
    assert "application/jsonl" in schema["content"]
    assert schema["content"]["application/jsonl"]["itemSchema"]["type"] == "integer"


def test_annotated_async_generator_stream() -> None:
    app = FastAPI()

    @app.get("/gen-items")
    async def stream_gen() -> Annotated[AsyncGenerator[str, None], "gen-meta"]:
        yield "chunk1"
        yield "chunk2"

    client = TestClient(app)
    response = client.get("/gen-items")
    assert response.status_code == 200
    assert response.text == '"chunk1"\n"chunk2"\n'


def test_nested_annotated_stream() -> None:
    app = FastAPI()

    @app.get("/nested")
    async def stream_nested() -> Annotated[
        Annotated[AsyncIterator[Item], "inner-meta"], "outer-meta"
    ]:
        yield Item(name="item-1")

    client = TestClient(app)
    response = client.get("/nested")
    assert response.status_code == 200
    assert '{"name":"item-1"}' in response.text

    openapi = app.openapi()
    schema = openapi["paths"]["/nested"]["get"]["responses"]["200"]
    assert "application/jsonl" in schema["content"]
    assert "$ref" in schema["content"]["application/jsonl"]["itemSchema"]

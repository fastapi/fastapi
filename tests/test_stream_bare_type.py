import json
from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str


app = FastAPI()


@app.get("/items/stream-bare-async")
async def stream_bare_async() -> AsyncIterable:
    yield {"name": "foo"}


@app.get("/items/stream-bare-sync")
def stream_bare_sync() -> Iterable:
    yield {"name": "bar"}


client = TestClient(app)


def test_stream_bare_async_iterable():
    """Test that bare AsyncIterable (no type args) works and streams JSONL."""
    response = client.get("/items/stream-bare-async")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo"}]


def test_stream_bare_sync_iterable():
    """Test that bare Iterable (no type args) works and streams JSONL."""
    response = client.get("/items/stream-bare-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "bar"}]

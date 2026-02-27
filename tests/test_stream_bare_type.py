import json
from typing import AsyncIterable, Iterable  # noqa: UP035 to test coverage

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
    response = client.get("/items/stream-bare-async")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo"}]


def test_stream_bare_sync_iterable():
    response = client.get("/items/stream-bare-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "bar"}]

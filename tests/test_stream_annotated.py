import json
from collections.abc import (
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Iterable,
    Iterator,
)
from collections.abc import AsyncGenerator as AbcAsyncGenerator
from collections.abc import AsyncIterable as AbcAsyncIterable
from collections.abc import AsyncIterator as AbcAsyncIterator
from typing import (
    Annotated,
    Any,
)

from fastapi import APIRouter, FastAPI
from fastapi.dependencies.utils import get_stream_item_type
from fastapi.sse import EventSourceResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


def test_get_stream_item_type_unwraps_annotated():
    assert get_stream_item_type(Annotated[AsyncIterator[int], "metadata"]) is int
    assert (
        get_stream_item_type(
            Annotated[Annotated[AbcAsyncIterator[str], "inner"], "outer"]
        )
        is str
    )
    assert get_stream_item_type(Annotated[AsyncIterable[Item], "meta"]) is Item
    assert get_stream_item_type(Annotated[AsyncGenerator[int, None], "meta"]) is int
    assert get_stream_item_type(Annotated[AbcAsyncGenerator[int, None], "meta"]) is int
    assert get_stream_item_type(Annotated[Iterator[float], "meta"]) is float
    assert get_stream_item_type(Annotated[Iterable[bytes], "meta"]) is bytes
    assert get_stream_item_type(Annotated[AsyncIterator[Any], "bare"]) is Any
    assert get_stream_item_type(Annotated[AsyncIterator, "unsubscripted"]) is None
    assert get_stream_item_type(Annotated[int, "not-stream"]) is None
    assert get_stream_item_type(int) is None
    assert get_stream_item_type(AsyncIterator[int]) is int


app = FastAPI()


@app.get("/stream-annotated-jsonl")
async def stream_annotated_jsonl() -> Annotated[
    AsyncIterator[Item], "item-stream-metadata"
]:
    yield Item(name="apple", price=1.5)
    yield Item(name="banana", price=2.0)


@app.get("/stream-nested-annotated-jsonl")
async def stream_nested_annotated_jsonl() -> Annotated[
    Annotated[AbcAsyncIterator[int], "inner"], "outer"
]:
    yield 100
    yield 200


@app.get("/stream-annotated-async-generator")
async def stream_annotated_async_generator() -> Annotated[
    AsyncGenerator[str, None], "gen-metadata"
]:
    yield "chunk1"
    yield "chunk2"


@app.get("/stream-annotated-sync")
def stream_annotated_sync() -> Annotated[Iterator[str], "sync-iterator-metadata"]:
    yield "foo"
    yield "bar"


@app.get("/stream-annotated-sse", response_class=EventSourceResponse)
async def stream_annotated_sse() -> Annotated[AsyncIterator[int], "sse-int-metadata"]:
    yield 1
    yield 2


router = APIRouter()


@router.get("/router-stream-annotated")
async def router_stream_annotated() -> Annotated[
    AbcAsyncIterable[Item], "router-stream"
]:
    yield Item(name="router-item", price=9.99)


app.include_router(router, prefix="/api")

client = TestClient(app)


def test_stream_annotated_jsonl():
    response = client.get("/stream-annotated-jsonl")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [
        {"name": "apple", "price": 1.5},
        {"name": "banana", "price": 2.0},
    ]


def test_stream_nested_annotated_jsonl():
    response = client.get("/stream-nested-annotated-jsonl")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [100, 200]


def test_stream_annotated_async_generator():
    response = client.get("/stream-annotated-async-generator")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == ["chunk1", "chunk2"]


def test_stream_annotated_sync():
    response = client.get("/stream-annotated-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == ["foo", "bar"]


def test_stream_annotated_sse():
    response = client.get("/stream-annotated-sse")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == "data: 1\n\ndata: 2\n\n"


def test_router_stream_annotated():
    response = client.get("/api/router-stream-annotated")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "router-item", "price": 9.99}]


def test_stream_annotated_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]

    # Verify JSONL itemSchema for Pydantic model
    jsonl_schema = paths["/stream-annotated-jsonl"]["get"]["responses"]["200"]
    assert jsonl_schema == {
        "description": "Successful Response",
        "content": {
            "application/jsonl": {"itemSchema": {"$ref": "#/components/schemas/Item"}}
        },
    }

    # Verify SSE contentSchema for integer stream
    sse_schema = paths["/stream-annotated-sse"]["get"]["responses"]["200"]
    data_schema = sse_schema["content"]["text/event-stream"]["itemSchema"][
        "properties"
    ]["data"]
    assert data_schema == {
        "type": "string",
        "contentMediaType": "application/json",
        "contentSchema": {
            "type": "integer",
            "title": "Streamitem Stream Annotated Sse Stream Annotated Sse Get",
        },
    }

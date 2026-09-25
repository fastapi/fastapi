import json
from collections.abc import AsyncIterable, Iterator

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    secret: str
    optional: str | None = None


class PriceItem(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get(
    "/items/stream-jsonl",
    response_model=Item,
    response_model_exclude={"secret"},
    response_model_exclude_none=True,
)
async def stream_jsonl():
    yield Item(name="foo", secret="hidden", optional=None)


@app.get(
    "/items/stream-async-iterable",
    response_model=AsyncIterable[Item],
    response_model_exclude={"secret"},
)
async def stream_async_iterable():
    yield Item(name="bar", secret="hidden")


@app.get(
    "/items/stream-iterator",
    response_model=Iterator[Item],
    response_model_exclude={"secret"},
)
def stream_iterator():
    yield Item(name="baz", secret="hidden")


@app.get(
    "/items/stream-sse",
    response_class=EventSourceResponse,
    response_model=Item,
    response_model_exclude={"secret"},
)
async def stream_sse():
    yield Item(name="sse-item", secret="hidden")


@app.get(
    "/items/stream-sse-events",
    response_class=EventSourceResponse,
)
async def stream_sse_events():
    yield ServerSentEvent(data="plain text", event="custom")


@app.get(
    "/items/stream-sse-server-sent-event-model",
    response_class=EventSourceResponse,
    response_model=ServerSentEvent,
)
async def stream_sse_server_sent_event_model():
    yield ServerSentEvent(data="sse-explicit", event="message")


@app.get(
    "/items/non-stream",
    response_model=Item,
    response_model_exclude={"secret"},
)
def non_stream():
    return Item(name="regular", secret="hidden")


@app.get(
    "/items/stream-invalid-async",
    response_model=PriceItem,
)
async def stream_invalid_async():
    yield {"name": "valid", "price": 10.0}
    yield {"name": "invalid", "price": "not-a-float"}


@app.get(
    "/items/stream-invalid-sync",
    response_model=PriceItem,
)
def stream_invalid_sync():
    yield {"name": "valid", "price": 10.0}
    yield {"name": "invalid", "price": "not-a-float"}


router = APIRouter()


@router.get(
    "/stream-router",
    response_model=Item,
    response_model_exclude={"secret"},
)
async def stream_router():
    yield Item(name="router-item", secret="hidden")


app.include_router(router, prefix="/api")

client = TestClient(app)


def test_stream_jsonl_with_explicit_response_model():
    response = client.get("/items/stream-jsonl")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo"}]


def test_stream_jsonl_with_async_iterable_response_model():
    response = client.get("/items/stream-async-iterable")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "bar", "optional": None}]


def test_stream_jsonl_with_iterator_response_model():
    response = client.get("/items/stream-iterator")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "baz", "optional": None}]


def test_stream_sse_with_explicit_response_model():
    response = client.get("/items/stream-sse")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == 'data: {"name":"sse-item","optional":null}\n\n'


def test_stream_sse_with_server_sent_event():
    response = client.get("/items/stream-sse-events")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == 'event: custom\ndata: "plain text"\n\n'


def test_stream_sse_with_server_sent_event_response_model():
    response = client.get("/items/stream-sse-server-sent-event-model")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.text == 'event: message\ndata: "sse-explicit"\n\n'


def test_non_stream_endpoint_remains_unchanged():
    response = client.get("/items/non-stream")
    assert response.status_code == 200
    assert response.json() == {"name": "regular", "optional": None}


def test_stream_jsonl_validation_failure_async():
    with pytest.raises(ResponseValidationError):
        client.get("/items/stream-invalid-async")


def test_stream_jsonl_validation_failure_sync():
    with pytest.raises(ResponseValidationError):
        client.get("/items/stream-invalid-sync")


def test_stream_router_with_explicit_response_model():
    response = client.get("/api/stream-router")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "router-item", "optional": None}]


def test_stream_openapi_schemas():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]

    jsonl_schema = paths["/items/stream-jsonl"]["get"]["responses"]["200"]
    assert jsonl_schema == {
        "description": "Successful Response",
        "content": {
            "application/jsonl": {"itemSchema": {"$ref": "#/components/schemas/Item"}}
        },
    }

    async_schema = paths["/items/stream-async-iterable"]["get"]["responses"]["200"]
    assert async_schema == {
        "description": "Successful Response",
        "content": {
            "application/jsonl": {"itemSchema": {"$ref": "#/components/schemas/Item"}}
        },
    }

    sse_schema = paths["/items/stream-sse"]["get"]["responses"]["200"]
    assert sse_schema == {
        "description": "Successful Response",
        "content": {
            "text/event-stream": {
                "itemSchema": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "contentMediaType": "application/json",
                            "contentSchema": {"$ref": "#/components/schemas/Item"},
                        },
                        "event": {"type": "string"},
                        "id": {"type": "string"},
                        "retry": {"type": "integer", "minimum": 0},
                    },
                    "required": ["data"],
                }
            }
        },
    }

    non_stream_schema = paths["/items/non-stream"]["get"]["responses"]["200"]
    assert non_stream_schema == {
        "description": "Successful Response",
        "content": {
            "application/json": {"schema": {"$ref": "#/components/schemas/Item"}}
        },
    }

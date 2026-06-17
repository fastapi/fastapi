import json
from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, SerializationInfo, field_serializer
from starlette.requests import Request


class ItemWithContext(BaseModel):
    name: str
    request_path: str | None = None

    @field_serializer("request_path", mode="plain")
    def serialize_request_path(
        self, value: str | None, info: SerializationInfo
    ) -> str | None:
        if not isinstance(info.context, Request):
            return value
        return info.context.url.path


app = FastAPI()


@app.get("/items/non-stream", response_model=ItemWithContext)
async def non_stream_item() -> ItemWithContext:
    return ItemWithContext(name="plain")


@app.get("/items/stream-jsonl")
async def stream_jsonl_items() -> AsyncIterable[ItemWithContext]:
    yield ItemWithContext(name="foo")


@app.get("/items/stream-sse", response_class=EventSourceResponse)
async def stream_sse_items() -> AsyncIterable[ItemWithContext]:
    yield ItemWithContext(name="bar")


client = TestClient(app)


def test_non_stream_response_model_serializer_receives_request_context() -> None:
    response = client.get("/items/non-stream")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"name": "plain", "request_path": "/items/non-stream"}


def test_jsonl_stream_response_model_serializer_receives_request_context() -> None:
    response = client.get("/items/stream-jsonl")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    items = [json.loads(line) for line in response.text.strip().splitlines()]
    assert items == [{"name": "foo", "request_path": "/items/stream-jsonl"}]


def test_sse_stream_response_model_serializer_receives_request_context() -> None:
    response = client.get("/items/stream-sse")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = [
        line.removeprefix("data: ")
        for line in response.text.strip().splitlines()
        if line.startswith("data: ")
    ]
    items = [json.loads(line) for line in data_lines]
    assert items == [{"name": "bar", "request_path": "/items/stream-sse"}]

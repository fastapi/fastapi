import asyncio
import time
from collections.abc import AsyncIterable, Iterable

import fastapi.routing
import pytest
from fastapi import APIRouter, FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.sse import ServerSentEvent
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


app = FastAPI()


@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


@app.get("/items/stream-sync", response_class=EventSourceResponse)
def sse_items_sync() -> Iterable[Item]:
    yield from items


@app.get("/items/stream-no-annotation", response_class=EventSourceResponse)
async def sse_items_no_annotation():
    for item in items:
        yield item


@app.get("/items/stream-sync-no-annotation", response_class=EventSourceResponse)
def sse_items_sync_no_annotation():
    yield from items


@app.get("/items/stream-dict", response_class=EventSourceResponse)
async def sse_items_dict():
    for item in items:
        yield {"name": item.name, "description": item.description}


@app.get("/items/stream-sse-event", response_class=EventSourceResponse)
async def sse_items_event():
    yield ServerSentEvent(data="hello", event="greeting", id="1")
    yield ServerSentEvent(data={"key": "value"}, event="json-data", id="2")
    yield ServerSentEvent(comment="just a comment")
    yield ServerSentEvent(data="retry-test", retry=5000)


@app.get("/items/stream-mixed", response_class=EventSourceResponse)
async def sse_items_mixed() -> AsyncIterable[Item]:
    yield items[0]
    yield ServerSentEvent(data="custom-event", event="special")
    yield items[1]


@app.get("/items/stream-string", response_class=EventSourceResponse)
async def sse_items_string():
    yield ServerSentEvent(data="plain text data")


@app.post("/items/stream-post", response_class=EventSourceResponse)
async def sse_items_post() -> AsyncIterable[Item]:
    for item in items:
        yield item


@app.get("/items/stream-raw", response_class=EventSourceResponse)
async def sse_items_raw():
    yield ServerSentEvent(raw_data="plain text without quotes")
    yield ServerSentEvent(raw_data="<div>html fragment</div>", event="html")
    yield ServerSentEvent(raw_data="cpu,87.3,1709145600", event="csv")


router = APIRouter()


@router.get("/events", response_class=EventSourceResponse)
async def stream_events():
    yield {"msg": "hello"}
    yield {"msg": "world"}


app.include_router(router, prefix="/api")


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as c:
        yield c


def test_async_generator_with_model(client: TestClient):
    response = client.get("/items/stream")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert response.headers["cache-control"] == "no-cache"
    assert response.headers["x-accel-buffering"] == "no"

    lines = response.text.strip().split("\n")
    data_lines = [line for line in lines if line.startswith("data: ")]
    assert len(data_lines) == 3
    assert '"name":"Plumbus"' in data_lines[0] or '"name": "Plumbus"' in data_lines[0]
    assert (
        '"name":"Portal Gun"' in data_lines[1]
        or '"name": "Portal Gun"' in data_lines[1]
    )
    assert (
        '"name":"Meeseeks Box"' in data_lines[2]
        or '"name": "Meeseeks Box"' in data_lines[2]
    )


def test_sync_generator_with_model(client: TestClient):
    response = client.get("/items/stream-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3


def test_async_generator_no_annotation(client: TestClient):
    response = client.get("/items/stream-no-annotation")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3


def test_sync_generator_no_annotation(client: TestClient):
    response = client.get("/items/stream-sync-no-annotation")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3


def test_dict_items(client: TestClient):
    response = client.get("/items/stream-dict")
    assert response.status_code == 200
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3
    assert '"name"' in data_lines[0]


def test_post_method_sse(client: TestClient):
    """SSE should work with POST (needed for MCP compatibility)."""
    response = client.post("/items/stream-post")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3


def test_sse_events_with_fields(client: TestClient):
    response = client.get("/items/stream-sse-event")
    assert response.status_code == 200
    text = response.text

    assert "event: greeting\n" in text
    assert 'data: "hello"\n' in text
    assert "id: 1\n" in text

    assert "event: json-data\n" in text
    assert "id: 2\n" in text
    assert 'data: {"key": "value"}\n' in text

    assert ": just a comment\n" in text

    assert "retry: 5000\n" in text
    assert 'data: "retry-test"\n' in text


def test_mixed_plain_and_sse_events(client: TestClient):
    response = client.get("/items/stream-mixed")
    assert response.status_code == 200
    text = response.text

    assert "event: special\n" in text
    assert 'data: "custom-event"\n' in text
    assert '"name"' in text


def test_string_data_json_encoded(client: TestClient):
    """Strings are always JSON-encoded (quoted)."""
    response = client.get("/items/stream-string")
    assert response.status_code == 200
    assert 'data: "plain text data"\n' in response.text


def test_server_sent_event_null_id_rejected():
    with pytest.raises(ValueError, match="null"):
        ServerSentEvent(data="test", id="has\0null")


def test_server_sent_event_negative_retry_rejected():
    with pytest.raises(ValueError):
        ServerSentEvent(data="test", retry=-1)


def test_server_sent_event_float_retry_rejected():
    with pytest.raises(ValueError):
        ServerSentEvent(data="test", retry=1.5)  # type: ignore[arg-type]


def test_raw_data_sent_without_json_encoding(client: TestClient):
    """raw_data is sent as-is, not JSON-encoded."""
    response = client.get("/items/stream-raw")
    assert response.status_code == 200
    text = response.text

    # raw_data should appear without JSON quotes
    assert "data: plain text without quotes\n" in text
    # Not JSON-quoted
    assert 'data: "plain text without quotes"' not in text

    assert "event: html\n" in text
    assert "data: <div>html fragment</div>\n" in text

    assert "event: csv\n" in text
    assert "data: cpu,87.3,1709145600\n" in text


def test_data_and_raw_data_mutually_exclusive():
    """Cannot set both data and raw_data."""
    with pytest.raises(ValueError, match="Cannot set both"):
        ServerSentEvent(data="json", raw_data="raw")


def test_sse_on_router_included_in_app(client: TestClient):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 2


# Keepalive ping tests


keepalive_app = FastAPI()


@keepalive_app.get("/slow-async", response_class=EventSourceResponse)
async def slow_async_stream():
    yield {"n": 1}
    # Sleep longer than the (monkeypatched) ping interval so a keepalive
    # comment is emitted before the next item.
    await asyncio.sleep(0.3)
    yield {"n": 2}


@keepalive_app.get("/slow-sync", response_class=EventSourceResponse)
def slow_sync_stream():
    yield {"n": 1}
    time.sleep(0.3)
    yield {"n": 2}


def test_keepalive_ping_async(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(fastapi.routing, "_PING_INTERVAL", 0.05)
    with TestClient(keepalive_app) as c:
        response = c.get("/slow-async")
    assert response.status_code == 200
    text = response.text
    # The keepalive comment ": ping" should appear between the two data events
    assert ": ping\n" in text
    data_lines = [line for line in text.split("\n") if line.startswith("data: ")]
    assert len(data_lines) == 2


def test_keepalive_ping_sync(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(fastapi.routing, "_PING_INTERVAL", 0.05)
    with TestClient(keepalive_app) as c:
        response = c.get("/slow-sync")
    assert response.status_code == 200
    text = response.text
    assert ": ping\n" in text
    data_lines = [line for line in text.split("\n") if line.startswith("data: ")]
    assert len(data_lines) == 2


def test_no_keepalive_when_fast(client: TestClient):
    """No keepalive comment when items arrive quickly."""
    response = client.get("/items/stream")
    assert response.status_code == 200
    # KEEPALIVE_COMMENT is ": ping\n\n".
    assert ": ping\n" not in response.text

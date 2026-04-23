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


# Tests for new SSE features (default_retry, on_disconnect, helpers)

default_retry_app = FastAPI()


@default_retry_app.get(
    "/with-default-retry",
    response_class=EventSourceResponse(default_retry=5000),
)
async def stream_with_default_retry() -> AsyncIterable[dict]:
    yield {"msg": "hello"}
    yield {"msg": "world"}


@default_retry_app.get(
    "/retry-override",
    response_class=EventSourceResponse(default_retry=5000),
)
async def stream_retry_override() -> AsyncIterable[ServerSentEvent]:
    # Event-level retry should override default
    yield ServerSentEvent(data="custom", retry=1000)
    # This one should use the default
    yield ServerSentEvent(data="default")


def test_default_retry_applied():
    """Test that default_retry is applied to events without explicit retry."""
    with TestClient(default_retry_app) as c:
        response = c.get("/with-default-retry")
        assert response.status_code == 200
        text = response.text
        # Both events should have retry: 5000
        assert text.count("retry: 5000") == 2


def test_event_retry_overrides_default():
    """Test that event-level retry overrides default_retry."""
    with TestClient(default_retry_app) as c:
        response = c.get("/retry-override")
        assert response.status_code == 200
        text = response.text
        # First event has explicit retry: 1000
        assert "retry: 1000\n" in text
        # Second event has default retry: 5000
        assert "retry: 5000\n" in text


# Tests for on_disconnect callback

disconnect_callback_called = False


disconnect_app = FastAPI()


async def on_disconnect_handler():
    global disconnect_callback_called
    disconnect_callback_called = True


# Create response instance with disconnect callback and use it in decorator
disconnect_response = EventSourceResponse(on_disconnect=on_disconnect_handler)


@disconnect_app.get("/with-disconnect", response_class=EventSourceResponse)
async def stream_with_disconnect():
    yield {"msg": "hello"}
    yield {"msg": "world"}


@disconnect_app.get("/instance-disconnect", response_class=disconnect_response)
async def stream_instance():
    yield {"msg": "hello"}


def test_on_disconnect_callback():
    """Test that on_disconnect callback is called when stream ends."""
    global disconnect_callback_called
    disconnect_callback_called = False

    with TestClient(disconnect_app) as c:
        response = c.get("/instance-disconnect")
        assert response.status_code == 200

    # Callback should have been called when stream ended
    assert disconnect_callback_called


# Tests for sse_event() helper function

from fastapi.sse import sse_event

helper_app = FastAPI()


@helper_app.get("/with-helper", response_class=EventSourceResponse)
async def stream_with_helper() -> AsyncIterable[ServerSentEvent]:
    yield sse_event(data={"status": "ok"}, event="status", id="1")
    yield sse_event(data="message", comment="keep-alive")
    yield sse_event(raw_data="raw text", event="raw")


def test_sse_event_helper():
    """Test the sse_event() helper function."""
    with TestClient(helper_app) as c:
        response = c.get("/with-helper")
        assert response.status_code == 200
        text = response.text

        # Check first event with all fields
        assert "event: status\n" in text
        assert "id: 1\n" in text
        assert 'data: {"status": "ok"}\n' in text

        # Check second event with comment
        assert ": keep-alive\n" in text
        assert 'data: "message"\n' in text

        # Check third event with raw_data
        assert "event: raw\n" in text
        assert "data: raw text\n" in text


def test_sse_event_creation():
    """Test creating ServerSentEvent via sse_event() helper."""
    event = sse_event(data={"key": "value"}, event="test", id="123", retry=3000)
    assert event.data == {"key": "value"}
    assert event.event == "test"
    assert event.id == "123"
    assert event.retry == 3000


def test_sse_event_raw_data():
    """Test sse_event() with raw_data."""
    event = sse_event(raw_data="plain text", event="log")
    assert event.raw_data == "plain text"
    assert event.event == "log"
    assert event.data is None


# Tests for SSEStream helper class

from fastapi.sse import SSEStream


@pytest.mark.anyio
async def test_sse_stream_helper():
    """Test SSEStream helper class."""
    async with SSEStream() as sse:
        assert sse.disconnected is False
        sse.mark_disconnected()
        assert sse.disconnected is True


def test_sse_stream_disconnected_property():
    """Test SSEStream disconnected property."""
    sse = SSEStream()
    assert sse.disconnected is False
    sse.mark_disconnected()
    assert sse.disconnected is True


# Tests for create_sse_stream() function

from fastapi.sse import create_sse_stream


def test_create_sse_stream():
    """Test create_sse_stream() function."""
    disconnect_called = False

    async def handler():
        nonlocal disconnect_called
        disconnect_called = True

    stream, response = create_sse_stream(on_disconnect=handler)

    assert isinstance(stream, SSEStream)
    assert isinstance(response, EventSourceResponse)
    assert response.on_disconnect is not None


@pytest.mark.anyio
async def test_create_sse_stream_disconnect():
    """Test that create_sse_stream marks stream as disconnected."""
    stream, response = create_sse_stream()

    # Call the disconnect callback
    await response.call_disconnect_callback()

    # Stream should be marked as disconnected
    assert stream.disconnected is True

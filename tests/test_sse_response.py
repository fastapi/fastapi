"""Tests for Server-Sent Events (SSE) response classes."""
import pytest
from fastapi import FastAPI
from fastapi.responses import SSEResponse, format_sse
from fastapi.testclient import TestClient


def test_format_sse_with_string_data():
    """Test format_sse with simple string data."""
    result = format_sse("Hello")
    assert result == "data: Hello\n\n"


def test_format_sse_with_dict_data():
    """Test format_sse with dict data."""
    result = format_sse({"data": "Hello", "event": "message"})
    assert result == "event: message\ndata: Hello\n\n"


def test_format_sse_with_all_params():
    """Test format_sse with all parameters."""
    result = format_sse("Hello", event="greeting", id="1", retry=5000)
    assert result == "id: 1\nevent: greeting\nretry: 5000\ndata: Hello\n\n"


def test_format_sse_multiline_data():
    """Test format_sse with multiline data."""
    result = format_sse("Line1\nLine2\nLine3")
    assert result == "data: Line1\ndata: Line2\ndata: Line3\n\n"


def test_format_sse_empty_data():
    """Test format_sse with empty data."""
    result = format_sse("")
    assert result == "data: \n\n"


def test_format_sse_with_event_only():
    """Test format_sse with only event type."""
    result = format_sse(data="test", event="myevent")
    assert result == "event: myevent\ndata: test\n\n"


def test_format_sse_with_retry():
    """Test format_sse with retry."""
    result = format_sse(data="test", retry=3000)
    assert result == "retry: 3000\ndata: test\n\n"


def test_format_sse_with_id():
    """Test format_sse with id."""
    result = format_sse(data="test", id=42)
    assert result == "id: 42\ndata: test\n\n"


# Integration tests with FastAPI


def test_sse_response_basic():
    """Test basic SSE response."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            for i in range(3):
                yield {"data": f"Message {i}"}

        return SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert "data: Message 0\n\n" in response.text
    assert "data: Message 1\n\n" in response.text
    assert "data: Message 2\n\n" in response.text


def test_sse_response_with_event_type():
    """Test SSE response with custom event type."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            for i in range(2):
                yield {"event": "notification", "data": f"Notice {i}"}

        return SSEResponse(event_generator())

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    assert "event: notification\ndata: Notice 0\n\n" in response.text
    assert "event: notification\ndata: Notice 1\n\n" in response.text


def test_sse_response_with_retry():
    """Test SSE response with retry configuration."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            for i in range(2):
                yield {"data": f"Message {i}"}

        return SSEResponse(event_generator(), retry=5000)

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    # Retry is sent as first event
    assert "retry: 5000\n\n" in response.text


def test_sse_response_with_event_serializer():
    """Test SSE response with custom event serializer."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def simple_generator():
            for i in range(3):
                yield f"Message {i}"

        def serializer(data: str) -> dict[str, str]:
            return {"data": data}

        return SSEResponse(simple_generator(), event_serializer=serializer)

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    assert "data: Message 0\n\n" in response.text
    assert "data: Message 1\n\n" in response.text
    assert "data: Message 2\n\n" in response.text


def test_sse_response_with_sync_generator():
    """Test SSE response with synchronous generator."""
    app = FastAPI()

    @app.get("/events")
    def get_events():
        def sync_generator():
            for i in range(3):
                yield {"data": f"Sync {i}"}

        return SSEResponse(sync_generator())

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    assert "data: Sync 0\n\n" in response.text
    assert "data: Sync 1\n\n" in response.text
    assert "data: Sync 2\n\n" in response.text


def test_sse_response_custom_status_code():
    """Test SSE response with custom status code."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            yield {"data": "test"}

        return SSEResponse(event_generator(), status_code=201)

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 201


def test_sse_response_custom_headers():
    """Test SSE response with custom headers."""
    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            yield {"data": "test"}

        return SSEResponse(
            event_generator(), headers={"X-Custom-Header": "custom-value"}
        )

    client = TestClient(app)
    response = client.get("/events")
    assert response.status_code == 200
    assert response.headers["x-custom-header"] == "custom-value"


def test_sse_export():
    """Test that SSEResponse is exported from fastapi."""
    from fastapi import SSEResponse
    from fastapi import format_sse
    assert SSEResponse is not None
    assert format_sse is not None

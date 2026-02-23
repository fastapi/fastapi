"""Tests for Server-Sent Events (SSE) response."""
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.responses import SSEResponse, sse_content
from fastapi.testclient import TestClient


def test_sse_response_basic():
    """Test basic SSE response with event data."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"event": "message", "data": "Hello"}
            yield {"data": "World"}

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    # Check that the SSE format is correct
    content = response.text
    assert "event: message" in content
    assert "data: Hello" in content
    assert "data: World" in content


def test_sse_response_with_retry():
    """Test SSE response with retry configuration."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"data": "Hello"}

        return SSEResponse(generator(), retry=5000)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "retry: 5000" in response.text


def test_sse_response_with_event_id():
    """Test SSE response with event ID."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"event": "update", "data": "test", "id": "1"}

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "event: update" in response.text
    assert "data: test" in response.text
    assert "id: 1" in response.text


def test_sse_response_string_content():
    """Test SSE response with pre-formatted string content."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[str, None]:
            yield "data: Hello\n\n"

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "data: Hello" in response.text


def test_sse_response_json_data():
    """Test SSE response with JSON data."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"data": {"message": "hello", "count": 42}}

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    # JSON data should be serialized
    assert '"message": "hello"' in response.text
    assert '"count": 42' in response.text


def test_sse_response_with_retry_in_event():
    """Test SSE response retry in event data overrides default."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            # Event-level retry should override constructor retry
            yield {"data": "Hello", "retry": 3000}

        return SSEResponse(generator(), retry=5000)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "retry: 3000" in response.text
    # The default retry should not appear
    lines = response.text.split("\n")
    retry_count = sum(1 for line in lines if line.startswith("retry:"))
    assert retry_count == 1


def test_sse_content_helper():
    """Test the sse_content helper function."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"event": "message", "data": "Hello"}
            yield {"data": "World"}

        from starlette.responses import StreamingResponse

        return StreamingResponse(sse_content(generator()), media_type="text/event-stream")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    content = response.text
    assert "event: message" in content
    assert "data: Hello" in content
    assert "data: World" in content


def test_sse_response_custom_media_type():
    """Test SSE response with custom media type."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"data": "Hello"}

        return SSEResponse(generator(), media_type="text/event-stream; charset=utf-8")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]


def test_sse_response_data_newlines():
    """Test SSE response with multiline data."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"data": "line1\nline2\nline3"}

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    # Each line should be prefixed with "data: "
    assert "data: line1" in response.text
    assert "data: line2" in response.text
    assert "data: line3" in response.text


def test_sse_response_multiple_events():
    """Test SSE response with multiple events."""
    app = FastAPI()

    @app.get("/events")
    def events():
        async def generator() -> AsyncGenerator[dict[str, Any], None]:
            yield {"event": "first", "data": "data1"}
            yield {"event": "second", "data": "data2", "id": "2"}
            yield {"data": "data3"}

        return SSEResponse(generator())

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/events")

    assert response.status_code == 200
    content = response.text
    # First event
    assert "event: first" in content
    assert "data: data1" in content
    # Second event
    assert "event: second" in content
    assert "data: data2" in content
    assert "id: 2" in content
    # Third event (no event type)
    assert content.count("data: data3") == 1

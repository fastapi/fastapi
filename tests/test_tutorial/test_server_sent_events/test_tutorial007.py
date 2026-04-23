"""
Test SSE disconnect callback functionality.
"""

import pytest
from fastapi.testclient import TestClient

pytestmark = [
    pytest.mark.anyio,
]


def test_disconnect_callback_called():
    """Test that on_disconnect callback is called when response completes."""
    from docs_src.server_sent_events import tutorial007_py310

    # Clear any previous disconnect events
    tutorial007_py310.disconnect_events.clear()

    client = TestClient(tutorial007_py310.app, raise_server_exceptions=True)

    # Make a request and read the full response
    response = client.get("/items/stream")
    assert response.status_code == 200
    _ = response.text  # Read full response

    # The disconnect callback should have been called
    assert len(tutorial007_py310.disconnect_events) == 1
    assert tutorial007_py310.disconnect_events[0] == "client_disconnected"


def test_disconnect_callback_multiple_requests():
    """Test that disconnect callback is called for each request."""
    from docs_src.server_sent_events import tutorial007_py310

    # Clear any previous disconnect events
    tutorial007_py310.disconnect_events.clear()

    client = TestClient(tutorial007_py310.app)

    # Make multiple requests
    for _ in range(3):
        response = client.get("/items/stream")
        assert response.status_code == 200
        _ = response.text

    # The disconnect callback should have been called for each request
    assert len(tutorial007_py310.disconnect_events) == 3


def test_stream_items_with_disconnect():
    """Test normal streaming with disconnect callback (no early disconnect)."""
    from docs_src.server_sent_events import tutorial007_py310

    # Clear any previous disconnect events
    tutorial007_py310.disconnect_events.clear()

    client = TestClient(tutorial007_py310.app)

    response = client.get("/items/stream")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    lines = response.text.strip().split("\n")

    # Check event structure
    event_lines = [line for line in lines if line.startswith("event: ")]
    assert len(event_lines) == 3
    assert all(line == "event: item_update" for line in event_lines)

    data_lines = [line for line in lines if line.startswith("data: ")]
    assert len(data_lines) == 3

    id_lines = [line for line in lines if line.startswith("id: ")]
    assert id_lines == ["id: 1", "id: 2", "id: 3"]

    # After response completes, disconnect should be called
    assert len(tutorial007_py310.disconnect_events) == 1

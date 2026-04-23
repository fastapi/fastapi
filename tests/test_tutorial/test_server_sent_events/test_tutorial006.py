import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial006_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.server_sent_events.{request.param}")

    client = TestClient(mod.app)
    return client


def test_stream_items_with_default_retry(client: TestClient):
    """Test that default_retry is applied to all events."""
    response = client.get("/items/stream")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    lines = response.text.strip().split("\n")

    # Check that retry: 3000 appears for each event
    retry_lines = [line for line in lines if line.startswith("retry: ")]
    assert len(retry_lines) == 3
    assert all(line == "retry: 3000" for line in retry_lines)


def test_stream_items_override_retry(client: TestClient):
    """Test that individual events can override the default retry."""
    response = client.get("/items/stream-override")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    lines = response.text.strip().split("\n")

    # Check that retry: 10000 (override) appears for each event
    retry_lines = [line for line in lines if line.startswith("retry: ")]
    assert len(retry_lines) == 3
    assert all(line == "retry: 10000" for line in retry_lines)


def test_stream_items_plain(client: TestClient):
    """Test that plain objects are automatically formatted as SSE with default retry."""
    response = client.get("/items/stream-plain")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    # Check data lines contain JSON-serialized items
    data_lines = [line for line in response.text.strip().split("\n") if line.startswith("data: ")]
    assert len(data_lines) == 3
    assert '"name":"Plumbus"' in data_lines[0]
    assert '"name":"Portal Gun"' in data_lines[1]
    assert '"name":"Meeseeks Box"' in data_lines[2]


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/stream": {
                    "get": {
                        "summary": "Stream Items With Default Retry",
                        "description": "Stream items with a default retry of 3000ms.",
                        "operationId": "stream_items_with_default_retry_items_stream_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {"type": "string"},
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/items/stream-override": {
                    "get": {
                        "summary": "Stream Items Override Retry",
                        "description": "Stream items where individual events can override the default retry.",
                        "operationId": "stream_items_override_retry_items_stream_override_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {"type": "string"},
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/items/stream-plain": {
                    "get": {
                        "summary": "Stream Items Plain",
                        "description": "Stream items as plain objects (automatically formatted as SSE).",
                        "operationId": "stream_items_plain_items_stream_plain_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {'type': 'object', 'properties': {'data': {'type': 'string', 'contentMediaType': 'application/json', 'contentSchema': {'$ref': '#/components/schemas/Item'}}, 'event': {'type': 'string'}, 'id': {'type': 'string'}, 'retry': {'type': 'integer', 'minimum': 0}}, 'required': ['data']}
                                    }
                                },
                            }
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "Item": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "price": {"type": "number", "title": "Price"},
                        },
                        "type": "object",
                        "required": ["name", "price"],
                        "title": "Item",
                    }
                }
            },
        }
    )

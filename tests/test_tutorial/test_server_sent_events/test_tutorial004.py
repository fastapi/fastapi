import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial004_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.server_sent_events.{request.param}")
    client = TestClient(mod.app)
    return client


def test_stream_all_items(client: TestClient):
    response = client.get("/items/stream")
    assert response.status_code == 200, response.text

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 3

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    assert id_lines == ["id: 0", "id: 1", "id: 2"]


def test_resume_from_last_event_id(client: TestClient):
    response = client.get(
        "/items/stream",
        headers={"last-event-id": "0"},
    )
    assert response.status_code == 200, response.text

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 2

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    assert id_lines == ["id: 1", "id: 2"]


def test_resume_from_last_item(client: TestClient):
    response = client.get(
        "/items/stream",
        headers={"last-event-id": "1"},
    )
    assert response.status_code == 200, response.text

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    assert len(data_lines) == 1

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    assert id_lines == ["id: 2"]


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
                        "summary": "Stream Items",
                        "operationId": "stream_items_items_stream_get",
                        "parameters": [
                            {
                                "name": "last-event-id",
                                "in": "header",
                                "required": False,
                                "schema": {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Last-Event-Id",
                                },
                            }
                        ],
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
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                            "input": {"title": "Input"},
                            "ctx": {"type": "object", "title": "Context"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )

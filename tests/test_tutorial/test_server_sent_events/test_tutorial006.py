import importlib
import json

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


def test_stream_items(client: TestClient):
    response = client.get("/items/stream")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    lines = response.text.strip().split("\n")

    event_lines = [line for line in lines if line.startswith("event: ")]
    assert len(event_lines) == 3
    assert all(line == "event: item_update" for line in event_lines)

    data_lines = [line for line in lines if line.startswith("data: ")]
    assert len(data_lines) == 3
    payloads = [json.loads(line[len("data: ") :]) for line in data_lines]
    assert payloads[0] == {"name": "Plumbus", "price": 32.99}
    assert payloads[1] == {"name": "Portal Gun", "price": 999.99}
    assert payloads[2] == {"name": "Meeseeks Box", "price": 49.99}

    id_lines = [line for line in lines if line.startswith("id: ")]
    assert id_lines == ["id: 1", "id: 2", "id: 3"]


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
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "$ref": "#/components/schemas/Item"
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
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

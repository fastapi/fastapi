import importlib
import json

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.stream_json_lines.{request.param}")

    client = TestClient(mod.app)
    return client


def test_stream_items_with_custom_header(client: TestClient):
    response = client.get("/items/stream")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "application/jsonl"
    assert response.headers["x-stream-source"] == "inventory"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [
        {"name": "Plumbus", "description": "A multi-purpose household device."},
        {"name": "Portal Gun", "description": "A portal opening device."},
        {"name": "Meeseeks Box", "description": "A box that summons a Meeseeks."},
    ]


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
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "$ref": "#/components/schemas/Item"
                                        },
                                    }
                                },
                            }
                        },
                        "summary": "Stream Items",
                        "operationId": "stream_items_items_stream_get",
                    }
                }
            },
            "components": {
                "schemas": {
                    "Item": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "description": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "null"},
                                ],
                                "title": "Description",
                            },
                        },
                        "type": "object",
                        "required": ["name", "description"],
                        "title": "Item",
                    }
                }
            },
        }
    )

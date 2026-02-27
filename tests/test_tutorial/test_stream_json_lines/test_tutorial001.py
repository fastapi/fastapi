import importlib
import json

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.stream_json_lines.{request.param}")

    client = TestClient(mod.app)
    return client


expected_items = [
    {"name": "Plumbus", "description": "A multi-purpose household device."},
    {"name": "Portal Gun", "description": "A portal opening device."},
    {"name": "Meeseeks Box", "description": "A box that summons a Meeseeks."},
]


@pytest.mark.parametrize(
    "path",
    [
        "/items/stream",
        "/items/stream-no-async",
        "/items/stream-no-annotation",
        "/items/stream-no-async-no-annotation",
    ],
)
def test_stream_items(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == expected_items


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
                },
                "/items/stream-no-async": {
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
                        "summary": "Stream Items No Async",
                        "operationId": "stream_items_no_async_items_stream_no_async_get",
                    }
                },
                "/items/stream-no-annotation": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {},
                                    }
                                },
                            }
                        },
                        "summary": "Stream Items No Annotation",
                        "operationId": "stream_items_no_annotation_items_stream_no_annotation_get",
                    }
                },
                "/items/stream-no-async-no-annotation": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {},
                                    }
                                },
                            }
                        },
                        "summary": "Stream Items No Async No Annotation",
                        "operationId": "stream_items_no_async_no_annotation_items_stream_no_async_no_annotation_get",
                    }
                },
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

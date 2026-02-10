import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dataclasses_.{request.param}")

    client = TestClient(mod.app)
    client.headers.clear()
    return client


def test_get_item(client: TestClient):
    response = client.get("/items/next")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
        "tax": None,
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/next": {
                    "get": {
                        "summary": "Read Next Item",
                        "operationId": "read_next_item_items_next_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                        "title": "Item",
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "price": {"title": "Price", "type": "number"},
                            "tags": {
                                "title": "Tags",
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "description": {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            },
                            "tax": {
                                "title": "Tax",
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                            },
                        },
                    }
                }
            },
        }
    )

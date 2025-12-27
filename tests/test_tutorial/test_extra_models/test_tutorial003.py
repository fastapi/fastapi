import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.extra_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_get_car(client: TestClient):
    response = client.get("/items/item1")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "All my friends drive a low rider",
        "type": "car",
    }


def test_get_plane(client: TestClient):
    response = client.get("/items/item2")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/{item_id}": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Response Read Item Items  Item Id  Get",
                                            "anyOf": [
                                                {
                                                    "$ref": "#/components/schemas/PlaneItem"
                                                },
                                                {
                                                    "$ref": "#/components/schemas/CarItem"
                                                },
                                            ],
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
                        "summary": "Read Item",
                        "operationId": "read_item_items__item_id__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Item Id", "type": "string"},
                                "name": "item_id",
                                "in": "path",
                            }
                        ],
                    }
                }
            },
            "components": {
                "schemas": {
                    "PlaneItem": {
                        "title": "PlaneItem",
                        "required": ["description", "size"],
                        "type": "object",
                        "properties": {
                            "description": {"title": "Description", "type": "string"},
                            "type": {
                                "title": "Type",
                                "type": "string",
                                "default": "plane",
                            },
                            "size": {"title": "Size", "type": "integer"},
                        },
                    },
                    "CarItem": {
                        "title": "CarItem",
                        "required": ["description"],
                        "type": "object",
                        "properties": {
                            "description": {"title": "Description", "type": "string"},
                            "type": {
                                "title": "Type",
                                "type": "string",
                                "default": "car",
                            },
                        },
                    },
                    "ValidationError": {
                        "title": "ValidationError",
                        "required": ["loc", "msg", "type"],
                        "type": "object",
                        "properties": {
                            "loc": {
                                "title": "Location",
                                "type": "array",
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                            },
                            "msg": {"title": "Message", "type": "string"},
                            "type": {"title": "Error Type", "type": "string"},
                        },
                    },
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                }
            },
        }
    )

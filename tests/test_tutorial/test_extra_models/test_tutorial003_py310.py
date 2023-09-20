import pytest
from dirty_equals import IsOneOf
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.extra_models.tutorial003_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_get_car(client: TestClient):
    response = client.get("/items/item1")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "All my friends drive a low rider",
        "type": "car",
    }


@needs_py310
def test_get_plane(client: TestClient):
    response = client.get("/items/item2")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    }


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
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
                                            {"$ref": "#/components/schemas/PlaneItem"},
                                            {"$ref": "#/components/schemas/CarItem"},
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
                    "required": IsOneOf(
                        ["description", "type", "size"],
                        # TODO: remove when deprecating Pydantic v1
                        ["description", "size"],
                    ),
                    "type": "object",
                    "properties": {
                        "description": {"title": "Description", "type": "string"},
                        "type": {"title": "Type", "type": "string", "default": "plane"},
                        "size": {"title": "Size", "type": "integer"},
                    },
                },
                "CarItem": {
                    "title": "CarItem",
                    "required": IsOneOf(
                        ["description", "type"],
                        # TODO: remove when deprecating Pydantic v1
                        ["description"],
                    ),
                    "type": "object",
                    "properties": {
                        "description": {"title": "Description", "type": "string"},
                        "type": {"title": "Type", "type": "string", "default": "car"},
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
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }

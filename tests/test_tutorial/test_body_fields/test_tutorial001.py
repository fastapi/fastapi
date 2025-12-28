import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an_py39",
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_fields.{request.param}")

    client = TestClient(mod.app)
    return client


def test_items_5(client: TestClient):
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": 3.0}})
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "item": {"name": "Foo", "price": 3.0, "description": None, "tax": None},
    }


def test_items_6(client: TestClient):
    response = client.put(
        "/items/6",
        json={
            "item": {
                "name": "Bar",
                "price": 0.2,
                "description": "Some bar",
                "tax": "5.4",
            }
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 6,
        "item": {
            "name": "Bar",
            "price": 0.2,
            "description": "Some bar",
            "tax": 5.4,
        },
    }


def test_invalid_price(client: TestClient):
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": -3.0}})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["body", "item", "price"],
                "msg": "Input should be greater than 0",
                "input": -3.0,
                "ctx": {"gt": 0.0},
            }
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "put": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
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
                    "summary": "Update Item",
                    "operationId": "update_item_items__item_id__put",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "integer"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
                                }
                            }
                        },
                        "required": True,
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
                        "description": {
                            "title": "The description of the item",
                            "anyOf": [
                                {"maxLength": 300, "type": "string"},
                                {"type": "null"},
                            ],
                        },
                        "price": {
                            "title": "Price",
                            "exclusiveMinimum": 0.0,
                            "type": "number",
                            "description": "The price must be greater than zero",
                        },
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
                        },
                    },
                },
                "Body_update_item_items__item_id__put": {
                    "title": "Body_update_item_items__item_id__put",
                    "required": ["item"],
                    "type": "object",
                    "properties": {"item": {"$ref": "#/components/schemas/Item"}},
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

import importlib
from typing import Union

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize("price", ["50.5", 50.5])
def test_post_with_tax(client: TestClient, price: Union[str, float]):
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": price, "description": "Some Foo", "tax": 0.3},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": "Some Foo",
        "tax": 0.3,
        "price_with_tax": 50.8,
    }


@pytest.mark.parametrize("price", ["50.5", 50.5])
def test_post_without_tax(client: TestClient, price: Union[str, float]):
    response = client.post(
        "/items/", json={"name": "Foo", "price": price, "description": "Some Foo"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": "Some Foo",
        "tax": None,
    }


def test_post_with_no_data(client: TestClient):
    response = client.post("/items/", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "name"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "price"],
                "msg": "Field required",
                "input": {},
            },
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
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
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
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
                        "price": {"title": "Price", "type": "number"},
                        "description": {
                            "title": "Description",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
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
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }

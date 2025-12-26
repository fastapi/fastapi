import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
        pytest.param("tutorial004_an_py39"),
        pytest.param("tutorial004_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_multiple_params.{request.param}")

    client = TestClient(mod.app)
    return client


def test_put_all(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "importance": 2,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
        params={"q": "somequery"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "importance": 2,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        },
        "user": {"username": "Dave", "full_name": None},
        "q": "somequery",
    }


def test_put_only_required(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "importance": 2,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "importance": 2,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        },
        "user": {"username": "Dave", "full_name": None},
    }


def test_put_missing_body(client: TestClient):
    response = client.put("/items/5")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": [
                    "body",
                    "item",
                ],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": None,
                "loc": [
                    "body",
                    "user",
                ],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": None,
                "loc": [
                    "body",
                    "importance",
                ],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


def test_put_empty_body(client: TestClient):
    response = client.put("/items/5", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "item"],
                "msg": "Field required",
                "input": None,
            },
            {
                "type": "missing",
                "loc": ["body", "user"],
                "msg": "Field required",
                "input": None,
            },
            {
                "type": "missing",
                "loc": ["body", "importance"],
                "msg": "Field required",
                "input": None,
            },
        ]
    }


def test_put_invalid_importance(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "importance": 0,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "importance"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
                "input": 0,
                "ctx": {"gt": 0},
            },
        ],
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
                        },
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Q",
                            },
                            "name": "q",
                            "in": "query",
                        },
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
                            "title": "Description",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "price": {"title": "Price", "type": "number"},
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
                        },
                    },
                },
                "User": {
                    "title": "User",
                    "required": ["username"],
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "full_name": {
                            "title": "Full Name",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                    },
                },
                "Body_update_item_items__item_id__put": {
                    "title": "Body_update_item_items__item_id__put",
                    "required": ["item", "user", "importance"],
                    "type": "object",
                    "properties": {
                        "item": {"$ref": "#/components/schemas/Item"},
                        "user": {"$ref": "#/components/schemas/User"},
                        "importance": {
                            "title": "Importance",
                            "type": "integer",
                            "exclusiveMinimum": 0.0,
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

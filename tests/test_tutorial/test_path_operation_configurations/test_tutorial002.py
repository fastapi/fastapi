import importlib

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest) -> TestClient:
    mod = importlib.import_module(
        f"docs_src.path_operation_configuration.{request.param}"
    )
    return TestClient(mod.app)


def test_post_items(client: TestClient):
    response = client.post(
        "/items/",
        json={
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": ["bar", "baz"],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "description": "Item description",
        "price": 42.0,
        "tax": 3.2,
        "tags": IsList("bar", "baz", check_order=False),
    }


def test_get_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "Foo", "price": 42}]


def test_get_users(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"username": "johndoe"}]


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "tags": ["items"],
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                },
                "post": {
                    "tags": ["items"],
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
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
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
                },
            },
            "/users/": {
                "get": {
                    "tags": ["users"],
                    "summary": "Read Users",
                    "operationId": "read_users_users__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "Item": {
                    "properties": {
                        "description": {
                            "anyOf": [
                                {
                                    "type": "string",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Description",
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                        "price": {
                            "title": "Price",
                            "type": "number",
                        },
                        "tags": {
                            "default": [],
                            "items": {
                                "type": "string",
                            },
                            "title": "Tags",
                            "type": "array",
                            "uniqueItems": True,
                        },
                        "tax": {
                            "anyOf": [
                                {
                                    "type": "number",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Tax",
                        },
                    },
                    "required": [
                        "name",
                        "price",
                    ],
                    "title": "Item",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
    }

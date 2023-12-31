import importlib
from pathlib import Path

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_pydanticv1


@pytest.fixture(scope="module")
def client():
    test_db = Path("./sql_app.db")
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    # Import while creating the client to create the DB after starting the test session
    from docs_src.sql_databases.sql_app import alt_main

    # Ensure import side effects are re-executed
    importlib.reload(alt_main)

    with TestClient(alt_main.app) as c:
        yield c
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_create_user(client):
    test_user = {"email": "johndoe@example.com", "password": "secret"}
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert test_user["email"] == data["email"]
    assert "id" in data
    response = client.post("/users/", json=test_user)
    assert response.status_code == 400, response.text


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "email" in data
    assert "id" in data


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_inexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == 404, response.text


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "email" in data[0]
    assert "id" in data[0]


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_create_item(client):
    item = {"title": "Foo", "description": "Something that fights"}
    response = client.post("/users/1/items/", json=item)
    assert response.status_code == 200, response.text
    item_data = response.json()
    assert item["title"] == item_data["title"]
    assert item["description"] == item_data["description"]
    assert "id" in item_data
    assert "owner_id" in item_data
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    user_data = response.json()
    item_to_check = [it for it in user_data["items"] if it["id"] == item_data["id"]][0]
    assert item_to_check["title"] == item["title"]
    assert item_to_check["description"] == item["description"]
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    user_data = response.json()
    item_to_check = [it for it in user_data["items"] if it["id"] == item_data["id"]][0]
    assert item_to_check["title"] == item["title"]
    assert item_to_check["description"] == item["description"]


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data
    first_item = data[0]
    assert "title" in first_item
    assert "description" in first_item


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response Read Users Users  Get",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/User"},
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
                    "summary": "Read Users",
                    "operationId": "read_users_users__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Skip",
                                "type": "integer",
                                "default": 0,
                            },
                            "name": "skip",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {
                                "title": "Limit",
                                "type": "integer",
                                "default": 100,
                            },
                            "name": "limit",
                            "in": "query",
                        },
                    ],
                },
                "post": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
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
                    "summary": "Create User",
                    "operationId": "create_user_users__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserCreate"}
                            }
                        },
                        "required": True,
                    },
                },
            },
            "/users/{user_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
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
                    "summary": "Read User",
                    "operationId": "read_user_users__user_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "User Id", "type": "integer"},
                            "name": "user_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/users/{user_id}/items/": {
                "post": {
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
                    "summary": "Create Item For User",
                    "operationId": "create_item_for_user_users__user_id__items__post",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "User Id", "type": "integer"},
                            "name": "user_id",
                            "in": "path",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ItemCreate"}
                            }
                        },
                        "required": True,
                    },
                }
            },
            "/items/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response Read Items Items  Get",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
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
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Skip",
                                "type": "integer",
                                "default": 0,
                            },
                            "name": "skip",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {
                                "title": "Limit",
                                "type": "integer",
                                "default": 100,
                            },
                            "name": "limit",
                            "in": "query",
                        },
                    ],
                }
            },
        },
        "components": {
            "schemas": {
                "ItemCreate": {
                    "title": "ItemCreate",
                    "required": ["title"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Description", "type": "string"}
                        ),
                    },
                },
                "Item": {
                    "title": "Item",
                    "required": ["title", "id", "owner_id"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Description", "type": "string"},
                        ),
                        "id": {"title": "Id", "type": "integer"},
                        "owner_id": {"title": "Owner Id", "type": "integer"},
                    },
                },
                "User": {
                    "title": "User",
                    "required": ["email", "id", "is_active"],
                    "type": "object",
                    "properties": {
                        "email": {"title": "Email", "type": "string"},
                        "id": {"title": "Id", "type": "integer"},
                        "is_active": {"title": "Is Active", "type": "boolean"},
                        "items": {
                            "title": "Items",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Item"},
                            "default": [],
                        },
                    },
                },
                "UserCreate": {
                    "title": "UserCreate",
                    "required": ["email", "password"],
                    "type": "object",
                    "properties": {
                        "email": {"title": "Email", "type": "string"},
                        "password": {"title": "Password", "type": "string"},
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

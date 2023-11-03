from typing import Optional

from dirty_equals import IsDict
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


user_router = APIRouter()
item_router = APIRouter()


@user_router.get("/")
def get_users():
    return [{"user_id": "u1"}, {"user_id": "u2"}]


@user_router.get("/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}


@item_router.get("/")
def get_items(user_id: Optional[str] = None):
    if user_id is None:
        return [{"item_id": "i1", "user_id": "u1"}, {"item_id": "i2", "user_id": "u2"}]
    else:
        return [{"item_id": "i2", "user_id": user_id}]


@item_router.get("/{item_id}")
def get_item(item_id: str, user_id: Optional[str] = None):
    if user_id is None:
        return {"item_id": item_id}
    else:
        return {"item_id": item_id, "user_id": user_id}


app.include_router(user_router, prefix="/users")
app.include_router(item_router, prefix="/items")

app.include_router(item_router, prefix="/users/{user_id}/items")


client = TestClient(app)


def test_get_users():
    """Check that /users returns expected data"""
    response = client.get("/users")
    assert response.status_code == 200, response.text
    assert response.json() == [{"user_id": "u1"}, {"user_id": "u2"}]


def test_get_user():
    """Check that /users/{user_id} returns expected data"""
    response = client.get("/users/abc123")
    assert response.status_code == 200, response.text
    assert response.json() == {"user_id": "abc123"}


def test_get_items_1():
    """Check that /items returns expected data"""
    response = client.get("/items")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"item_id": "i1", "user_id": "u1"},
        {"item_id": "i2", "user_id": "u2"},
    ]


def test_get_items_2():
    """Check that /items returns expected data with user_id specified"""
    response = client.get("/items?user_id=abc123")
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "i2", "user_id": "abc123"}]


def test_get_item_1():
    """Check that /items/{item_id} returns expected data"""
    response = client.get("/items/item01")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "item01"}


def test_get_item_2():
    """Check that /items/{item_id} returns expected data with user_id specified"""
    response = client.get("/items/item01?user_id=abc123")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "item01", "user_id": "abc123"}


def test_get_users_items():
    """Check that /users/{user_id}/items returns expected data"""
    response = client.get("/users/abc123/items")
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "i2", "user_id": "abc123"}]


def test_get_users_item():
    """Check that /users/{user_id}/items returns expected data"""
    response = client.get("/users/abc123/items/item01")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "item01", "user_id": "abc123"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users/": {
                "get": {
                    "summary": "Get Users",
                    "operationId": "get_users_users__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
            "/users/{user_id}": {
                "get": {
                    "summary": "Get User",
                    "operationId": "get_user_users__user_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "User Id", "type": "string"},
                            "name": "user_id",
                            "in": "path",
                        }
                    ],
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
                }
            },
            "/items/": {
                "get": {
                    "summary": "Get Items",
                    "operationId": "get_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "name": "user_id",
                            "in": "query",
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "User Id",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "User Id", "type": "string"}
                            ),
                        }
                    ],
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
                }
            },
            "/items/{item_id}": {
                "get": {
                    "summary": "Get Item",
                    "operationId": "get_item_items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "name": "item_id",
                            "in": "path",
                        },
                        {
                            "required": False,
                            "name": "user_id",
                            "in": "query",
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "User Id",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "User Id", "type": "string"}
                            ),
                        },
                    ],
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
                }
            },
            "/users/{user_id}/items/": {
                "get": {
                    "summary": "Get Items",
                    "operationId": "get_items_users__user_id__items__get",
                    "parameters": [
                        {
                            "required": True,
                            "name": "user_id",
                            "in": "path",
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "User Id",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "User Id", "type": "string"}
                            ),
                        }
                    ],
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
                }
            },
            "/users/{user_id}/items/{item_id}": {
                "get": {
                    "summary": "Get Item",
                    "operationId": "get_item_users__user_id__items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "name": "item_id",
                            "in": "path",
                        },
                        {
                            "required": True,
                            "name": "user_id",
                            "in": "path",
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "User Id",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "User Id", "type": "string"}
                            ),
                        },
                    ],
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
                }
            },
        },
        "components": {
            "schemas": {
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
            }
        },
    }

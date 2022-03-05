from fastapi.testclient import TestClient

from docs_src.generate_clients.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "tags": ["items"],
                "summary": "Get Items",
                "operationId": "items-get_items",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Items-Get Items",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["items"],
                "summary": "Create Item",
                "operationId": "items-create_item",
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
                                "schema": {
                                    "$ref": "#/components/schemas/ResponseMessage"
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
            },
        },
        "/users/": {
            "post": {
                "tags": ["users"],
                "summary": "Create User",
                "operationId": "users-create_user",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ResponseMessage"
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
            "Item": {
                "title": "Item",
                "required": ["name", "price"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {"title": "Price", "type": "number"},
                },
            },
            "ResponseMessage": {
                "title": "ResponseMessage",
                "required": ["message"],
                "type": "object",
                "properties": {"message": {"title": "Message", "type": "string"}},
            },
            "User": {
                "title": "User",
                "required": ["username", "email"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
                    "email": {"title": "Email", "type": "string"},
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
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi():
    with client:
        response = client.get("/openapi.json")

        assert response.json() == openapi_schema


def test_post_items():
    response = client.post("/items/", json={"name": "Foo", "price": 5})
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Item received"}


def test_post_users():
    response = client.post(
        "/users/", json={"username": "Foo", "email": "foo@example.com"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "User received"}


def test_get_items():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]

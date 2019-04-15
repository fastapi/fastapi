import pytest
from starlette.testclient import TestClient

from dependencies.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
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
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Q", "type": "string"},
                        "name": "q",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {"title": "Skip", "type": "integer", "default": 0},
                        "name": "skip",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {"title": "Limit", "type": "integer", "default": 100},
                        "name": "limit",
                        "in": "query",
                    },
                ],
            }
        },
        "/users/": {
            "get": {
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
                "summary": "Read Users",
                "operationId": "read_users_users__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Q", "type": "string"},
                        "name": "q",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {"title": "Skip", "type": "integer", "default": 0},
                        "name": "skip",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {"title": "Limit", "type": "integer", "default": 100},
                        "name": "limit",
                        "in": "query",
                    },
                ],
            }
        },
    },
    "components": {
        "schemas": {
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/items", 200, {"q": None, "skip": 0, "limit": 100}),
        ("/items?q=foo", 200, {"q": "foo", "skip": 0, "limit": 100}),
        ("/items?q=foo&skip=5", 200, {"q": "foo", "skip": 5, "limit": 100}),
        ("/items?q=foo&skip=5&limit=30", 200, {"q": "foo", "skip": 5, "limit": 30}),
        ("/users", 200, {"q": None, "skip": 0, "limit": 100}),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response

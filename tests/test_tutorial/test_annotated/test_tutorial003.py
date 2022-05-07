import pytest
from fastapi.testclient import TestClient

from docs_src.annotated.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__item_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMinimum": 0.0,
                            "type": "integer",
                        },
                        "name": "item_id",
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
        "/users": {
            "get": {
                "summary": "Read Users",
                "operationId": "read_users_users_get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {
                            "title": "User Id",
                            "minLength": 1,
                            "type": "string",
                            "default": "me",
                        },
                        "name": "user_id",
                        "in": "query",
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}

item_id_negative = {
    "detail": [
        {
            "ctx": {"limit_value": 0},
            "loc": ["path", "item_id"],
            "msg": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt",
        }
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/items/1", 200, {"item_id": 1}),
        ("/items/-1", 422, item_id_negative),
        ("/users", 200, {"user_id": "me"}),
        ("/users?user_id=foo", 200, {"user_id": "foo"}),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response

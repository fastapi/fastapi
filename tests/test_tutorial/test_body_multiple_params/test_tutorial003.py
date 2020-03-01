import pytest
from fastapi.testclient import TestClient

from body_multiple_params.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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
                    "price": {"title": "Price", "type": "number"},
                    "description": {"title": "Description", "type": "string"},
                    "tax": {"title": "Tax", "type": "number"},
                },
            },
            "User": {
                "title": "User",
                "required": ["username"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
                    "full_name": {"title": "Full Name", "type": "string"},
                },
            },
            "Body_update_item_items__item_id__put": {
                "title": "Body_update_item_items__item_id__put",
                "required": ["item", "user", "importance"],
                "type": "object",
                "properties": {
                    "item": {"$ref": "#/components/schemas/Item"},
                    "user": {"$ref": "#/components/schemas/User"},
                    "importance": {"title": "Importance", "type": "integer"},
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


# Test required and embedded body parameters with no bodies sent
@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/items/5",
            {
                "importance": 2,
                "item": {"name": "Foo", "price": 50.5},
                "user": {"username": "Dave"},
            },
            200,
            {
                "item_id": 5,
                "importance": 2,
                "item": {
                    "name": "Foo",
                    "price": 50.5,
                    "description": None,
                    "tax": None,
                },
                "user": {"username": "Dave", "full_name": None},
            },
        ),
        (
            "/items/5",
            None,
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "item"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "importance"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            "/items/5",
            [],
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "item"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "importance"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
    ],
)
def test_post_body(path, body, expected_status, expected_response):
    response = client.put(path, json=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response

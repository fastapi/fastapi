import pytest
from starlette.testclient import TestClient

from body.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                "summary": "Create Item Post",
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
                    "description": {"title": "Description", "type": "string"},
                    "tax": {"title": "Tax", "type": "number"},
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


def test_openapi_scheme():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


price_missing = {
    "detail": [
        {
            "loc": ["body", "item", "price"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

price_not_float = {
    "detail": [
        {
            "loc": ["body", "item", "price"],
            "msg": "value is not a valid float",
            "type": "type_error.float",
        }
    ]
}

name_price_missing = {
    "detail": [
        {
            "loc": ["body", "item", "name"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "item", "price"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}


@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/items/",
            {"name": "Foo", "price": 50.5},
            200,
            {"name": "Foo", "price": 50.5, "description": None, "tax": None},
        ),
        (
            "/items/",
            {"name": "Foo", "price": "50.5"},
            200,
            {"name": "Foo", "price": 50.5, "description": None, "tax": None},
        ),
        (
            "/items/",
            {"name": "Foo", "price": "50.5", "description": "Some Foo"},
            200,
            {"name": "Foo", "price": 50.5, "description": "Some Foo", "tax": None},
        ),
        (
            "/items/",
            {"name": "Foo", "price": "50.5", "description": "Some Foo", "tax": 0.3},
            200,
            {"name": "Foo", "price": 50.5, "description": "Some Foo", "tax": 0.3},
        ),
        ("/items/", {"name": "Foo"}, 422, price_missing),
        ("/items/", {"name": "Foo", "price": "twenty"}, 422, price_not_float),
        ("/items/", {}, 422, name_price_missing),
    ],
)
def test_post_body(path, body, expected_status, expected_response):
    response = client.post(path, json=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response

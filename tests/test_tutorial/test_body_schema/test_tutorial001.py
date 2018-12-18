import sys

import pytest
from starlette.testclient import TestClient

from body_schema.tutorial001 import app

client = TestClient(app)


print(sys.path)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                "summary": "Update Item Put",
                "operationId": "update_item_items__item_id__put",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "integer"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Body_update_item"}
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
                        "title": "The description of the item",
                        "maxLength": 300,
                        "type": "string",
                    },
                    "price": {
                        "title": "Price",
                        "exclusiveMinimum": 0.0,
                        "type": "number",
                        "description": "The price must be greater than zero",
                    },
                    "tax": {"title": "Tax", "type": "number"},
                },
            },
            "Body_update_item": {
                "title": "Body_update_item",
                "required": ["item"],
                "type": "object",
                "properties": {"item": {"$ref": "#/components/schemas/Item"}},
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


def openapi_schema():
    response = client.put("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


price_not_greater = {
    "detail": [
        {
            "ctx": {"limit_value": 0},
            "loc": ["body", "item", "price"],
            "msg": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt",
        }
    ]
}


@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/items/5",
            {"item": {"name": "Foo", "price": 3.0}},
            200,
            {
                "item_id": 5,
                "item": {"name": "Foo", "price": 3.0, "description": None, "tax": None},
            },
        ),
        (
            "/items/6",
            {
                "item": {
                    "name": "Bar",
                    "price": 0.2,
                    "description": "Some bar",
                    "tax": "5.4",
                }
            },
            200,
            {
                "item_id": 6,
                "item": {
                    "name": "Bar",
                    "price": 0.2,
                    "description": "Some bar",
                    "tax": 5.4,
                },
            },
        ),
        ("/items/5", {"item": {"name": "Foo", "price": -3.0}}, 422, price_not_greater),
    ],
)
def test(path, body, expected_status, expected_response):
    response = client.put(path, json=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response

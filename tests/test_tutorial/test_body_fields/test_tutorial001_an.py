import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_fields.tutorial001_an import app

    client = TestClient(app)
    return client


def test_items_5(client: TestClient):
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": 3.0}})
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "item": {"name": "Foo", "price": 3.0, "description": None, "tax": None},
    }


def test_items_6(client: TestClient):
    response = client.put(
        "/items/6",
        json={
            "item": {
                "name": "Bar",
                "price": 0.2,
                "description": "Some bar",
                "tax": "5.4",
            }
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 6,
        "item": {
            "name": "Bar",
            "price": 0.2,
            "description": "Some bar",
            "tax": 5.4,
        },
    }


def test_invalid_price(client: TestClient):
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": -3.0}})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["body", "item", "price"],
                    "msg": "Input should be greater than 0",
                    "input": -3.0,
                    "ctx": {"gt": 0.0},
                    "url": match_pydantic_error_url("greater_than"),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "ctx": {"limit_value": 0},
                    "loc": ["body", "item", "price"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                }
            ]
        }
    )


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
                        "description": IsDict(
                            {
                                "title": "The description of the item",
                                "anyOf": [
                                    {"maxLength": 300, "type": "string"},
                                    {"type": "null"},
                                ],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {
                                "title": "The description of the item",
                                "maxLength": 300,
                                "type": "string",
                            }
                        ),
                        "price": {
                            "title": "Price",
                            "exclusiveMinimum": 0.0,
                            "type": "number",
                            "description": "The price must be greater than zero",
                        },
                        "tax": IsDict(
                            {
                                "title": "Tax",
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Tax", "type": "number"}
                        ),
                    },
                },
                "Body_update_item_items__item_id__put": {
                    "title": "Body_update_item_items__item_id__put",
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

from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.handling_errors.tutorial005 import app

client = TestClient(app)


def test_post_validation_error():
    response = client.post("/items/", json={"title": "towel", "size": "XL"})
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "size"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "XL",
                }
            ],
            "body": {"title": "towel", "size": "XL"},
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "size"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ],
            "body": {"title": "towel", "size": "XL"},
        }
    )


def test_post():
    data = {"title": "towel", "size": 5}
    response = client.post("/items/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
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
            }
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
                    "required": ["title", "size"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "size": {"title": "Size", "type": "integer"},
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

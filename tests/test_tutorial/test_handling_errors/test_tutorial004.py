from fastapi.testclient import TestClient

from docs_src.handling_errors.tutorial004 import app

client = TestClient(app)


def test_get_validation_error():
    response = client.get("/items/foo")
    assert response.status_code == 400, response.text
    # TODO: remove when deprecating Pydantic v1
    assert (
        # TODO: remove when deprecating Pydantic v1
        "path -> item_id" in response.text
        or "'loc': ('path', 'item_id')" in response.text
    )
    assert (
        # TODO: remove when deprecating Pydantic v1
        "value is not a valid integer" in response.text
        or "Input should be a valid integer, unable to parse string as an integer"
        in response.text
    )


def test_get_http_error():
    response = client.get("/items/3")
    assert response.status_code == 418, response.text
    assert response.content == b"Nope! I don't like 3."


def test_get():
    response = client.get("/items/2")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": 2}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
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
                    "summary": "Read Item",
                    "operationId": "read_item_items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "integer"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            }
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

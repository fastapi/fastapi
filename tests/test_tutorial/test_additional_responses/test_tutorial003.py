from fastapi.testclient import TestClient

from additional_responses.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "404": {
                        "description": "The item was not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Message"}
                            }
                        },
                    },
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"},
                                "example": {"id": "bar", "value": "The bar tenders"},
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
                "summary": "Read Item",
                "operationId": "read_item_items__item_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            }
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "title": "Item",
                "required": ["id", "value"],
                "type": "object",
                "properties": {
                    "id": {"title": "Id", "type": "string"},
                    "value": {"title": "Value", "type": "string"},
                },
            },
            "Message": {
                "title": "Message",
                "required": ["message"],
                "type": "object",
                "properties": {"message": {"title": "Message", "type": "string"}},
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


def test_path_operation():
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"id": "foo", "value": "there goes my hero"}


def test_path_operation_not_found():
    response = client.get("/items/bar")
    assert response.status_code == 404
    assert response.json() == {"message": "Item not found"}

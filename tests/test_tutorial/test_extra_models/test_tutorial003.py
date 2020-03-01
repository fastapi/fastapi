from fastapi.testclient import TestClient

from extra_models.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Read Item Items  Item Id  Get",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/PlaneItem"},
                                        {"$ref": "#/components/schemas/CarItem"},
                                    ],
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
            "PlaneItem": {
                "title": "PlaneItem",
                "required": ["description", "size"],
                "type": "object",
                "properties": {
                    "description": {"title": "Description", "type": "string"},
                    "type": {"title": "Type", "type": "string", "default": "plane"},
                    "size": {"title": "Size", "type": "integer"},
                },
            },
            "CarItem": {
                "title": "CarItem",
                "required": ["description"],
                "type": "object",
                "properties": {
                    "description": {"title": "Description", "type": "string"},
                    "type": {"title": "Type", "type": "string", "default": "car"},
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


def test_get_car():
    response = client.get("/items/item1")
    assert response.status_code == 200
    assert response.json() == {
        "description": "All my friends drive a low rider",
        "type": "car",
    }


def test_get_plane():
    response = client.get("/items/item2")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    }

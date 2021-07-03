from fastapi.testclient import TestClient

from docs_src.body_nested_models.tutorial009 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/index-weights/": {
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
                "summary": "Create Index Weights",
                "operationId": "create_index_weights_index_weights__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "title": "Weights",
                                "type": "object",
                                "additionalProperties": {"type": "number"},
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
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_post_body():
    data = {"2": 2.2, "3": 3.3}
    response = client.post("/index-weights/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_post_invalid_body():
    data = {"foo": 2.2, "3": 3.3}
    response = client.post("/index-weights/", json=data)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "__key__"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }

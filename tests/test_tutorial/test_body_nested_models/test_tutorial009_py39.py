import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39

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


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_nested_models.tutorial009_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


@needs_py39
def test_post_body(client: TestClient):
    data = {"2": 2.2, "3": 3.3}
    response = client.post("/index-weights/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


@needs_py39
def test_post_invalid_body(client: TestClient):
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

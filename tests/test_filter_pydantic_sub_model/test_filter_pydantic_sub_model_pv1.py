import pytest
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient

from ..utils import needs_pydanticv1


@pytest.fixture(name="client")
def get_client():
    from .app_pv1 import app

    client = TestClient(app)
    return client


@needs_pydanticv1
def test_filter_sub_model(client: TestClient):
    response = client.get("/model/modelA")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "modelA",
        "description": "model-a-desc",
        "model_b": {"username": "test-user"},
    }


@needs_pydanticv1
def test_validator_is_cloned(client: TestClient):
    with pytest.raises(ResponseValidationError) as err:
        client.get("/model/modelX")
    assert err.value.errors() == [
        {
            "loc": ("response", "name"),
            "msg": "name must end in A",
            "type": "value_error",
        }
    ]


@needs_pydanticv1
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/model/{name}": {
                "get": {
                    "summary": "Get Model A",
                    "operationId": "get_model_a_model__name__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Name", "type": "string"},
                            "name": "name",
                            "in": "path",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ModelA"}
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
                "ModelA": {
                    "title": "ModelA",
                    "required": ["name", "model_b"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                        "model_b": {"$ref": "#/components/schemas/ModelB"},
                    },
                },
                "ModelB": {
                    "title": "ModelB",
                    "required": ["username"],
                    "type": "object",
                    "properties": {"username": {"title": "Username", "type": "string"}},
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

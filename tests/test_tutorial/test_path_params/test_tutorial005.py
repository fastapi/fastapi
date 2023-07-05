import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial005 import app

client = TestClient(app)


@pytest.mark.parametrize(
    "url,status_code,expected",
    [
        (
            "/models/alexnet",
            200,
            {"model_name": "alexnet", "message": "Deep Learning FTW!"},
        ),
        (
            "/models/lenet",
            200,
            {"model_name": "lenet", "message": "LeCNN all the images"},
        ),
        (
            "/models/resnet",
            200,
            {"model_name": "resnet", "message": "Have some residuals"},
        ),
        (
            "/models/foo",
            422,
            {
                "detail": [
                    {
                        "ctx": {"enum_values": ["alexnet", "resnet", "lenet"]},
                        "loc": ["path", "model_name"],
                        "msg": "value is not a valid enumeration member; permitted: 'alexnet', 'resnet', 'lenet'",
                        "type": "type_error.enum",
                    }
                ]
            },
        ),
    ],
)
def test_get_enums(url, status_code, expected):
    response = client.get(url)
    assert response.status_code == status_code
    assert response.json() == expected


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/models/{model_name}": {
                "get": {
                    "summary": "Get Model",
                    "operationId": "get_model_models__model_name__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"$ref": "#/components/schemas/ModelName"},
                            "name": "model_name",
                            "in": "path",
                        }
                    ],
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
                "ModelName": {
                    "title": "ModelName",
                    "enum": ["alexnet", "resnet", "lenet"],
                    "type": "string",
                    "description": "An enumeration.",
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

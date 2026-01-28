from fastapi.testclient import TestClient

from docs_src.path_params.tutorial005_py39 import app

client = TestClient(app)


def test_get_enums_alexnet():
    response = client.get("/models/alexnet")
    assert response.status_code == 200
    assert response.json() == {"model_name": "alexnet", "message": "Deep Learning FTW!"}


def test_get_enums_lenet():
    response = client.get("/models/lenet")
    assert response.status_code == 200
    assert response.json() == {"model_name": "lenet", "message": "LeCNN all the images"}


def test_get_enums_resnet():
    response = client.get("/models/resnet")
    assert response.status_code == 200
    assert response.json() == {"model_name": "resnet", "message": "Have some residuals"}


def test_get_enums_invalid():
    response = client.get("/models/foo")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["path", "model_name"],
                "msg": "Input should be 'alexnet', 'resnet' or 'lenet'",
                "input": "foo",
                "ctx": {"expected": "'alexnet', 'resnet' or 'lenet'"},
            }
        ]
    }


def test_openapi_schema():
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

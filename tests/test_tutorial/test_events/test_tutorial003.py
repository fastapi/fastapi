from fastapi.testclient import TestClient

from docs_src.events.tutorial003 import (
    app,
    fake_answer_to_everything_ml_model,
    ml_models,
)


def test_events():
    assert not ml_models, "ml_models should be empty"
    with TestClient(app) as client:
        assert ml_models["answer_to_everything"] == fake_answer_to_everything_ml_model
        response = client.get("/predict", params={"x": 2})
        assert response.status_code == 200, response.text
        assert response.json() == {"result": 84.0}
    assert not ml_models, "ml_models should be empty"


def test_openapi_schema():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        assert response.json() == {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/predict": {
                    "get": {
                        "summary": "Predict",
                        "operationId": "predict_predict_get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "X", "type": "number"},
                                "name": "x",
                                "in": "query",
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
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
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

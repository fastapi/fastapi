import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial012_py39"),
        pytest.param("tutorial012_an_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.query_params_str_validations.{request.param}"
    )

    client = TestClient(mod.app)
    return client


def test_default_query_values(client: TestClient):
    url = "/items/"
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["foo", "bar"]}


def test_multi_query_values(client: TestClient):
    url = "/items/?q=baz&q=foobar"
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["baz", "foobar"]}


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
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
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Q",
                                "type": "array",
                                "items": {"type": "string"},
                                "default": ["foo", "bar"],
                            },
                            "name": "q",
                            "in": "query",
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

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39

openapi_schema = {
    "openapi": "3.0.2",
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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
    from docs_src.query_params_str_validations.tutorial011_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


@needs_py39
def test_multi_query_values(client: TestClient):
    url = "/items/?q=foo&q=bar"
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["foo", "bar"]}


@needs_py39
def test_query_no_values(client: TestClient):
    url = "/items/"
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == {"q": None}

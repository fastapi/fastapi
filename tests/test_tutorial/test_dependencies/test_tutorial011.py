import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        "tutorial011_py39",
        pytest.param("tutorial011_an_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/query-checker/",
            200,
            {"fixed_content_in_query": False},
        ),
        (
            "/query-checker/?q=qwerty",
            200,
            {"fixed_content_in_query": False},
        ),
        (
            "/query-checker/?q=foobar",
            200,
            {"fixed_content_in_query": True},
        ),
    ],
)
def test_get(path, expected_status, expected_response, client: TestClient):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/query-checker/": {
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
                    "summary": "Read Query Check",
                    "operationId": "read_query_check_query_checker__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "",
                                "title": "Q",
                            },
                            "name": "q",
                            "in": "query",
                        },
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

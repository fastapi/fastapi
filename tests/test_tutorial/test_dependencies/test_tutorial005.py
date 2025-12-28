import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_py310", marks=needs_py310),
        pytest.param("tutorial005_an_py39"),
        pytest.param("tutorial005_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path,cookie,expected_status,expected_response",
    [
        (
            "/items",
            "from_cookie",
            200,
            {"q_or_cookie": "from_cookie"},
        ),
        (
            "/items?q=foo",
            "from_cookie",
            200,
            {"q_or_cookie": "foo"},
        ),
        (
            "/items",
            None,
            200,
            {"q_or_cookie": None},
        ),
    ],
)
def test_get(path, cookie, expected_status, expected_response, client: TestClient):
    if cookie is not None:
        client.cookies.set("last_query", cookie)
    else:
        client.cookies.clear()
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
                    "summary": "Read Query",
                    "operationId": "read_query_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Q",
                            },
                            "name": "q",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Last Query",
                            },
                            "name": "last_query",
                            "in": "cookie",
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

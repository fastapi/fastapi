import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial006c_py39"),
        pytest.param("tutorial006c_py310", marks=needs_py310),
        pytest.param("tutorial006c_an_py39"),
        pytest.param("tutorial006c_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.query_params_str_validations.{request.param}"
    )
    client = TestClient(mod.app)
    return client


@pytest.mark.xfail(
    reason="Code example is not valid. See https://github.com/fastapi/fastapi/issues/12419"
)
def test_query_params_str_validations_no_query(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {  # pragma: no cover
        "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
    }


@pytest.mark.xfail(
    reason="Code example is not valid. See https://github.com/fastapi/fastapi/issues/12419"
)
def test_query_params_str_validations_empty_str(client: TestClient):
    response = client.get("/items/?q=")
    assert response.status_code == 200
    assert response.json() == {  # pragma: no cover
        "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
    }


def test_query_params_str_validations_q_query(client: TestClient):
    response = client.get("/items/", params={"q": "query"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
        "q": "query",
    }


def test_query_params_str_validations_q_short(client: TestClient):
    response = client.get("/items/", params={"q": "fa"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_short",
                "loc": ["query", "q"],
                "msg": "String should have at least 3 characters",
                "input": "fa",
                "ctx": {"min_length": 3},
            }
        ]
    }


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
                            "required": True,
                            "schema": {
                                "anyOf": [
                                    {"type": "string", "minLength": 3},
                                    {"type": "null"},
                                ],
                                "title": "Q",
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

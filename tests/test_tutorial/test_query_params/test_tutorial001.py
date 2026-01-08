import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.query_params.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    ("path", "expected_json"),
    [
        (
            "/items/",
            [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}],
        ),
        (
            "/items/?skip=1",
            [{"item_name": "Bar"}, {"item_name": "Baz"}],
        ),
        (
            "/items/?skip=1&limit=1",
            [{"item_name": "Bar"}],
        ),
    ],
)
def test_read_user_item(client: TestClient, path, expected_json):
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == expected_json


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Item",
                    "operationId": "read_item_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Skip",
                                "type": "integer",
                                "default": 0,
                            },
                            "name": "skip",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {
                                "title": "Limit",
                                "type": "integer",
                                "default": 10,
                            },
                            "name": "limit",
                            "in": "query",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
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

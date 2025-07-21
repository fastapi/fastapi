import importlib

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py39, needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py310", marks=needs_py310),
        "tutorial003_an",
        pytest.param("tutorial003_an_py39", marks=needs_py39),
        pytest.param("tutorial003_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.header_params.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path,headers,expected_status,expected_response",
    [
        ("/items", None, 200, {"X-Token values": None}),
        ("/items", {"x-token": "foo"}, 200, {"X-Token values": ["foo"]}),
        # TODO: fix this, is it a bug?
        # ("/items", [("x-token", "foo"), ("x-token", "bar")], 200, {"X-Token values": ["foo", "bar"]}),
    ],
)
def test(path, headers, expected_status, expected_response, client: TestClient):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "title": "X-Token",
                                    "anyOf": [
                                        {"type": "array", "items": {"type": "string"}},
                                        {"type": "null"},
                                    ],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {
                                    "title": "X-Token",
                                    "type": "array",
                                    "items": {"type": "string"},
                                }
                            ),
                            "name": "x-token",
                            "in": "header",
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

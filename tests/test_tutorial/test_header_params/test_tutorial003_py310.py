import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.header_params.tutorial003_py310 import app

    client = TestClient(app)
    return client


@needs_py310
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


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    # insert_assert(response.json())
    assert response.json() == {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "X-Token",
                                "type": "array",
                                "items": {"type": "string"},
                            },
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

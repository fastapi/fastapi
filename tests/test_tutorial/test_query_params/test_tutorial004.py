import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
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
            "/users/123/items/foo",
            {
                "item_id": "foo",
                "owner_id": 123,
                "description": "This is an amazing item that has a long description",
            },
        ),
        (
            "/users/1/items/bar?q=somequery",
            {
                "item_id": "bar",
                "owner_id": 1,
                "q": "somequery",
                "description": "This is an amazing item that has a long description",
            },
        ),
        (
            "/users/42/items/baz?short=true",
            {"item_id": "baz", "owner_id": 42},
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
            "/users/{user_id}/items/{item_id}": {
                "get": {
                    "summary": "Read User Item",
                    "operationId": "read_user_item_users__user_id__items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "User Id", "type": "integer"},
                            "name": "user_id",
                            "in": "path",
                        },
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "name": "item_id",
                            "in": "path",
                        },
                        {
                            "required": False,
                            "schema": {
                                "title": "Q",
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                            },
                            "name": "q",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {
                                "title": "Short",
                                "type": "boolean",
                                "default": False,
                            },
                            "name": "short",
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

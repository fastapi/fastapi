import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial003_py39 import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("user_id", "expected_response"),
    [
        ("me", {"user_id": "the current user"}),
        ("alice", {"user_id": "alice"}),
    ],
)
def test_get_users(user_id: str, expected_response: dict):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    assert response.json() == expected_response


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users/me": {
                "get": {
                    "operationId": "read_user_me_users_me_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read User Me",
                },
            },
            "/users/{user_id}": {
                "get": {
                    "operationId": "read_user_users__user_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "user_id",
                            "required": True,
                            "schema": {
                                "title": "User Id",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
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
                    "summary": "Read User",
                },
            },
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
    }

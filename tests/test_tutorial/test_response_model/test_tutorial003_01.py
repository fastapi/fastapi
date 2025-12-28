import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_01_py39"),
        pytest.param("tutorial003_01_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.response_model.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_user(client: TestClient):
    response = client.post(
        "/user/",
        json={
            "username": "foo",
            "password": "fighter",
            "email": "foo@example.com",
            "full_name": "Grave Dohl",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "foo",
        "email": "foo@example.com",
        "full_name": "Grave Dohl",
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/user/": {
                    "post": {
                        "summary": "Create User",
                        "operationId": "create_user_user__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/UserIn"}
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/BaseUser"
                                        }
                                    }
                                },
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
                    "BaseUser": {
                        "title": "BaseUser",
                        "required": ["username", "email"],
                        "type": "object",
                        "properties": {
                            "username": {"title": "Username", "type": "string"},
                            "email": {
                                "title": "Email",
                                "type": "string",
                                "format": "email",
                            },
                            "full_name": {
                                "title": "Full Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            },
                        },
                    },
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                    "UserIn": {
                        "title": "UserIn",
                        "required": ["username", "email", "password"],
                        "type": "object",
                        "properties": {
                            "username": {"title": "Username", "type": "string"},
                            "email": {
                                "title": "Email",
                                "type": "string",
                                "format": "email",
                            },
                            "full_name": {
                                "title": "Full Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            },
                            "password": {"title": "Password", "type": "string"},
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
    )

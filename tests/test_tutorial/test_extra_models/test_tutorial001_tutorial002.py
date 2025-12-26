import importlib

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.extra_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post(client: TestClient):
    response = client.post(
        "/user/",
        json={
            "username": "johndoe",
            "password": "secret",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/user/": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/UserOut",
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
                }
            }
        },
        "components": {
            "schemas": {
                "UserIn": {
                    "title": "UserIn",
                    "required": IsList(
                        "username", "password", "email", check_order=False
                    ),
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "password": {"title": "Password", "type": "string"},
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
                "UserOut": {
                    "title": "UserOut",
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

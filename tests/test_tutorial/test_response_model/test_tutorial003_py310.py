import pytest
from dirty_equals import IsDict, IsOneOf
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.response_model.tutorial003_py310 import app

    client = TestClient(app)
    return client


@needs_py310
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


@needs_py310
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
                                    "schema": {"$ref": "#/components/schemas/UserOut"}
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
                "UserOut": {
                    "title": "UserOut",
                    "required": IsOneOf(
                        ["username", "email", "full_name"],
                        # TODO: remove when deprecating Pydantic v1
                        ["username", "email"],
                    ),
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "email": {
                            "title": "Email",
                            "type": "string",
                            "format": "email",
                        },
                        "full_name": IsDict(
                            {
                                "title": "Full Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Full Name", "type": "string"}
                        ),
                    },
                },
                "UserIn": {
                    "title": "UserIn",
                    "required": ["username", "password", "email"],
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "password": {"title": "Password", "type": "string"},
                        "email": {
                            "title": "Email",
                            "type": "string",
                            "format": "email",
                        },
                        "full_name": IsDict(
                            {
                                "title": "Full Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Full Name", "type": "string"}
                        ),
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

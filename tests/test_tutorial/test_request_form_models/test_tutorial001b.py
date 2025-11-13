import importlib

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(
    name="client",
    params=[
        "tutorial001b",
        "tutorial001b_an",
        pytest.param("tutorial001b_an_py39", marks=needs_py39),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_body_form(client: TestClient):
    response = client.post(
        "/users/",
        data={"username": "Foo", "password": "secret"},
        files={"avatar": ("avatar.png", b"filebytes")},
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "Foo",
        "password": "secret",
        "avatar_file_size": 9,
    }


def test_post_body_form_no_avatar(client: TestClient):
    response = client.post("/users/", data={"username": "Foo", "password": "secret"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "avatar"],
                    "msg": "Field required",
                    "input": {"username": "Foo", "password": "secret"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "avatar"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "paths": {
            "/users/": {
                "post": {
                    "operationId": "create_user_users__post",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "$ref": "#/components/schemas/FormData",
                                },
                            },
                        },
                        "required": True,
                    },
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
                    "summary": "Create User",
                },
            },
        },
        "components": {
            "schemas": {
                "FormData": {
                    "properties": {
                        "avatar": {
                            "format": "binary",
                            "title": "Avatar",
                            "type": "string",
                        },
                        "password": {
                            "title": "Password",
                            "type": "string",
                        },
                        "username": {
                            "title": "Username",
                            "type": "string",
                        },
                    },
                    "required": [
                        "username",
                        "password",
                        "avatar",
                    ],
                    "title": "FormData",
                    "type": "object",
                },
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

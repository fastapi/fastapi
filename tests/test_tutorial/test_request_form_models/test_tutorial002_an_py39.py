import pytest
from fastapi.testclient import TestClient

from tests.utils import needs_py39, needs_pydanticv2


@pytest.fixture(name="client")
def get_client():
    from docs_src.request_form_models.tutorial002_an_py39 import app

    client = TestClient(app)
    return client


@needs_pydanticv2
@needs_py39
def test_post_body_form(client: TestClient):
    response = client.post("/login/", data={"username": "Foo", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "Foo", "password": "secret"}


@needs_pydanticv2
@needs_py39
def test_post_body_extra_form(client: TestClient):
    response = client.post(
        "/login/", data={"username": "Foo", "password": "secret", "extra": "extra"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["body", "extra"],
                "msg": "Extra inputs are not permitted",
                "input": "extra",
            }
        ]
    }


@needs_pydanticv2
@needs_py39
def test_post_body_form_no_password(client: TestClient):
    response = client.post("/login/", data={"username": "Foo"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "password"],
                "msg": "Field required",
                "input": {"username": "Foo"},
            }
        ]
    }


@needs_pydanticv2
@needs_py39
def test_post_body_form_no_username(client: TestClient):
    response = client.post("/login/", data={"password": "secret"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": {"password": "secret"},
            }
        ]
    }


@needs_pydanticv2
@needs_py39
def test_post_body_form_no_data(client: TestClient):
    response = client.post("/login/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "password"],
                "msg": "Field required",
                "input": {},
            },
        ]
    }


@needs_pydanticv2
@needs_py39
def test_post_body_json(client: TestClient):
    response = client.post("/login/", json={"username": "Foo", "password": "secret"})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": {},
            },
            {
                "type": "missing",
                "loc": ["body", "password"],
                "msg": "Field required",
                "input": {},
            },
        ]
    }


@needs_pydanticv2
@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/login/": {
                "post": {
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
                    "summary": "Login",
                    "operationId": "login_login__post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {"$ref": "#/components/schemas/FormData"}
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "FormData": {
                    "properties": {
                        "username": {"type": "string", "title": "Username"},
                        "password": {"type": "string", "title": "Password"},
                    },
                    "additionalProperties": False,
                    "type": "object",
                    "required": ["username", "password"],
                    "title": "FormData",
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

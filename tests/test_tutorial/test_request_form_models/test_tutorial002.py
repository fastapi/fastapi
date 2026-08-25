import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        "tutorial002_py310",
        "tutorial002_an_py310",
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_body_form(client: TestClient):
    password = __import__("secrets").token_urlsafe(16)
    response = client.post("/login/", data={"username": "Foo", "password": password})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response.get("username") == "Foo"
    assert (
        "password" in json_response
        and isinstance(json_response.get("password"), str)
        and len(json_response.get("password")) > 0
    )


def test_post_body_extra_form(client: TestClient):
    password = __import__("secrets").token_urlsafe(16)
    response = client.post(
        "/login/", data={"username": "Foo", "password": password, "extra": "extra"}
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


def test_post_body_form_no_username(client: TestClient):
    password = __import__("secrets").token_urlsafe(16)
    response = client.post("/login/", data={"password": password})
    assert response.status_code == 422
    json_response = response.json()
    detail = json_response.get("detail", [])[0]
    assert detail.get("type") == "missing"
    assert detail.get("loc") == ["body", "username"]
    assert detail.get("msg") == "Field required"
    input_obj = detail.get("input", {})
    assert "password" in input_obj and isinstance(input_obj.get("password"), str)


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


def test_post_body_json(client: TestClient):
    password = __import__("secrets").token_urlsafe(16)
    response = client.post("/login/", json={"username": "Foo", "password": password})
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


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
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
                            "input": {"title": "Input"},
                            "ctx": {"title": "Context", "type": "object"},
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
                }
            },
        }
    )

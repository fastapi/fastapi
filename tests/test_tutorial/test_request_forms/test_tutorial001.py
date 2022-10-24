import pytest
from fastapi.testclient import TestClient

from docs_src.request_forms.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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
                            "schema": {
                                "$ref": "#/components/schemas/Body_login_login__post"
                            }
                        }
                    },
                    "required": True,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_login_login__post": {
                "title": "Body_login_login__post",
                "required": ["username", "password"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


password_required = {
    "detail": [
        {
            "loc": ["body", "password"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}
username_required = {
    "detail": [
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}
username_and_password_required = {
    "detail": [
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "password"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}


@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/login/",
            {"username": "Foo", "password": "secret"},
            200,
            {"username": "Foo"},
        ),
        ("/login/", {"username": "Foo"}, 422, password_required),
        ("/login/", {"password": "secret"}, 422, username_required),
        ("/login/", None, 422, username_and_password_required),
    ],
)
def test_post_body_form(path, body, expected_status, expected_response):
    response = client.post(path, data=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_post_body_json():
    response = client.post("/login/", json={"username": "Foo", "password": "secret"})
    assert response.status_code == 422, response.text
    assert response.json() == username_and_password_required

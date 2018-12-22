import pytest
from starlette.testclient import TestClient

from request_forms.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                "summary": "Login Post",
                "operationId": "login_login__post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {"$ref": "#/components/schemas/Body_login"}
                        }
                    },
                    "required": True,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_login": {
                "title": "Body_login",
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
                        "items": {"type": "string"},
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


def test_openapi_scheme():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


item_id_not_int = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}

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
    print(response.text)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_post_body_json():
    response = client.post("/login/", json={"username": "Foo", "password": "secret"})
    print(response.text)
    assert response.status_code == 422
    assert response.json() == username_and_password_required

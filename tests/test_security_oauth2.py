import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

reusable_oauth2 = OAuth2(
    flows={
        "password": {
            "tokenUrl": "/token",
            "scopes": {"read:users": "Read the users", "write:users": "Create users"},
        }
    }
)


class User(BaseModel):
    username: str


# Here we use string annotations to test them
def get_current_user(oauth_header: "str" = Security(reusable_oauth2)):
    user = User(username=oauth_header)
    return user


@app.post("/login")
# Here we use string annotations to test them
def read_current_user(form_data: "OAuth2PasswordRequestFormStrict" = Depends()):
    return form_data


@app.get("/users/me")
# Here we use string annotations to test them
def read_current_user(current_user: "User" = Depends(get_current_user)):
    return current_user


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/login": {
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
                "summary": "Read Current User",
                "operationId": "read_current_user_login_post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_read_current_user_login_post"
                            }
                        }
                    },
                    "required": True,
                },
            }
        },
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Current User",
                "operationId": "read_current_user_users_me_get",
                "security": [{"OAuth2": []}],
            }
        },
    },
    "components": {
        "schemas": {
            "Body_read_current_user_login_post": {
                "title": "Body_read_current_user_login_post",
                "required": ["grant_type", "username", "password"],
                "type": "object",
                "properties": {
                    "grant_type": {
                        "title": "Grant Type",
                        "pattern": "password",
                        "type": "string",
                    },
                    "username": {"title": "Username", "type": "string"},
                    "password": {"title": "Password", "type": "string"},
                    "scope": {"title": "Scope", "type": "string", "default": ""},
                    "client_id": {"title": "Client Id", "type": "string"},
                    "client_secret": {"title": "Client Secret", "type": "string"},
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
        },
        "securitySchemes": {
            "OAuth2": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "scopes": {
                            "read:users": "Read the users",
                            "write:users": "Create users",
                        },
                        "tokenUrl": "/token",
                    }
                },
            }
        },
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    assert response.status_code == 200
    assert response.json() == {"username": "Bearer footokenbar"}


def test_security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    assert response.status_code == 200
    assert response.json() == {"username": "Other footokenbar"}


def test_security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


required_params = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": "field required",
            "type": "value_error.missing",
        },
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

grant_type_required = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

grant_type_incorrect = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": 'string does not match regex "password"',
            "type": "value_error.str.regex",
            "ctx": {"pattern": "password"},
        }
    ]
}


@pytest.mark.parametrize(
    "data,expected_status,expected_response",
    [
        (None, 422, required_params),
        ({"username": "johndoe", "password": "secret"}, 422, grant_type_required),
        (
            {"username": "johndoe", "password": "secret", "grant_type": "incorrect"},
            422,
            grant_type_incorrect,
        ),
        (
            {"username": "johndoe", "password": "secret", "grant_type": "password"},
            200,
            {
                "grant_type": "password",
                "username": "johndoe",
                "password": "secret",
                "scopes": [],
                "client_id": None,
                "client_secret": None,
            },
        ),
    ],
)
def test_strict_login(data, expected_status, expected_response):
    response = client.post("/login", data=data)
    assert response.status_code == expected_status
    assert response.json() == expected_response

from typing import Optional

from dirty_equals import IsDict
from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2, OAuth2PasswordRequestFormStrict
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

reusable_oauth2 = OAuth2(
    flows={
        "password": {
            "tokenUrl": "token",
            "scopes": {"read:users": "Read the users", "write:users": "Create users"},
        }
    },
    description="OAuth2 security scheme",
    auto_error=False,
)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: Optional[str] = Security(reusable_oauth2)):
    if oauth_header is None:
        return None
    user = User(username=oauth_header)
    return user


@app.post("/login")
def login(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    return form_data


@app.get("/users/me")
def read_users_me(current_user: Optional[User] = Depends(get_current_user)):
    if current_user is None:
        return {"msg": "Create an account first"}
    return current_user


client = TestClient(app)


def test_security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "Bearer footokenbar"}


def test_security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "Other footokenbar"}


def test_security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_strict_login_None():
    response = client.post("/login", data=None)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "grant_type"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "password"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
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
    )


def test_strict_login_no_grant_type():
    response = client.post("/login", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "grant_type"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "grant_type"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_strict_login_incorrect_grant_type():
    response = client.post(
        "/login",
        data={"username": "johndoe", "password": "secret", "grant_type": "incorrect"},
    )
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "grant_type"],
                    "msg": "String should match pattern 'password'",
                    "input": "incorrect",
                    "ctx": {"pattern": "password"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "grant_type"],
                    "msg": 'string does not match regex "password"',
                    "type": "value_error.str.regex",
                    "ctx": {"pattern": "password"},
                }
            ]
        }
    )


def test_strict_login_correct_correct_grant_type():
    response = client.post(
        "/login",
        data={"username": "johndoe", "password": "secret", "grant_type": "password"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "grant_type": "password",
        "username": "johndoe",
        "password": "secret",
        "scopes": [],
        "client_id": None,
        "client_secret": None,
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
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
                    "summary": "Login",
                    "operationId": "login_login_post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_login_login_post"
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
                    "summary": "Read Users Me",
                    "operationId": "read_users_me_users_me_get",
                    "security": [{"OAuth2": []}],
                }
            },
        },
        "components": {
            "schemas": {
                "Body_login_login_post": {
                    "title": "Body_login_login_post",
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
                        "client_id": IsDict(
                            {
                                "title": "Client Id",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Client Id", "type": "string"}
                        ),
                        "client_secret": IsDict(
                            {
                                "title": "Client Secret",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Client Secret", "type": "string"}
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
                            "tokenUrl": "token",
                        }
                    },
                    "description": "OAuth2 security scheme",
                }
            },
        },
    }

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.security.tutorial003_an_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_login(client: TestClient):
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() == {"access_token": "johndoe", "token_type": "bearer"}


@needs_py310
def test_login_incorrect_password(client: TestClient):
    response = client.post(
        "/token", data={"username": "johndoe", "password": "incorrect"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


@needs_py310
def test_login_incorrect_username(client: TestClient):
    response = client.post("/token", data={"username": "foo", "password": "secret"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


@needs_py310
def test_no_token(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@needs_py310
def test_token(client: TestClient):
    response = client.get("/users/me", headers={"Authorization": "Bearer johndoe"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }


@needs_py310
def test_incorrect_token(client: TestClient):
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@needs_py310
def test_incorrect_token_type(client: TestClient):
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@needs_py310
def test_inactive_user(client: TestClient):
    response = client.get("/users/me", headers={"Authorization": "Bearer alice"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/token": {
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
                    "operationId": "login_token_post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_login_token_post"
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
                    "security": [{"OAuth2PasswordBearer": []}],
                }
            },
        },
        "components": {
            "schemas": {
                "Body_login_token_post": {
                    "title": "Body_login_token_post",
                    "required": ["username", "password"],
                    "type": "object",
                    "properties": {
                        "grant_type": IsDict(
                            {
                                "title": "Grant Type",
                                "anyOf": [
                                    {"pattern": "password", "type": "string"},
                                    {"type": "null"},
                                ],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {
                                "title": "Grant Type",
                                "pattern": "password",
                                "type": "string",
                            }
                        ),
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
                "OAuth2PasswordBearer": {
                    "type": "oauth2",
                    "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                }
            },
        },
    }

from starlette.testclient import TestClient

from security.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {"password": {"scopes": {}, "tokenUrl": "/token"}},
            }
        },
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_login():
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "johndoe", "token_type": "bearer"}


def test_login_incorrect_password():
    response = client.post(
        "/token", data={"username": "johndoe", "password": "incorrect"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_incorrect_username():
    response = client.post("/token", data={"username": "foo", "password": "secret"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer johndoe"})
    assert response.status_code == 200
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }


def test_incorrect_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_incorrect_token_type():
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_inactive_user():
    response = client.get("/users/me", headers={"Authorization": "Bearer alice"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}

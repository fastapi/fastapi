from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.security.tutorial005_an import (
    app,
    create_access_token,
    fake_users_db,
    get_password_hash,
    verify_password,
)

client = TestClient(app)


def get_access_token(username="johndoe", password="secret", scope=None):
    data = {"username": username, "password": password}
    if scope:
        data["scope"] = scope
    response = client.post("/token", data=data)
    content = response.json()
    access_token = content.get("access_token")
    return access_token


def test_login():
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200, response.text
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"


def test_login_incorrect_password():
    response = client.post(
        "/token", data={"username": "johndoe", "password": "incorrect"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_incorrect_username():
    response = client.post("/token", data={"username": "foo", "password": "secret"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Incorrect username or password"}


def test_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_token():
    access_token = get_access_token(scope="me")
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
    }


def test_incorrect_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'


def test_incorrect_token_type():
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_verify_password():
    assert verify_password("secret", fake_users_db["johndoe"]["hashed_password"])


def test_get_password_hash():
    assert get_password_hash("secretalice")


def test_create_access_token():
    access_token = create_access_token(data={"data": "foo"})
    assert access_token


def test_token_no_sub():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZm9vIn0.9ynBhuYb4e6aW3oJr_K_TBgwcMTDpRToQIE25L57rOE"
        },
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'


def test_token_no_username():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmb28ifQ.NnExK_dlNAYyzACrXtXDrcWOgGY2JuPbI4eDaHdfK5Y"
        },
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'


def test_token_no_scope():
    access_token = get_access_token()
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'


def test_token_inexistent_user():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZTpib2IifQ.HcfCW67Uda-0gz54ZWTqmtgJnZeNem0Q757eTa9EZuw"
        },
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'


def test_token_inactive_user():
    access_token = get_access_token(
        username="alice", password="secretalice", scope="me"
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}


def test_read_items():
    access_token = get_access_token(scope="me items")
    response = client.get(
        "/users/me/items/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "Foo", "owner": "johndoe"}]


def test_read_system_status():
    access_token = get_access_token()
    response = client.get(
        "/status/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"status": "ok"}


def test_read_system_status_no_token():
    response = client.get("/status/")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_openapi_schema():
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
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Token"}
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
                    "summary": "Login For Access Token",
                    "operationId": "login_for_access_token_token_post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_login_for_access_token_token_post"
                                }
                            }
                        },
                        "required": True,
                    },
                }
            },
            "/users/me/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            },
                        }
                    },
                    "summary": "Read Users Me",
                    "operationId": "read_users_me_users_me__get",
                    "security": [{"OAuth2PasswordBearer": ["me"]}],
                }
            },
            "/users/me/items/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read Own Items",
                    "operationId": "read_own_items_users_me_items__get",
                    "security": [{"OAuth2PasswordBearer": ["items", "me"]}],
                }
            },
            "/status/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read System Status",
                    "operationId": "read_system_status_status__get",
                    "security": [{"OAuth2PasswordBearer": []}],
                }
            },
        },
        "components": {
            "schemas": {
                "User": {
                    "title": "User",
                    "required": ["username"],
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "email": IsDict(
                            {
                                "title": "Email",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Email", "type": "string"}
                        ),
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
                        "disabled": IsDict(
                            {
                                "title": "Disabled",
                                "anyOf": [{"type": "boolean"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Disabled", "type": "boolean"}
                        ),
                    },
                },
                "Token": {
                    "title": "Token",
                    "required": ["access_token", "token_type"],
                    "type": "object",
                    "properties": {
                        "access_token": {"title": "Access Token", "type": "string"},
                        "token_type": {"title": "Token Type", "type": "string"},
                    },
                },
                "Body_login_for_access_token_token_post": {
                    "title": "Body_login_for_access_token_token_post",
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
                    "flows": {
                        "password": {
                            "scopes": {
                                "me": "Read information about the current user.",
                                "items": "Read items.",
                            },
                            "tokenUrl": "token",
                        }
                    },
                }
            },
        },
    }

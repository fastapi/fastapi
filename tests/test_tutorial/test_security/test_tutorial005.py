from starlette.testclient import TestClient

from security.tutorial005 import (
    app,
    create_access_token,
    fake_users_db,
    get_password_hash,
    verify_password,
)

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
                "summary": "Route Login Access Token Post",
                "operationId": "route_login_access_token_token_post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_route_login_access_token"
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
                "summary": "Read Users Me Get",
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
                "summary": "Read Own Items Get",
                "operationId": "read_own_items_users_me_items__get",
                "security": [{"OAuth2PasswordBearer": ["items", "me"]}],
            }
        },
    },
    "components": {
        "schemas": {
            "Body_route_login_access_token": {
                "title": "Body_route_login_access_token",
                "required": ["username", "password"],
                "type": "object",
                "properties": {
                    "grant_type": {
                        "title": "Grant_Type",
                        "pattern": "password",
                        "type": "string",
                    },
                    "username": {"title": "Username", "type": "string"},
                    "password": {"title": "Password", "type": "string"},
                    "scope": {"title": "Scope", "type": "string", "default": ""},
                    "client_id": {"title": "Client_Id", "type": "string"},
                    "client_secret": {"title": "Client_Secret", "type": "string"},
                },
            },
            "Token": {
                "title": "Token",
                "required": ["access_token", "token_type"],
                "type": "object",
                "properties": {
                    "access_token": {"title": "Access_Token", "type": "string"},
                    "token_type": {"title": "Token_Type", "type": "string"},
                },
            },
            "User": {
                "title": "User",
                "required": ["username"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
                    "email": {"title": "Email", "type": "string"},
                    "full_name": {"title": "Full_Name", "type": "string"},
                    "disabled": {"title": "Disabled", "type": "boolean"},
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
                "flows": {
                    "password": {
                        "scopes": {
                            "me": "Read information about the current user.",
                            "items": "Read items.",
                        },
                        "tokenUrl": "/token",
                    }
                },
            }
        },
    },
}


def get_access_token(username="johndoe", password="secret", scope=None):
    data = {"username": username, "password": password}
    if scope:
        data["scope"] = scope
    response = client.post("/token", data=data)
    content = response.json()
    access_token = content.get("access_token")
    return access_token


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_login():
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"


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
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_token():
    access_token = get_access_token(scope="me")
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
    }


def test_incorrect_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}


def test_incorrect_token_type():
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


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
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_no_username():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmb28ifQ.NnExK_dlNAYyzACrXtXDrcWOgGY2JuPbI4eDaHdfK5Y"
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_no_scope():
    access_token = get_access_token()
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}


def test_token_inexistent_user():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZTpib2IifQ.HcfCW67Uda-0gz54ZWTqmtgJnZeNem0Q757eTa9EZuw"
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_inactive_user():
    access_token = get_access_token(
        username="alice", password="secretalice", scope="me"
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}


def test_read_items():
    access_token = get_access_token(scope="me items")
    response = client.get(
        "/users/me/items/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == [{"item_id": "Foo", "owner": "johndoe"}]

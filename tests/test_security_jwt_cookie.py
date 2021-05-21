from fastapi import FastAPI, Response, Security
from fastapi.security.jwt import JwtAuth, JwtAuthCredentials, JwtAuthRefresh
from fastapi.testclient import TestClient

app = FastAPI()

access_security = JwtAuth(secret_key="secret_key", places={"cookie"})
refresh_security = JwtAuthRefresh(secret_key="secret_key", places={"cookie"})


@app.post("/auth")
def auth(response: Response):
    subject = {"username": "username", "role": "user"}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = access_security.create_refresh_token(subject=subject)

    access_security.set_access_cookie(response, access_token)
    refresh_security.set_refresh_cookie(response, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.delete("/auth")
def logout(response: Response):
    access_security.unset_access_cookie(response)
    refresh_security.unset_refresh_cookie(response)

    return {"msg": "Successful logout"}


@app.post("/refresh")
def refresh(credentials: JwtAuthCredentials = Security(refresh_security)):
    access_token = refresh_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.get("/users/me")
def read_current_user(credentials: JwtAuthCredentials = Security(access_security)):
    return {"username": credentials["username"], "role": credentials["role"]}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/auth": {
            "post": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Auth",
                "operationId": "auth_auth_post",
            },
            "delete": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Logout",
                "operationId": "logout_auth_delete",
            },
        },
        "/refresh": {
            "post": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Refresh",
                "operationId": "refresh_refresh_post",
                "security": [{"JwtRefreshBearer": []}, {"JwtRefreshCookie": []}],
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
                "security": [{"JwtAccessBearer": []}, {"JwtAccessCookie": []}],
            }
        },
    },
    "components": {
        "securitySchemes": {
            "JwtAccessBearer": {"type": "http", "scheme": "bearer"},
            "JwtAccessCookie": {
                "type": "apiKey",
                "name": "access_token_cookie",
                "in": "cookie",
            },
            "JwtRefreshBearer": {"type": "http", "scheme": "bearer"},
            "JwtRefreshCookie": {
                "type": "apiKey",
                "name": "refresh_token_cookie",
                "in": "cookie",
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_jwt_auth():
    response = client.post("/auth")
    assert response.status_code == 200, response.text

    assert "access_token_cookie" in response.cookies
    assert response.cookies["access_token_cookie"] == response.json()["access_token"]
    assert "refresh_token_cookie" in response.cookies
    assert response.cookies["refresh_token_cookie"] == response.json()["refresh_token"]


def test_security_jwt_logout():
    response = client.delete("/auth")
    assert response.status_code == 200, response.text

    assert "access_token_cookie" in response.headers["set-cookie"]
    assert 'access_token_cookie=""; Max-Age=-1;' in response.headers["set-cookie"]
    assert "refresh_token_cookie" in response.headers["set-cookie"]
    assert (
        'refresh_token_cookie=""; HttpOnly; Max-Age=-1'
        in response.headers["set-cookie"]
    )
    # assert "access_token_cookie" not in response.cookies
    # assert response.cookies["access_token_cookie"].max_age == -1
    # assert "refresh_token_cookie" not in response.cookies
    # assert response.cookies["refresh_token_cookie"].max_age == -1


def test_security_jwt_access_cookie():
    client.cookies.clear()
    access_token = client.post("/auth").json()["access_token"]

    response = client.get("/users/me", cookies={"access_token_cookie": access_token})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "username", "role": "user"}


def test_security_jwt_access_cookie_wrong():
    client.cookies.clear()
    response = client.get(
        "/users/me", cookies={"access_token_cookie": "wrong_access_token_cookie"}
    )
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")

    response = client.get(
        "/users/me", cookies={"access_token_cookie": "wrong.access_token.cookie"}
    )
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")


def test_security_jwt_access_cookie_changed():
    client.cookies.clear()
    access_token = client.post("/auth").json()["access_token"]

    access_token = access_token.split(".")[0] + ".wrong." + access_token.split(".")[-1]

    response = client.get("/users/me", cookies={"access_token_cookie": access_token})
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")


def test_security_jwt_access_cookie_no_credentials():
    client.cookies.clear()
    response = client.get("/users/me", cookies={})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}


def test_security_jwt_refresh_cookie():
    client.cookies.clear()
    refresh_token = client.post("/auth").json()["refresh_token"]

    response = client.post("/refresh", cookies={"refresh_token_cookie": refresh_token})
    assert response.status_code == 200, response.text

    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["access_token"]
    assert "refresh_token" in response_json
    assert response_json["refresh_token"]


def test_security_jwt_refresh_cookie_wrong():
    client.cookies.clear()
    response = client.post(
        "/refresh", cookies={"refresh_token_cookie": "wrong_refresh_token_cookie"}
    )
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")

    response = client.post(
        "/refresh", cookies={"refresh_token_cookie": "wrong.refresh_token.cookie"}
    )
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")


def test_security_jwt_refresh_cookie_wrong_using_access_token():
    client.cookies.clear()
    tokens = client.post("/auth").json()
    access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]
    assert access_token != refresh_token

    response = client.post("/refresh", cookies={"refresh_token_cookie": access_token})
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token: 'type' is not 'refresh'")


def test_security_jwt_refresh_cookie_changed():
    client.cookies.clear()
    refresh_token = client.post("/auth").json()["refresh_token"]

    refresh_token = (
        refresh_token.split(".")[0] + ".wrong." + refresh_token.split(".")[-1]
    )

    response = client.post("/refresh", cookies={"refresh_token_cookie": refresh_token})
    assert response.status_code == 401, response.text
    assert response.json()["detail"].startswith("Wrong token:")


def test_security_jwt_refresh_cookie_no_credentials():
    client.cookies.clear()
    response = client.post("/refresh", cookies={})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}

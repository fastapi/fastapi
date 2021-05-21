import datetime
from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security.jwt import JwtAuth, JwtAuthCredentials, JwtAuthRefresh
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

app = FastAPI()

access_security = JwtAuth(secret_key="secret_key", auto_error=False)
refresh_security = JwtAuthRefresh(secret_key="secret_key", auto_error=False)


@app.post("/auth")
def auth():
    subject = {"username": "username", "role": "user"}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = access_security.create_refresh_token(subject=subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/refresh")
def refresh(credentials: Optional[JwtAuthCredentials] = Security(refresh_security)):
    if credentials is None:
        return {"msg": "Create an account first"}

    access_token = refresh_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.get("/users/me")
def read_current_user(
    credentials: Optional[JwtAuthCredentials] = Security(access_security),
):
    if credentials is None:
        return {"msg": "Create an account first"}
    return {"username": credentials["username"], "role": credentials["role"]}


class _FakeDateTime(datetime.datetime):  # pragma: no cover
    @staticmethod
    def now(**kwargs):
        return datetime.datetime.now() + datetime.timedelta(days=42)

    @staticmethod
    def utcnow(**kwargs):
        return datetime.datetime.utcnow() + datetime.timedelta(days=42)


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
            }
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


def test_security_jwt_access_token():
    access_token = client.post("/auth").json()["access_token"]

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "username", "role": "user"}


def test_security_jwt_access_token_wrong():
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer wrong_access_token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}

    response = client.get(
        "/users/me", headers={"Authorization": "Bearer wrong.access.token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_access_token_changed():
    access_token = client.post("/auth").json()["access_token"]

    access_token = access_token.split(".")[0] + ".wrong." + access_token.split(".")[-1]

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_access_token_timeout(mocker: MockerFixture):
    access_token = client.post("/auth").json()["access_token"]

    mocker.patch("jwt.api_jwt.datetime", _FakeDateTime)  # 42 days left

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_token():
    refresh_token = client.post("/auth").json()["refresh_token"]

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200, response.text


def test_security_jwt_refresh_token_wrong():
    response = client.post(
        "/refresh", headers={"Authorization": "Bearer wrong_refresh_token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}

    response = client.post(
        "/refresh", headers={"Authorization": "Bearer wrong.refresh.token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_token_using_access_token():
    tokens = client.post("/auth").json()
    access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]
    assert access_token != refresh_token

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_token_changed():
    refresh_token = client.post("/auth").json()["refresh_token"]

    refresh_token = (
        refresh_token.split(".")[0] + ".wrong." + refresh_token.split(".")[-1]
    )

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_token_timeout(mocker: MockerFixture):
    refresh_token = client.post("/auth").json()["refresh_token"]

    mocker.patch("jwt.api_jwt.datetime", _FakeDateTime)  # 42 days left

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}

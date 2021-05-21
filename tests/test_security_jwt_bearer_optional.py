from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security.jwt import (
    JwtAccessBearer,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)
from fastapi.testclient import TestClient

app = FastAPI()

access_security = JwtAccessBearer(secret_key="secret_key", auto_error=False)
refresh_security = JwtRefreshBearer(secret_key="secret_key", auto_error=False)


@app.post("/auth")
def auth():
    subject = {"username": "username", "role": "user"}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = access_security.create_refresh_token(subject=subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/refresh")
def refresh(
    credentials: Optional[JwtAuthorizationCredentials] = Security(refresh_security),
):
    if credentials is None:
        return {"msg": "Create an account first"}

    access_token = refresh_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.get("/users/me")
def read_current_user(
    credentials: Optional[JwtAuthorizationCredentials] = Security(access_security),
):
    if credentials is None:
        return {"msg": "Create an account first"}
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
                "security": [{"JwtRefreshBearer": []}],
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
                "security": [{"JwtAccessBearer": []}],
            }
        },
    },
    "components": {
        "securitySchemes": {
            "JwtAccessBearer": {"type": "http", "scheme": "bearer"},
            "JwtRefreshBearer": {"type": "http", "scheme": "bearer"},
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


def test_security_jwt_access_bearer():
    access_token = client.post("/auth").json()["access_token"]

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "username", "role": "user"}


def test_security_jwt_access_bearer_wrong():
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer wrong_access_token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_access_bearer_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_access_bearer_incorrect_scheme_credentials():
    response = client.get("/users/me", headers={"Authorization": "Basic notreally"})
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_bearer():
    refresh_token = client.post("/auth").json()["refresh_token"]

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200, response.text


def test_security_jwt_refresh_bearer_wrong():
    response = client.post(
        "/refresh", headers={"Authorization": "Bearer wrong_refresh_token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_bearer_no_credentials():
    response = client.post("/refresh")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_jwt_refresh_bearer_incorrect_scheme_credentials():
    response = client.post("/refresh", headers={"Authorization": "Basic notreally"})
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}

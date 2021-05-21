from fastapi import FastAPI, Security
from fastapi.security.jwt import JwtAuth, JwtAuthCredentials, JwtAuthRefresh
from fastapi.testclient import TestClient

app = FastAPI()

access_security = JwtAuth(secret_key="secret_key", places={"header"})
refresh_security = JwtAuthRefresh(secret_key="secret_key", places={"header"})


@app.post("/auth")
def auth():
    subject = {"username": "username", "role": "user"}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = access_security.create_refresh_token(subject=subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


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
    assert response.status_code == 401, response.text


def test_security_jwt_access_bearer_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}


def test_security_jwt_access_bearer_incorrect_scheme_credentials():
    response = client.get("/users/me", headers={"Authorization": "Basic notreally"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}
    # assert response.json() == {"detail": "Invalid authentication credentials"}


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
    assert response.status_code == 401, response.text


def test_security_jwt_refresh_bearer_no_credentials():
    response = client.post("/refresh")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}


def test_security_jwt_refresh_bearer_incorrect_scheme_credentials():
    response = client.post("/refresh", headers={"Authorization": "Basic notreally"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Credentials are not provided"}
    # assert response.json() == {"detail": "Invalid authentication credentials"}

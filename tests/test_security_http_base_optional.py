from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPBase(scheme="Other", auto_error=False)


@app.get("/users/me")
def read_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):
    if credentials is None:
        return {"msg": "Create an account first"}
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
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
                "security": [{"HTTPBase": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {"HTTPBase": {"type": "http", "scheme": "Other"}}
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_security_http_base():
    response = client.get("/users/me", headers={"Authorization": "Other foobar"})
    assert response.status_code == 200
    assert response.json() == {"scheme": "Other", "credentials": "foobar"}


def test_security_http_base_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"msg": "Create an account first"}

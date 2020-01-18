from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest
from starlette.testclient import TestClient

app = FastAPI()

security = HTTPDigest(auto_error=False)


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
                "security": [{"HTTPDigest": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {"HTTPDigest": {"type": "http", "scheme": "digest"}}
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_security_http_digest():
    response = client.get("/users/me", headers={"Authorization": "Digest foobar"})
    assert response.status_code == 200
    assert response.json() == {"scheme": "Digest", "credentials": "foobar"}


def test_security_http_digest_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"msg": "Create an account first"}


def test_security_http_digest_incorrect_scheme_credentials():
    response = client.get(
        "/users/me", headers={"Authorization": "Other invalidauthorization"}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid authentication credentials"}

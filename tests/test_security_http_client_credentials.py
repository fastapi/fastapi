from base64 import b64encode

from fastapi import FastAPI, Security
from fastapi.security import HTTPBasicClientCredentials, HTTPClientCredentials
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPBasicClientCredentials(auto_error=True, scheme_name="basic")


class ClientCredentialsAuthMock:
    def __call__(self, r):
        auth_mock = b64encode(b"max:powersecret").decode("ascii")
        r.headers["Authorization"] = f"Basic {auth_mock}"
        return r


@app.get("/users/me")
def read_current_user(credentials: HTTPClientCredentials = Security(security)):
    return {
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
    }


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/me": {
            "get": {
                "summary": "Read Current User",
                "operationId": "read_current_user_users_me_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "security": [{"basic": []}],
            }
        }
    },
    "components": {"securitySchemes": {"basic": {"type": "http", "scheme": "basic"}}},
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_http_basic():
    auth = ClientCredentialsAuthMock()
    response = client.get("/users/me", auth=auth)
    assert response.status_code == 200, response.text
    assert response.json() == {"client_id": "max", "client_secret": "powersecret"}


def test_security_http_basic_no_credentials():
    response = client.get("/users/me")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401, response.text
    assert response.headers["WWW-Authenticate"] == "Basic"


def test_security_http_basic_invalid_credentials():
    response = client.get(
        "/users/me", headers={"Authorization": "Basic notabase64token"}
    )
    assert response.status_code == 401, response.text
    assert response.headers["WWW-Authenticate"] == "Basic"
    assert response.json() == {"detail": "Invalid authentication credentials"}


def test_security_http_basic_non_basic_credentials():
    payload = b64encode(b"johnsecret").decode("ascii")
    auth_header = f"Basic {payload}"
    response = client.get("/users/me", headers={"Authorization": auth_header})
    assert response.status_code == 401, response.text
    assert response.headers["WWW-Authenticate"] == "Basic"
    assert response.json() == {"detail": "Invalid authentication credentials"}

import importlib
from base64 import b64encode

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial006_py39"),
        pytest.param("tutorial006_an_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.security.{request.param}")

    client = TestClient(mod.app)
    return client


def test_security_http_basic(client: TestClient):
    response = client.get("/users/me", auth=("john", "secret"))
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "john", "password": "secret"}


def test_security_http_basic_no_credentials(client: TestClient):
    response = client.get("/users/me")
    www_auth = response.headers["WWW-Authenticate"]
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401, response.text
    assert www_auth.lower().startswith("basic")
    assert 'realm="' in www_auth.lower()


def test_security_http_basic_invalid_credentials(client: TestClient):
    response = client.get(
        "/users/me", headers={"Authorization": "Basic notabase64token"}
    )
    www_auth = response.headers["WWW-Authenticate"]
    assert response.status_code == 401, response.text
    assert www_auth.lower().startswith("basic")
    assert 'realm="' in www_auth.lower()
    assert response.json() == {"detail": "Not authenticated"}


def test_security_http_basic_non_basic_credentials(client: TestClient):
    payload = b64encode(b"johnsecret").decode("ascii")
    auth_header = f"Basic {payload}"
    response = client.get("/users/me", headers={"Authorization": auth_header})
    www_auth = response.headers["WWW-Authenticate"]
    assert response.status_code == 401, response.text
    assert www_auth.lower().startswith("basic")
    assert 'realm="' in www_auth.lower()
    assert response.json() == {"detail": "Not authenticated"}


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
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
                    "security": [{"HTTPBasic": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {"HTTPBasic": {"type": "http", "scheme": "basic"}}
        },
    }

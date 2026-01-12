import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_an_py39",
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.authentication_error_status_code.{request.param}"
    )

    client = TestClient(mod.app)
    return client


def test_get_me(client: TestClient):
    response = client.get("/me", headers={"Authorization": "Bearer secrettoken"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "You are authenticated",
        "token": "secrettoken",
    }


def test_get_me_no_credentials(client: TestClient):
    response = client.get("/me")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/me": {
                    "get": {
                        "summary": "Read Me",
                        "operationId": "read_me_me_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [{"HTTPBearer403": []}],
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "HTTPBearer403": {"type": "http", "scheme": "bearer"}
                }
            },
        }
    )

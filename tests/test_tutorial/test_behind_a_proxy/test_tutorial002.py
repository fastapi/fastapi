import pytest
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(name="client", scope="module")
def get_client() -> TestClient:
    with pytest.warns(FastAPIDeprecationWarning, match="fastapi run --root-path"):
        from docs_src.behind_a_proxy.tutorial002_py310 import app
    return TestClient(app)


def test_main(client: TestClient):
    response = client.get("/app")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "root_path": "/api/v1"}


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/app": {
                    "get": {
                        "summary": "Read Main",
                        "operationId": "read_main_app_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                }
            },
            "servers": [{"url": "/api/v1"}],
        }
    )

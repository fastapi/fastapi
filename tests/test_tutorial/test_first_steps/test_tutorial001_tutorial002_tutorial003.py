import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_py310",
        "tutorial003_py310",
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.first_steps.{request.param}")
    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/", 200, {"message": "Hello World"}),
        ("/nonexistent", 404, {"detail": "Not Found"}),
    ],
)
def test_get_path(client: TestClient, path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "summary": "Root",
                        "operationId": "root__get",
                    }
                }
            },
        }
    )

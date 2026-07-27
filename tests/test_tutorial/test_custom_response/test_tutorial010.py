import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial010_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.custom_response.{request.param}")
    client = TestClient(mod.app)
    return client


def test_get_custom_response(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.text == snapshot("<h1>Items</h1><p>This is a list of items.</p>")


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}}
                                },
                            }
                        },
                        "summary": "Read Items",
                        "operationId": "read_items_items__get",
                    }
                }
            },
        }
    )

from fastapi.testclient import TestClient

from docs_src.behind_a_proxy.tutorial002 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_main():
    response = client.get("/app")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "root_path": "/api/v1"}

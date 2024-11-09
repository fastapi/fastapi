from fastapi.testclient import TestClient

from docs_src.sub_applications.tutorial001 import app

client = TestClient(app)

openapi_schema_main = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/app": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Main",
                "operationId": "read_main_app_get",
            }
        }
    },
}
openapi_schema_sub = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/sub": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Sub",
                "operationId": "read_sub_sub_get",
            }
        }
    },
    "servers": [{"url": "/subapi"}],
}


def test_openapi_schema_main():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema_main


def test_main():
    response = client.get("/app")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World from main app"}


def test_openapi_schema_sub():
    response = client.get("/subapi/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema_sub


def test_sub():
    response = client.get("/subapi/sub")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World from sub API"}

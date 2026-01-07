from fastapi.testclient import TestClient

from docs_src.middleware.tutorial001_py39 import app

client = TestClient(app)


def test_response_headers():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert "X-Process-Time" in response.headers


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "paths": {},
    }

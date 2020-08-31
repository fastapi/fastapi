from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial005 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "summary": "Main",
                "operationId": "main__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"text/plain": {"schema": {"type": "string"}}},
                    }
                },
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.text == "Hello World"

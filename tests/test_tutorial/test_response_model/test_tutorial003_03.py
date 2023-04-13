from fastapi.testclient import TestClient

from docs_src.response_model.tutorial003_03 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/teleport": {
            "get": {
                "summary": "Get Teleport",
                "operationId": "get_teleport_teleport_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
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


def test_get_portal():
    response = client.get("/teleport", follow_redirects=False)
    assert response.status_code == 307, response.text
    assert response.headers["location"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

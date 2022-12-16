from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial006 import app

client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/typer": {
            "get": {
                "summary": "Redirect Typer",
                "operationId": "redirect_typer_typer_get",
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


def test_get():
    response = client.get("/typer", follow_redirects=False)
    assert response.status_code == 307, response.text
    assert response.headers["location"] == "https://typer.tiangolo.com"

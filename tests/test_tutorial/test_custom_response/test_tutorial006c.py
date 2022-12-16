from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial006c import app

client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/pydantic": {
            "get": {
                "summary": "Redirect Pydantic",
                "operationId": "redirect_pydantic_pydantic_get",
                "responses": {"302": {"description": "Successful Response"}},
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_redirect_status_code():
    response = client.get("/pydantic", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://pydantic-docs.helpmanual.io/"

from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial006b import app

client = TestClient(app)


def test_redirect_response_class():
    response = client.get("/fastapi", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://fastapi.tiangolo.com"


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/fastapi": {
                "get": {
                    "summary": "Redirect Fastapi",
                    "operationId": "redirect_fastapi_fastapi_get",
                    "responses": {"307": {"description": "Successful Response"}},
                }
            }
        },
    }

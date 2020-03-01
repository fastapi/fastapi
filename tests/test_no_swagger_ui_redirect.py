from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(swagger_ui_oauth2_redirect_url=None)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    print(client.base_url)
    assert "oauth2RedirectUrl" not in response.text


def test_swagger_ui_no_oauth2_redirect():
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 404


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}

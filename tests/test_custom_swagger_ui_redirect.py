from fastapi import FastAPI
from starlette.testclient import TestClient

swagger_ui_oauth2_redirect_url = "/docs/redirect"

app = FastAPI(swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url)


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
    assert (
        f"oauth2RedirectUrl: window.location.origin + '{swagger_ui_oauth2_redirect_url}'"
        in response.text
    )


def test_swagger_ui_oauth2_redirect():
    response = client.get(swagger_ui_oauth2_redirect_url)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_response():
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}

from starlette.testclient import TestClient

from extending_openapi.tutorial002 import app

client = TestClient(app)


def test_swagger_ui_html():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "/static/swagger-ui-bundle.js" in response.text
    assert "/static/swagger-ui.css" in response.text


def test_redoc_html():
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "/static/redoc.standalone.js" in response.text

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/api_route", 200, {"message": "Hello World"}),
        ("/non_decorated_route", 200, {"message": "Hello World"}),
        ("/nonexistent", 404, {"detail": "Not Found"}),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    assert (
        "oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect'"
        in response.text
    )


def test_swagger_ui_oauth2_redirect():
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc():
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "redoc@2" in response.text


def test_enum_status_code_response():
    response = client.get("/enum-status-code")
    assert response.status_code == 201, response.text
    assert response.json() == "foo bar"


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {}
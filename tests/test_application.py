import pytest
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/api_route": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Non Operation Get",
                "operationId": "non_operation_api_route_get",
            }
        },
        "/non_decorated_route": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Non Decorated Route Get",
                "operationId": "non_decorated_route_non_decorated_route_get",
            }
        },
    },
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/api_route", 200, {"message": "Hello World"}),
        ("/nonexistent", 404, {"detail": "Not Found"}),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui-dist" in response.text


def test_redoc():
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc@next" in response.text

import pytest
from starlette.testclient import TestClient

from first_steps.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Root",
                "operationId": "root__get",
            }
        }
    },
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/", 200, {"message": "Hello World"}),
        ("/nonexistent", 404, {"detail": "Not Found"}),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response

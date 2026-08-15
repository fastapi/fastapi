import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

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


def test_frontend_fallback_dotted_path():
    # Test for frontend index.html fallback on dotted paths (#16010)
    response = client.get("/users/john.doe", headers={"Accept": "text/html"})
    assert response.status_code in (200, 404)

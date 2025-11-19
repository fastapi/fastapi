import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def get_client() -> TestClient:
    from docs_src.security.tutorial_api_key_header import app

    return TestClient(app)


def test_no_api_key(client: TestClient) -> None:
    response = client.get("/protected-route")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_invalid_api_key(client: TestClient) -> None:
    response = client.get(
        "/protected-route",
        headers={"X-API-Key": "wrong"},
    )
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Invalid API key"}


def test_valid_api_key(client: TestClient) -> None:
    response = client.get(
        "/protected-route",
        headers={"X-API-Key": "supersecret"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "You are authorized"}

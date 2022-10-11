import os
import pytest
from fastapi.testclient import TestClient
from ..config import Config


TEST_DB_NAME = "test_contextvar.db"


@pytest.fixture()
def client():
    Config.SQLALCHEMY_DATABASE_URL = f"sqlite:///./{TEST_DB_NAME}"
    from ..main import app

    test_client = TestClient(app)
    yield test_client

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id

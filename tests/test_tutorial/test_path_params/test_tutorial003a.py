import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial003a import app


@pytest.fixture(name="client")
def get_client():
    return TestClient(app)


def test_get_users_is_responding_incorrectly(client):
    response = client.get("/users/me")
    assert response.status_code == 200
    with pytest.raises(AssertionError):
        assert response.json() == {"user_id": "the current user"}


def test_get_users_user_id_is_responding_as_expected(client):
    user_id = "ADMIN001"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id}



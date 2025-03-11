import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="app")
def fastapi_app_wrong_path_operations_order():
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/users/{user_id}")
    async def read_user(user_id: str):
        return {"user_id": user_id}

    @app.get("/users/me")
    async def read_user_me():
        return {"user_id": "the current user"}

    return app


@pytest.fixture(name="client")
def get_client(app):
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

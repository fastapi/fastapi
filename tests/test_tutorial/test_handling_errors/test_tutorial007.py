from fastapi.testclient import TestClient

from docs_src.handling_errors.tutorial007 import app

client = TestClient(app)


def test_unauthenticated():
    response = client.get("/secrets")
    assert response.status_code == 401, response.text
    assert response.json() == {
        "detail": "Access denied. Check your credentials or permissions."
    }


def test_unauthorized():
    response = client.get("/secrets", params={"auth_user_id": 1})
    assert response.status_code == 403, response.text
    assert response.json() == {
        "detail": "Access denied. Check your credentials or permissions."
    }


def test_success():
    response = client.get("/secrets", params={"auth_user_id": 0})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": "Secret information"}

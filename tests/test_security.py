import pytest
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)


def test_security_oauth2_password_bearer():
    response = client.get(
        "/security/oauth2b", headers={"Authorization": "Bearer footokenbar"}
    )
    assert response.status_code == 200
    assert response.json() == {"username": "footokenbar"}


def test_security_oauth2_password_bearer_wrong_header():
    response = client.get("/security/oauth2b", headers={"Authorization": "footokenbar"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_security_oauth2_password_bearer_no_header():
    response = client.get("/security/oauth2b")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

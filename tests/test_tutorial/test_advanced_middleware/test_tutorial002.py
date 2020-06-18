from fastapi.testclient import TestClient

from advanced_middleware.tutorial002 import app


def test_middleware():
    client = TestClient(app, base_url="http://example.com")
    response = client.get("/")
    assert response.status_code == 200, response.text
    client = TestClient(app, base_url="http://subdomain.example.com")
    response = client.get("/")
    assert response.status_code == 200, response.text
    client = TestClient(app, base_url="http://invalidhost")
    response = client.get("/")
    assert response.status_code == 400, response.text

from fastapi.testclient import TestClient

from docs_src.advanced_middleware.tutorial002_py310 import app


def test_middleware():
    client = TestClient(app, base_url="https://example.com:443")
    response = client.get("/")
    assert response.status_code == 200, response.text
    client = TestClient(app, base_url="https://subdomain.example.com:443")
    response = client.get("/")
    assert response.status_code == 200, response.text
    client = TestClient(app, base_url="https://invalidhost:443")
    response = client.get("/")
    assert response.status_code == 400, response.text

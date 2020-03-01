from fastapi.testclient import TestClient

from advanced_middleware.tutorial001 import app


def test_middleware():
    client = TestClient(app, base_url="https://testserver")
    response = client.get("/")
    assert response.status_code == 200

    client = TestClient(app)
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://testserver/"

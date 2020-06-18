from fastapi.testclient import TestClient

from custom_request_and_route.tutorial003 import app

client = TestClient(app)


def test_get():
    response = client.get("/")
    assert response.json() == {"message": "Not timed"}
    assert "X-Response-Time" not in response.headers


def test_get_timed():
    response = client.get("/timed")
    assert response.json() == {"message": "It's the time of my life"}
    assert "X-Response-Time" in response.headers
    assert float(response.headers["X-Response-Time"]) >= 0

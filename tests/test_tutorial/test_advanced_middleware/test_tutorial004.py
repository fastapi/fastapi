from fastapi.testclient import TestClient

from docs_src.advanced_middleware.tutorial004_py310 import app

client = TestClient(app)


def test_middleware():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == "Hello World"
    assert float(response.headers["X-Process-Time"]) >= 0

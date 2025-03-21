from docs_src.middleware.tutorial001 import app
from fastapi.testclient import TestClient


def test_add_process_time_header_middleware():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
    assert "X-Process-Time" in response.headers
    assert len(response.headers["X-Process-Time"]) > 0


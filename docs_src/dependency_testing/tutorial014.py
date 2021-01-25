from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial014 import app


client = TestClient(app)


def test_tutorial014():
    response = client.get("/raise-my-custom-exception", params={"value": "value"})
    assert response.status_code == 400

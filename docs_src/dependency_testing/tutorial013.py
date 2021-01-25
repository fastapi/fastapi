from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial013 import app


client = TestClient(app)


def test_tutorial013():
    response = client.get("/raise-exception-after-yield", params={"value": "value"})
    assert response.status_code == 400

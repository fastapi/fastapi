from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_default_404():
    app = FastAPI()
    client = TestClient(app)

    response = client.get("/non-existing-route")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

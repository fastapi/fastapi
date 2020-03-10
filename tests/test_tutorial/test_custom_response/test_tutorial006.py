from fastapi.testclient import TestClient

from custom_response.tutorial006 import app

client = TestClient(app)


def test_get():
    response = client.get("/typer", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://typer.tiangolo.com"

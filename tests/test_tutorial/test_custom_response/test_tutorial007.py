from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial007 import app

client = TestClient(app)


def test_get():
    fake_content = b"some fake video bytes"
    response = client.get("/")
    assert response.content == fake_content * 10

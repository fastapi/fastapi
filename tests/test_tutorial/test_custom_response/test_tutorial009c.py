from docs_src.custom_response.tutorial009c import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get():
    response = client.get("/")
    assert response.content == b'{\n  "message": "Hello World"\n}'

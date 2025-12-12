from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial009c_py39 import app

client = TestClient(app)


def test_get():
    response = client.get("/")
    assert response.content == b'{\n  "message": "Hello World"\n}'

import pytest

from fastapi.testclient import TestClient

from docs_src.custom_response.tutorial009c import app

client = TestClient(app)


@pytest.mark.skip(reason="skipping orjson tests")
def test_get():
    response = client.get("/")
    assert response.content == b'{\n  "message": "Hello World"\n}'

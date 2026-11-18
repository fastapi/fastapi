import pytest
from fastapi.testclient import TestClient

from docs_src.request_body_limits.tutorial001 import app

client = TestClient(app)


def test_item():
    response = client.post("/items", json={"name": "Plumbus"})
    assert response.status_code == 200
    assert response.json() == {"name": "Plumbus"}


@pytest.mark.parametrize("path", ["/uploads/", "/uploads/small"])
def test_upload(path):
    # Larger than the application default, within both upload limits.
    contents = b"x" * (1024 * 1024 + 1)
    response = client.post(path, files={"file": ("example.txt", contents)})
    assert response.status_code == 200
    assert response.json() == {"filename": "example.txt", "size": len(contents)}


def test_item_limit():
    response = client.post("/items", content=b"x" * (1024 * 1024 + 1))
    assert response.status_code == 413

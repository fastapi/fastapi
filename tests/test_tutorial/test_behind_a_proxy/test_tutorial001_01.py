from fastapi.testclient import TestClient

from docs_src.behind_a_proxy.tutorial001_01_py39 import app

client = TestClient(
    app,
    base_url="https://example.com",
    follow_redirects=False,
)


def test_redirect() -> None:
    response = client.get("/items")
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/items/"


def test_no_redirect() -> None:
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == ["plumbus", "portal gun"]

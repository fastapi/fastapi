from fastapi.testclient import TestClient


def test_default_example():
    from docs_src.opentelemetry.tutorial001 import app

    with TestClient(app) as client:
        assert client.get("/items/1").json() == {"item_id": 1}

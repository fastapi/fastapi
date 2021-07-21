from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial013 import app


client = TestClient(app)


def test_wiring():
    assert client.get("/").status_code == 200

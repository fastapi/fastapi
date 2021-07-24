from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial013 import app

client = TestClient(app)


def test_tutorial_13():
    client.get("/")

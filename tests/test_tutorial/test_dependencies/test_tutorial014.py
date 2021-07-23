from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial014 import app


def test_tutorial_13():
    with TestClient(app):
        ...  # pragma: no cover

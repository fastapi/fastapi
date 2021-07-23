from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from .tutorial001 import Settings, app, get_config


def sqlite_config():
    return Settings(db_url=f"sqlite:///./{uuid4()}.db")


def test_create_read():
    with patch.dict(app.dependency_overrides, {get_config: sqlite_config}):
        with TestClient(app) as client:
            note = {"text": "Foo bar", "completed": False}
            response = client.post("/notes/", json=note)
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["text"] == note["text"]
            assert data["completed"] == note["completed"]
            assert "id" in data
            response = client.get("/notes/")
            assert response.status_code == 200, response.text
            assert data in response.json()

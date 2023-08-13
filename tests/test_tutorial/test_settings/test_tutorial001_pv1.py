from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from ...utils import needs_pydanticv1


@needs_pydanticv1
def test_settings(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    from docs_src.settings.tutorial001_pv1 import app

    client = TestClient(app)
    response = client.get("/info")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "admin@example.com",
        "items_per_user": 50,
    }

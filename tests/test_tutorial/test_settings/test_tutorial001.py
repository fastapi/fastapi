import importlib

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from ...utils import needs_pydanticv1, needs_pydanticv2


@pytest.fixture(
    name="app",
    params=[
        pytest.param("tutorial001", marks=needs_pydanticv2),
        pytest.param("tutorial001_pv1", marks=needs_pydanticv1),
    ],
)
def get_app(request: pytest.FixtureRequest, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    mod = importlib.import_module(f"docs_src.settings.{request.param}")
    return mod.app


def test_settings(app):
    client = TestClient(app)
    response = client.get("/info")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "admin@example.com",
        "items_per_user": 50,
    }

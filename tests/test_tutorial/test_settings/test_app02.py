from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from docs_src.settings.app02 import main, test_main

client = TestClient(main.app)


def test_settings(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    settings = main.get_settings()
    assert settings.app_name == "Awesome API"
    assert settings.items_per_user == 50


def test_override_settings():
    test_main.test_app()

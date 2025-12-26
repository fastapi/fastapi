import importlib
from types import ModuleType

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from ...utils import needs_pydanticv1


@pytest.fixture(
    name="mod_path",
    params=[
        pytest.param("app03_py39"),
        pytest.param("app03_an_py39"),
    ],
)
def get_mod_path(request: pytest.FixtureRequest):
    mod_path = f"docs_src.settings.{request.param}"
    return mod_path


@pytest.fixture(name="main_mod")
def get_main_mod(mod_path: str) -> ModuleType:
    main_mod = importlib.import_module(f"{mod_path}.main")
    return main_mod


def test_settings(main_mod: ModuleType, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    settings = main_mod.get_settings()
    assert settings.app_name == "Awesome API"
    assert settings.admin_email == "admin@example.com"
    assert settings.items_per_user == 50


@needs_pydanticv1
def test_settings_pv1(mod_path: str, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    config_mod = importlib.import_module(f"{mod_path}.config_pv1")
    settings = config_mod.Settings()
    assert settings.app_name == "Awesome API"
    assert settings.admin_email == "admin@example.com"
    assert settings.items_per_user == 50


def test_endpoint(main_mod: ModuleType, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    client = TestClient(main_mod.app)
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "admin@example.com",
        "items_per_user": 50,
    }

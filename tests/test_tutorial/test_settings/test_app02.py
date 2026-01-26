import importlib
from types import ModuleType

import pytest
from pytest import MonkeyPatch


@pytest.fixture(
    name="mod_path",
    params=[
        pytest.param("app02_py39"),
        pytest.param("app02_an_py39"),
    ],
)
def get_mod_path(request: pytest.FixtureRequest):
    mod_path = f"docs_src.settings.{request.param}"
    return mod_path


@pytest.fixture(name="main_mod")
def get_main_mod(mod_path: str) -> ModuleType:
    main_mod = importlib.import_module(f"{mod_path}.main")
    return main_mod


@pytest.fixture(name="test_main_mod")
def get_test_main_mod(mod_path: str) -> ModuleType:
    test_main_mod = importlib.import_module(f"{mod_path}.test_main")
    return test_main_mod


def test_settings(main_mod: ModuleType, monkeypatch: MonkeyPatch):
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    settings = main_mod.get_settings()
    assert settings.app_name == "Awesome API"
    assert settings.items_per_user == 50


def test_override_settings(test_main_mod: ModuleType):
    test_main_mod.test_app()

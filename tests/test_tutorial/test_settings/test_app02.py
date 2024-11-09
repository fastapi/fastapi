from pytest import MonkeyPatch

from ...utils import needs_pydanticv2


@needs_pydanticv2
def test_settings(monkeypatch: MonkeyPatch):
    from docs_src.settings.app02 import main

    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    settings = main.get_settings()
    assert settings.app_name == "Awesome API"
    assert settings.items_per_user == 50


@needs_pydanticv2
def test_override_settings():
    from docs_src.settings.app02 import test_main

    test_main.test_app()

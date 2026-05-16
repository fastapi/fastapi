import importlib
from typing import Any

import pytest


def test_optional_imports_broken_installation(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that an ImportError during the import of an optional JSON library
    (like orjson or ujson) does not crash the entire fastapi.responses module.
    """
    real_import_module = importlib.import_module

    def fake_import_module(name: str, package: str | None = None) -> Any:
        if name == "ujson":
            raise ImportError(
                "simulated binary/load failure for ujson"
            )  # pragma: no cover
        if name == "orjson":
            raise ImportError(
                "simulated binary/load failure for orjson"
            )  # pragma: no cover
        return real_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)

    import fastapi.responses

    # Force a reload to ensure the module initialization runs with our monkeypatch
    try:
        importlib.reload(fastapi.responses)
        # Verify that the fallback worked and they are now None
        assert fastapi.responses.ujson is None
        assert fastapi.responses.orjson is None
    finally:
        # Revert the monkeypatch manually early so we can restore the module
        monkeypatch.undo()
        # Restore test isolation by reloading the module cleanly
        importlib.reload(fastapi.responses)

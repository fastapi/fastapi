import importlib
import sys
from typing import Any

import pytest

def test_optional_imports_broken_installation(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that an ImportError during the import of an optional JSON library
    (like orjson or ujson) does not crash the entire fastapi.responses module.
    """
    real_import_module = importlib.import_module

    def fake_import_module(name: str, package: str | None = None) -> Any:
        if name in ("ujson", "orjson"):
            raise ImportError(f"simulated binary/load failure for {name}")
        return real_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)

    # Force a reload to ensure the module initialization runs with our monkeypatch
    if "fastapi.responses" in sys.modules:
        del sys.modules["fastapi.responses"]

    # This should not raise an ImportError
    import fastapi.responses  # noqa: F401

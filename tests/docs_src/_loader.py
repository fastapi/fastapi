"""Load `docs_src` tutorial modules by path for smoke tests."""

import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

_DOCS_SRC = Path(__file__).resolve().parent.parent.parent / "docs_src"


def load_docs_src_module(unique_name: str, *relative_parts: str):
    path = _DOCS_SRC.joinpath(*relative_parts)
    spec = importlib.util.spec_from_file_location(unique_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module
    spec.loader.exec_module(module)
    return module


def docs_src_test_client(unique_name: str, *relative_parts: str) -> TestClient:
    mod = load_docs_src_module(unique_name, *relative_parts)
    return TestClient(mod.app)

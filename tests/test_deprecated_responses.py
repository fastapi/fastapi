import subprocess
import sys
import warnings

import pytest
from fastapi import FastAPI
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.responses import ORJSONResponse, UJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

from tests.utils import needs_orjson, needs_ujson


class Item(BaseModel):
    name: str
    price: float


# ORJSON


def _make_orjson_app() -> FastAPI:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        app = FastAPI(default_response_class=ORJSONResponse)

    @app.get("/items")
    def get_items() -> Item:
        return Item(name="widget", price=9.99)

    return app


@needs_orjson
def test_orjson_response_returns_correct_data():
    app = _make_orjson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}


@needs_orjson
def test_orjson_response_emits_deprecation_warning():
    with pytest.warns(FastAPIDeprecationWarning, match="ORJSONResponse is deprecated"):
        ORJSONResponse(content={"hello": "world"})


# UJSON


def _make_ujson_app() -> FastAPI:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        app = FastAPI(default_response_class=UJSONResponse)

    @app.get("/items")
    def get_items() -> Item:
        return Item(name="widget", price=9.99)

    return app


@needs_ujson
def test_ujson_response_returns_correct_data():
    app = _make_ujson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}


@needs_ujson
def test_ujson_response_emits_deprecation_warning():
    with pytest.warns(FastAPIDeprecationWarning, match="UJSONResponse is deprecated"):
        UJSONResponse(content={"hello": "world"})


# Optional-import resilience


def test_responses_importable_when_orjson_raises_import_error():
    # A corrupt/broken orjson install raises ImportError (not ModuleNotFoundError)
    # when its C extension fails to load. fastapi.responses must remain importable.
    script = (
        "import importlib; _real = importlib.import_module\n"
        "def _fake(name, package=None):\n"
        "    if name == 'orjson': raise ImportError('binary load failed')\n"
        "    return _real(name, package)\n"
        "importlib.import_module = _fake\n"
        "import fastapi.responses\n"
        "assert fastapi.responses.orjson is None\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_responses_importable_when_ujson_raises_import_error():
    script = (
        "import importlib; _real = importlib.import_module\n"
        "def _fake(name, package=None):\n"
        "    if name == 'ujson': raise ImportError('binary load failed')\n"
        "    return _real(name, package)\n"
        "importlib.import_module = _fake\n"
        "import fastapi.responses\n"
        "assert fastapi.responses.ujson is None\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

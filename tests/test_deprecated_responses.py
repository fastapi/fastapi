import importlib
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


@pytest.mark.parametrize("module_name", ["orjson", "ujson"])
def test_importing_fastapi_responses_ignores_broken_optional_json_installs(
    monkeypatch: pytest.MonkeyPatch, module_name: str
) -> None:
    import fastapi.responses as responses

    real_import_module = importlib.import_module

    def fake_import_module(name: str, package: str | None = None):
        if name == module_name:
            raise ImportError(f"simulated broken {module_name} install")
        return real_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    try:
        reloaded = importlib.reload(responses)
        assert getattr(reloaded, module_name) is None
    finally:
        monkeypatch.setattr(importlib, "import_module", real_import_module)
        importlib.reload(responses)

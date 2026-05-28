import importlib
import sys
import warnings
from types import ModuleType

import fastapi
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


def _import_responses_with_failed_optional_import(
    monkeypatch: pytest.MonkeyPatch, module_name: str
) -> ModuleType:
    original_responses = sys.modules.pop("fastapi.responses", None)
    had_responses_attr = hasattr(fastapi, "responses")
    original_responses_attr = getattr(fastapi, "responses", None)
    if had_responses_attr:
        delattr(fastapi, "responses")

    real_import_module = importlib.import_module

    def import_module(name: str, package: str | None = None) -> ModuleType:
        if name == module_name:
            raise ImportError(f"broken {module_name}")
        return real_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", import_module)
    try:
        return real_import_module("fastapi.responses")
    finally:
        sys.modules.pop("fastapi.responses", None)
        if original_responses is not None:
            sys.modules["fastapi.responses"] = original_responses
        if had_responses_attr:
            fastapi.responses = original_responses_attr


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


def test_orjson_import_error_does_not_break_responses_import(
    monkeypatch: pytest.MonkeyPatch,
):
    responses = _import_responses_with_failed_optional_import(monkeypatch, "orjson")

    response = responses.JSONResponse(content={"hello": "world"})
    assert response.body == b'{"hello":"world"}'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        with pytest.raises(RuntimeError, match="orjson must be installed") as exc_info:
            responses.ORJSONResponse(content={"hello": "world"})
    assert isinstance(exc_info.value.__cause__, ImportError)
    assert str(exc_info.value.__cause__) == "broken orjson"


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


def test_ujson_import_error_does_not_break_responses_import(
    monkeypatch: pytest.MonkeyPatch,
):
    responses = _import_responses_with_failed_optional_import(monkeypatch, "ujson")

    response = responses.JSONResponse(content={"hello": "world"})
    assert response.body == b'{"hello":"world"}'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        with pytest.raises(RuntimeError, match="ujson must be installed") as exc_info:
            responses.UJSONResponse(content={"hello": "world"})
    assert isinstance(exc_info.value.__cause__, ImportError)
    assert str(exc_info.value.__cause__) == "broken ujson"

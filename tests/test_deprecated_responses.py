import warnings

import pytest
from fastapi import FastAPI
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.responses import ORJSONResponse, UJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


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


def test_orjson_response_returns_correct_data():
    app = _make_orjson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}


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


def test_ujson_response_returns_correct_data():
    app = _make_ujson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}


def test_ujson_response_emits_deprecation_warning():
    with pytest.warns(FastAPIDeprecationWarning, match="UJSONResponse is deprecated"):
        UJSONResponse(content={"hello": "world"})

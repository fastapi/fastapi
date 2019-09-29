from typing import Any

import orjson
from fastapi import APIRouter, FastAPI
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.testclient import TestClient


class ORJSONResponse(JSONResponse):
    media_type = "application/x-orjson"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


class OverrideResponse(JSONResponse):
    media_type = "application/x-override"


app = FastAPI(default_response_class=ORJSONResponse)
router_a = APIRouter()
router_a_a = APIRouter()
router_a_b_override = APIRouter()  # Overrides default class
router_b_override = APIRouter()  # Overrides default class
router_b_a = APIRouter()
router_b_a_c_override = APIRouter()  # Overrides default class again


@app.get("/")
def get_root():
    return {"msg": "Hello World"}


@app.get("/override", response_class=PlainTextResponse)
def get_path_override():
    return "Hello World"


@router_a.get("/")
def get_a():
    return {"msg": "Hello A"}


@router_a.get("/override", response_class=PlainTextResponse)
def get_a_path_override():
    return "Hello A"


@router_a_a.get("/")
def get_a_a():
    return {"msg": "Hello A A"}


@router_a_a.get("/override", response_class=PlainTextResponse)
def get_a_a_path_override():
    return "Hello A A"


@router_a_b_override.get("/")
def get_a_b():
    return "Hello A B"


@router_a_b_override.get("/override", response_class=HTMLResponse)
def get_a_b_path_override():
    return "Hello A B"


@router_b_override.get("/")
def get_b():
    return "Hello B"


@router_b_override.get("/override", response_class=HTMLResponse)
def get_b_path_override():
    return "Hello B"


@router_b_a.get("/")
def get_b_a():
    return "Hello B A"


@router_b_a.get("/override", response_class=HTMLResponse)
def get_b_a_path_override():
    return "Hello B A"


@router_b_a_c_override.get("/")
def get_b_a_c():
    return "Hello B A C"


@router_b_a_c_override.get("/override", response_class=OverrideResponse)
def get_b_a_c_path_override():
    return {"msg": "Hello B A C"}


router_b_a.include_router(
    router_b_a_c_override, prefix="/c", default_response_class=HTMLResponse
)
router_b_override.include_router(router_b_a, prefix="/a")
router_a.include_router(router_a_a, prefix="/a")
router_a.include_router(
    router_a_b_override, prefix="/b", default_response_class=PlainTextResponse
)
app.include_router(router_a, prefix="/a")
app.include_router(
    router_b_override, prefix="/b", default_response_class=PlainTextResponse
)


client = TestClient(app)

orjson_type = "application/x-orjson"
text_type = "text/plain; charset=utf-8"
html_type = "text/html; charset=utf-8"
override_type = "application/x-override"


def test_app():
    with client:
        response = client.get("/")
    assert response.json() == {"msg": "Hello World"}
    assert response.headers["content-type"] == orjson_type


def test_app_override():
    with client:
        response = client.get("/override")
    assert response.content == b"Hello World"
    assert response.headers["content-type"] == text_type


def test_router_a():
    with client:
        response = client.get("/a")
    assert response.json() == {"msg": "Hello A"}
    assert response.headers["content-type"] == orjson_type


def test_router_a_override():
    with client:
        response = client.get("/a/override")
    assert response.content == b"Hello A"
    assert response.headers["content-type"] == text_type


def test_router_a_a():
    with client:
        response = client.get("/a/a")
    assert response.json() == {"msg": "Hello A A"}
    assert response.headers["content-type"] == orjson_type


def test_router_a_a_override():
    with client:
        response = client.get("/a/a/override")
    assert response.content == b"Hello A A"
    assert response.headers["content-type"] == text_type


def test_router_a_b():
    with client:
        response = client.get("/a/b")
    assert response.content == b"Hello A B"
    assert response.headers["content-type"] == text_type


def test_router_a_b_override():
    with client:
        response = client.get("/a/b/override")
    assert response.content == b"Hello A B"
    assert response.headers["content-type"] == html_type


def test_router_b():
    with client:
        response = client.get("/b")
    assert response.content == b"Hello B"
    assert response.headers["content-type"] == text_type


def test_router_b_override():
    with client:
        response = client.get("/b/override")
    assert response.content == b"Hello B"
    assert response.headers["content-type"] == html_type


def test_router_b_a():
    with client:
        response = client.get("/b/a")
    assert response.content == b"Hello B A"
    assert response.headers["content-type"] == text_type


def test_router_b_a_override():
    with client:
        response = client.get("/b/a/override")
    assert response.content == b"Hello B A"
    assert response.headers["content-type"] == html_type


def test_router_b_a_c():
    with client:
        response = client.get("/b/a/c")
    assert response.content == b"Hello B A C"
    assert response.headers["content-type"] == html_type


def test_router_b_a_c_override():
    with client:
        response = client.get("/b/a/c/override")
    assert response.json() == {"msg": "Hello B A C"}
    assert response.headers["content-type"] == override_type

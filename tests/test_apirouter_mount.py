"""Tests for mounting StaticFiles under APIRouter (issue #10180)."""

from pathlib import Path

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient


def test_mount_staticfiles_under_router_with_prefix(tmp_path: Path) -> None:
    """StaticFiles mounted on APIRouter with prefix should be accessible."""
    static_file = tmp_path / "hello.txt"
    static_file.write_text("hello world")

    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/app")
    def read_main() -> dict:
        return {"message": "Hello World from main app"}

    api_router.mount("/static", StaticFiles(directory=tmp_path), name="static")
    app.include_router(api_router)

    client = TestClient(app)

    # Regular route should still work
    r = client.get("/api/app")
    assert r.status_code == 200

    # StaticFiles should be accessible under router prefix
    r = client.get("/api/static/hello.txt")
    assert r.status_code == 200
    assert r.text == "hello world"


def test_mount_staticfiles_under_router_without_prefix(tmp_path: Path) -> None:
    """StaticFiles mounted on APIRouter without prefix should be accessible."""
    static_file = tmp_path / "test.txt"
    static_file.write_text("test content")

    app = FastAPI()
    router = APIRouter()
    router.mount("/static", StaticFiles(directory=tmp_path), name="static")
    app.include_router(router)

    client = TestClient(app)

    r = client.get("/static/test.txt")
    assert r.status_code == 200
    assert r.text == "test content"


def test_mount_staticfiles_with_include_router_prefix(tmp_path: Path) -> None:
    """include_router prefix + router prefix + mount path should all combine."""
    static_file = tmp_path / "file.txt"
    static_file.write_text("combined prefix")

    app = FastAPI()
    router = APIRouter(prefix="/api")
    router.mount("/static", StaticFiles(directory=tmp_path), name="static")
    app.include_router(router, prefix="/v1")

    client = TestClient(app)

    r = client.get("/v1/api/static/file.txt")
    assert r.status_code == 200
    assert r.text == "combined prefix"


def test_mount_non_staticfiles_app_raises_error() -> None:
    """Mounting a non-StaticFiles ASGI app on APIRouter should raise FastAPIError."""
    router = APIRouter()
    sub_app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="APIRouter does not support mounting ASGI applications other than StaticFiles.",
    ):
        router.mount("/sub", sub_app)

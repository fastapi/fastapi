import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient


def test_mount_static_files_to_apirouter(tmp_path):
    static_asset = tmp_path / "index.html"
    static_asset.write_text("Hello, World!")

    router = APIRouter()
    router.mount("/static", StaticFiles(directory=tmp_path), name="static")

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert response.text == "Hello, World!"


def test_mount_app_to_apirouter_raises():
    router = APIRouter()
    sub_app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="APIRouter does not support mounting ASGI applications other than StaticFiles.",
    ):
        router.mount("/sub", sub_app)

from pathlib import Path

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient


@pytest.mark.parametrize("root_path", ["", "/v1"])
@pytest.mark.parametrize(
    ("router_prefix", "include_prefix", "request_prefix"),
    [
        ("", "", ""),
        ("/router", "", "/router"),
        ("", "/router_1", "/router_1"),
        ("/router", "/router_1", "/router_1/router"),
    ],
)
def test_mount_static_files_to_apirouter(
    tmp_path: Path,
    root_path: str,
    router_prefix: str,
    include_prefix: str,
    request_prefix: str,
):
    static_asset = tmp_path / "index.html"
    static_asset.write_text("Hello, World!")

    router = APIRouter(prefix=router_prefix)
    router.mount("/static", StaticFiles(directory=tmp_path), name="static")

    app = FastAPI(root_path=root_path or None)
    app.include_router(router, prefix=include_prefix)

    client = TestClient(app)
    response = client.get(f"{root_path}{request_prefix}/static/index.html")
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

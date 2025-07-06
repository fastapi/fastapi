import importlib
import os
from pathlib import Path
from typing import TypedDict

import pytest
from fastapi.testclient import TestClient

ROOT_PATH = "/api"


class Params(TypedDict):
    app_root_path: str
    asgi_root_path: str
    request_prefix: str


@pytest.fixture(
    params=[
        Params(app_root_path="", asgi_root_path="", request_prefix=""),
        Params(app_root_path="/api", asgi_root_path="", request_prefix="/api"),
        Params(app_root_path="/api", asgi_root_path="", request_prefix=""),
        Params(app_root_path="", asgi_root_path="/api", request_prefix="/api"),
        Params(app_root_path="", asgi_root_path="/api", request_prefix=""),
    ],
    ids=[
        "Without root_path, request without prefix",
        "FastAPI(root_path=root_path), request with prefix",
        "FastAPI(root_path=root_path), request without prefix",
        "TestClient(root_path=root_path), request with prefix",
        "TestClient(root_path=root_path), request without prefix",
    ],
)
def params(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture()
def client(params: Params, monkeypatch):
    static_dir: Path = Path(os.getcwd()) / "static"
    static_dir.mkdir(exist_ok=True)

    monkeypatch.setenv("ROOT_PATH", params["app_root_path"])
    from docs_src.custom_docs_ui import tutorial002
    importlib.reload(tutorial002)
    app = tutorial002.app

    with TestClient(app, root_path=params["asgi_root_path"]) as client:
        yield client

    static_dir.rmdir()


def test_swagger_ui_html(client: TestClient, params: Params):
    request_prefix = params["request_prefix"]
    root_path = params["app_root_path"] or params["asgi_root_path"]

    response = client.get(f"{request_prefix}/docs")
    assert response.status_code == 200, response.text
    assert f"{root_path}/static/swagger-ui-bundle.js" in response.text
    assert f"{root_path}/static/swagger-ui.css" in response.text
    assert f"{root_path}/docs/oauth2-redirect" in response.text

    response = client.get(f"{request_prefix}/openapi.json")
    assert response.status_code == 200


def test_swagger_ui_oauth2_redirect_html(client: TestClient, params: Params):
    request_prefix = params["request_prefix"]

    response = client.get(f"{request_prefix}/docs/oauth2-redirect")
    assert response.status_code == 200, response.text
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc_html(client: TestClient, params: Params):
    request_prefix = params["request_prefix"]
    root_path = params["app_root_path"] or params["asgi_root_path"]

    response = client.get(f"{request_prefix}/redoc")

    assert response.status_code == 200, response.text
    assert f"{root_path}/static/redoc.standalone.js" in response.text

    response = client.get(f"{request_prefix}/openapi.json")
    assert response.status_code == 200


def test_api(client: TestClient, params: Params):
    request_prefix = params["request_prefix"]

    response = client.get(f"{request_prefix}/users/john")
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Hello john"

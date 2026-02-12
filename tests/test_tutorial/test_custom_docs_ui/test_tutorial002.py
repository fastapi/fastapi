import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    params=["", "/api"],
    ids=["Without path prefix", "With /api path prefix"],
)
def path_prefix(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture
def client(path_prefix: str):
    static_dir: Path = Path(os.getcwd()) / "static"
    print(static_dir)
    static_dir.mkdir(exist_ok=True)
    from docs_src.custom_docs_ui.tutorial002_py310 import app

    with TestClient(app, root_path=path_prefix, base_url="http://server") as client:
        yield client

    static_dir.rmdir()


def test_swagger_ui_html(client: TestClient, path_prefix: str):
    response = client.get(f"{path_prefix}/docs")
    assert response.request.url == f"http://server{path_prefix}/docs"
    assert response.status_code == 200, response.text
    assert f"{path_prefix}/static/swagger-ui-bundle.js" in response.text
    assert f"{path_prefix}/static/swagger-ui.css" in response.text
    assert f"{path_prefix}/docs/oauth2-redirect" in response.text


def test_openapi_json(client: TestClient, path_prefix: str):
    response = client.get(f"{path_prefix}/openapi.json")
    assert response.request.url == f"http://server{path_prefix}/openapi.json"
    assert response.status_code == 200, response.text
    assert response.json()["openapi"] == "3.1.0"


def test_swagger_ui_oauth2_redirect_html(client: TestClient, path_prefix: str):
    response = client.get(f"{path_prefix}/docs/oauth2-redirect")
    assert response.request.url == f"http://server{path_prefix}/docs/oauth2-redirect"
    assert response.status_code == 200, response.text
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc_html(client: TestClient, path_prefix: str):
    response = client.get(f"{path_prefix}/redoc")
    assert response.request.url == f"http://server{path_prefix}/redoc"
    assert response.status_code == 200, response.text
    assert f"{path_prefix}/static/redoc.standalone.js" in response.text
    assert f"{path_prefix}/openapi.json" in response.text


def test_api(client: TestClient, path_prefix: str):
    response = client.get(f"{path_prefix}/users/john")
    assert response.request.url == f"http://server{path_prefix}/users/john"
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Hello john"

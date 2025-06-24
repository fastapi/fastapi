import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

root_path = "/api"


@pytest.fixture(scope="module")
def client():
    static_dir: Path = Path(os.getcwd()) / "static"
    print(static_dir)
    static_dir.mkdir(exist_ok=True)
    os.environ["ROOT_PATH"] = root_path
    from docs_src.custom_docs_ui.tutorial002 import app

    with TestClient(app) as client:
        yield client

    os.environ.pop("ROOT_PATH", None)
    static_dir.rmdir()


def test_swagger_ui_html(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert f"{root_path}/static/swagger-ui-bundle.js" in response.text
    assert f"{root_path}/static/swagger-ui.css" in response.text
    assert f"{root_path}/docs/oauth2-redirect" in response.text

    response = client.get(f"{root_path}/openapi.json")
    assert response.status_code == 200


def test_swagger_ui_oauth2_redirect_html(client: TestClient):
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 200, response.text
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc_html(client: TestClient):
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    assert f"{root_path}/static/redoc.standalone.js" in response.text

    response = client.get(f"{root_path}/openapi.json")
    assert response.status_code == 200


def test_api(client: TestClient):
    response = client.get("/users/john")
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Hello john"

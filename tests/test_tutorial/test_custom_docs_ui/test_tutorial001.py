import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    static_dir: Path = Path(os.getcwd()) / "static"
    print(static_dir)
    static_dir.mkdir(exist_ok=True)
    from docs_src.custom_docs_ui.tutorial001 import app

    with TestClient(app) as client:
        yield client
    static_dir.rmdir()


def test_swagger_ui_html(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert (
        "https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js" in response.text
    )
    assert "https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" in response.text


def test_swagger_ui_oauth2_redirect_html(client: TestClient):
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 200, response.text
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc_html(client: TestClient):
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    assert "https://unpkg.com/redoc@next/bundles/redoc.standalone.js" in response.text


def test_api(client: TestClient):
    response = client.get("/users/john")
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Hello john"

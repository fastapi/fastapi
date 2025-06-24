import pytest
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ["root_path", "using_test_client"],
    [
        ("/api", True),
        ("/api", False),
        ("", True),
        ("", False),
    ],
)
def test_swagger_docs_with_static_assets(
    root_path: str,
    using_test_client: bool,
):
    app_kwargs = {}
    client_kwargs = {}
    if not using_test_client:
        app_kwargs = {"root_path": root_path}
    if using_test_client:
        client_kwargs = {"root_path": root_path}

    app = FastAPI(
        title="FastAPI",
        docs_url=None,
        redoc_url=None,
        **app_kwargs,
    )

    app.mount(
        "/static",
        StaticFiles(directory="tests/test_offline_docs/static"),
        name="static",
    )

    @app.get("/")
    async def custom_swagger_ui_html(req: Request):
        """
        Sets up a localized version of the Swagger (OpenAPI) docs that can be run without assets from the Internet.
        """
        root_path = req.scope.get("root_path", "").rstrip("/")
        return get_swagger_ui_html(
            openapi_url=f"{root_path}/openapi.json",
            title=app.title,
            swagger_js_url=f"{root_path}/static/swagger.js",
            swagger_css_url=f"{root_path}/static/swagger.css",
        )

    client = TestClient(app, **client_kwargs)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    swagger_html = response.text

    response = client.get("/openapi.json")
    assert response.status_code == 200

    response = client.get(f"{root_path}/openapi.json")
    assert response.status_code == 200

    response = client.get(f"{root_path}/static/swagger.js")
    assert response.status_code == 200

    response = client.get(f"{root_path}/static/swagger.css")
    assert response.status_code == 200

    assert f"{root_path}/static/swagger.js" in swagger_html
    assert f"{root_path}/static/swagger.css" in swagger_html


@pytest.mark.parametrize(
    ["root_path", "using_test_client"],
    [
        ("/api", True),
        ("/api", False),
        ("", True),
        ("", False),
    ],
)
def test_redoc_docs_with_static_assets(
    root_path: str,
    using_test_client: bool,
):
    app_kwargs = {}
    client_kwargs = {}
    if not using_test_client:
        app_kwargs = {"root_path": root_path}
    if using_test_client:
        client_kwargs = {"root_path": root_path}

    app = FastAPI(
        title="FastAPI",
        docs_url=None,
        redoc_url=None,
        **app_kwargs,
    )

    app.mount(
        "/static",
        StaticFiles(directory="tests/test_offline_docs/static"),
        name="static",
    )

    @app.get("/")
    async def custom_redoc_html(req: Request):
        """
        Sets up a localized version of the Redoc docs that can be run without assets from the Internet.
        """
        root_path = req.scope.get("root_path", "").rstrip("/")
        return get_redoc_html(
            openapi_url=f"{root_path}/openapi.json",
            title=app.title,
            redoc_js_url=f"{root_path}/static/redoc.js",
        )

    client = TestClient(app, **client_kwargs)

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    redoc_html = response.text

    response = client.get("/openapi.json")
    assert response.status_code == 200

    response = client.get(f"{root_path}/openapi.json")
    assert response.status_code == 200

    response = client.get(f"{root_path}/static/redoc.js")
    assert response.status_code == 200

    assert f"{root_path}/static/redoc.js" in redoc_html

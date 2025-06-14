from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

root_path = "/api"

app = FastAPI(
    title="FastAPI",
    root_path=root_path,
    docs_url=None,
    redoc_url=None,
)

app.mount(
    "/static", StaticFiles(directory="tests/test_offline_docs/static"), name="static"
)


@app.get("/")
async def custom_swagger_ui_html():
    """
    Sets up a localized version of the Swagger (OpenAPI) docs that can be run without assets from the Internet.
    """

    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title,
        swagger_js_url="/static/swagger.js",
        swagger_css_url="/static/swagger.css",
    )


client = TestClient(app)


def test_static_assets():
    """
    Verify static assets can still be loaded properly even behind a proxy (root_path)
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    swagger_html = response.text

    response = client.get("/openapi.json")
    assert response.status_code == 200

    response = client.get("/static/swagger.js")
    assert response.status_code == 200

    response = client.get("/static/swagger.css")
    assert response.status_code == 200

    assert "/static/swagger.js" in swagger_html
    assert f"{root_path}/static/swagger.js" not in swagger_html
    assert "/static/swagger.css" in swagger_html
    assert f"{root_path}/static/swagger.css" not in swagger_html

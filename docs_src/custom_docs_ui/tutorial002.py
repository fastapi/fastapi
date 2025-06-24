import os

from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

root_path = os.getenv("ROOT_PATH", "")

app = FastAPI(docs_url=None, redoc_url=None, root_path=root_path)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    return get_swagger_ui_html(
        openapi_url=f"{root_path}{app.openapi_url}",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=f"{root_path}{app.swagger_ui_oauth2_redirect_url}",
        swagger_js_url=f"{root_path}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{root_path}/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    return get_redoc_html(
        openapi_url=f"{root_path}{app.openapi_url}",
        title=app.title + " - ReDoc",
        redoc_js_url=f"{root_path}/static/redoc.standalone.js",
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}

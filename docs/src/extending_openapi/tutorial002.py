from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from starlette.requests import Request
from starlette.responses import HTMLResponse


app = FastAPI(docs_url=None, redoc_url=None)


async def swagger_ui_html(req: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
    )

app.add_route('/docs', swagger_ui_html, include_in_schema=False)

if app.swagger_ui_oauth2_redirect_url:
    async def swagger_ui_redirect(req: Request) -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    app.add_route(
        app.swagger_ui_oauth2_redirect_url,
        swagger_ui_redirect,
        include_in_schema=False
    )


async def redoc_html(req: Request) -> HTMLResponse:
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - ReDoc',
        redoc_js_url='/static/redoc.standalone.js',
    )

app.add_route('/redoc', redoc_html, include_in_schema=False)

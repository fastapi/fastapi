from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with Users",
        "externalDocs": {
            "description": "Users documentation",
            "url": "https://fastapi.tiangolo.com",
        },
    },
    {
        "name": "Pets",
        "description": "Operations with *Pets*",
    },
]

app = FastAPI(docs_url=None, openapi_tags=tags_metadata, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        tags_sorter='"alpha"',
        operations_sorter='function(e,t) {\
            if (e.get("path").length < t.get("path").length) {return -1;}\
            if (e.get("path").length > t.get("path").length) {return 1;}\
            return 0;\
            }',
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/users/{username}", tags=["Users"])
async def read_user(username: str):
    return {"message": f"Hello {username}"}


@app.get("/pets/{name}", tags=["Pets"])
async def read_pets(name: str):
    return {"message": f"A new pet : {name}"}

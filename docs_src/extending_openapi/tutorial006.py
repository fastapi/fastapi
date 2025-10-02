from fastapi import FastAPI
from fastapi.openapi.docs import (
    LayoutOptions,
    RouterOptions,
    TryItCredentialPolicyOptions,
    get_stoplight_elements_html,
)

app = FastAPI(stoplight_elements_url=None)


@app.get("/elements", include_in_schema=False)
async def elements_html():
    return get_stoplight_elements_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Elements",
        stoplight_elements_js_url="https://unpkg.com/@stoplight/elements/web-components.min.js",
        stoplight_elements_css_url="https://unpkg.com/@stoplight/elements/styles.min.css",
        stoplight_elements_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        api_description_document="",
        base_path="",
        hide_internal=False,
        hide_try_it=False,
        try_it_cors_proxy="",
        try_it_credential_policy=TryItCredentialPolicyOptions.OMIT,
        layout=LayoutOptions.SIDEBAR,
        logo="",
        router=RouterOptions.HISTORY,
    )


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}

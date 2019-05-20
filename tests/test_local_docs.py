import inspect

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


def test_strings_in_generated_swagger():
    sig = inspect.signature(get_swagger_ui_html)
    swagger_js_url = sig.parameters.get("swagger_js_url").default
    swagger_css_url = sig.parameters.get("swagger_css_url").default
    swagger_favicon_url = sig.parameters.get("swagger_favicon_url").default
    html = get_swagger_ui_html(openapi_url="/docs", title="title")
    body_content = html.body.decode()
    assert swagger_js_url in body_content
    assert swagger_css_url in body_content
    assert swagger_favicon_url in body_content


def test_strings_in_custom_swagger():
    swagger_js_url = "swagger_fake_file.js"
    swagger_css_url = "swagger_fake_file.css"
    swagger_favicon_url = "swagger_fake_file.png"
    html = get_swagger_ui_html(
        openapi_url="/docs",
        title="title",
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url,
        swagger_favicon_url=swagger_favicon_url,
    )
    body_content = html.body.decode()
    assert swagger_js_url in body_content
    assert swagger_css_url in body_content
    assert swagger_favicon_url in body_content


def test_strings_in_generated_redoc():
    sig = inspect.signature(get_redoc_html)
    redoc_js_url = sig.parameters.get("redoc_js_url").default
    redoc_favicon_url = sig.parameters.get("redoc_favicon_url").default
    html = get_redoc_html(openapi_url="/docs", title="title")
    body_content = html.body.decode()
    assert redoc_js_url in body_content
    assert redoc_favicon_url in body_content


def test_strings_in_custom_redoc():
    redoc_js_url = "fake_redoc_file.js"
    redoc_favicon_url = "fake_redoc_file.png"
    html = get_redoc_html(
        openapi_url="/docs",
        title="title",
        redoc_js_url=redoc_js_url,
        redoc_favicon_url=redoc_favicon_url,
    )
    body_content = html.body.decode()
    assert redoc_js_url in body_content
    assert redoc_favicon_url in body_content

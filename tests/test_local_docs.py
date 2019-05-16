import inspect

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


def test_string_in_generated_swagger():
    sig = inspect.signature(get_swagger_ui_html)
    swagger_js_url = sig.parameters.get("swagger_js_url").default
    swagger_css_url = sig.parameters.get("swagger_css_url").default
    swagger_favicon_url = sig.parameters.get("swagger_favicon_url").default
    html = get_swagger_ui_html(openapi_url="/docs", title="title")
    assert swagger_js_url in html.body.decode()
    assert swagger_css_url in html.body.decode()
    assert swagger_favicon_url in html.body.decode()
    fake = {
        "swagger_js_url": "fake_js",
        "swagger_css_url": "fake_css",
        "swagger_favicon_url": "fake_favicon",
    }
    html = get_swagger_ui_html(openapi_url="/docs", title="title", **fake)
    for k in fake.keys():
        assert fake.get(k) in html.body.decode()


def test_string_in_generated_redoc():
    sig = inspect.signature(get_redoc_html)
    redoc_js_url = sig.parameters.get("redoc_js_url").default
    redoc_favicon_url = sig.parameters.get("redoc_favicon_url").default
    html = get_redoc_html(openapi_url="/docs", title="title")
    assert redoc_js_url in html.body.decode()
    assert redoc_favicon_url in html.body.decode()
    fake = {"redoc_js_url": "fake_js", "redoc_favicon_url": "fake_favicon"}
    html = get_redoc_html(openapi_url="/docs", title="title", **fake)
    for k in fake.keys():
        assert fake.get(k) in html.body.decode()

from itertools import permutations

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


def test_string_in_generated_swagger():
    custom_kwargs_keys = ["swagger_js_url", "swagger_css_url", "swagger_favicon_url"]
    fake = {
        "swagger_js_url": "fake_js",
        "swagger_css_url": "fake_css",
        "swagger_favicon_url": "fake_favicon",
    }
    for r in range(3):
        for permutation in permutations(custom_kwargs_keys, r):
            custom_kwargs = {}
            for p in permutation:
                if p == "swagger_js_url":
                    custom_kwargs["swagger_js_url"] = fake.get(p)
                elif p == "swagger_css_url":
                    custom_kwargs["swagger_css_url"] = fake.get(p)
                elif p == "swagger_favicon_url":
                    custom_kwargs["swagger_favicon_url"] = fake.get(p)
            html = get_swagger_ui_html(
                openapi_url="/docs", title="title", **custom_kwargs
            )
            for k in custom_kwargs.keys():
                assert fake.get(k) in html.body.decode()


def test_string_in_generated_redoc():
    custom_kwargs_keys = ["redoc_js_url", "redoc_favicon_url"]
    fake = {"redoc_js_url": "fake_js", "redoc_favicon_url": "fake_favicon"}
    for r in range(3):
        for permutation in permutations(custom_kwargs_keys, r):
            custom_kwargs = {}
            for p in permutation:
                if p == "redoc_js_url":
                    custom_kwargs["redoc_js_url"] = fake.get(p)
                elif p == "redoc_favicon_url":
                    custom_kwargs["redoc_favicon_url"] = fake.get(p)
            html = get_redoc_html(openapi_url="/redoc", title="title", **custom_kwargs)
            for k in custom_kwargs.keys():
                assert fake.get(k) in html.body.decode()

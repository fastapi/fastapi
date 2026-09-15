from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


def test_init_oauth_html_chars_are_escaped():
    xss_payload = "Evil</script><script>alert(1)</script>"
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"appName": xss_payload},
    )
    body = bytes(html.body).decode()

    assert "</script><script>" not in body
    assert "\\u003c/script\\u003e\\u003cscript\\u003e" in body


def test_swagger_ui_parameters_html_chars_are_escaped():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        swagger_ui_parameters={"customKey": "<img src=x onerror=alert(1)>"},
    )
    body = bytes(html.body).decode()
    assert "<img src=x onerror=alert(1)>" not in body
    assert "\\u003cimg" in body


def test_swagger_ui_html_fields_are_escaped():
    xss_payload = "x</title><script>alert(1)</script>"
    html = get_swagger_ui_html(
        openapi_url="/openapi.json'; alert(1); '",
        title=xss_payload,
        swagger_js_url='swagger.js" onerror="alert(1)',
        swagger_css_url='swagger.css" onload="alert(1)',
        swagger_favicon_url='favicon.ico" onload="alert(1)',
        oauth2_redirect_url="/docs/oauth2-redirect'; alert(1); '",
    )
    body = bytes(html.body).decode()

    assert xss_payload not in body
    assert "&lt;/title&gt;&lt;script&gt;alert(1)&lt;/script&gt;" in body
    assert 'swagger.js" onerror="alert(1)' not in body
    assert "swagger.js&quot; onerror=&quot;alert(1)" in body
    assert "url: \"/openapi.json'; alert(1); '\"," in body
    assert (
        "oauth2RedirectUrl: window.location.origin + "
        "\"/docs/oauth2-redirect'; alert(1); '\","
    ) in body


def test_redoc_html_fields_are_escaped():
    xss_payload = "x</title><script>alert(1)</script>"
    html = get_redoc_html(
        openapi_url='openapi.json" onmouseover="alert(1)',
        title=xss_payload,
        redoc_js_url='redoc.js" onerror="alert(1)',
        redoc_favicon_url='favicon.ico" onload="alert(1)',
    )
    body = bytes(html.body).decode()

    assert xss_payload not in body
    assert "&lt;/title&gt;&lt;script&gt;alert(1)&lt;/script&gt;" in body
    assert 'openapi.json" onmouseover="alert(1)' not in body
    assert "openapi.json&quot; onmouseover=&quot;alert(1)" in body
    assert 'redoc.js" onerror="alert(1)' not in body
    assert "redoc.js&quot; onerror=&quot;alert(1)" in body


def test_normal_init_oauth_still_works():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"clientId": "my-client", "appName": "My App"},
    )
    body = bytes(html.body).decode()
    assert '"clientId": "my-client"' in body
    assert '"appName": "My App"' in body
    assert "ui.initOAuth" in body

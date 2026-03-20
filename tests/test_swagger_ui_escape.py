from fastapi.openapi.docs import get_swagger_ui_html


def test_init_oauth_html_chars_are_escaped():
    xss_payload = "Evil</script><script>alert(1)</script>"
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"appName": xss_payload},
    )
    body = html.body.decode()

    assert "</script><script>" not in body
    assert "\\u003c/script\\u003e\\u003cscript\\u003e" in body


def test_swagger_ui_parameters_html_chars_are_escaped():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        swagger_ui_parameters={"customKey": "<img src=x onerror=alert(1)>"},
    )
    body = html.body.decode()
    assert "<img src=x onerror=alert(1)>" not in body
    assert "\\u003cimg" in body


def test_normal_init_oauth_still_works():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test",
        init_oauth={"clientId": "my-client", "appName": "My App"},
    )
    body = html.body.decode()
    assert '"clientId": "my-client"' in body
    assert '"appName": "My App"' in body
    assert "ui.initOAuth" in body

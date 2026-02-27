from typing import Annotated

from annotated_doc import Doc
from starlette.responses import HTMLResponse


def get_asyncapi_html(
    *,
    asyncapi_url: Annotated[
        str,
        Doc(
            """
            The AsyncAPI URL that AsyncAPI Studio should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/asyncapi.json`.

            Read more about it in the
            [FastAPI docs for AsyncAPI](https://fastapi.tiangolo.com/advanced/asyncapi/).
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    asyncapi_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the AsyncAPI Studio JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://unpkg.com/@asyncapi/react-component@latest/browser/standalone/index.js",
    asyncapi_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    docs_url: Annotated[
        str | None,
        Doc(
            """
            The URL to the OpenAPI docs (Swagger UI) for navigation link.
            """
        ),
    ] = None,
) -> HTMLResponse:
    """
    Generate and return the HTML that loads AsyncAPI Studio for the interactive
    WebSocket API docs (normally served at `/asyncapi-docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load AsyncAPI Studio's JavaScript.
    """
    navigation_html = ""
    if docs_url:
        navigation_html = f"""
    <div style="padding: 10px; background-color: #f5f5f5; border-bottom: 1px solid #ddd;">
        <a href="{docs_url}" style="color: #007bff; text-decoration: none; margin-right: 20px;">
            📄 OpenAPI Docs (REST API)
        </a>
        <span style="color: #666;">WebSocket API Documentation</span>
    </div>
    """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="{asyncapi_favicon_url}">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        #asyncapi {{
            height: 100vh;
            width: 100%;
        }}
    </style>
    </head>
    <body>
    {navigation_html}
    <div id="asyncapi"></div>
    <script src="{asyncapi_js_url}"></script>
    <script>
        (async function() {{
            const asyncapiSpec = await fetch('{asyncapi_url}').then(res => res.json());
            const AsyncApiStandalone = window.AsyncApiStandalone || window.AsyncAPIStandalone;
            if (AsyncApiStandalone) {{
                AsyncApiStandalone.render({{
                    schema: asyncapiSpec,
                    config: {{
                        show: {{
                            sidebar: true,
                            info: true,
                            servers: true,
                            operations: true,
                            messages: true,
                        }},
                    }},
                }}, document.getElementById('asyncapi'));
            }} else {{
                document.getElementById('asyncapi').innerHTML =
                    '<div style="padding: 20px; text-align: center;">' +
                    '<h2>Failed to load AsyncAPI Studio</h2>' +
                    '<p>Please check your internet connection and try again.</p>' +
                    '</div>';
            }}
        }})();
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

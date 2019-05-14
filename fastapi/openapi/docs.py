from typing import Dict

from starlette.responses import HTMLResponse


def get_swagger_ui_html(
    *, openapi_url: str, title: str, swagger_locations: Dict
) -> HTMLResponse:
    html = f"""
    <! doctype html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_locations.get("css")}">
    <link rel="shortcut icon" href="{swagger_locations.get("favicon")}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_locations.get("js")}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"

    }})
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


def get_redoc_html(*, openapi_url: str, title: str) -> HTMLResponse:
    return HTMLResponse(
        """
    <!DOCTYPE html>
<html>
  <head>
    <title>
    """
        + title
        + """
    </title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">

    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url='"""
        + openapi_url
        + """'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>
    """
    )

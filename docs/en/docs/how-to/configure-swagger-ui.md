# Configure Swagger UI { #configure-swagger-ui }

You can configure some extra <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI parameters</a>.

To configure them, pass the `swagger_ui_parameters` argument when creating the `FastAPI()` app object or to the `get_swagger_ui_html()` function.

`swagger_ui_parameters` receives a dictionary with the configurations passed to Swagger UI directly.

FastAPI converts the configurations to **JSON** to make them compatible with JavaScript, as that's what Swagger UI needs.

## Disable Syntax Highlighting { #disable-syntax-highlighting }

For example, you could disable syntax highlighting in Swagger UI.

Without changing the settings, syntax highlighting is enabled by default:

<img src="/img/tutorial/extending-openapi/image02.png">

But you can disable it by setting `syntaxHighlight` to `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...and then Swagger UI won't show the syntax highlighting anymore:

<img src="/img/tutorial/extending-openapi/image03.png">

## Change the Theme { #change-the-theme }

The same way you could set the syntax highlighting theme with the key `"syntaxHighlight.theme"` (notice that it has a dot in the middle):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

That configuration would change the syntax highlighting color theme:

<img src="/img/tutorial/extending-openapi/image04.png">

## Change Default Swagger UI Parameters { #change-default-swagger-ui-parameters }

FastAPI includes some default configuration parameters appropriate for most of the use cases.

It includes these default configurations:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

You can override any of them by setting a different value in the argument `swagger_ui_parameters`.

For example, to disable `deepLinking` you could pass these settings to `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Other Swagger UI Parameters { #other-swagger-ui-parameters }

To see all the other possible configurations you can use, read the official <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">docs for Swagger UI parameters</a>.

## JavaScript-only settings { #javascript-only-settings }

Swagger UI also allows other configurations to be **JavaScript-only** objects (for example, JavaScript functions).

FastAPI also includes these JavaScript-only `presets` settings:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

These are **JavaScript** objects, not strings, so you can't pass them from Python code directly.

If you need to use JavaScript-only configurations like those, you can use one of the methods above. Override all the Swagger UI *path operation* and manually write any JavaScript you need.

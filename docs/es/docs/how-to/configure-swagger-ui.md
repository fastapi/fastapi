# Configurar Swagger UI

Puedes configurar algunos <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">parámetros adicionales de Swagger UI</a>.

Para configurarlos, pasa el argumento `swagger_ui_parameters` al crear el objeto de la app `FastAPI()` o a la función `get_swagger_ui_html()`.

`swagger_ui_parameters` recibe un diccionario con las configuraciones pasadas directamente a Swagger UI.

FastAPI convierte las configuraciones a **JSON** para hacerlas compatibles con JavaScript, ya que eso es lo que Swagger UI necesita.

## Desactivar el resaltado de sintaxis

Por ejemplo, podrías desactivar el resaltado de sintaxis en Swagger UI.

Sin cambiar la configuración, el resaltado de sintaxis está activado por defecto:

<img src="/img/tutorial/extending-openapi/image02.png">

Pero puedes desactivarlo estableciendo `syntaxHighlight` en `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...y entonces Swagger UI ya no mostrará el resaltado de sintaxis:

<img src="/img/tutorial/extending-openapi/image03.png">

## Cambiar el tema

De la misma manera, podrías configurar el tema del resaltado de sintaxis con la clave `"syntaxHighlight.theme"` (ten en cuenta que tiene un punto en el medio):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Esa configuración cambiaría el tema de color del resaltado de sintaxis:

<img src="/img/tutorial/extending-openapi/image04.png">

## Cambiar los parámetros predeterminados de Swagger UI

FastAPI incluye algunos parámetros de configuración predeterminados apropiados para la mayoría de los casos de uso.

Incluye estas configuraciones predeterminadas:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Puedes sobrescribir cualquiera de ellos estableciendo un valor diferente en el argumento `swagger_ui_parameters`.

Por ejemplo, para desactivar `deepLinking` podrías pasar estas configuraciones a `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Otros parámetros de Swagger UI

Para ver todas las demás configuraciones posibles que puedes usar, lee la <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">documentación oficial de los parámetros de Swagger UI</a>.

## Configuraciones solo de JavaScript

Swagger UI también permite otras configuraciones que son objetos **solo de JavaScript** (por ejemplo, funciones de JavaScript).

FastAPI también incluye estas configuraciones `presets` solo de JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Estos son objetos de **JavaScript**, no strings, por lo que no puedes pasarlos directamente desde código de Python.

Si necesitas usar configuraciones solo de JavaScript como esas, puedes usar uno de los métodos anteriores. Sobrescribe toda la *path operation* de Swagger UI y escribe manualmente cualquier JavaScript que necesites.

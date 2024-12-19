# Configurar Swagger UI

Puedes configurar algunos parámetros extra <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank"> para Swagger UI</a>.

Para configurarlos, usa el argumento `swagger_ui_parameters` al crear el objeto app `FastAPI()` o en la función `get_swagger_ui_html()`.

`swagger_ui_parameters` recibe un diccionario con la configuración que se desea pasar directamente a Swagger UI.

FastAPI convierte esta configuración a **JSON** para hacerla compatible con JavaScript, tal y como Swagger UI necesita.

## Deshabilitar el Resaltado de Texto

Por ejemplo, puedes deshabilitar el resaltado de texto en Swagger UI.

Sin cambiar la configuración, el resaltado de texto está habilitado por defecto:

<img src="/img/tutorial/extending-openapi/image02.png">

Pero puedes deshabilitarlo estableciendo la clave `syntaxHighlight` a `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...y de este modo, Swagger UI no realizará el restaltado de texto:

<img src="/img/tutorial/extending-openapi/image03.png">

## Cambiar el Tema del Resaltado de Texto

Del mismo modo, puedes establecer el tema del resaltado de texto con la clave `"syntaxHighlight.theme"` (observa que existe un punto en la mitad):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Esa configuración cambiará el tema de color del resaltado de texto:

<img src="/img/tutorial/extending-openapi/image04.png">

## Cambiar Parámetros por Defecto de Swagger UI

FastAPI incluye una configuración por defecto para algunos parámetros apropiada para la mayoría de los casos.

En concreto, incluye estas configuraciones por defecto:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Puedes sobreescribir cualquiera de ellos estableciendo un valor diferente en el argumento `swagger_ui_parameters`.

Por ejemplo, para deshabilitar `deepLinking` podrías pasar esta configuración a `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Otros Parámetros de Swagger UI

Para ver todas las posibles configuraciones que puedes usar, lee la documentación oficial <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank"> para los parámetros de Swagger UI</a>.

## Parámetros usando JavaScript

Swagger UI también permite otras configuraciones usando sólo objetos **JavaScript** (por ejemplo, funciones JavaScript).

FastAPI permite usar estos parámetros JavaScript mediante `presets` :

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Son objetos **JavaScript**, no strings, por lo que no puedes pasarlos directamente desde código Python.

Si necesitas realizar configuraciones usando sólo JavaScript, puedes usar alguno de los métodos anteriores. Sobreescribir toda la *path operation* de Swagger UI y, de forma manual, escribir cualquier código JavaScript que necesites.

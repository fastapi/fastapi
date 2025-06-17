# Extender OpenAPI

Hay algunos casos en los que podrías necesitar modificar el esquema de OpenAPI generado.

En esta sección verás cómo hacerlo.

## El proceso normal

El proceso normal (por defecto) es el siguiente.

Una aplicación (instance) de `FastAPI` tiene un método `.openapi()` que se espera que devuelva el esquema de OpenAPI.

Como parte de la creación del objeto de la aplicación, se registra una *path operation* para `/openapi.json` (o para lo que sea que configures tu `openapi_url`).

Simplemente devuelve un response JSON con el resultado del método `.openapi()` de la aplicación.

Por defecto, lo que hace el método `.openapi()` es revisar la propiedad `.openapi_schema` para ver si tiene contenido y devolverlo.

Si no lo tiene, lo genera usando la función de utilidad en `fastapi.openapi.utils.get_openapi`.

Y esa función `get_openapi()` recibe como parámetros:

* `title`: El título de OpenAPI, mostrado en la documentación.
* `version`: La versión de tu API, por ejemplo `2.5.0`.
* `openapi_version`: La versión de la especificación OpenAPI utilizada. Por defecto, la más reciente: `3.1.0`.
* `summary`: Un breve resumen de la API.
* `description`: La descripción de tu API, esta puede incluir markdown y se mostrará en la documentación.
* `routes`: Una list de rutas, estas son cada una de las *path operations* registradas. Se toman de `app.routes`.

/// info | Información

El parámetro `summary` está disponible en OpenAPI 3.1.0 y versiones superiores, soportado por FastAPI 0.99.0 y superiores.

///

## Sobrescribir los valores por defecto

Usando la información anterior, puedes usar la misma función de utilidad para generar el esquema de OpenAPI y sobrescribir cada parte que necesites.

Por ejemplo, vamos a añadir <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">la extensión OpenAPI de ReDoc para incluir un logo personalizado</a>.

### **FastAPI** normal

Primero, escribe toda tu aplicación **FastAPI** como normalmente:

{* ../../docs_src/extending_openapi/tutorial001.py hl[1,4,7:9] *}

### Generar el esquema de OpenAPI

Luego, usa la misma función de utilidad para generar el esquema de OpenAPI, dentro de una función `custom_openapi()`:

{* ../../docs_src/extending_openapi/tutorial001.py hl[2,15:21] *}

### Modificar el esquema de OpenAPI

Ahora puedes añadir la extensión de ReDoc, agregando un `x-logo` personalizado al "objeto" `info` en el esquema de OpenAPI:

{* ../../docs_src/extending_openapi/tutorial001.py hl[22:24] *}

### Cachear el esquema de OpenAPI

Puedes usar la propiedad `.openapi_schema` como un "cache", para almacenar tu esquema generado.

De esa forma, tu aplicación no tendrá que generar el esquema cada vez que un usuario abra la documentación de tu API.

Se generará solo una vez, y luego se usará el mismo esquema cacheado para las siguientes requests.

{* ../../docs_src/extending_openapi/tutorial001.py hl[13:14,25:26] *}

### Sobrescribir el método

Ahora puedes reemplazar el método `.openapi()` por tu nueva función.

{* ../../docs_src/extending_openapi/tutorial001.py hl[29] *}

### Revisa

Una vez que vayas a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> verás que estás usando tu logo personalizado (en este ejemplo, el logo de **FastAPI**):

<img src="/img/tutorial/extending-openapi/image01.png">

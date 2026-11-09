# Form Data { #form-data }

Cuando necesitas recibir campos de formulario en lugar de JSON, puedes usar `Form`.

/// note | Nota

Para usar formularios, primero instala [`python-multipart`](https://github.com/Kludex/python-multipart).

Añádelo a tu proyecto:

```console
$ uv add python-multipart
```

///

## Importa `Form` { #import-form }

Importa `Form` desde `fastapi`:

{* ../../docs_src/request_forms/tutorial001.py hl[3] *}

## Define parámetros de `Form` { #define-form-parameters }

Crea parámetros de formulario de la misma manera que lo harías para `Body` o `Query`:

{* ../../docs_src/request_forms/tutorial001.py hl[9] *}

Por ejemplo, en una de las formas en las que se puede usar la especificación OAuth2 (llamada "password flow") se requiere enviar un `username` y `password` como campos de formulario.

La <dfn title="especificación">especificación</dfn> requiere que los campos se llamen exactamente `username` y `password`, y que se envíen como campos de formulario, no JSON.

Con `Form` puedes declarar las mismas configuraciones que con `Body` (y `Query`, `Path`, `Cookie`), incluyendo validación, ejemplos, un alias (por ejemplo, `user-name` en lugar de `username`), etc.

/// note | Nota

`Form` es una clase que hereda directamente de `Body`.

///

/// tip | Consejo

Para declarar bodies de formularios, necesitas usar `Form` explícitamente, porque sin él, los parámetros se interpretarían como parámetros de query o como parámetros de body (JSON).

///

## Campos de formulario booleanos { #boolean-form-fields }

Los navegadores omiten las casillas de verificación no marcadas al enviar formularios HTML. Declara un parámetro de formulario booleano con un valor por defecto de `False` para recibir `False` cuando la casilla no esté marcada:

{* ../../docs_src/request_forms/tutorial002.py hl[9] *}

Una casilla de verificación marcada envía su valor, que por defecto es `"on"`. **FastAPI** acepta `"on"` como `True`.

## Sobre "Campos de formulario" { #about-form-fields }

La manera en que los formularios HTML (`<form></form>`) envían los datos al servidor normalmente usa una codificación "especial" para esos datos, es diferente de JSON.

**FastAPI** se encargará de leer esos datos del lugar correcto en lugar de JSON.

/// note | Detalles técnicos

Los datos de formularios normalmente se codifican usando el "media type" `application/x-www-form-urlencoded`.

Pero cuando el formulario incluye archivos, se codifica como `multipart/form-data`. Leerás sobre la gestión de archivos en el próximo capítulo.

Puedes usar `Form(media_type="multipart/form-data")` para describir un formulario multipart en OpenAPI. Basta con configurarlo en un parámetro al combinar parámetros de formulario o modelos.

Si quieres leer más sobre estas codificaciones y campos de formulario, dirígete a la [documentación web de <abbr title="Mozilla Developer Network - Red de Desarrolladores de Mozilla">MDN</abbr> para `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).

///

/// warning | Advertencia

Puedes declarar múltiples parámetros `Form` en una *path operation*, pero no puedes también declarar campos `Body` que esperas recibir como JSON, ya que el request tendrá el body codificado usando `application/x-www-form-urlencoded` en lugar de `application/json`.

Esto no es una limitación de **FastAPI**, es parte del protocolo HTTP.

///

## Recapitulación { #recap }

Usa `Form` para declarar parámetros de entrada de form data.

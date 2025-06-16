# Form Data

Cuando necesitas recibir campos de formulario en lugar de JSON, puedes usar `Form`.

/// info | Información

Para usar forms, primero instala <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo, y luego instalarlo, por ejemplo:

```console
$ pip install python-multipart
```

///

## Importar `Form`

Importar `Form` desde `fastapi`:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## Definir parámetros de `Form`

Crea parámetros de formulario de la misma manera que lo harías para `Body` o `Query`:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

Por ejemplo, en una de las formas en las que se puede usar la especificación OAuth2 (llamada "password flow") se requiere enviar un `username` y `password` como campos de formulario.

La <abbr title="specification">especificación</abbr> requiere que los campos se llamen exactamente `username` y `password`, y que se envíen como campos de formulario, no JSON.

Con `Form` puedes declarar las mismas configuraciones que con `Body` (y `Query`, `Path`, `Cookie`), incluyendo validación, ejemplos, un alias (por ejemplo, `user-name` en lugar de `username`), etc.

/// info | Información

`Form` es una clase que hereda directamente de `Body`.

///

/// tip | Consejo

Para declarar bodies de forms, necesitas usar `Form` explícitamente, porque sin él, los parámetros se interpretarían como parámetros de query o como parámetros de body (JSON).

///

## Sobre "Campos de Formulario"

La manera en que los forms HTML (`<form></form>`) envían los datos al servidor normalmente usa una codificación "especial" para esos datos, es diferente de JSON.

**FastAPI** se encargará de leer esos datos del lugar correcto en lugar de JSON.

/// note | Detalles técnicos

Los datos de forms normalmente se codifican usando el "media type" `application/x-www-form-urlencoded`.

Pero cuando el formulario incluye archivos, se codifica como `multipart/form-data`. Leerás sobre la gestión de archivos en el próximo capítulo.

Si quieres leer más sobre estas codificaciones y campos de formulario, dirígete a la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs para <code>POST</code></a>.

///

/// warning | Advertencia

Puedes declarar múltiples parámetros `Form` en una *path operation*, pero no puedes también declarar campos `Body` que esperas recibir como JSON, ya que el request tendrá el body codificado usando `application/x-www-form-urlencoded` en lugar de `application/json`.

Esto no es una limitación de **FastAPI**, es parte del protocolo HTTP.

///

## Recapitulación

Usa `Form` para declarar parámetros de entrada de datos de formulario.

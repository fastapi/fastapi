# Usar el Request Directamente

Hasta ahora, has estado declarando las partes del request que necesitas con sus tipos.

Tomando datos de:

* El path como parámetros.
* Headers.
* Cookies.
* etc.

Y al hacerlo, **FastAPI** está validando esos datos, convirtiéndolos y generando documentación para tu API automáticamente.

Pero hay situaciones donde podrías necesitar acceder al objeto `Request` directamente.

## Detalles sobre el objeto `Request`

Como **FastAPI** es en realidad **Starlette** por debajo, con una capa de varias herramientas encima, puedes usar el objeto <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> de Starlette directamente cuando lo necesites.

También significa que si obtienes datos del objeto `Request` directamente (por ejemplo, leyendo el cuerpo) no serán validados, convertidos o documentados (con OpenAPI, para la interfaz automática de usuario de la API) por FastAPI.

Aunque cualquier otro parámetro declarado normalmente (por ejemplo, el cuerpo con un modelo de Pydantic) seguiría siendo validado, convertido, anotado, etc.

Pero hay casos específicos donde es útil obtener el objeto `Request`.

## Usa el objeto `Request` directamente

Imaginemos que quieres obtener la dirección IP/host del cliente dentro de tu *path operation function*.

Para eso necesitas acceder al request directamente.

{* ../../docs_src/using_request_directly/tutorial001.py hl[1,7:8] *}

Al declarar un parámetro de *path operation function* con el tipo siendo `Request`, **FastAPI** sabrá pasar el `Request` en ese parámetro.

/// tip | Consejo

Nota que en este caso, estamos declarando un parámetro de path además del parámetro del request.

Así que, el parámetro de path será extraído, validado, convertido al tipo especificado y anotado con OpenAPI.

De la misma manera, puedes declarar cualquier otro parámetro como normalmente, y adicionalmente, obtener también el `Request`.

///

## Documentación de `Request`

Puedes leer más detalles sobre el <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">objeto `Request` en el sitio de documentación oficial de Starlette</a>.

/// note | Detalles Técnicos

Podrías también usar `from starlette.requests import Request`.

**FastAPI** lo proporciona directamente solo como conveniencia para ti, el desarrollador. Pero viene directamente de Starlette.

///

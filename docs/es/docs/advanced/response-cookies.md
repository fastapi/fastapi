# Cookies de Response

## Usar un parámetro `Response`

Puedes declarar un parámetro de tipo `Response` en tu *path operation function*.

Y luego puedes establecer cookies en ese objeto de response *temporal*.

{* ../../docs_src/response_cookies/tutorial002.py hl[1, 8:9] *}

Y entonces puedes devolver cualquier objeto que necesites, como normalmente lo harías (un `dict`, un modelo de base de datos, etc).

Y si declaraste un `response_model`, todavía se utilizará para filtrar y convertir el objeto que devolviste.

**FastAPI** utilizará ese response *temporal* para extraer las cookies (también los headers y el código de estado), y las pondrá en el response final que contiene el valor que devolviste, filtrado por cualquier `response_model`.

También puedes declarar el parámetro `Response` en las dependencias, y establecer cookies (y headers) en ellas.

## Devolver una `Response` directamente

También puedes crear cookies al devolver una `Response` directamente en tu código.

Para hacer eso, puedes crear un response como se describe en [Devolver un Response Directamente](response-directly.md){.internal-link target=_blank}.

Luego establece Cookies en ella, y luego devuélvela:

{* ../../docs_src/response_cookies/tutorial001.py hl[10:12] *}

/// tip | Consejo

Ten en cuenta que si devuelves un response directamente en lugar de usar el parámetro `Response`, FastAPI lo devolverá directamente.

Así que tendrás que asegurarte de que tus datos son del tipo correcto. Por ejemplo, que sea compatible con JSON, si estás devolviendo un `JSONResponse`.

Y también que no estés enviando ningún dato que debería haber sido filtrado por un `response_model`.

///

### Más información

/// note | Detalles Técnicos

También podrías usar `from starlette.responses import Response` o `from starlette.responses import JSONResponse`.

**FastAPI** proporciona los mismos `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

Y como el `Response` se puede usar frecuentemente para establecer headers y cookies, **FastAPI** también lo proporciona en `fastapi.Response`.

///

Para ver todos los parámetros y opciones disponibles, revisa la <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">documentación en Starlette</a>.

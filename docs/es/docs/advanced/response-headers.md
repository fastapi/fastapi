# Response Headers

## Usa un parámetro `Response`

Puedes declarar un parámetro de tipo `Response` en tu *función de path operation* (como puedes hacer para cookies).

Y luego puedes establecer headers en ese objeto de response *temporal*.

{* ../../docs_src/response_headers/tutorial002.py hl[1, 7:8] *}

Y luego puedes devolver cualquier objeto que necesites, como harías normalmente (un `dict`, un modelo de base de datos, etc).

Y si declaraste un `response_model`, aún se usará para filtrar y convertir el objeto que devolviste.

**FastAPI** usará ese response *temporal* para extraer los headers (también cookies y el código de estado), y los pondrá en el response final que contiene el valor que devolviste, filtrado por cualquier `response_model`.

También puedes declarar el parámetro `Response` en dependencias y establecer headers (y cookies) en ellas.

## Retorna una `Response` directamente

También puedes agregar headers cuando devuelves un `Response` directamente.

Crea un response como se describe en [Retorna un Response Directamente](response-directly.md){.internal-link target=_blank} y pasa los headers como un parámetro adicional:

{* ../../docs_src/response_headers/tutorial001.py hl[10:12] *}

/// note | Detalles Técnicos

También podrías usar `from starlette.responses import Response` o `from starlette.responses import JSONResponse`.

**FastAPI** proporciona las mismas `starlette.responses` como `fastapi.responses` solo por conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles provienen directamente de Starlette.

Y como el `Response` se puede usar frecuentemente para establecer headers y cookies, **FastAPI** también lo proporciona en `fastapi.Response`.

///

## Headers Personalizados

Ten en cuenta que los headers propietarios personalizados se pueden agregar <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando el prefijo 'X-'</a>.

Pero si tienes headers personalizados que quieres que un cliente en un navegador pueda ver, necesitas agregarlos a tus configuraciones de CORS (leer más en [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), usando el parámetro `expose_headers` documentado en <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">la documentación CORS de Starlette</a>.

# Headers de Respuesta

## Usar un parámetro `Response`

Puedes declarar un parámetro de tipo `Response` en tu *función de operación de path* (de manera similar como se hace con las cookies).

Y entonces, podrás configurar las cookies en ese objeto de response *temporal*.

```Python hl_lines="1  7-8"
{!../../../docs_src/response_headers/tutorial002.py!}
```

Posteriormente, puedes devolver cualquier objeto que necesites, como normalmente harías (un `dict`, un modelo de base de datos, etc).

Si declaraste un `response_model`, este se continuará usando para filtrar y convertir el objeto que devolviste.

**FastAPI** usará ese response *temporal* para extraer los headers (al igual que las cookies y el status code), además las pondrá en el response final que contendrá el valor retornado y filtrado por algún `response_model`.

También puedes declarar el parámetro `Response` en dependencias, así como configurar los headers (y las cookies) en ellas.


## Retornar una `Response` directamente

Adicionalmente, puedes añadir headers cuando se retorne una `Response` directamente.

Crea un response tal como se describe en [Retornar una respuesta directamente](response-directly.md){.internal-link target=_blank} y pasa los headers como un parámetro adicional:

```Python hl_lines="10-12"
{!../../../docs_src/response_headers/tutorial001.py!}
```

/// note | Detalles Técnicos

También podrías utilizar `from starlette.responses import Response` o `from starlette.responses import JSONResponse`.

**FastAPI** proporciona las mismas `starlette.responses` en `fastapi.responses` sólo que de una manera más conveniente para ti, el desarrollador. En otras palabras, muchas de las responses disponibles provienen directamente de Starlette.


Y como la `Response` puede ser usada frecuentemente para configurar headers y cookies, **FastAPI** también la provee en `fastapi.Response`.

///

## Headers Personalizados

Ten en cuenta que se pueden añadir headers propietarios personalizados <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando el prefijo 'X-'</a>.

Si tienes headers personalizados y deseas que un cliente pueda verlos en el navegador, es necesario que los añadas a tus configuraciones de CORS (puedes leer más en [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), usando el parámetro `expose_headers` documentado en <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>.

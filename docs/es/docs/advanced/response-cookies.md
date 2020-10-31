# Cookies de Respuesta

## Usar un parámetro `Response` 

Puedes declarar un parámetro de tipo `Response` en tu *path operation function*.

Y entonces, podrás configurar las cookies en ese objeto de 
response *temporal*.


```Python hl_lines="1  8-9"
{!../../../docs_src/response_cookies/tutorial002.py!}
```

Posteriormente, podrá retornar cualquier objeto que necesite, como lo haría normalmente (un `diccionario`, un modelo de base de datos, etc).

Si declaraste un `response_model`, este se continuará usando para filtrar y convertir el objeto que devolviste. 

**FastAPI** usará esa *temporal* response para extraer las cookies (al igual que los headers y el status code), además las pondrá en la respuesta final que contendrá el valor retornado y filtrado por algún `response_model`.


También podrás declarar el parámetro `Response` en dependencias, así como configurar las cookies (y headers) en ellas.


## Retornar una `Response` directamente 

Adicionalmente, puedes crear cookies cuando se retorne una `Response` directamente en tu código. 

Para hacer esto, puedes crear una respuesta tal como se describe en [Retornar una respuesta directamente](response-directly.md){.internal-link target=_blank}.


Posteriormente configurar las Cookies en él, y finalmente retornarlo, como explicamos a continuación:

```Python hl_lines="10-12"
{!../../../docs_src/response_cookies/tutorial001.py!}
```

!!! tip
    Tenga en mente que si retorna una respuesta directamente,
    en lugar de usar el parámetro `Response`, FastAPI la devolverá tal cual.
    

    De este modo, tendrás que asegurarte que los datos son del tipo correcto. Por ejemplo, si corresponde con un JSON, si estás retornando un `JSONResponse`.


    Además, deberás estar seguro que no estás enviando ningún dato que debería haber sido filtrado por un `response_model`.
    
### Información adicional

!!! note "Detalles Técnicos"
    También podrías utilizar `from starlette.responses import Response` o `from starlette.responses import JSONResponse`.

    **FastAPI** proporciona las mismas `starlette.responses` en `fastapi.responses` sólo que de una manera más conveniente para ti, el desarrollador. En otras palabras, muchas de las respuestas disponibles provienen directamente de Starlette.
    

    Y como la `Response` puede ser usada frecuentemente para configurar headers y cookies, **FastAPI** también la provee en `fastapi.Response`.

To see all the available parameters and options, check the <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">documentation in Starlette</a>.

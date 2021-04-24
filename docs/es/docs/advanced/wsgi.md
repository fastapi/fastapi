# Incluyendo WSGI - Flask, Django, entre otros 

Puedes montar aplicaciones WSGI como observaste en [Sub Aplicaciones - Montajes](./sub-applications.md){.internal-link target=_blank}, [Detrás de un Proxy](./behind-a-proxy.md){.internal-link target=_blank}.

Para esto , puedes utilizar `WSGIMiddleware` y posteriormente utilizarlo para empaquetar tú aplicación WSGI , por ejemplo , Flask, Django, etc.

## Usando `WSGIMiddleware`

Necesitas importar `WSGIMiddleware`.

Luego , empaquetar la aplicación WSGI (p.ej Flask) con el <abbr>middleware</abbr>.

Y posteriormente montandolo asignándole un <abbr>path</abbr>.

```Python hl_lines="2-3  22"
{!../../../docs_src/wsgi/tutorial001.py!}
```

## Pruébalo

Ahora , cada petición que se encuentre bajo el <abbr>path</abbr> `/v1/` será manejado por la aplicación de Flask.

Y el resto va ser manejado por **FastAPI**.

Si lo ejecutas con Uvicorn y te dirijes a <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> observaras la respuesta de Flask:

```txt
Hello, World from Flask!
```

Y si te diriges a <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> veras las respuesta de FastAPI:

```JSON
{
    "message": "Hello World"
}
```

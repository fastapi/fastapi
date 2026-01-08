# Incluyendo WSGI - Flask, Django, otros { #including-wsgi-flask-django-others }

Puedes montar aplicaciones WSGI como viste con [Sub Aplicaciones - Mounts](sub-applications.md){.internal-link target=_blank}, [Detrás de un Proxy](behind-a-proxy.md){.internal-link target=_blank}.

Para eso, puedes usar `WSGIMiddleware` y usarlo para envolver tu aplicación WSGI, por ejemplo, Flask, Django, etc.

## Usando `WSGIMiddleware` { #using-wsgimiddleware }

Necesitas importar `WSGIMiddleware`.

Luego envuelve la aplicación WSGI (p. ej., Flask) con el middleware.

Y luego móntala bajo un path.

{* ../../docs_src/wsgi/tutorial001_py39.py hl[2:3,3] *}

## Revisa { #check-it }

Ahora, cada request bajo el path `/v1/` será manejado por la aplicación Flask.

Y el resto será manejado por **FastAPI**.

Si lo ejecutas y vas a <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> verás el response de Flask:

```txt
Hello, World from Flask!
```

Y si vas a <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> verás el response de FastAPI:

```JSON
{
    "message": "Hello World"
}
```

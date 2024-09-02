# WSGI inkludieren – Flask, Django und andere

Sie können WSGI-Anwendungen mounten, wie Sie es in [Unteranwendungen – Mounts](sub-applications.md){.internal-link target=_blank}, [Hinter einem Proxy](behind-a-proxy.md){.internal-link target=_blank} gesehen haben.

Dazu können Sie die `WSGIMiddleware` verwenden und damit Ihre WSGI-Anwendung wrappen, zum Beispiel Flask, Django usw.

## `WSGIMiddleware` verwenden

Sie müssen `WSGIMiddleware` importieren.

Wrappen Sie dann die WSGI-Anwendung (z. B. Flask) mit der Middleware.

Und dann mounten Sie das auf einem Pfad.

```Python hl_lines="2-3  23"
{!../../../docs_src/wsgi/tutorial001.py!}
```

## Es ansehen

Jetzt wird jede Anfrage unter dem Pfad `/v1/` von der Flask-Anwendung verarbeitet.

Und der Rest wird von **FastAPI** gehandhabt.

Wenn Sie das mit Uvicorn ausführen und auf <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> gehen, sehen Sie die Response von Flask:

```txt
Hello, World from Flask!
```

Und wenn Sie auf <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> gehen, sehen Sie die Response von FastAPI:

```JSON
{
    "message": "Hello World"
}
```

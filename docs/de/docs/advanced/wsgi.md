# WSGI inkludieren – Flask, Django und andere { #including-wsgi-flask-django-others }

Sie können WSGI-Anwendungen mounten, wie Sie es in [Unteranwendungen – Mounts](sub-applications.md){.internal-link target=_blank}, [Hinter einem Proxy](behind-a-proxy.md){.internal-link target=_blank} gesehen haben.

Dazu können Sie die `WSGIMiddleware` verwenden und damit Ihre WSGI-Anwendung wrappen, zum Beispiel Flask, Django usw.

## `WSGIMiddleware` verwenden { #using-wsgimiddleware }

Sie müssen `WSGIMiddleware` importieren.

Wrappen Sie dann die WSGI-Anwendung (z. B. Flask) mit der Middleware.

Und dann mounten Sie das auf einem Pfad.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,3] *}

## Es testen { #check-it }

Jetzt wird jeder <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> unter dem Pfad `/v1/` von der Flask-Anwendung verarbeitet.

Und der Rest wird von **FastAPI** gehandhabt.

Wenn Sie das ausführen und auf <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> gehen, sehen Sie die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> von Flask:

```txt
Hello, World from Flask!
```

Und wenn Sie auf <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> gehen, sehen Sie die Response von FastAPI:

```JSON
{
    "message": "Hello World"
}
```

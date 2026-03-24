# WSGI inkludieren – Flask, Django und andere { #including-wsgi-flask-django-others }

Sie können WSGI-Anwendungen mounten, wie Sie es in [Unteranwendungen – Mounts](sub-applications.md), [Hinter einem Proxy](behind-a-proxy.md) gesehen haben.

Dazu können Sie die `WSGIMiddleware` verwenden und damit Ihre WSGI-Anwendung wrappen, zum Beispiel Flask, Django usw.

## `WSGIMiddleware` verwenden { #using-wsgimiddleware }

/// info | Info

Dafür muss `a2wsgi` installiert sein, z. B. mit `pip install a2wsgi`.

///

Sie müssen `WSGIMiddleware` aus `a2wsgi` importieren.

Wrappen Sie dann die WSGI-Anwendung (z. B. Flask) mit der Middleware.

Und dann mounten Sie das auf einem Pfad.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Hinweis

Früher wurde empfohlen, `WSGIMiddleware` aus `fastapi.middleware.wsgi` zu verwenden, dies ist jetzt deprecatet.

Stattdessen wird empfohlen, das Paket `a2wsgi` zu verwenden. Die Nutzung bleibt gleich.

Stellen Sie lediglich sicher, dass das Paket `a2wsgi` installiert ist und importieren Sie `WSGIMiddleware` korrekt aus `a2wsgi`.

///

## Es testen { #check-it }

Jetzt wird jeder <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> unter dem Pfad `/v1/` von der Flask-Anwendung verarbeitet.

Und der Rest wird von **FastAPI** gehandhabt.

Wenn Sie das ausführen und auf [http://localhost:8000/v1/](http://localhost:8000/v1/) gehen, sehen Sie die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> von Flask:

```txt
Hello, World from Flask!
```

Und wenn Sie auf [http://localhost:8000/v2](http://localhost:8000/v2) gehen, sehen Sie die Response von FastAPI:

```JSON
{
    "message": "Hello World"
}
```

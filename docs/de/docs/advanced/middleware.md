# Fortgeschrittene Middleware

Im Haupttutorial haben Sie gelesen, wie Sie Ihrer Anwendung [benutzerdefinierte Middleware](../tutorial/middleware.md){.internal-link target=_blank} hinzufügen können.

Und dann auch, wie man [CORS mittels der `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank} handhabt.

In diesem Abschnitt werden wir sehen, wie man andere Middlewares verwendet.

## ASGI-Middleware hinzufügen

Da **FastAPI** auf Starlette basiert und die <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>-Spezifikation implementiert, können Sie jede ASGI-Middleware verwenden.

Eine Middleware muss nicht speziell für FastAPI oder Starlette gemacht sein, um zu funktionieren, solange sie der ASGI-Spezifikation genügt.

Im Allgemeinen handelt es sich bei ASGI-Middleware um Klassen, die als erstes Argument eine ASGI-Anwendung erwarten.

In der Dokumentation für ASGI-Middlewares von Drittanbietern wird Ihnen wahrscheinlich gesagt, etwa Folgendes zu tun:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Aber FastAPI (eigentlich Starlette) bietet eine einfachere Möglichkeit, welche sicherstellt, dass die internen Middlewares zur Behandlung von Serverfehlern und benutzerdefinierten Exceptionhandlern ordnungsgemäß funktionieren.

Dazu verwenden Sie `app.add_middleware()` (wie schon im Beispiel für CORS gesehen).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` empfängt eine Middleware-Klasse als erstes Argument und dann alle weiteren Argumente, die an die Middleware übergeben werden sollen.

## Integrierte Middleware

**FastAPI** enthält mehrere Middlewares für gängige Anwendungsfälle. Wir werden als Nächstes sehen, wie man sie verwendet.

/// note | "Technische Details"

Für die nächsten Beispiele könnten Sie auch `from starlette.middleware.something import SomethingMiddleware` verwenden.

**FastAPI** bietet mehrere Middlewares via `fastapi.middleware` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Middlewares kommen aber direkt von Starlette.

///

## `HTTPSRedirectMiddleware`

Erzwingt, dass alle eingehenden Requests entweder `https` oder `wss` sein müssen.

Alle eingehenden Requests an `http` oder `ws` werden stattdessen an das sichere Schema umgeleitet.

```Python hl_lines="2  6"
{!../../../docs_src/advanced_middleware/tutorial001.py!}
```

## `TrustedHostMiddleware`

Erzwingt, dass alle eingehenden Requests einen korrekt gesetzten `Host`-Header haben, um sich vor HTTP-Host-Header-Angriffen zu schützen.

```Python hl_lines="2  6-8"
{!../../../docs_src/advanced_middleware/tutorial002.py!}
```

Die folgenden Argumente werden unterstützt:

* `allowed_hosts` – Eine Liste von Domain-Namen, die als Hostnamen zulässig sein sollten. Wildcard-Domains wie `*.example.com` werden unterstützt, um Subdomains zu matchen. Um jeden Hostnamen zu erlauben, verwenden Sie entweder `allowed_hosts=["*"]` oder lassen Sie diese Middleware weg.

Wenn ein eingehender Request nicht korrekt validiert wird, wird eine „400“-Response gesendet.

## `GZipMiddleware`

Verarbeitet GZip-Responses für alle Requests, die `"gzip"` im `Accept-Encoding`-Header enthalten.

Diese Middleware verarbeitet sowohl Standard- als auch Streaming-Responses.

```Python hl_lines="2  6"
{!../../../docs_src/advanced_middleware/tutorial003.py!}
```

Die folgenden Argumente werden unterstützt:

* `minimum_size` – Antworten, die kleiner als diese Mindestgröße in Bytes sind, nicht per GZip komprimieren. Der Defaultwert ist `500`.

## Andere Middlewares

Es gibt viele andere ASGI-Middlewares.

Zum Beispiel:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorns `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Um mehr über weitere verfügbare Middlewares herauszufinden, besuchen Sie <a href="https://www.starlette.io/middleware/" class="external-link" target="_blank">Starlettes Middleware-Dokumentation</a> und die <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a>.

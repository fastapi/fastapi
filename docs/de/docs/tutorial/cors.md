# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS oder <abbr title="Herkunftsübergreifende Ressourcenfreigabe">„Cross-Origin Resource Sharing“</abbr></a>
beschreibt die Situation, wenn ein Frontend, das in einem Browser läuft, Javascript-Code ausführt, der mit einem Backend kommuniziert, welches ein anderes „Origin“ als das Frontend hat.

## <abbr title="Ursprung, Herkunft, Quelle">Origin</abbr>

Ein Origin ist die Kombination aus Protokoll (`http`, `https`), Domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`) und Port (`80`, `443`, `8080`).

Folglich sind das hier alles unterschiedliche Origins:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Sogar wenn sich alle auf `localhost` befinden, verwenden sie unterschiedliche Protokolle oder Ports, also sind es unterschiedliche „Origins“.

## Schritte

Angenommen, Sie haben eine Frontend-Anwendung, die in Ihrem Browser unter `http://localhost:8080` läuft, und ihr JavaScript versucht, mit einem Backend unter `http://localhost` zu kommunizieren (da wir keinen Port angeben, geht der Browser vom Standardport `80` aus).

Dann sendet der Browser einen HTTP-`OPTIONS`-Request an das `:80`-Backend, und wenn dieses Backend die entsprechenden Header sendet, die die Kommunikation von diesem anderen Origin (`http://localhost:8080`) erlauben, lässt der Browser das JavaScript im `:8080`-Frontend dessen Request an das `:80`-Backend senden.


Um dies zu erreichen, muss das `:80`-Backend eine Liste der „erlaubten Origins“ haben.

In diesem Fall müsste diese Liste `http://localhost:8080` enthalten, damit das `:8080`-Frontend korrekt funktioniert.

## Wildcards

Es ist auch möglich, die Liste als `"*"` (ein „Wildcard“) zu deklarieren, um zu sagen, dass alle Origins erlaubt sind.

Aber dies wird nur bestimmte Arten von Kommunikation erlauben, wobei alles ausgeschlossen wird, was Anmeldeinformationen beinhaltet: Cookies, Autorisierungs-Header wie solche, die mit Bearer Tokens verwendet werden, usw.

Damit also alles richtig funktioniert, ist es besser, die erlaubten Origins explizit anzugeben.

## `CORSMiddleware` verwenden

Sie können das in Ihrer **FastAPI**-Anwendung mit der `CORSMiddleware` konfigurieren.

* Importieren Sie `CORSMiddleware`.
* Erstellen Sie eine Liste der erlaubten Origins (als Strings).
* Fügen Sie das Ganze als „Middleware“ zu Ihrer **FastAPI**-Anwendung hinzu.

Sie können auch angeben, ob Ihr Backend Folgendes erlaubt:

* Zugangsdaten (Credentials) – Autorisierungs-Header, Cookies, usw.
* Spezifische HTTP-Methoden (`POST`, `PUT`) oder alle davon mit dem Wildcard `"*"`.
* Spezifische HTTP-Header oder alle davon mit dem Wildcard `"*"`.

```Python hl_lines="2  6-11  13-19"
{!../../../docs_src/cors/tutorial001.py!}
```

Die Defaultparameter, die von der `CORSMiddleware`-Implementierung verwendet werden, sind standardmäßig restriktiv, sodass Sie bestimmte Origins, Methoden oder Header explizit aktivieren müssen, damit Browser sie in einem Cross-Domain-Kontext verwenden dürfen.

Die folgenden Argumente werden unterstützt:

* `allow_origins` – Eine Liste von Origins, die berechtigt sein sollten, Cross-Origin-Requests durchzuführen. Z. B. `['https://example.org', 'https://www.example.org']`. Sie können `['*']` verwenden, um jedes Origin zu erlauben.
* `allow_origin_regex` - Ein Regex-String, der mit Origins übereinstimmt, die berechtigt sein sollten, Cross-Origin-Requests zu stellen. z. B. `'https://.*\.example\.org'`.
* `allow_methods` – Eine Liste von HTTP-Methoden, die für Cross-Origin-Requests erlaubt sein sollten. Standardmäßig auf `['GET']` gesetzt. Sie können `['*']` verwenden, um alle Standardmethoden zu erlauben.
* `allow_headers` – Eine Liste von HTTP-Request-Headern, die für Cross-Origin-Requests unterstützt werden sollten. Standardmäßig auf `[]` gesetzt. Sie können `['*']` verwenden, um alle Header zu erlauben. Die Header `Accept`, `Accept-Language`, `Content-Language` und `Content-Type` sind immer für <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">einfache CORS-Requests</a> erlaubt.
* `allow_credentials` – Bestimmt, dass Cookies für Cross-Origin-Requests unterstützt werden sollen. Standardmäßig auf `False` gesetzt. Außerdem darf `allow_origins` nicht auf `['*']` gesetzt sein, um Anmeldeinformationen zu erlauben, Origins müssen angegeben werden.
* `expose_headers` – Bestimmt, welche Response-Header für den Browser zugänglich gemacht werden sollen. Standardmäßig auf `[]` gesetzt.
* `max_age` – Legt eine maximale Zeitspanne in Sekunden fest, für die Browser CORS-Responses cachen dürfen. Standardmäßig auf `600` gesetzt.

Die Middleware antwortet auf zwei bestimmte Arten von HTTP-Requests ...

### CORS <abbr title="Vorab-Anfragen">Preflight-Requests</abbr>

Dies sind alle `OPTIONS`-Requests mit `Origin` und `Access-Control-Request-Method`-Headern.

In dem Fall wird die Middleware den eingehenden Request abfangen und mit entsprechenden CORS-Headern antworten, und entweder eine `200` oder `400`-Response zu Informationszwecken senden.

### Einfache Requests

Jeder Request mit einem `Origin`-Header. In dem Fall wird die Middleware den Request wie gewohnt weiterleiten, aber die entsprechenden CORS-Header der Response beifügen.

## Weitere Informationen

Für weitere Informationen zu <abbr title="Cross-Origin Resource Sharing – Herkunftsübergreifende Ressourcenfreigabe">CORS</abbr>, besuchen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS Dokumentation</a>.

!!! note "Technische Details"
    Sie können auch `from starlette.middleware.cors import CORSMiddleware` verwenden.

    **FastAPI** stellt mehrere Middlewares in `fastapi.middleware` zur Verfügung, als Annehmlichkeit für Sie, den Entwickler. Die meisten dieser verfügbaren Middlewares kommen jedoch direkt von Starlette.

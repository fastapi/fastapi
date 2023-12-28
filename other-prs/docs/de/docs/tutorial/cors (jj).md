# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS oder "Cross-Origin Resource Sharing"</a>
beschreibt die Situation, wenn ein Frontend (aus JavaScript-Code), das in einem Browser läuft und mit einem Backend kommuniziert, welches in einem anderen "Ursprung" als das Frontend ist.

## Ursprung

Der Ursprung ist die Kombination aus Protokoll (`http`, `https`), Domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`) und Port (`80`, `443`, `8080`).

So sind alle diese unterschiedliche Ursprünge:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Sogar wenn sie alle in `localhost` sind, verwenden sie unterschiedliche Protokolle oder Ports, also sind sie unterschiedliche "Ursprünge".

## Schritte

Angenommen, Sie haben eine Frontend-Anwendung, die in Ihrem Browser unter `http://localhost:8080` läuft, und ihr JavaScript versucht, mit einem Backend unter `http://localhost` zu kommunizieren (da wir keinen Port angeben, geht der Browser vom Standardport `80` aus).

Dann sendet der Browser eine HTTP `OPTIONS`-Anfrage an das Backend, und wenn das Backend die entsprechenden Header sendet, die die Kommunikation von diesem anderen Ursprung (`http://localhost:8080`) autorisieren, lässt der Browser das JavaScript im Frontend seine Anfrage an das Backend senden.


Um dies zu erreichen, muss das Backend eine Liste der "erlaubten Ursprünge" haben.

In diesem Fall müsste es `http://localhost:8080` für das Frontend enthalten, um korrekt zu funktionieren.

## Wildcards

Es ist auch möglich, die Liste als `"*"` (ein "Wildcard") zu deklarieren, um zu sagen, dass alle erlaubt sind.

Aber dies wird nur bestimmte Arten von Kommunikation erlauben, wobei alles ausgeschlossen wird, was Anmeldeinformationen beinhaltet: Cookies, Autorisierungs-Header wie die mit Bearer Tokens verwendet werden, etc.

Um alles richtig funktionieren zu lassen, ist es besser, die erlaubten Ursprünge explizit anzugeben.

## Verwende `CORSMiddleware`

Du kannst es in deiner **FastAPI**-Anwendung mit der `CORSMiddleware` konfigurieren.

* Importiere `CORSMiddleware`.
* Erstelle eine Liste der erlaubten Ursprünge (als strings).
* Füge es als "Middleware" zu deiner **FastAPI**-Anwendung hinzu.

Du kannst auch angeben, ob dein Backend erlaubt:

* Zugangsdaten (Autorisierungs-Header, Cookies, etc).
* Spezifische HTTP-Methoden (`POST`, `PUT`) oder alle mit dem Wildcard `"*"`.
* Spezifische HTTP-Header oder alle mit dem Wildcard `"*"`.

```Python hl_lines="2  6-11  13-19"
{!../../../docs_src/cors/tutorial001.py!}
```

Der Standardparameter, der von der `CORSMiddleware`-Implementierung verwendet wird, ist standardmäßig restriktiv, so dass du bestimmte Ursprünge, Methoden oder Header explizit aktivieren musst, damit Browser sie in einem Cross-Domain-Kontext verwenden dürfen.

Die folgenden Argumente werden unterstützt:

* `allow_origins` - Eine Liste von Ursprüngen, die berechtigt sein sollten, Cross-Origin-Anfragen zu stellen. Z.B. `['https://example.org', 'https://www.example.org']`. Du kannst `['*']` verwenden, um jeden Ursprung zu erlauben.
* `allow_origin_regex` - Ein Regex-String, der mit Ursprüngen übereinstimmt, die berechtigt sein sollten, Cross-Origin-Anfragen zu stellen. z.B. `'https://.*\.example\.org'`.
* `allow_methods` - Eine Liste von HTTP-Methoden, die für Cross-Origin-Anfragen erlaubt sein sollten. Standardmäßig auf `['GET']` gesetzt. Du kannst `['*']` verwenden, um alle Standardmethoden zu erlauben.
* `allow_headers` - Eine Liste von HTTP-Anfrage-Headern, die für Cross-Origin-Anfragen unterstützt werden sollten. Standardmäßig auf `[]` gesetzt. Du kannst `['*']` verwenden, um alle Header zu erlauben. Die Header `Accept`, `Accept-Language`, `Content-Language` und `Content-Type` sind immer für <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">einfache CORS-Anfragen</a> erlaubt.
* `allow_credentials` - Bestimmt das Cookies für Cross-Origin-Anfragen unterstützt werden sollen. Standardmäßig auf `False` gesetzt. Außerdem kann `allow_origins` nicht auf `['*']` gesetzt werden, damit Anmeldeinformationen erlaubt werden, Ursprünge müssen angegeben werden.
* `expose_headers` - Bestimt welche Antwort-Header für den Browser zugänglich gemacht werden sollen. Standardmäßig auf `[]` gesetzt.
* `max_age` - Legt eine maximale Zeit in Sekunden fest, die Browser verwenden, um CORS-Antworten zu cachen. Standardmäßig auf `600` gesetzt.

Die Middleware reagiert auf zwei bestimmte Arten von HTTP-Anfragen...

### CORS Preflight-Anfragen

Dies sind alle `OPTIONS`-Anfragen mit `Origin` und `Access-Control-Request-Method`-Headern.

In diesem Fall kann die Middleware die eingehende Anfrage abfangen und mit entsprechenden CORS-Headern antworten, und entweder eine `200` oder `400`-Antwort zu Informationszwecken senden.

### Einfache Anfragen

Jede Anfrage mit einem `Origin`-Header. In diesem Fall wird die Middleware die Anfrage wie gewohnt weiterleiten, aber die entsprechenden CORS-Header in der Antwort enthalten.

## Weitere Informationen

Für weitere Informationen zu <abbr title="Cross-Origin Resource Sharing">CORS</abbr>, gehe auf die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS Dokumentation</a>.

!!! note "Technische Details"
    Du kannst auch `from starlette.middleware.cors import CORSMiddleware` verwenden.

    **FastAPI** stellt mehrere Middlewares in `fastapi.middleware` als Annehmlichkeit für Sie, den Entwickler. Die meisten der verfügbaren Middlewares kommen jedoch direkt von Starlette.

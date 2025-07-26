# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS oder „Cross-Origin Resource Sharing“</a> bezieht sich auf die Situationen, in denen ein Frontend, das in einem Browser läuft, JavaScript-Code enthält, der mit einem Backend kommuniziert, und das Backend sich in einem anderen „Ursprung“ als das Frontend befindet.

## Ursprung

Ein Ursprung ist die Kombination aus Protokoll (`http`, `https`), Domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`) und Port (`80`, `443`, `8080`).

Also sind all diese unterschiedliche Ursprünge:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Auch wenn sie alle auf `localhost` sind, verwenden sie unterschiedliche Protokolle oder Ports, also sind sie verschiedene „Ursprünge“.

## Schritte

Nehmen wir also an, Sie haben ein Frontend, das in Ihrem Browser unter `http://localhost:8080` läuft, und dessen JavaScript versucht, mit einem Backend zu kommunizieren, das unter `http://localhost` läuft (da wir keinen Port angeben, nimmt der Browser den Defaultport `80` an).

Dann wird der Browser einen HTTP `OPTIONS`-Request an das `:80`-Backend senden, und wenn das Backend die entsprechenden Header sendet, die die Kommunikation von diesem anderen Ursprung (`http://localhost:8080`) autorisieren, dann lässt der `:8080`-Browser das JavaScript im Frontend seine Anfrage an das `:80`-Backend senden.

Um dies zu erreichen, muss das `:80`-Backend eine Liste von „erlaubten Ursprüngen“ haben.

In diesem Fall müsste die Liste `http://localhost:8080` enthalten, damit das `:8080`-Frontend korrekt funktioniert.

## Wildcards

Es ist auch möglich, die Liste als `"*"` (ein „Wildcard“) anzugeben, um zu sagen, dass alle erlaubt sind.

Aber das wird nur bestimmte Arten der Kommunikation erlauben, alles ausschließend, was Anmeldeinformationen umfasst: Cookies, Authorization-Header wie diejenigen, die mit Bearer-Tokens verwendet werden, usw.

Daher ist es besser, die erlaubten Ursprünge explizit anzugeben, damit alles korrekt funktioniert.

## Verwenden Sie `CORSMiddleware`

Sie können es in Ihrer **FastAPI**-Anwendung mit der `CORSMiddleware` konfigurieren.

* Importieren Sie `CORSMiddleware`.
* Erstellen Sie eine Liste der erlaubten Ursprünge (als Strings).
* Fügen Sie es Ihrer **FastAPI**-Anwendung als „Middleware“ hinzu.

Sie können auch angeben, ob Ihr Backend Folgendes zulässt:

* Anmeldeinformationen (Authorization-Header, Cookies, usw.).
* Bestimmte HTTP-Methoden (`POST`, `PUT`) oder alle mit dem Wildcard `"*"`.
* Bestimmte HTTP-Header oder alle mit dem Wildcard `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

Die von der `CORSMiddleware`-Implementierung verwendeten Defaultparameter sind standardmäßig restriktiv, daher müssen Sie bestimmte Ursprünge, Methoden oder Header explizit aktivieren, damit Browser sie in einem Cross-Domain-Kontext verwenden können.

Die folgenden Argumente werden unterstützt:

* `allow_origins` - Eine Liste von Ursprüngen, die Cross-Origin-Requests durchführen dürfen. Z.B. `['https://example.org', 'https://www.example.org']`. Sie können `['*']` verwenden, um jeden Ursprung zuzulassen.
* `allow_origin_regex` - Ein Regex-String, der mit Ursprüngen übereinstimmen muss, die Cross-Origin-Requests durchführen dürfen. z.B. `'https://.*\.example\.org'`.
* `allow_methods` - Eine Liste von HTTP-Methoden, die für Cross-Origin-Requests erlaubt sein sollten. Standardmäßig `['GET']`. Sie können `['*']` verwenden, um alle Standardmethoden zuzulassen.
* `allow_headers` - Eine Liste von HTTP-Anfrage-Headern, die für Cross-Origin-Requests unterstützt werden sollten. Standardmäßig `[]`. Sie können `['*']` verwenden, um alle Header zuzulassen. Die Header `Accept`, `Accept-Language`, `Content-Language` und `Content-Type` sind immer für <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">einfache CORS-Anfragen</a> erlaubt.
* `allow_credentials` - Zeigt an, dass Cookies für Cross-Origin-Requests unterstützt werden sollten. Standardmäßig `False`.

    Keiner der `allow_origins`, `allow_methods` und `allow_headers` kann auf `['*']` gesetzt werden, wenn `allow_credentials` auf `True` gesetzt ist. Alle müssen <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">explizit angegeben</a> werden.

* `expose_headers` - Gibt an, welche Response-Header dem Browser zugänglich gemacht werden sollen. Standardmäßig `[]`.
* `max_age` - Legt eine maximale Zeit in Sekunden fest, wie lange Browser CORS-Responses cachen dürfen. Standardmäßig `600`.

Die Middleware antwortet auf zwei besondere Arten von HTTP-Requests...

### CORS Preflight-Anfragen

Dies sind alle `OPTIONS`-Requests mit `Origin`- und `Access-Control-Request-Method`-Headern.

In diesem Fall wird die Middleware den eingehenden Request abfangen und mit den entsprechenden CORS-Headern antworten und entweder eine `200`- oder `400`-Response zu Informationszwecken senden.

### Einfache Anfragen

Jede Anfrage mit einem `Origin`-Header. In diesem Fall wird die Middleware den Request normal durchlassen, aber die entsprechenden CORS-Header zur Response hinzufügen.

## Weitere Informationen

Für weitere Informationen über <abbr title="Cross-Origin Resource Sharing">CORS</abbr> lesen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS Dokumentation</a>.

/// note | Technische Details

Sie könnten auch `from starlette.middleware.cors import CORSMiddleware` verwenden.

**FastAPI** bietet mehrere Middlewares in `fastapi.middleware` an, lediglich als Bequemlichkeit für Sie, den Entwickler. Aber die meisten der verfügbaren Middlewares stammen direkt von Starlette.

///

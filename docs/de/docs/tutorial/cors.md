# CORS (Cross-Origin Resource Sharing) { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS oder <abbr title="Ressourcenfreigabe zwischen Ursprüngen">„Cross-Origin Resource Sharing“</abbr></a> bezieht sich auf Situationen, in denen ein Frontend, das in einem Browser läuft, JavaScript-Code enthält, der mit einem Backend kommuniziert, und das Backend sich in einem anderen „Origin“ als das Frontend befindet.

## Origin { #origin }

Ein <abbr title="Ursprung">Origin</abbr> ist die Kombination aus Protokoll (`http`, `https`), Domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`) und Port (`80`, `443`, `8080`).

Alle folgenden sind also unterschiedliche Origins:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Auch wenn sie alle in `localhost` sind, verwenden sie unterschiedliche Protokolle oder Ports, daher sind sie unterschiedliche „Origins“.

## Schritte { #steps }

Angenommen, Sie haben ein Frontend, das in Ihrem Browser unter `http://localhost:8080` läuft, und dessen JavaScript versucht, mit einem Backend zu kommunizieren, das unter `http://localhost` läuft (da wir keinen Port angegeben haben, geht der Browser vom Default-Port `80` aus).

Dann wird der Browser ein HTTP-`OPTIONS`-<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> an das `:80`-Backend senden, und wenn das Backend die entsprechenden Header sendet, die die Kommunikation von diesem anderen Origin (`http://localhost:8080`) autorisieren, lässt der `:8080`-Browser das JavaScript im Frontend seinen Request an das `:80`-Backend senden.

Um dies zu erreichen, muss das `:80`-Backend eine Liste von „erlaubten Origins“ haben.

In diesem Fall müsste die Liste `http://localhost:8080` enthalten, damit das `:8080`-Frontend korrekt funktioniert.

## Wildcards { #wildcards }

Es ist auch möglich, die Liste als `"*"` (ein „Wildcard“) zu deklarieren, um anzuzeigen, dass alle erlaubt sind.

Aber das erlaubt nur bestimmte Arten der Kommunikation und schließt alles aus, was Anmeldeinformationen beinhaltet: Cookies, Autorisierungsheader wie die, die mit Bearer Tokens verwendet werden, usw.

Um sicherzustellen, dass alles korrekt funktioniert, ist es besser, die erlaubten Origins explizit anzugeben.

## `CORSMiddleware` verwenden { #use-corsmiddleware }

Sie können das in Ihrer **FastAPI**-Anwendung mit der `CORSMiddleware` konfigurieren.

* Importieren Sie `CORSMiddleware`.
* Erstellen Sie eine Liste der erlaubten Origins (als Strings).
* Fügen Sie es als „Middleware“ zu Ihrer **FastAPI**-Anwendung hinzu.

Sie können auch angeben, ob Ihr Backend erlaubt:

* Anmeldeinformationen (Autorisierungsheader, Cookies, usw.).
* Bestimmte HTTP-Methoden (`POST`, `PUT`) oder alle mit der Wildcard `"*"`.
* Bestimmte HTTP-Header oder alle mit der Wildcard `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

Die von der `CORSMiddleware`-Implementierung verwendeten Defaultparameter sind standardmäßig restriktiv, daher müssen Sie bestimmte Origins, Methoden oder Header ausdrücklich aktivieren, damit Browser sie in einem Cross-Domain-Kontext verwenden dürfen.

Die folgenden Argumente werden unterstützt:

* `allow_origins` – Eine Liste von Origins, die Cross-Origin-Requests machen dürfen. z. B. `['https://example.org', 'https://www.example.org']`. Sie können `['*']` verwenden, um jedes Origin zuzulassen.
* `allow_origin_regex` – Ein Regex-String zum Abgleichen gegen Origins, die Cross-Origin-Requests machen dürfen. z. B. `'https://.*\.example\.org'`.
* `allow_methods` – Eine Liste von HTTP-Methoden, die für Cross-Origin-Requests erlaubt sein sollen. Standardmäßig `['GET']`. Sie können `['*']` verwenden, um alle Standardmethoden zu erlauben.
* `allow_headers` – Eine Liste von HTTP-Requestheadern, die für Cross-Origin-Requests unterstützt werden sollten. Standardmäßig `[]`. Sie können `['*']` verwenden, um alle Header zu erlauben. Die Header `Accept`, `Accept-Language`, `Content-Language` und `Content-Type` sind immer für <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">einfache CORS-Requests</a> erlaubt.
* `allow_credentials` – Anzeigen, dass Cookies für Cross-Origin-Requests unterstützt werden sollten. Standardmäßig `False`.

    Keines der `allow_origins`, `allow_methods` und `allow_headers` kann auf `['*']` gesetzt werden, wenn `allow_credentials` auf `True` gesetzt ist. Alle müssen <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">explizit angegeben</a> werden.

* `expose_headers` – Angabe der Responseheader, auf die der Browser zugreifen können soll. Standardmäßig `[]`.
* `max_age` – Legt eine maximale Zeit in Sekunden fest, die Browser CORS-Responses zwischenspeichern dürfen. Standardmäßig `600`.

Die Middleware antwortet auf zwei besondere Arten von HTTP-Requests ...

### CORS-Preflight-Requests { #cors-preflight-requests }

Dies sind alle `OPTIONS`-Requests mit `Origin`- und `Access-Control-Request-Method`-Headern.

In diesem Fall wird die Middleware den eingehenden Request abfangen und mit entsprechenden CORS-Headern, und entweder einer `200`- oder `400`-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> zu Informationszwecken antworten.

### Einfache Requests { #simple-requests }

Jeder Request mit einem `Origin`-Header. In diesem Fall wird die Middleware den Request wie gewohnt durchlassen, aber entsprechende CORS-Header in die Response aufnehmen.

## Weitere Informationen { #more-info }

Weitere Informationen zu <abbr title="Cross-Origin Resource Sharing – Ressourcenfreigabe zwischen Ursprüngen">CORS</abbr> finden Sie in der <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS-Dokumentation</a>.

/// note | Technische Details

Sie könnten auch `from starlette.middleware.cors import CORSMiddleware` verwenden.

**FastAPI** bietet mehrere Middlewares in `fastapi.middleware` nur als Komfort für Sie, den Entwickler. Aber die meisten der verfügbaren Middlewares stammen direkt von Starlette.

///

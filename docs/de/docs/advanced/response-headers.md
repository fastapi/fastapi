# Response-Header { #response-headers }

## Einen `Response`-Parameter verwenden { #use-a-response-parameter }

Sie können einen Parameter vom Typ `Response` in Ihrer *Pfadoperation-Funktion* deklarieren (wie Sie es auch für Cookies tun können).

Und dann können Sie Header in diesem *vorübergehenden* <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>-Objekt festlegen.

{* ../../docs_src/response_headers/tutorial002.py hl[1, 7:8] *}

Anschließend können Sie wie gewohnt jedes gewünschte Objekt zurückgeben (ein `dict`, ein Datenbankmodell, usw.).

Und wenn Sie ein `response_model` deklariert haben, wird es weiterhin zum Filtern und Konvertieren des von Ihnen zurückgegebenen Objekts verwendet.

**FastAPI** verwendet diese *vorübergehende* Response, um die Header (auch Cookies und Statuscode) zu extrahieren und fügt diese in die endgültige Response ein, die den von Ihnen zurückgegebenen Wert enthält, gefiltert nach einem beliebigen `response_model`.

Sie können den Parameter `Response` auch in Abhängigkeiten deklarieren und darin Header (und Cookies) festlegen.

## Eine `Response` direkt zurückgeben { #return-a-response-directly }

Sie können auch Header hinzufügen, wenn Sie eine `Response` direkt zurückgeben.

Erstellen Sie eine Response wie in [Eine Response direkt zurückgeben](response-directly.md){.internal-link target=_blank} beschrieben und übergeben Sie die Header als zusätzlichen Parameter:

{* ../../docs_src/response_headers/tutorial001.py hl[10:12] *}

/// note | Technische Details

Sie können auch `from starlette.responses import Response` oder `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

Und da die `Response` häufig zum Setzen von Headern und Cookies verwendet wird, stellt **FastAPI** diese auch unter `fastapi.Response` bereit.

///

## Benutzerdefinierte Header { #custom-headers }

Beachten Sie, dass benutzerdefinierte proprietäre Header <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">mittels des Präfix `X-`</a> hinzugefügt werden können.

Wenn Sie jedoch benutzerdefinierte Header haben, die ein Client in einem Browser sehen können soll, müssen Sie diese zu Ihrer CORS-Konfiguration hinzufügen (weitere Informationen finden Sie unter [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), unter Verwendung des Parameters `expose_headers`, dokumentiert in <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlettes CORS-Dokumentation</a>.

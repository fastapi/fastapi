# Response-Cookies

## Einen `Response`-Parameter verwenden

Sie können einen Parameter vom Typ `Response` in Ihrer *Pfadoperation-Funktion* deklarieren.

Und dann können Sie Cookies in diesem *vorübergehenden* Response-Objekt setzen.

```Python hl_lines="1  8-9"
{!../../../docs_src/response_cookies/tutorial002.py!}
```

Anschließend können Sie wie gewohnt jedes gewünschte Objekt zurückgeben (ein `dict`, ein Datenbankmodell, usw.).

Und wenn Sie ein `response_model` deklariert haben, wird es weiterhin zum Filtern und Konvertieren des von Ihnen zurückgegebenen Objekts verwendet.

**FastAPI** verwendet diese *vorübergehende* Response, um die Cookies (auch Header und Statuscode) zu extrahieren und fügt diese in die endgültige Response ein, die den von Ihnen zurückgegebenen Wert enthält, gefiltert nach einem beliebigen `response_model`.

Sie können den `Response`-Parameter auch in Abhängigkeiten deklarieren und darin Cookies (und Header) setzen.

## Eine `Response` direkt zurückgeben

Sie können Cookies auch erstellen, wenn Sie eine `Response` direkt in Ihrem Code zurückgeben.

Dazu können Sie eine Response erstellen, wie unter [Eine Response direkt zurückgeben](response-directly.md){.internal-link target=_blank} beschrieben.

Setzen Sie dann Cookies darin und geben Sie sie dann zurück:

```Python hl_lines="10-12"
{!../../../docs_src/response_cookies/tutorial001.py!}
```

/// tip | "Tipp"

Beachten Sie, dass, wenn Sie eine Response direkt zurückgeben, anstatt den `Response`-Parameter zu verwenden, FastAPI diese direkt zurückgibt.

Sie müssen also sicherstellen, dass Ihre Daten vom richtigen Typ sind. Z. B. sollten diese mit JSON kompatibel sein, wenn Sie eine `JSONResponse` zurückgeben.

Und auch, dass Sie keine Daten senden, die durch ein `response_model` hätten gefiltert werden sollen.

///

### Mehr Informationen

/// note | "Technische Details"

Sie können auch `from starlette.responses import Response` oder `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

Und da die `Response` häufig zum Setzen von Headern und Cookies verwendet wird, stellt **FastAPI** diese auch unter `fastapi.Response` bereit.

///

Um alle verfügbaren Parameter und Optionen anzuzeigen, sehen Sie sich deren <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">Dokumentation in Starlette</a> an.

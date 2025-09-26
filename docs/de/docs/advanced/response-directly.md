# Eine Response direkt zurückgeben { #return-a-response-directly }

Wenn Sie eine **FastAPI** *Pfadoperation* erstellen, können Sie normalerweise beliebige Daten davon zurückgeben: ein `dict`, eine `list`, ein Pydantic-Modell, ein Datenbankmodell, usw.

Standardmäßig konvertiert **FastAPI** diesen Rückgabewert automatisch nach JSON, mithilfe des `jsonable_encoder`, der in [JSON-kompatibler Encoder](../tutorial/encoder.md){.internal-link target=_blank} erläutert wird.

Dann würde es hinter den Kulissen diese JSON-kompatiblen Daten (z. B. ein `dict`) in eine `JSONResponse` einfügen, die zum Senden der <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> an den Client verwendet wird.

Sie können jedoch direkt eine `JSONResponse` von Ihren *Pfadoperationen* zurückgeben.

Das kann beispielsweise nützlich sein, um benutzerdefinierte Header oder Cookies zurückzugeben.

## Eine `Response` zurückgeben { #return-a-response }

Tatsächlich können Sie jede `Response` oder jede Unterklasse davon zurückgeben.

/// tip | Tipp

`JSONResponse` selbst ist eine Unterklasse von `Response`.

///

Und wenn Sie eine `Response` zurückgeben, wird **FastAPI** diese direkt weiterleiten.

Es wird keine Datenkonvertierung mit Pydantic-Modellen durchführen, es wird den Inhalt nicht in irgendeinen Typ konvertieren, usw.

Dadurch haben Sie viel Flexibilität. Sie können jeden Datentyp zurückgeben, jede Datendeklaration oder -validierung überschreiben, usw.

## Verwendung des `jsonable_encoder` in einer `Response` { #using-the-jsonable-encoder-in-a-response }

Da **FastAPI** keine Änderungen an einer von Ihnen zurückgegebenen `Response` vornimmt, müssen Sie sicherstellen, dass deren Inhalt dafür bereit ist.

Sie können beispielsweise kein Pydantic-Modell in eine `JSONResponse` einfügen, ohne es zuvor in ein `dict` zu konvertieren, bei dem alle Datentypen (wie `datetime`, `UUID`, usw.) in JSON-kompatible Typen konvertiert wurden.

In diesen Fällen können Sie den `jsonable_encoder` verwenden, um Ihre Daten zu konvertieren, bevor Sie sie an eine Response übergeben:

{* ../../docs_src/response_directly/tutorial001.py hl[6:7,21:22] *}

/// note | Technische Details

Sie könnten auch `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

///

## Eine benutzerdefinierte `Response` zurückgeben { #returning-a-custom-response }

Das obige Beispiel zeigt alle Teile, die Sie benötigen, ist aber noch nicht sehr nützlich, da Sie das `item` einfach direkt hätten zurückgeben können, und **FastAPI** würde es für Sie in eine `JSONResponse` einfügen, es in ein `dict` konvertieren, usw. All das standardmäßig.

Sehen wir uns nun an, wie Sie damit eine benutzerdefinierte Response zurückgeben können.

Nehmen wir an, Sie möchten eine <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a>-Response zurückgeben.

Sie könnten Ihren XML-Inhalt als String in eine `Response` einfügen und sie zurückgeben:

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

## Anmerkungen { #notes }

Wenn Sie eine `Response` direkt zurücksenden, werden deren Daten weder validiert, konvertiert (serialisiert), noch automatisch dokumentiert.

Sie können sie aber trotzdem wie unter [Zusätzliche Responses in OpenAPI](additional-responses.md){.internal-link target=_blank} beschrieben dokumentieren.

In späteren Abschnitten erfahren Sie, wie Sie diese benutzerdefinierten `Response`s verwenden/deklarieren und gleichzeitig über automatische Datenkonvertierung, Dokumentation, usw. verfügen.

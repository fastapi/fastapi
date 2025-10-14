# Zusätzliche Statuscodes { #additional-status-codes }

Standardmäßig liefert **FastAPI** die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> als `JSONResponse` zurück und fügt den Inhalt, den Sie aus Ihrer *Pfadoperation* zurückgeben, in diese `JSONResponse` ein.

Es wird der Default-Statuscode oder derjenige verwendet, den Sie in Ihrer *Pfadoperation* festgelegt haben.

## Zusätzliche Statuscodes { #additional-status-codes_1 }

Wenn Sie neben dem Hauptstatuscode weitere Statuscodes zurückgeben möchten, können Sie dies tun, indem Sie direkt eine `Response` zurückgeben, wie etwa eine `JSONResponse`, und den zusätzlichen Statuscode direkt festlegen.

Angenommen, Sie möchten eine *Pfadoperation* haben, die das Aktualisieren von Artikeln ermöglicht und bei Erfolg den HTTP-Statuscode 200 „OK“ zurückgibt.

Sie möchten aber auch, dass sie neue Artikel akzeptiert. Und wenn die Artikel vorher nicht vorhanden waren, werden diese Artikel erstellt und der HTTP-Statuscode 201 „Created“ zurückgegeben.

Um dies zu erreichen, importieren Sie `JSONResponse`, und geben Sie Ihren Inhalt direkt zurück, indem Sie den gewünschten `status_code` setzen:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | Achtung

Wenn Sie eine `Response` direkt zurückgeben, wie im obigen Beispiel, wird sie direkt zurückgegeben.

Sie wird nicht mit einem Modell usw. serialisiert.

Stellen Sie sicher, dass sie die gewünschten Daten enthält und dass die Werte gültiges JSON sind (wenn Sie `JSONResponse` verwenden).

///

/// note | Technische Details

Sie können auch `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette. Dasselbe gilt für `status`.

///

## OpenAPI- und API-Dokumentation { #openapi-and-api-docs }

Wenn Sie zusätzliche Statuscodes und Responses direkt zurückgeben, werden diese nicht in das OpenAPI-Schema (die API-Dokumentation) aufgenommen, da FastAPI keine Möglichkeit hat, im Voraus zu wissen, was Sie zurückgeben werden.

Sie können das jedoch in Ihrem Code dokumentieren, indem Sie Folgendes verwenden: [Zusätzliche Responses](additional-responses.md){.internal-link target=_blank}.

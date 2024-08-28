# Zusätzliche Statuscodes

Standardmäßig liefert **FastAPI** die Rückgabewerte (Responses) als `JSONResponse` zurück und fügt den Inhalt der jeweiligen *Pfadoperation* in das `JSONResponse` Objekt ein.

Es wird der Default-Statuscode oder derjenige verwendet, den Sie in Ihrer *Pfadoperation* festgelegt haben.

## Zusätzliche Statuscodes

Wenn Sie neben dem Hauptstatuscode weitere Statuscodes zurückgeben möchten, können Sie dies tun, indem Sie direkt eine `Response` zurückgeben, wie etwa eine `JSONResponse`, und den zusätzlichen Statuscode direkt festlegen.

Angenommen, Sie möchten eine *Pfadoperation* haben, die das Aktualisieren von Artikeln ermöglicht und bei Erfolg den HTTP-Statuscode 200 „OK“ zurückgibt.

Sie möchten aber auch, dass sie neue Artikel akzeptiert. Und wenn die Elemente vorher nicht vorhanden waren, werden diese Elemente erstellt und der HTTP-Statuscode 201 „Created“ zurückgegeben.

Um dies zu erreichen, importieren Sie `JSONResponse`, und geben Sie Ihren Inhalt direkt zurück, indem Sie den gewünschten `status_code` setzen:

//// tab | Python 3.10+

```Python hl_lines="4  25"
{!> ../../../docs_src/additional_status_codes/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="4  25"
{!> ../../../docs_src/additional_status_codes/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="4  26"
{!> ../../../docs_src/additional_status_codes/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="2  23"
{!> ../../../docs_src/additional_status_codes/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ nicht annotiert

/// tip | "Tipp"

Bevorzugen Sie die `Annotated`-Version, falls möglich.

///

```Python hl_lines="4  25"
{!> ../../../docs_src/additional_status_codes/tutorial001.py!}
```

////

/// warning | "Achtung"

Wenn Sie eine `Response` direkt zurückgeben, wie im obigen Beispiel, wird sie direkt zurückgegeben.

Sie wird nicht mit einem Modell usw. serialisiert.

Stellen Sie sicher, dass sie die gewünschten Daten enthält und dass die Werte gültiges JSON sind (wenn Sie `JSONResponse` verwenden).

///

/// note | "Technische Details"

Sie können auch `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette. Das Gleiche gilt für `status`.

///

## OpenAPI- und API-Dokumentation

Wenn Sie zusätzliche Statuscodes und Responses direkt zurückgeben, werden diese nicht in das OpenAPI-Schema (die API-Dokumentation) aufgenommen, da FastAPI keine Möglichkeit hat, im Voraus zu wissen, was Sie zurückgeben werden.

Sie können das jedoch in Ihrem Code dokumentieren, indem Sie Folgendes verwenden: [Zusätzliche Responses](additional-responses.md){.internal-link target=_blank}.

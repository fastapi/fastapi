# Fehlerbehandlung

Es gibt viele Situationen, in denen Sie einem Client, der Ihre API benutzt, einen Fehler zurückgeben müssen.

Dieser Client könnte ein Browser mit einem Frontend, Code von jemand anderem, ein <abbr title="Internet of Things – Internet der Dinge: Geräte, die über das Internet Informationen austauschen">IoT</abbr>-Gerät, usw., sein.

Sie müssten beispielsweise einem Client sagen:

* Dass er nicht die notwendigen Berechtigungen hat, eine Aktion auszuführen.
* Dass er zu einer Ressource keinen Zugriff hat.
* Dass die Ressource, auf die er zugreifen möchte, nicht existiert.
* usw.

In diesen Fällen geben Sie normalerweise einen **HTTP-Statuscode** im Bereich **400** (400 bis 499) zurück.

Das ist vergleichbar mit den HTTP-Statuscodes im Bereich 200 (von 200 bis 299). Diese „200“er Statuscodes bedeuten, dass der Request in einem bestimmten Aspekt ein „Success“ („Erfolg“) war.

Die Statuscodes im 400er-Bereich bedeuten hingegen, dass es einen Fehler gab.

Erinnern Sie sich an all diese **404 Not Found** Fehler (und Witze)?

## `HTTPException` verwenden

Um HTTP-Responses mit Fehlern zum Client zurückzugeben, verwenden Sie `HTTPException`.

### `HTTPException` importieren

```Python hl_lines="1"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### Eine `HTTPException` in Ihrem Code auslösen

`HTTPException` ist eine normale Python-<abbr title="Exception – Ausnahme, Fehler: Python-Objekt, das einen Fehler nebst Metadaten repräsentiert">Exception</abbr> mit einigen zusätzlichen Daten, die für APIs relevant sind.

Weil es eine Python-Exception ist, geben Sie sie nicht zurück, (`return`), sondern Sie lösen sie aus (`raise`).

Das bedeutet auch, wenn Sie in einer Hilfsfunktion sind, die Sie von ihrer *Pfadoperation-Funktion* aus aufrufen, und Sie lösen eine `HTTPException` von innerhalb dieser Hilfsfunktion aus, dann wird der Rest der *Pfadoperation-Funktion* nicht ausgeführt, sondern der Request wird sofort abgebrochen und der HTTP-Error der `HTTP-Exception` wird zum Client gesendet.

Der Vorteil, eine Exception auszulösen (`raise`), statt sie zurückzugeben (`return`) wird im Abschnitt über Abhängigkeiten und Sicherheit klarer werden.

Im folgenden Beispiel lösen wir, wenn der Client eine ID anfragt, die nicht existiert, eine Exception mit dem Statuscode `404` aus.

```Python hl_lines="11"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### Die resultierende Response

Wenn der Client `http://example.com/items/foo` anfragt (ein `item_id` `"foo"`), erhält dieser Client einen HTTP-Statuscode 200 und folgende JSON-Response:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Aber wenn der Client `http://example.com/items/bar` anfragt (ein nicht-existierendes `item_id` `"bar"`), erhält er einen HTTP-Statuscode 404 (der „Not Found“-Fehler), und eine JSON-Response wie folgt:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | "Tipp"

Wenn Sie eine `HTTPException` auslösen, können Sie dem Parameter `detail` jeden Wert übergeben, der nach JSON konvertiert werden kann, nicht nur `str`.

Zum Beispiel ein `dict`, eine `list`, usw.

Das wird automatisch von **FastAPI** gehandhabt und der Wert nach JSON konvertiert.

///

## Benutzerdefinierte Header hinzufügen

Es gibt Situationen, da ist es nützlich, dem HTTP-Error benutzerdefinierte Header hinzufügen zu können, etwa in einigen Sicherheitsszenarien.

Sie müssen das wahrscheinlich nicht direkt in ihrem Code verwenden.

Aber falls es in einem fortgeschrittenen Szenario notwendig ist, können Sie benutzerdefinierte Header wie folgt hinzufügen:

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial002.py!}
```

## Benutzerdefinierte Exceptionhandler definieren

Sie können benutzerdefinierte <abbr title="Exceptionhandler – Ausnahmebehandler: Funktion, die sich um die Bearbeitung einer Exception kümmert">Exceptionhandler</abbr> hinzufügen, mithilfe <a href="https://www.starlette.io/exceptions/" class="external-link" target="_blank">derselben Werkzeuge für Exceptions von Starlette</a>.

Nehmen wir an, Sie haben eine benutzerdefinierte Exception `UnicornException`, die Sie (oder eine Bibliothek, die Sie verwenden) `raise`n könnten.

Und Sie möchten diese Exception global mit FastAPI handhaben.

Sie könnten einen benutzerdefinierten Exceptionhandler mittels `@app.exception_handler()` hinzufügen:

```Python hl_lines="5-7  13-18  24"
{!../../../docs_src/handling_errors/tutorial003.py!}
```

Wenn Sie nun `/unicorns/yolo` anfragen, `raise`d die *Pfadoperation* eine `UnicornException`.

Aber diese wird von `unicorn_exception_handler` gehandhabt.

Sie erhalten also einen sauberen Error mit einem Statuscode `418` und dem JSON-Inhalt:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | "Technische Details"

Sie können auch `from starlette.requests import Request` und `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette. Das Gleiche gilt für `Request`.

///

## Die Default-Exceptionhandler überschreiben

**FastAPI** hat einige Default-Exceptionhandler.

Diese Handler kümmern sich darum, Default-JSON-Responses zurückzugeben, wenn Sie eine `HTTPException` `raise`n, und wenn der Request ungültige Daten enthält.

Sie können diese Exceptionhandler mit ihren eigenen überschreiben.

### Requestvalidierung-Exceptions überschreiben

Wenn ein Request ungültige Daten enthält, löst **FastAPI** intern einen `RequestValidationError` aus.

Und bietet auch einen Default-Exceptionhandler dafür.

Um diesen zu überschreiben, importieren Sie den `RequestValidationError` und verwenden Sie ihn in `@app.exception_handler(RequestValidationError)`, um Ihren Exceptionhandler zu dekorieren.

Der Exceptionhandler wird einen `Request` und die Exception entgegennehmen.

```Python hl_lines="2  14-16"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

Wenn Sie nun `/items/foo` besuchen, erhalten Sie statt des Default-JSON-Errors:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

eine Textversion:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs. `ValidationError`

/// warning | "Achtung"

Das folgende sind technische Details, die Sie überspringen können, wenn sie für Sie nicht wichtig sind.

///

`RequestValidationError` ist eine Unterklasse von Pydantics <a href="https://pydantic-docs.helpmanual.io/usage/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>.

**FastAPI** verwendet diesen, sodass Sie, wenn Sie ein Pydantic-Modell für `response_model` verwenden, und ihre Daten fehlerhaft sind, einen Fehler in ihrem Log sehen.

Aber der Client/Benutzer sieht ihn nicht. Stattdessen erhält der Client einen <abbr title="Interner Server-Fehler">„Internal Server Error“</abbr> mit einem HTTP-Statuscode `500`.

Das ist, wie es sein sollte, denn wenn Sie einen Pydantic-`ValidationError` in Ihrer *Response* oder irgendwo sonst in ihrem Code haben (es sei denn, im *Request* des Clients), ist das tatsächlich ein Bug in ihrem Code.

Und während Sie den Fehler beheben, sollten ihre Clients/Benutzer keinen Zugriff auf interne Informationen über den Fehler haben, da das eine Sicherheitslücke aufdecken könnte.

### den `HTTPException`-Handler überschreiben

Genauso können Sie den `HTTPException`-Handler überschreiben.

Zum Beispiel könnten Sie eine Klartext-Response statt JSON für diese Fehler zurückgeben wollen:

```Python hl_lines="3-4  9-11  22"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

/// note | "Technische Details"

Sie können auch `from starlette.responses import PlainTextResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, als Annehmlichkeit für Sie, den Entwickler. Die meisten verfügbaren Responses kommen aber direkt von Starlette.

///

### Den `RequestValidationError`-Body verwenden

Der `RequestValidationError` enthält den empfangenen `body` mit den ungültigen Daten.

Sie könnten diesen verwenden, während Sie Ihre Anwendung entwickeln, um den Body zu loggen und zu debuggen, ihn zum Benutzer zurückzugeben, usw.

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial005.py!}
```

Jetzt versuchen Sie, einen ungültigen Artikel zu senden:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Sie erhalten eine Response, die Ihnen sagt, dass die Daten ungültig sind, und welche den empfangenen Body enthält.

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPIs `HTTPException` vs. Starlettes `HTTPException`

**FastAPI** hat seine eigene `HTTPException`.

Und **FastAPI**s `HTTPException`-Fehlerklasse erbt von Starlettes `HTTPException`-Fehlerklasse.

Der einzige Unterschied besteht darin, dass **FastAPIs** `HTTPException` alles für das Feld `detail` akzeptiert, was nach JSON konvertiert werden kann, während Starlettes `HTTPException` nur Strings zulässt.

Sie können also weiterhin **FastAPI**s `HTTPException` wie üblich in Ihrem Code auslösen.

Aber wenn Sie einen Exceptionhandler registrieren, registrieren Sie ihn für Starlettes `HTTPException`.

Auf diese Weise wird Ihr Handler, wenn irgendein Teil von Starlettes internem Code, oder eine Starlette-Erweiterung, oder -Plugin eine Starlette-`HTTPException` auslöst, in der Lage sein, diese zu fangen und zu handhaben.

Damit wir in diesem Beispiel beide `HTTPException`s im selben Code haben können, benennen wir Starlettes Exception um zu `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**s Exceptionhandler wiederverwenden

Wenn Sie die Exception zusammen mit denselben Default-Exceptionhandlern von **FastAPI** verwenden möchten, können Sie die Default-Exceptionhandler von `fastapi.Exception_handlers` importieren und wiederverwenden:

```Python hl_lines="2-5  15  21"
{!../../../docs_src/handling_errors/tutorial006.py!}
```

In diesem Beispiel `print`en Sie nur den Fehler mit einer sehr ausdrucksstarken Nachricht, aber Sie sehen, worauf wir hinauswollen. Sie können mit der Exception etwas machen und dann einfach die Default-Exceptionhandler wiederverwenden.

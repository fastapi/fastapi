# Fehler behandeln { #handling-errors }

Es gibt viele Situationen, in denen Sie einem Client, der Ihre API nutzt, einen Fehler mitteilen müssen.

Dieser Client könnte ein Browser mit einem Frontend sein, ein Code von jemand anderem, ein IoT-Gerät usw.

Sie könnten dem Client mitteilen müssen, dass:

* Der Client nicht genügend Berechtigungen für diese Operation hat.
* Der Client keinen Zugriff auf diese Ressource hat.
* Die Ressource, auf die der Client versucht hat, zuzugreifen, nicht existiert.
* usw.

In diesen Fällen würden Sie normalerweise einen **HTTP-Statuscode** im Bereich **400** (von 400 bis 499) zurückgeben.

Dies ist vergleichbar mit den HTTP-Statuscodes im Bereich 200 (von 200 bis 299). Diese „200“-Statuscodes bedeuten, dass der <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> in irgendeiner Weise erfolgreich war.

Die Statuscodes im Bereich 400 bedeuten hingegen, dass es einen Fehler seitens des Clients gab.

Erinnern Sie sich an all diese **„404 Not Found“** Fehler (und Witze)?

## `HTTPException` verwenden { #use-httpexception }

Um HTTP-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> mit Fehlern an den Client zurückzugeben, verwenden Sie `HTTPException`.

### `HTTPException` importieren { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001.py hl[1] *}

### Eine `HTTPException` in Ihrem Code auslösen { #raise-an-httpexception-in-your-code }

`HTTPException` ist eine normale Python-Exception mit zusätzlichen Daten, die für APIs relevant sind.

Weil es eine Python-Exception ist, geben Sie sie nicht zurück (`return`), sondern lösen sie aus (`raise`).

Das bedeutet auch, wenn Sie sich innerhalb einer Hilfsfunktion befinden, die Sie innerhalb Ihrer *Pfadoperation-Funktion* aufrufen, und Sie die `HTTPException` aus dieser Hilfsfunktion heraus auslösen, wird der restliche Code in der *Pfadoperation-Funktion* nicht ausgeführt. Der Request wird sofort abgebrochen und der HTTP-Error der `HTTPException` wird an den Client gesendet.

Der Vorteil des Auslösens einer Exception gegenüber dem Zurückgeben eines Wertes wird im Abschnitt über Abhängigkeiten und Sicherheit deutlicher werden.

In diesem Beispiel lösen wir eine Exception mit einem Statuscode von `404` aus, wenn der Client einen Artikel mit einer nicht existierenden ID anfordert:

{* ../../docs_src/handling_errors/tutorial001.py hl[11] *}

### Die resultierende Response { #the-resulting-response }

Wenn der Client `http://example.com/items/foo` anfordert (ein `item_id` `"foo"`), erhält dieser Client einen HTTP-Statuscode 200 und diese JSON-Response:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Aber wenn der Client `http://example.com/items/bar` anfordert (ein nicht-existierendes `item_id` `"bar"`), erhält er einen HTTP-Statuscode 404 (der „Not Found“-Error) und eine JSON-Response wie:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Tipp

Wenn Sie eine `HTTPException` auslösen, können Sie dem Parameter `detail` jeden Wert übergeben, der in JSON konvertiert werden kann, nicht nur `str`.

Sie könnten ein `dict`, eine `list`, usw. übergeben.

Diese werden von **FastAPI** automatisch gehandhabt und in JSON konvertiert.

///

## Benutzerdefinierte Header hinzufügen { #add-custom-headers }

Es gibt Situationen, in denen es nützlich ist, dem HTTP-Error benutzerdefinierte Header hinzuzufügen. Zum Beispiel in einigen Sicherheitsszenarien.

Sie werden es wahrscheinlich nicht direkt in Ihrem Code verwenden müssen.

Aber falls Sie es für ein fortgeschrittenes Szenario benötigen, können Sie benutzerdefinierte Header hinzufügen:

{* ../../docs_src/handling_errors/tutorial002.py hl[14] *}

## Benutzerdefinierte Exceptionhandler installieren { #install-custom-exception-handlers }

Sie können benutzerdefinierte <abbr title="Ausnahmebehandler: Funktion, die sich um die Bearbeitung einer Exception kümmert">Exceptionhandler</abbr> mit <a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">den gleichen Exception-Werkzeugen von Starlette</a> hinzufügen.

Angenommen, Sie haben eine benutzerdefinierte Exception `UnicornException`, die Sie (oder eine Bibliothek, die Sie verwenden) `raise`n könnten.

Und Sie möchten diese Exception global mit FastAPI handhaben.

Sie könnten einen benutzerdefinierten Exceptionhandler mit `@app.exception_handler()` hinzufügen:

{* ../../docs_src/handling_errors/tutorial003.py hl[5:7,13:18,24] *}

Hier, wenn Sie `/unicorns/yolo` anfordern, wird die *Pfadoperation* eine `UnicornException` `raise`n.

Aber diese wird von `unicorn_exception_handler` gehandhabt.

Sie erhalten also einen sauberen Fehler mit einem HTTP-Statuscode von `418` und dem JSON-Inhalt:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Technische Details

Sie könnten auch `from starlette.requests import Request` und `from starlette.responses import JSONResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, nur als Annehmlichkeit für Sie, den Entwickler. Aber die meisten verfügbaren Responses kommen direkt von Starlette. Dasselbe gilt für `Request`.

///

## Die Default-Exceptionhandler überschreiben { #override-the-default-exception-handlers }

**FastAPI** hat einige Default-Exceptionhandler.

Diese Handler sind dafür verantwortlich, die Default-JSON-Responses zurückzugeben, wenn Sie eine `HTTPException` `raise`n und wenn der Request ungültige Daten enthält.

Sie können diese Exceptionhandler mit Ihren eigenen überschreiben.

### Überschreiben von Request-Validierungs-Exceptions { #override-request-validation-exceptions }

Wenn ein Request ungültige Daten enthält, löst **FastAPI** intern einen `RequestValidationError` aus.

Und es enthält auch einen Default-Exceptionhandler für diesen.

Um diesen zu überschreiben, importieren Sie den `RequestValidationError` und verwenden Sie ihn mit `@app.exception_handler(RequestValidationError)`, um den Exceptionhandler zu dekorieren.

Der Exceptionhandler erhält einen `Request` und die Exception.

{* ../../docs_src/handling_errors/tutorial004.py hl[2,14:16] *}

Wenn Sie nun zu `/items/foo` gehen, erhalten Sie anstelle des standardmäßigen JSON-Fehlers mit:

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

eine Textversion mit:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs. `ValidationError` { #requestvalidationerror-vs-validationerror }

/// warning | Achtung

Dies sind technische Details, die Sie überspringen können, wenn sie für Sie jetzt nicht wichtig sind.

///

`RequestValidationError` ist eine Unterklasse von Pydantics <a href="https://docs.pydantic.dev/latest/concepts/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>.

**FastAPI** verwendet diesen so, dass, wenn Sie ein Pydantic-Modell in `response_model` verwenden und Ihre Daten einen Fehler haben, Sie den Fehler in Ihrem Log sehen.

Aber der Client/Benutzer wird ihn nicht sehen. Stattdessen erhält der Client einen „Internal Server Error“ mit einem HTTP-Statuscode `500`.

Es sollte so sein, denn wenn Sie einen Pydantic `ValidationError` in Ihrer *Response* oder irgendwo anders in Ihrem Code haben (nicht im *Request* des Clients), ist es tatsächlich ein Fehler in Ihrem Code.

Und während Sie den Fehler beheben, sollten Ihre Clients/Benutzer keinen Zugriff auf interne Informationen über den Fehler haben, da das eine Sicherheitslücke aufdecken könnte.

### Überschreiben des `HTTPException`-Fehlerhandlers { #override-the-httpexception-error-handler }

Auf die gleiche Weise können Sie den `HTTPException`-Handler überschreiben.

Zum Beispiel könnten Sie eine Klartext-Response statt JSON für diese Fehler zurückgeben wollen:

{* ../../docs_src/handling_errors/tutorial004.py hl[3:4,9:11,22] *}

/// note | Technische Details

Sie könnten auch `from starlette.responses import PlainTextResponse` verwenden.

**FastAPI** bietet dieselben `starlette.responses` auch via `fastapi.responses` an, nur als Annehmlichkeit für Sie, den Entwickler. Aber die meisten verfügbaren Responses kommen direkt von Starlette.

///

### Verwenden des `RequestValidationError`-Bodys { #use-the-requestvalidationerror-body }

Der `RequestValidationError` enthält den empfangenen `body` mit den ungültigen Daten.

Sie könnten diesen während der Entwicklung Ihrer Anwendung verwenden, um den Body zu loggen und zu debuggen, ihn an den Benutzer zurückzugeben usw.

{* ../../docs_src/handling_errors/tutorial005.py hl[14] *}

Versuchen Sie nun, einen ungültigen Artikel zu senden:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Sie erhalten eine Response, die Ihnen sagt, dass die Daten ungültig sind und die den empfangenen Body enthält:

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

#### FastAPIs `HTTPException` vs. Starlettes `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** hat seine eigene `HTTPException`.

Und die `HTTPException`-Fehlerklasse von **FastAPI** erbt von der `HTTPException`-Fehlerklasse von Starlette.

Der einzige Unterschied besteht darin, dass die `HTTPException` von **FastAPI** beliebige JSON-konvertierbare Daten für das `detail`-Feld akzeptiert, während die `HTTPException` von Starlette nur Strings dafür akzeptiert.

Sie können also weiterhin die `HTTPException` von **FastAPI** wie üblich in Ihrem Code auslösen.

Aber wenn Sie einen Exceptionhandler registrieren, sollten Sie ihn für die `HTTPException` von Starlette registrieren.

Auf diese Weise, wenn irgendein Teil des internen Codes von Starlette, oder eine Starlette-Erweiterung oder ein Plug-in, eine Starlette `HTTPException` auslöst, wird Ihr Handler in der Lage sein, diese abzufangen und zu handhaben.

Um in diesem Beispiel beide `HTTPException`s im selben Code zu haben, wird die Exception von Starlette zu `StarletteHTTPException` umbenannt:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Die Exceptionhandler von **FastAPI** wiederverwenden { #reuse-fastapis-exception-handlers }

Wenn Sie die Exception zusammen mit den gleichen Default-Exceptionhandlern von **FastAPI** verwenden möchten, können Sie die Default-Exceptionhandler aus `fastapi.exception_handlers` importieren und wiederverwenden:

{* ../../docs_src/handling_errors/tutorial006.py hl[2:5,15,21] *}

In diesem Beispiel geben Sie nur den Fehler mit einer sehr ausdrucksstarken Nachricht aus, aber Sie verstehen das Prinzip. Sie können die Exception verwenden und dann einfach die Default-Exceptionhandler wiederverwenden.

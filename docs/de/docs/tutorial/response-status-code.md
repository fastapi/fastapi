# Response-Statuscode

So wie ein Responsemodell, können Sie auch einen HTTP-Statuscode für die Response deklarieren, mithilfe des Parameters `status_code`, und zwar in jeder der *Pfadoperationen*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* usw.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

/// note | "Hinweis"

Beachten Sie, dass `status_code` ein Parameter der „Dekorator“-Methode ist (`get`, `post`, usw.). Nicht der *Pfadoperation-Funktion*, so wie die anderen Parameter und der Body.

///

Dem `status_code`-Parameter wird eine Zahl mit dem HTTP-Statuscode übergeben.

/// info

Alternativ kann `status_code` auch ein `IntEnum` erhalten, so wie Pythons <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>.

///

Das wird:

* Diesen Statuscode mit der Response zurücksenden.
* Ihn als solchen im OpenAPI-Schema dokumentieren (und somit in den Benutzeroberflächen):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | "Hinweis"

Einige Responsecodes (siehe nächster Abschnitt) kennzeichnen, dass die Response keinen Body hat.

FastAPI versteht das und wird in der OpenAPI-Dokumentation anzeigen, dass es keinen Responsebody gibt.

///

## Über HTTP-Statuscodes

/// note | "Hinweis"

Wenn Sie bereits wissen, was HTTP-Statuscodes sind, überspringen Sie dieses Kapitel und fahren Sie mit dem nächsten fort.

///

In HTTP senden Sie als Teil der Response einen aus drei Ziffern bestehenden numerischen Statuscode.

Diese Statuscodes haben einen Namen zugeordnet, um sie besser zu erkennen, aber der wichtige Teil ist die Zahl.

Kurz:

* `100` und darüber stehen für „Information“. Diese verwenden Sie selten direkt. Responses mit diesen Statuscodes können keinen Body haben.
* **`200`** und darüber stehen für Responses, die „Successful“ („Erfolgreich“) waren. Diese verwenden Sie am häufigsten.
    * `200` ist der Default-Statuscode, welcher bedeutet, alles ist „OK“.
    * Ein anderes Beispiel ist `201`, „Created“ („Erzeugt“). Wird in der Regel verwendet, wenn ein neuer Datensatz in der Datenbank erzeugt wurde.
    * Ein spezieller Fall ist `204`, „No Content“ („Kein Inhalt“). Diese Response wird verwendet, wenn es keinen Inhalt gibt, der zum Client zurückgeschickt wird, diese Response hat also keinen Body.
* **`300`** und darüber steht für „Redirection“ („Umleitung“).  Responses mit diesen Statuscodes können einen oder keinen Body haben, mit Ausnahme von `304`, „Not Modified“ („Nicht verändert“), welche keinen haben darf.
* **`400`** und darüber stehen für „Client error“-Responses („Client-Fehler“). Auch diese verwenden Sie am häufigsten.
    * Ein Beispiel ist `404`, für eine „Not Found“-Response („Nicht gefunden“).
    * Für allgemeine Fehler beim Client können Sie einfach `400` verwenden.
* `500` und darüber stehen für Server-Fehler. Diese verwenden Sie fast nie direkt. Wenn etwas an irgendeiner Stelle in Ihrem Anwendungscode oder im Server schiefläuft, wird automatisch einer dieser Fehler-Statuscodes zurückgegeben.

/// tip | "Tipp"

Um mehr über Statuscodes zu lernen, und welcher wofür verwendet wird, lesen Sie die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network – Mozilla-Entwickler-Netzwerk">MDN</abbr> Dokumentation über HTTP-Statuscodes</a>.

///

## Abkürzung, um die Namen zu erinnern

Schauen wir uns das vorherige Beispiel noch einmal an:

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

`201` ist der Statuscode für „Created“ („Erzeugt“).

Aber Sie müssen sich nicht daran erinnern, welcher dieser Codes was bedeutet.

Sie können die Hilfsvariablen von `fastapi.status` verwenden.

```Python hl_lines="1  6"
{!../../../docs_src/response_status_code/tutorial002.py!}
```

Diese sind nur eine Annehmlichkeit und enthalten dieselbe Nummer, aber auf diese Weise können Sie die Autovervollständigung Ihres Editors verwenden, um sie zu finden:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | "Technische Details"

Sie können auch `from starlette import status` verwenden.

**FastAPI** bietet dieselben `starlette.status`-Codes auch via `fastapi.status` an, als Annehmlichkeit für Sie, den Entwickler. Sie kommen aber direkt von Starlette.

///

## Den Defaultwert ändern

Später sehen Sie, im [Handbuch für fortgeschrittene Benutzer](../advanced/response-change-status-code.md){.internal-link target=_blank}, wie Sie einen anderen Statuscode zurückgeben können, als den Default, den Sie hier deklarieren.

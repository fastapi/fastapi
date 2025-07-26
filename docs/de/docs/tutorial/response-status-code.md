# Response-Statuscode

Genauso wie Sie ein Responsemodell angeben können, können Sie auch den HTTP-Statuscode für die Response mit dem Parameter `status_code` in jeder der *Pfadoperationen* deklarieren:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* usw.

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

/// note | Hinweis

Beachten Sie, dass `status_code` ein Parameter der „Dekorator“-Methode ist (`get`, `post`, usw.). Nicht der *Pfadoperation-Funktion*, wie alle anderen Parameter und der Body.

///

Dem `status_code`-Parameter wird eine Zahl mit dem HTTP-Statuscode übergeben.

/// info | Hinweis

Alternativ kann `status_code` auch ein `IntEnum` erhalten, wie z.B. Pythons <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>.

///

Dies wird:

* Diesen Statuscode mit der Response zurücksenden.
* Diesen im OpenAPI-Schema dokumentieren (und somit in den Benutzeroberflächen):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Hinweis

Einige Responsecodes (siehe nächster Abschnitt) kennzeichnen, dass die Response keinen Body hat.

FastAPI erkennt dies und erstellt OpenAPI-Dokumentationen, die zeigen, dass es keinen Responsebody gibt.

///

## Über HTTP-Statuscodes

/// note | Hinweis

Wenn Sie bereits wissen, was HTTP-Statuscodes sind, können Sie diesen Abschnitt überspringen und mit dem nächsten fortfahren.

///

In HTTP senden Sie einen nummerischen Statuscode mit 3 Ziffern als Teil der Response.

Diese Statuscodes haben einen zugeordneten Namen, um sie leichter zu erkennen, aber der wichtige Teil ist die Zahl.

Kurz gefasst:

* `100 - 199` stehen für „Information“. Sie verwenden diese selten direkt. Responses mit diesen Statuscodes dürfen keinen Body haben.
* **`200 - 299`** stehen für „Successful“-Responses („Erfolgreich“). Diese werden Sie am häufigsten verwenden.
    * `200` ist der Default-Statuscode, was bedeutet, alles ist „OK“.
    * Ein weiteres Beispiel wäre `201`, „Created“ („Erzeugt“). Dieser wird üblicherweise verwendet, nachdem ein neuer Datensatz in der Datenbank erstellt wurde.
    * Ein spezieller Fall ist `204`, „No Content“ („Kein Inhalt“). Diese Response wird verwendet, wenn kein Inhalt an den Client zurückgeschickt werden soll, diese Response darf also keinen Body haben.
* **`300 - 399`** stehen für „Redirection“ („Umleitung“). Responses mit diesen Statuscodes können einen Body haben oder nicht, außer bei `304`, „Not Modified“ („Nicht verändert“), die keinen haben darf.
* **`400 - 499`** stehen für „Client error“-Responses („Client-Fehler“). Diese sind die zweithäufigsten, die Sie vermutlich verwenden werden.
    * Ein Beispiel ist `404`, für eine „Not Found“-Response („Nicht gefunden“).
    * Für allgemeine Fehler beim Client können Sie einfach `400` verwenden.
* `500 - 599` stehen für Server-Fehler. Diese verwenden Sie fast nie direkt. Wenn in Ihrem Anwendungscode oder Server etwas schiefgeht, wird automatisch einer dieser Fehler-Statuscodes zurückgegeben.

/// tip | Tipp

Um mehr über die einzelnen Statuscodes zu erfahren und welcher wofür verwendet wird, sehen Sie sich die <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> Dokumentation über HTTP-Statuscodes</a> an.

///

## Abkürzung zur Erinnerung an die Namen

Lassen Sie uns das vorherige Beispiel noch einmal anschauen:

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

`201` ist der Statuscode für „Created“ („Erzeugt“).

Aber Sie müssen sich nicht merken, was jeder dieser Codes bedeutet.

Sie können die Annehmlichkeit von Variablen aus `fastapi.status` nutzen.

{* ../../docs_src/response_status_code/tutorial002.py hl[1,6] *}

Diese sind nur eine Annehmlichkeit, sie enthalten dieselbe Zahl, aber so können Sie die Autovervollständigung Ihres Editors verwenden, um sie zu finden:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Technische Details

Sie könnten auch `from starlette import status` verwenden.

**FastAPI** bietet dieselben `starlette.status`-Codes auch über `fastapi.status` an, rein zu Ihrer Annehmlichkeit als Entwickler. Aber sie stammen direkt von Starlette.

///

## Den Defaultwert ändern

Später, im [Handbuch für fortgeschrittene Benutzer](../advanced/response-change-status-code.md){.internal-link target=_blank}, werden Sie sehen, wie Sie einen anderen Statuscode zurückgeben können, als den Default, den Sie hier deklarieren.

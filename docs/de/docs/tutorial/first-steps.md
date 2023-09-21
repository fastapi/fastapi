# Erste Schritte

Das einfachste FastAPI-Programm könnte wie folgt aussehen:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Kopieren Sie das in eine Datei `main.py`.

Starten Sie den Live-Server:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! Hinweis
    Der Befehl `uvicorn main:app` bezieht sich auf:

    * `main`: die Datei `main.py` (ein sogenanntes Python-"Modul").
    * `app`: das Objekt, welches in der Datei `main.py` mit der Zeile `app = FastAPI()` erzeugt wurde.
    * `--reload`: lässt den Server nach Codeänderungen neu starten. Verwenden Sie das nur während der Entwicklung.

In der Konsolenausgabe sollte es eine Zeile geben, die ungefähr so aussieht:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Diese Zeile zeigt die URL, unter der Ihre Anwendung auf Ihrem lokalen Computer bereitgestellt wird.

### Testen Sie es

Öffnen Sie <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> in Ihrem Browser.

Sie sehen die JSON-Antwort:

```JSON
{"message": "Hello World"}
```

### Interaktive API-Dokumentation

Gehen Sie als Nächstes zu <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs </a>.

Sie sehen die automatisch erzeugte, interaktive API-Dokumentation (bereitgestellt durch <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation

Als Nächstes gehen Sie zu <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Dort sehen Sie die alternative, automatisch erstellte Dokumentation (bereitgestellt durch <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** generiert ein "Schema" für Ihre API unter Verwendung des **OpenAPI**-Standards zur Definition von APIs.

#### "Schema"

Ein "Schema" ist eine Definition oder Beschreibung von etwas. Nicht der Code, der es implementiert, sondern nur eine abstrakte Beschreibung.

#### API-"Schema"

In diesem Fall ist  <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> eine Spezifikation, die vorschreibt, wie ein Schema für Ihre API zu definieren ist.

Diese Schema-Definition enthält Ihre API-Pfade, die möglichen Parameter, welche diese entgegennehmen, usw.

#### Daten-"Schema"

Der Begriff "Schema" kann sich auch auf die Form von Daten beziehen, wie z.B. einen JSON-Inhalt.

In diesem Fall sind die JSON-Attribute und deren Datentypen, usw. gemeint.

#### OpenAPI und JSON Schemata

OpenAPI definiert ein API-Schema für Ihre API. Dieses Schema enthält Definitionen (oder "Schemata") der Daten, die von Ihrer API unter Verwendung von **JSON Schema**, dem Standard für JSON-Datenschemata, gesendet und empfangen werden.

#### Betrachten Sie die `openapi.json`

Falls Sie wissen möchten, wie das rohe OpenAPI-Schema aussieht: FastAPI generiert automatisch ein JSON (Schema) mit den Beschreibungen Ihrer gesamten API.

Sie können es direkt ansehen unter: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json </a>.

Es wird ein JSON angezeigt, welches ungefähr so aussieht (Ausschnitt):

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### Wofür OpenAPI gedacht ist

Das OpenAPI-Schema ist die Grundlage für die beiden enthaltenen interaktiven Dokumentationssysteme.

Es gibt Dutzende Alternativen, alle basierend auf OpenAPI. Sie können jede dieser Alternativen problemlos zu Ihrer Anwendung hinzufügen, die Sie mit **FastAPI** erstellt haben.

Ebenfalls können Sie es verwenden, um automatisch Code zu generieren, für Clients, die mit Ihrer API kommunizieren. Zum Beispiel für Frontend-, Mobil- oder IoT-Anwendungen.

## Rekapitulation, Schritt für Schritt

### Schritt 1: Importieren von `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` ist eine Python-Klasse, die alle Funktionalität für Ihre API bereitstellt.

!!! Hinweis "Technische Details"
    `FastAPI`  ist eine Klasse, die direkt von `Starlette` erbt.

    Sie können alle <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> Funktionalitäten auch mit `FastAPI` nutzen.

### Schritt 2: Erzeugen einer `FastAPI` "Instanz"

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Hier ist die `app`-Variable eine "Instanz" der Klasse `FastAPI`.

Dies wird der Einstiegspunkt jeder Interaktion sein, um ihre ganze API zu erstellen.

Diese `app`  ist die gleiche, auf die sich `uvicorn` im Kommando bezieht:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Wenn Sie Ihre Anwendung wie folgt erstellen:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

Und das in eine Datei `main.py` einfügen, dann würden Sie `uvicorn` wie folgt aufrufen:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Schritt 3: Erstellen einer *Pfad-Operation*

#### Pfad

"Pfad" bezieht sich hier auf den letzten Teil der URL, beginnend mit dem ersten `/`.

Sprich, in einer URL wie:

```
https://example.com/items/foo
```

... wäre der Pfad:

```
/items/foo
```

!!! Info
    Ein "Pfad" wird häufig auch als "Endpunkt" oder "Route" bezeichnet.

Bei der Erstellung einer API ist der "Pfad" die Hauptmethode zur Trennung von "Anliegen" und "Ressourcen".

#### Operation

"Operation" bezieht sich hier auf eine der HTTP-"Methoden".

Eine von diesen:

* `POST`
* `GET`
* `PUT`
* `DELETE`

... und die etwas Exotischeren:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Im HTTP-Protokoll können Sie mit jedem Pfad über eine (oder mehrere) dieser "Methoden" kommunizieren.

---

Wenn Sie APIs bauen, verwenden Sie normalerweise diese spezifischen HTTP-Methoden, um eine bestimmte Aktion durchzuführen.

Normalerweise verwenden Sie:

* `POST`: um Daten zu erzeugen.
* `GET`: um Daten zu lesen.
* `PUT`: um Daten zu aktualisieren.
* `DELETE`: um Daten zu löschen.

Daher wird in OpenAPI jede dieser HTTP-Methoden als "Operation" bezeichnet.

Wir werden sie auch "**Operationen**" nennen.

#### Definieren eines *Pfad-Operation-Dekorators*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Das `@app.get("/")` sagt **FastAPI**, dass die Funktion direkt darunter für die Bearbeitung von Anfragen zuständig ist, die an:

 * den Pfad `/`
 * unter der Verwendung der <abbr title="eine HTTP GET Methode"><code>get</code> Operation</abbr> gehen

!!! Info "`@decorator` Information"
    Diese `@etwas`-Syntax wird in Python "Dekorator" genannt.

    Sie platzieren sie über einer Funktion. Wie ein hübscher, dekorativer Hut (Ich nehme an, daher kommt der Begriff).

    Ein "Dekorator" nimmt die darunter stehende Funktion und macht etwas damit.

    In unserem Fall teilt dieser Dekorator **FastAPI** mit, dass die folgende Funktion mit dem **Pfad** `/` und der **Operation** `get` zusammenhängt.

    Es ist der "**Pfad-Operation-Dekorator**".

Sie können auch die anderen Operationen verwenden:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Oder die exotischeren:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    Es steht Ihnen frei, jede Operation (HTTP-Methode) so zu verwenden, wie Sie es wünschen.

    **FastAPI** erzwingt keine bestimmte Bedeutung.

    Die hier aufgeführten Informationen dienen als Leitfaden, nicht als Anforderung.

    Wenn Sie beispielsweise GraphQL verwenden, führen Sie normalerweise alle Aktionen nur mit "POST"-Operationen durch.

### Schritt 4: Definieren der **Pfad-Operation-Funktion**

Das ist unsere "**Pfad-Operation-Funktion**":

* **Pfad**: ist `/`.
* **Operation**: ist `get`.
* **Funktion**: ist die Funktion direkt unter dem "Dekorator" (unter `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Das ist eine Python-Funktion.

Sie wird von **FastAPI** aufgerufen, immer wenn sie eine Anfrage an die URL "`/`" mit einer `GET`-Operation erhält.

In diesem Fall handelt es sich um eine `async`-Funktion (eine asynchrone Funktion).

---

Sie könnten sie auch als normale Funktion anstelle von `async def` definieren:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! Hinweis
    Wenn Sie den Unterschied nicht kennen, lesen Sie [Async: *"In Eile?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Schritt 5: den Inhalt zurückgeben

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Sie können ein `dict`, `list`, einzelne Werte wie `str`, `int`, usw. zurückgeben.

Sie können auch Pydantic-Modelle zurückgeben (dazu später mehr).

Es gibt viele andere Objekte und Modelle, die automatisch zu JSON konvertiert werden (einschließlich ORMs usw.). Versuchen Sie, Ihre Lieblingsobjekte zu verwenden. Es ist sehr wahrscheinlich, dass sie bereits unterstützt werden.

## Zusammenfassung

* `FastAPI` importieren.
* Erstellen einer `app` Instanz.
* Schreiben eines **Pfad-Operation-Dekorators** (wie z.B. `@app.get("/")`).
* Schreiben einer **Pfad-Operation-Funktion** (wie z.B. oben `def root(): ...`).
* Starten des Entwicklungsservers (z.B. `uvicorn main:app --reload`).

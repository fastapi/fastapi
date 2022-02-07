# Erste Schritte

Die einfachste FastAPI-Datei könnte wie folgt aussehen:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Kopieren Sie diese in die Datei `main.py`.

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

    * `main`: die Datei `main.py` (das Python "Modul").
    * `app`: das Objekt, das innerhalb von `main.py` mit der Zeile `app = FastAPI()` erzeugt wird.
    * `--reload`: lässt den Server nach Codeänderungen neu starten. Nur für die Entwicklung zu verwenden.

In der Ausgabe sieht man eine Zeile wie diese:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

In dieser Zeile wird die URL angezeigt, unter der Ihre Anwendung auf Ihrem lokalen Rechner bereitgestellt wird.

### Probieren Sie es aus

Öffnen Sie ihren Browser unter der Addresse <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Sie bekommen die JSON-Antwort als:

```JSON
{"message": "Hello World"}
```

### Interaktive API-Dokumentation

Jetzt gehen Sie auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Es wird die automatische interaktive API-Dokumentation angezeigt (zur Verfügung gestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation

Gehen Sie jetzt auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Jetzt wird die alternative automatische Dokumentation angezeigt (zur Verfügung gestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** generiert ein "Schema" für Ihre gesamte API unter Verwendung des **OpenAPI**-Standards zur Definition von APIs.

#### "Schema"

Ein "Schema" ist eine Definition oder Beschreibung von etwas. Nicht der Code, der es implementiert, sondern nur eine abstrakte Beschreibung.

#### API "Schema"

Hier ist, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> eine Spezifikation, welche vorschreibt wie Ihr API Schema zu definieren ist.

Diese Schemadefinition enthält Ihre API-Pfade, die möglichen Parameter, welche diese übernehmen können und mehr.

#### Daten "Schema"

Der Begriff "Schema" kann sich auch auf die Form von Daten beziehen, z.B. einen JSON-Inhalt.

In diesem Fall wären damit die JSON-Attribute und die Datentypen gemeint, die sie verwenden, usw.

#### OpenAPI und JSON-Schema

OpenAPI definiert ein API-Schema für Ihre API. Und dieses Schema enthält Definitionen (oder "Schemata") der Daten, die von Ihrer API unter Verwendung des **JSON Schemas**, eines Standards für JSON-Datenschemata, gesendet und empfangen werden.

#### Überprüfen Sie die `openapi.json`.

Wenn Sie wissen möchten, wie das rohe OpenAPI-Schema aussieht, generiert FastAPI automatisch ein JSON-Schema mit den Beschreibungen Ihrer gesamten API.

Sie finden es unter: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Es wird ein JSON Objekt angezeigt, welches etwa so anfängt:

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

#### Wofür ist die OpenAPI?

Das OpenAPI-Schema ist die Grundlage für die beiden enthaltenen interaktiven Dokumentationssysteme.

Und es gibt Dutzende von Alternativen, die alle auf OpenAPI basieren. Sie können jede dieser Alternativen leicht zu Ihrer mit **FastAPI** erstellten Anwendung hinzufügen.

Sie können es auch verwenden, um automatischen Code für Clients zu generieren, die mit Ihrer API kommunizieren. Zum Beispiel für Frontend-, mobile oder IoT-Anwendungen.

## Schritt für Schritt Wiederholung

### Schritt 1: `FastAPI` importieren

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` ist eine Python-Klasse, die die gesamte Funktionalität für Ihre API bereitstellt.

!!! Hinweis "Technische Details"
    `FastAPI` ist eine Klasse, die direkt von `Starlette` erbt..

    Sie können alle <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> Funktionen auch mit `FastAPI` nutzen.

### Schritt 2: Erstellen einer `FastAPI` "Instanz"

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Hier wird die Variable `app` eine `Instanz` der Klasse `FastAPI` sein.

Dies wird der Hauptpunkt der Interaktion sein, um Ihre gesamte API zu erstellen.

Diese "App" ist dieselbe, auf die im Befehl "uvicorn" verwiesen wird:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Wenn Sie Ihre App so erstellen:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

Und in eine Datei `main.py` schreiben, würden Sie `uvicorn` wie folgt aufrufen:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Schritt 3: Erstellen einer *Pfadoperation*

#### Pfad

"Pfad" bezieht sich hier auf den letzten Teil der URL, beginnend mit dem ersten `/`.

Also für eine URL wie:

```
https://example.com/items/foo
```

...wäre der Pfad:

```
/items/foo
```

!!! Information
    Ein "Pfad" wird gemeinhin auch als "Endpunkt" oder "Route" bezeichnet.

Bei der Erstellung einer API ist der "Pfad" die wichtigste Methode zur Trennung von "Anliegen" und "Ressourcen".

#### Operation

"Operation" bezieht sich hier auf eine der HTTP-"Methoden".

wie:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...und die exotischeren unter ihnen:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Beim HTTP-Protokoll können Sie mit jedem Pfad über eine (oder mehrere) dieser "Methoden" kommunizieren.

---

Bei der Erstellung von APIs verwenden Sie normalerweise diese spezifischen HTTP-Methoden, um eine bestimmte Aktion durchzuführen.

Normalerweise verwenden Sie:

* `POST`: um Daten anzulegen.
* `GET`: um Daten zu lesen.
* `PUT`: um Daten zu aktualisieren.
* `DELETE`: um Daten zu löschen.

In der OpenAPI wird also jede der HTTP-Methoden als "Operation" bezeichnet.

Wir werden sie auch "**Operationen**" nennen.

#### Definieren eines *Pfadoperations-Dekorators*.

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Das `@app.get("/")` sagt **FastAPI**, dass die Funktion direkt darunter für die Bearbeitung von Anfragen zuständig ist, die an:

* den Pfad `/`
* mit einer <abbr title=" HTTP GET Methode"><code>get</code> Operation</abbr> gesendet werden.

!!! Information "`@decorator` Info"


    Diese `@etwas` Syntax wird in Python "Decorator" genannt.

    Man schreibt ihn über eine Funktion. Wie ein hübsches dekoratives Hütchen (daher kommt wohl der Begriff).

    Ein "Dekorator" erweitert die darunter stehende Funktion.

    In unserem Fall teilt dieser Dekorator **FastAPI** mit, dass die folgende Funktion dem **Pfad** `/` mit einer `get` **Operation** entspricht.

    Es handelt sich um den "**Pfadoperations-Dekorator**".

Sie können auch die anderen Operationen verwenden:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Und die exotischeren unter ihnen:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! Hinweis
    Es steht Ihnen frei, jede Operation (HTTP-Methode) so zu verwenden, wie Sie es wünschen.

    Die **FastAPI** erzwingt keine bestimmte Bedeutung.

    Die hier aufgeführten Informationen dienen als Leitfaden und sind nicht verbindlich.

    Wenn Sie beispielsweise GraphQL verwenden, führen Sie normalerweise alle Aktionen nur mit "POST"-Operationen durch.

### Schritt 4: Die **Pfadoperations-Funktion** definieren

Dies ist unsere "**Pfadoperations-Funktion**":

* **Pfad**: ist `/`.
* **Operation**: ist `get`.
* **FunKtion**: ist die Funktion unterhalb des "Dekorators" (unterhalb von `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Dies ist eine Python-Funktion.

Sie wird von **FastAPI** immer dann aufgerufen, wenn sie eine Anfrage an die URL "`/`" mittels einer `GET`-Operation erhält.

In diesem Fall handelt es sich um eine `async`-Funktion.

---

Sie könnten sie auch als normale Funktion anstelle von `async def` definieren:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! Hinweis
    Wenn Sie den Unterschied nicht kennen, lesen Sie den [Async: *"In a hurry? "*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Schritt 5: Rückgabe des Inhalts

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Sie können ein `Dict`, eine `List`, einzelne Werte wie `str`, `int`, usw. zurückgeben.

Sie können auch Pydantic-Modelle zurückgeben (dazu später mehr).

Es gibt viele andere Objekte und Modelle, die automatisch in JSON konvertiert werden (einschließlich ORMs, usw.). Versuchen Sie, Ihre Lieblingsobjekte zu verwenden. Es ist sehr wahrscheinlich, dass sie bereits unterstützt werden.

## Wiederholung

* Importieren Sie `FastAPI`.
* Erstellen Sie eine `app` Instanz.
* Legen Sie einen **Pfadoperations-Dekorator** an (wie `@app.get("/")`).
* Schreiben Sie eine **Pfadoperations-Funktion** (wie `def root(): ...` oben).
* Starten Sie den Entwicklungsserver (z.B. `uvicorn main:app --reload`).

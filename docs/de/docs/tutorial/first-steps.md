# Erste Schritte { #first-steps }

Die einfachste FastAPI-Datei könnte wie folgt aussehen:

{* ../../docs_src/first_steps/tutorial001.py *}

Kopieren Sie das in eine Datei `main.py`.

Starten Sie den Live-Server:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

In der Konsolenausgabe sollte es eine Zeile geben, die ungefähr so aussieht:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Diese Zeile zeigt die URL, unter der Ihre App auf Ihrem lokalen Computer bereitgestellt wird.

### Es testen { #check-it }

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Sie werden die JSON-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> sehen:

```JSON
{"message": "Hello World"}
```

### Interaktive API-Dokumentation { #interactive-api-docs }

Gehen Sie als Nächstes auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie werden die automatisch erzeugte, interaktive API-Dokumentation sehen (bereitgestellt durch <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation { #alternative-api-docs }

Gehen Sie nun auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Dort sehen Sie die alternative, automatische Dokumentation (bereitgestellt durch <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** generiert ein „Schema“ mit all Ihren APIs unter Verwendung des **OpenAPI**-Standards zur Definition von APIs.

#### „Schema“ { #schema }

Ein „Schema“ ist eine Definition oder Beschreibung von etwas. Nicht der eigentliche Code, der es implementiert, sondern lediglich eine abstrakte Beschreibung.

#### API-„Schema“ { #api-schema }

In diesem Fall ist <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> eine Spezifikation, die vorschreibt, wie ein Schema für Ihre API zu definieren ist.

Diese Schemadefinition enthält Ihre API-Pfade, die möglichen Parameter, welche diese entgegennehmen, usw.

#### Daten-„Schema“ { #data-schema }

Der Begriff „Schema“ kann sich auch auf die Form von Daten beziehen, wie z. B. einen JSON-Inhalt.

In diesem Fall sind die JSON-Attribute und deren Datentypen, usw. gemeint.

#### OpenAPI und JSON Schema { #openapi-and-json-schema }

OpenAPI definiert ein API-Schema für Ihre API. Dieses Schema enthält Definitionen (oder „Schemas“) der Daten, die von Ihrer API unter Verwendung von **JSON Schema**, dem Standard für JSON-Datenschemata, gesendet und empfangen werden.

#### Die `openapi.json` testen { #check-the-openapi-json }

Falls Sie wissen möchten, wie das rohe OpenAPI-Schema aussieht: FastAPI generiert automatisch ein JSON (Schema) mit den Beschreibungen Ihrer gesamten API.

Sie können es direkt einsehen unter: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Es wird ein JSON angezeigt, welches ungefähr so aussieht:

```JSON
{
    "openapi": "3.1.0",
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

#### Wofür OpenAPI gedacht ist { #what-is-openapi-for }

Das OpenAPI-Schema ist die Grundlage für die beiden enthaltenen interaktiven Dokumentationssysteme.

Es gibt dutzende Alternativen, die alle auf OpenAPI basieren. Sie können jede dieser Alternativen problemlos zu Ihrer mit **FastAPI** erstellten Anwendung hinzufügen.

Ebenfalls können Sie es verwenden, um automatisch Code für Clients zu generieren, die mit Ihrer API kommunizieren. Zum Beispiel für Frontend-, Mobile- oder IoT-Anwendungen.

## Zusammenfassung, Schritt für Schritt { #recap-step-by-step }

### Schritt 1: `FastAPI` importieren { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI` ist eine Python-Klasse, die die gesamte Funktionalität für Ihre API bereitstellt.

/// note | Technische Details

`FastAPI` ist eine Klasse, die direkt von `Starlette` erbt.

Sie können alle <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>-Funktionalitäten auch mit `FastAPI` nutzen.

///

### Schritt 2: Erzeugen einer `FastAPI`-„Instanz“ { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

In diesem Beispiel ist die Variable `app` eine „Instanz“ der Klasse `FastAPI`.

Dies wird der Hauptinteraktionspunkt für die Erstellung all Ihrer APIs sein.

### Schritt 3: Erstellen einer *Pfadoperation* { #step-3-create-a-path-operation }

#### Pfad { #path }

„Pfad“ bezieht sich hier auf den letzten Teil der URL, beginnend mit dem ersten `/`.

In einer URL wie:

```
https://example.com/items/foo
```

... wäre der Pfad folglich:

```
/items/foo
```

/// info | Info

Ein „Pfad“ wird häufig auch als „Endpunkt“ oder „Route“ bezeichnet.

///

Bei der Erstellung einer API ist der „Pfad“ die wichtigste Möglichkeit zur Trennung von „Anliegen“ und „Ressourcen“.

#### Operation { #operation }

„Operation“ bezieht sich hier auf eine der HTTP-„Methoden“.

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

Im HTTP-Protokoll können Sie mit jedem Pfad über eine (oder mehrere) dieser „Methoden“ kommunizieren.

---

Bei der Erstellung von APIs verwenden Sie normalerweise diese spezifischen HTTP-Methoden, um eine bestimmte Aktion durchzuführen.

Normalerweise verwenden Sie:

* `POST`: um Daten zu erzeugen (create).
* `GET`: um Daten zu lesen (read).
* `PUT`: um Daten zu aktualisieren (update).
* `DELETE`: um Daten zu löschen (delete).

In OpenAPI wird folglich jede dieser HTTP-Methoden als „Operation“ bezeichnet.

Wir werden sie auch „**Operationen**“ nennen.

#### Definieren eines *Pfadoperation-Dekorators* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

Das `@app.get("/")` sagt **FastAPI**, dass die Funktion direkt darunter für die Bearbeitung von <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> zuständig ist, die an:

* den Pfad `/`
* unter der Verwendung der <abbr title="eine HTTP-GET-Methode"><code>get</code>-Operation</abbr> gehen

/// info | `@decorator` Info

Diese `@something`-Syntax wird in Python „Dekorator“ genannt.

Sie platzieren ihn über einer Funktion. Wie ein hübscher, dekorativer Hut (daher kommt wohl der Begriff).

Ein „Dekorator“ nimmt die darunter stehende Funktion und macht etwas damit.

In unserem Fall teilt dieser Dekorator **FastAPI** mit, dass die folgende Funktion mit dem **Pfad** `/` und der **Operation** `get` zusammenhängt.

Dies ist der „**Pfadoperation-Dekorator**“.

///

Sie können auch die anderen Operationen verwenden:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Und die exotischeren:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Tipp

Es steht Ihnen frei, jede Operation (HTTP-Methode) so zu verwenden, wie Sie es möchten.

**FastAPI** erzwingt keine bestimmte Bedeutung.

Die hier aufgeführten Informationen dienen als Leitfaden und sind nicht verbindlich.

Wenn Sie beispielsweise GraphQL verwenden, führen Sie normalerweise alle Aktionen nur mit „POST“-Operationen durch.

///

### Schritt 4: Definieren der **Pfadoperation-Funktion** { #step-4-define-the-path-operation-function }

Das ist unsere „**Pfadoperation-Funktion**“:

* **Pfad**: ist `/`.
* **Operation**: ist `get`.
* **Funktion**: ist die Funktion direkt unter dem „Dekorator“ (unter `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Dies ist eine Python-Funktion.

Sie wird von **FastAPI** immer dann aufgerufen, wenn sie einen Request an die URL „`/`“ mittels einer `GET`-Operation erhält.

In diesem Fall handelt es sich um eine `async`-Funktion.

---

Sie könnten sie auch als normale Funktion anstelle von `async def` definieren:

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note | Hinweis

Wenn Sie den Unterschied nicht kennen, lesen Sie [Async: *„In Eile?“*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Schritt 5: den Inhalt zurückgeben { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Sie können ein `dict`, eine `list`, einzelne Werte wie `str`, `int`, usw. zurückgeben.

Sie können auch Pydantic-Modelle zurückgeben (dazu später mehr).

Es gibt viele andere Objekte und Modelle, die automatisch zu JSON konvertiert werden (einschließlich ORMs, usw.). Versuchen Sie, Ihre Lieblingsobjekte zu verwenden. Es ist sehr wahrscheinlich, dass sie bereits unterstützt werden.

## Zusammenfassung { #recap }

* Importieren Sie `FastAPI`.
* Erstellen Sie eine `app` Instanz.
* Schreiben Sie einen **Pfadoperation-Dekorator** unter Verwendung von Dekoratoren wie `@app.get("/")`.
* Definieren Sie eine **Pfadoperation-Funktion**, zum Beispiel `def root(): ...`.
* Starten Sie den Entwicklungsserver mit dem Befehl `fastapi dev`.

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI Framework, hoch performant, einfach zu erlernen, schnell zu schreiben und bereit für eine produktiv Umgebung.</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/fastapi" target="_blank">
    <img src="https://travis-ci.com/tiangolo/fastapi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Package version">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Join the chat at https://gitter.im/tiangolo/fastapi">
</a>
</p>

---

**Dokumentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Quellcode**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI ist ein, modernes und schnelles (hoch performantes), Web Framework zur Erstellung von API's mit Python 3.6+. Es basiert auf Standard Python Type Hints.
Die Hauptfeatures sind:

- **Schnell**: Sehr hohe Performance, auf Augenhöhe mit **NodeJS** und **Go** (dank Starlette und Pydantic). [Eines der schnellsten verfügbaren Python Frameworks](#performance).

- **schnelle Entwicklung**: Erhöht die Entwicklungsgeschwindigkeit um ca. 200% - 300%. \*
- **weniger Bugs**: Verringert die Chance auf menschliche (durch Entwickler entstandene) Fehler um bis zu 40 %. \*
- **Intuitiv**: Großartige Editor Unterstützung. <abbr title="auch bekannt als auto-complete, autocompletion, IntelliSense">Vervollständigung</abbr> überall. So benötigen Sie weniger Zeit zum debuggen.
- **Einfach**: Mit dem Ziel erstellt einfach zu verwenden und einfach zu Lernen zu sein. Dadurch verbringen Sie weniger Zeit mit dem Lesen der Dokumentation.
- **Kurz**: Minimiert Code Duplizierung. Jede Parameterdeklaration erfüllt mehrere Aufgaben. So entstehen weniger Bugs.
- **Robust**: Erhalten Sie produktionsreifen Code, mit einer automatischen interaktiven Dokumentation.
- **Standards-based**: Basierend auf (und vollständig kompatibel zu) offenen Standards für APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (auch bekannt als Swagger) und <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>\* basierend auf Tests mit einem internen Entwickler Team, welches Produktivanwengungen entwickelt.</small>

## Meinungen

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, das FastAPI der CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Wenn Sie eine <abbr title="Kommandozeileninterface">CLI</abbr> Anwendung erstellen, probieren Sie <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> aus.

**Typer** ist so etwas wie FastAPI's kleiner Bruder und soll das **FastAPI der CLIs** sein. ⌨️ 🚀

## Vorraussetungen

Python 3.6+

FastAPI steht auf den Schultern von Giganten:

- <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> für die Webinteraktionen.
- <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> für die Validierung von Daten.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Für einen produktiven Einsatz benötigen Sie außerdem noch einen ASGI Server, zum Beispiel <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> oder <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## Beispiel

### Erstellen

- Erstellen Sie eine Datei namens `main.py` mit folgendem Inhalt:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>oder verwenden Sie <code>async def</code>...</summary>

Wenn Ihr Code `async` / `await` verwendet, benutzen Sie `async def`:

```Python hl_lines="7 12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**Anmerkung**:

Falls Sie sich unsicher sind, finden Sie weitere Informationen in der _"In a hurry?"_ Sektion <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank"> unter `async` und `await` in der Dokumentation</a>.

</details>

### Ausführen

Starten Sie den Server mit folgendem Befehl

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Mehr über den <code>uvicorn main:app --reload</code> Befehl...</summary>

Der Befehl `uvicorn main:app` bezieht sich auf:

- `uvicorn`: ruft den Uvicorn Webserver auf.
- `main`: die Datei `main.py` (oder das Python Module).
- `app`: das Objekt, welches in der `main.py` in der Zeile `app = FastAPI()` erstellt wurde.
- `--reload`: sorgt dafür, daß der Server nach Veränderungen am Code neugestartet wird. Dies sollte nur während der Entwicklung genutzt werden.

</details>

### Überprüfen

Rufen Sie folgende Seite in Ihrem Browser auf <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Sie werden folgende JSON Antwort sehen:

```JSON
{"item_id": 5, "q": "somequery"}
```

Sie haben bereits eine API, mit folgenden Funktionen, erstellt:

- Empfang von HTTP Anfragen auf den _Pfaden_ `/` und `/items/{item_id}`.
- Beide _Pfade_ nehmen `GET` <em>Operationen</em> (auch bekannt als HTTP _Methoden_) entgegen.
- Der _Pfad_ `/items/{item_id}` hat einen _Pfad Parameter_ `item_id` der vom Typ `int` sein sollte.
- Der _Pfad_ `/items/{item_id}` hat einen optionalen _Query Parameter_ namens `q` der vom Typ `str` sein sollte.

### Interaktive API Dokumentation

Rufen Sie jetzt folgende URL auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie werden eine automatisch erstellte interaktive API Dokumentation (bereitgestellt durch <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) sehen:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API Dokumentation

Wenn Sie jetzt die URL <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> aufrufen, sehen Sie eine alternative Dokumentaion (bereitgestellt durch <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>).

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Bespiel Aktualisierung

Verändern Sie nun die Datei `main.py` um den Body einer `PUT` Anfrage zu empfangen.

Sie deklarieren den Body dazu mit standard Python Typen, Pydantic sei dank.

```Python hl_lines="2  7 8 9 10  23 24 25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Der Server sollte die Änderungen automatisch laden, weil wir `--reload` zum `uvicorn` Befehl hinzugefügt haben.

### Aktualiserung der interaktiven Dokumentation

Rufen Sie jetzt wieder <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> auf.

- Die interaktive API Dokumentation wird automatisch aktualisiert und enthält nun den neuen Body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- Klicken Sie auf den "Try it out" Button. Dieser erlaubt es Ihnen die Parameter auszufüllen, um direkt mit der API zu interagieren.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

- Klicken Sie nun auf den "Execute" Button. Die Benutzeroberfläche wird nun mit Ihrer API kommunizieren, die Parameter sowie den Body senden, die Rückgabewerte empfangen und Ihnen diese anzeigen.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Aktualiserung der alternativen API Dokumentation

Rufen Sie nun erneut <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> auf.

- Die alternative Dokumentation berücksichtigt nun auch den neuen Query Parameter sowie den Body.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Zusammenfassung

Sie deklarieren die Typen von Parametern, dem Body, usw. **einmalig** als Funktionsparameter.

Dies erfolgt mit modernen Standard Python Type Hints.

Sie müssen keine neue Syntax, Methoden oder Klassen einer bestimmten Bibliothek erlernen.

Nur Standard **Python 3.6+**.

Als Beispiel, für einen `int`:

```Python
item_id: int
```

oder für ein komplexes `Item` Modell:

```Python
item: Item
```

...mit dieser einen Deklarierung erhalten Sie:

- Editor Unterstützung, inklusive:
  - Vervollständigung.
  - Typ Überprüfungen.
- Validierung von Daten:
  - Automatische und aussagekräftige Fehlermeldungen, wenn die Daten ungültig sind.
  - Validierung von tief verschachtelten JSON Objekten.
- <abbr title="Auch bekannt als: Serialisierung, Parsen, Marshallisierung">Kovertierung</abbr> von Eingabedaten: Vom Netzwerk zu Python Daten und Typen. Dazu zählen:
  - JSON.
  - Pfad Parameter.
  - Query Parameter.
  - Cookies.
  - Headers.
  - Forms.
  - Files.
- <abbr title="Auch bekannt als: Serialisierung, Parsen, Marshallisierung">Konvertierung</abbr> von Ausgabedaten: konvertieren von Python Daten und Typen zu "Netzwerkdaten" (als JSON):
  - Konvertiert (`str`, `int`, `float`, `bool`, `list`, usw.).
  - `datetime` Objekte.
  - `UUID` Objekte.
  - Datenbank Modelle.
  - ...und vieles mehr.
- automatische interaktive Dokumentation, mit zwei verschiedenen Benutzeroberflächen:
  - Swagger UI.
  - ReDoc.

---

Mit Bezug auf unser vorheriges Beispiel, wird **FastAPI**:

- validieren ob es eine `item_id` in dem Pfad für `GET` und `PUT` Anfragen gibt.
- validieren das `item_id` vom Typ `int` ist für `GET` und `PUT` Anfragen.
  - falls dies nicht der Fall ist, erhält der Client eine hilfreiche und aussagekräftige Fehlermeldung.
- überprüfen ob es einen optionalen Query Parameter mit dem Namen `q` (wie in `http://127.0.0.1:8000/items/foo?q=somequery`) für `GET` Anfragen gibt.
  - da der `q` Parameter mit `= None` deklariert wurde, ist er optional.
  - ohne das `None` wäre er ein erforderlicher Parameter (wie im Body der `PUT` Anfrage).
- bei `PUT` Anfragen an `/items/{item_id}`, wird der Body als JSON eingelesen:
  - es wird überprüft ob das erforderliche Attribut `name` vorhanden und vom Typ `str` ist.
  - es wird überprüft ob das erforderliche Attribut `price` vorhanden und vom Typ `float`ist.
  - es wird überprüft ob das optionale Attribut `is_offer` vorhanden und vom Typ `bool` ist.
  - all dies funktioniert auch bei tief verschachtelten JSON Objekten,
- automatische Konvertierung von und zu JSON
- alles wird im OpenAPI Standard dokumentiert und kann so für verschwiedene Zwecke genutzt werden:
  - interaktive Dokumentationen.
  - Generierung von Client-Librarys für viele Programmiersprachen.
- direktes bereitstellen von 2 interaktiven Dokumentationen per Web.

---

Hiermit haben wir nur an der Oberfläche gekratzt, aber Sie erhalten bereits eine grobe Idee wie alles funktioniert.

Versuchen Sie die folgende Zeile zu ändern:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...von:

```Python
        ... "item_name": item.name ...
```

...zu:

```Python
        ... "item_price": item.price ...
```

...und sehen Sie wie Ihr Editor Ihnen die Attribute und Typen automatisch vervollständigt:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Ein umfassenderes Beispiel mit mehr Funktionen finden Sie im <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Spoiler Warnung**: Das Tutorial - User Guide umfasst folgende Themen:

- Deklaration von **Parametern** von verschiedenen Orten: **Headers**, **Cookies**, **Form Feldern** and **Files**.
- Bestimmung von **Validierungs Einschränkungen** z.B. `maximum_length` oder `regex`.
- Ein sehr mächtiges und einfach zu verwendendes System zur **<abbr title="auch bekannt als Komponenten, Resourcen, Provider, Services, Injectables">Dependency Injection</abbr>**
- Sicherheit und Authentifizierung, mit der Unterstützung von **OAuth2** mit **JWT Tokens** und **HTTP Basic** auth.
- fortschrittliche (aber genauso einfache) Techniken zum deklarieren von **tief verschachtelten JSON Modellen** (dank Pydantic).
- viele extra Funktionen (dank Starlette) zum Beispiel:
  - **WebSockets**
  - **GraphQL**
  - extrem einfache Erstellung von Tests mit `requests` und `pytest`
  - **CORS**
  - **Cookie Sessions**
  - ...und vieles mehr.

## Performance

Unabhängige TechEmpower Benchmarks zeigen das **FastAPI** Anwendungen, die unter Uvicorn laufen
<a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">zu den schnellsten verfügbaren Python Frameworks zählen.</a> und nur geringfügig langsamer als Starlette und Uvicorn selbst sind (diese werden intern von FastAPI verwendet). (\*)

Mehr dazu erfahren Sie unter <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## optionale Abhängigkeiten

Verwendet von Pydantic:

- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - für schnelleres JSON <abbr title="Konvertierung des, durch die Webanfrage erhaltenen, Strings in Python Daten">"parsen"</abbr>.
- <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - für die Validierung von E-Mail Addressen.

Verwendet von Starlette:

- <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - wird für den `TestClient` benötigt.
- <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - wird benötigt falls Sie die `FileResponse` oder `StaticFiles` nutzen wollen.
- <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - wird benötigt falls die standard Template Konfiguration benutzen wollen.
- <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - wird für das <abbr title="converting the string that comes from an HTTP request into Python data">"Parsen"</abbr> von Form Daten verwendet mit `request.form()`.
- <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Wird für die `SessionMiddleware` Unterstützung verwendet.
- <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - wird für Starlette's `SchemaGenerator` verwendet (Sie benötigen es vielleicht nicht für FastAPI).
- <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - wird für die `GraphQLApp` Unterstüzung benötigt.
- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - wird benötigt falls `UJSONResponse` verwendet werden soll.

Verwendet von FastAPI / Starlette:

- <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - der Server der Ihr Programm lädt und bereitstellt.
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - wird benötigt falls `ORJSONResponse` verwendet werden soll..

Sie können alle diese Pakete mit dem Befehl `pip install fastapi[all]` installieren.

## Lizenz

Dieses Projekt ist unter den Bedingungen der MIT Lizenz lizensiert.

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/de"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI-Framework, hohe Performanz, leicht zu lernen, schnell zu entwickeln, produktionsreif</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Testabdeckung">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Paketversion">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Unterstützte Python-Versionen">
</a>
</p>

---

**Dokumentation**: <a href="https://fastapi.tiangolo.com/de" target="_blank">https://fastapi.tiangolo.com/de</a>

**Quellcode**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI ist ein modernes, schnelles (hohe Performanz) Web-Framework zum Erstellen von APIs mit Python, basierend auf Standard-Python-Typhinweisen.

Die wichtigsten Features:

* **Schnell**: Sehr hohe Performanz, auf Augenhöhe mit **NodeJS** und **Go** (dank Starlette und Pydantic). [Eines der schnellsten verfügbaren Python-Frameworks](#performance).
* **Schnell zu entwickeln**: Erhöhen Sie die Geschwindigkeit bei der Entwicklung von Features um etwa 200 % bis 300 %. *
* **Weniger Bugs**: Reduzieren Sie ca. 40 % der menschlich (vom Entwickler) verursachten Fehler. *
* **Intuitiv**: Hervorragende Editor-Unterstützung. <abbr title="auch bekannt als: Auto-Complete, Autocompletion, IntelliSense">Completion</abbr> überall. Weniger Zeit mit Debugging verbringen.
* **Einfach**: Darauf ausgelegt, einfach zu verwenden und zu erlernen. Weniger Zeit mit der Dokumentation verbringen.
* **Kurz**: Code-Duplizierung minimieren. Mehrere Features aus jeder Parameterdeklaration. Weniger Bugs.
* **Robust**: Produktionsreifen Code erhalten. Mit automatischer interaktiver Dokumentation.
* **Standardbasiert**: Basierend auf (und vollständig kompatibel mit) den offenen Standards für APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (früher bekannt als Swagger) und <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Schätzung basierend auf Tests mit einem internen Entwicklungsteam, das Produktionsanwendungen erstellt.</small>

## Sponsoren { #sponsors }

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/de/fastapi-people/#sponsors" class="external-link" target="_blank">Weitere Sponsoren</a>

## Meinungen { #opinions }

„_[...] Ich nutze **FastAPI** derzeit sehr viel. [...] Ich plane sogar, es für alle **ML-Services** meines Teams bei **Microsoft** zu verwenden. Einige davon werden in das Kernprodukt **Windows** integriert und einige in **Office**-Produkte._“

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(Ref.)</small></a></div>

---

„_Wir haben die **FastAPI**-Bibliothek verwendet, um einen **REST**-Server zu starten, der für **Predictions** abgefragt werden kann. [für Ludwig]_“

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin und Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(Ref.)</small></a></div>

---

„_**Netflix** freut sich, die Open-Source-Veröffentlichung unseres Orchestrierungs-Frameworks für **Krisenmanagement** bekannt zu geben: **Dispatch**! [gebaut mit **FastAPI**]_“

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(Ref.)</small></a></div>

---

„_Ich bin hellauf begeistert von **FastAPI**. Es macht so viel Spaß!_“

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a>-Podcast-Moderator</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(Ref.)</small></a></div>

---

„_Ehrlich gesagt, was Sie gebaut haben, wirkt super solide und gepflegt. In vielerlei Hinsicht ist es das, was ich mir für **Hug** gewünscht habe – es ist wirklich inspirierend zu sehen, dass jemand das baut._“

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a>-Ersteller</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(Ref.)</small></a></div>

---

„_Wenn Sie ein **modernes Framework** zum Erstellen von REST-APIs lernen möchten, schauen Sie sich **FastAPI** an [...] Es ist schnell, einfach zu verwenden und leicht zu lernen [...]_“

„_Wir sind für unsere **APIs** auf **FastAPI** umgestiegen [...] Ich denke, es wird Ihnen gefallen [...]_“

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a>-Gründer – <a href="https://spacy.io" target="_blank">spaCy</a>-Ersteller</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(Ref.)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(Ref.)</small></a></div>

---

„_Wenn jemand eine produktionsreife Python-API bauen möchte, würde ich **FastAPI** sehr empfehlen. Es ist **wunderschön entworfen**, **einfach zu benutzen** und **hoch skalierbar**, es ist zu einer **Schlüsselkomponente** unserer API-First-Entwicklungsstrategie geworden und treibt viele Automatisierungen und Services an, wie unseren Virtual TAC Engineer._“

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(Ref.)</small></a></div>

---

## **Typer**, das FastAPI der CLIs { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Wenn Sie eine <abbr title="Command Line Interface – Kommandozeileninterface">CLI</abbr>-App bauen, die im Terminal statt als Web-API verwendet wird, sehen Sie sich <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> an.

**Typer** ist FastAPIs kleiner Bruder. Und es soll das **FastAPI der CLIs** sein. ⌨️ 🚀

## Voraussetzungen { #requirements }

FastAPI steht auf den Schultern von Giganten:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> für die Web-Teile.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> für die Daten-Teile.

## Installation { #installation }

Erstellen und aktivieren Sie eine <a href="https://fastapi.tiangolo.com/de/virtual-environments/" class="external-link" target="_blank">virtuelle Umgebung</a> und installieren Sie dann FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Hinweis**: Stellen Sie sicher, dass Sie `"fastapi[standard]"` in Anführungszeichen setzen, damit es in allen Terminals funktioniert.

## Beispiel { #example }

### Erstellen { #create-it }

Erstellen Sie eine Datei `main.py` mit:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Oder <code>async def</code> verwenden ...</summary>

Wenn Ihr Code `async` / `await` verwendet, nutzen Sie `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Hinweis**:

Wenn Sie es nicht wissen, sehen Sie sich den Abschnitt „In Eile?“ über <a href="https://fastapi.tiangolo.com/de/async/#in-a-hurry" target="_blank">`async` und `await` in der Dokumentation</a> an.

</details>

### Ausführen { #run-it }

Starten Sie den Server mit:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Über den Befehl <code>fastapi dev main.py</code> ...</summary>

Der Befehl `fastapi dev` liest Ihre Datei `main.py`, erkennt die **FastAPI**-App darin und startet einen Server mit <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Standardmäßig startet `fastapi dev` mit aktiviertem Auto-Reload für lokale Entwicklung.

Mehr dazu in der <a href="https://fastapi.tiangolo.com/de/fastapi-cli/" target="_blank">FastAPI-CLI-Dokumentation</a>.

</details>

### Prüfen { #check-it }

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Sie sehen die JSON-Response:

```JSON
{"item_id": 5, "q": "somequery"}
```

Sie haben bereits eine API erstellt, die:

* HTTP-Requests in den _Pfade(n)_ `/` und `/items/{item_id}` empfängt.
* Beide _Pfade_ nehmen `GET`-<em>Operationen</em> (auch bekannt als HTTP-_Methoden_) an.
* Der _Pfad_ `/items/{item_id}` hat einen _Pfad-Parameter_ `item_id`, der ein `int` sein sollte.
* Der _Pfad_ `/items/{item_id}` hat einen optionalen `str`-_Query-Parameter_ `q`.

### Interaktive API-Dokumentation { #interactive-api-docs }

Gehen Sie jetzt zu <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen die automatische interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation { #alternative-api-docs }

Und jetzt gehen Sie zu <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Sie sehen die alternative automatische Dokumentation (bereitgestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Beispiel aktualisieren { #example-upgrade }

Ändern Sie nun die Datei `main.py`, um einen Body von einem `PUT`-Request zu empfangen.

Deklarieren Sie den Body mit Standard-Python-Typen, dank Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Der `fastapi dev`-Server sollte automatisch neu laden.

### Interaktive API-Dokumentation aktualisieren { #interactive-api-docs-upgrade }

Gehen Sie jetzt zu <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Die interaktive API-Dokumentation wird automatisch aktualisiert, einschließlich des neuen Bodys:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klicken Sie auf die Schaltfläche „Try it out“, damit können Sie die Parameter ausfüllen und direkt mit der API interagieren:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klicken Sie dann auf die Schaltfläche „Execute“, die Benutzeroberfläche kommuniziert mit Ihrer API, sendet die Parameter, erhält die Ergebnisse und zeigt sie auf dem Bildschirm an:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API-Dokumentation aktualisieren { #alternative-api-docs-upgrade }

Und jetzt gehen Sie zu <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Die alternative Dokumentation spiegelt ebenfalls den neuen Query-Parameter und den Body wider:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Zusammenfassung { #recap }

Kurz gesagt, Sie deklarieren **einmal** die Typen von Parametern, Body, usw. als Funktionsparameter.

Sie tun das mit modernen Standard-Python-Typen.

Sie müssen keine neue Syntax, Methoden oder Klassen einer bestimmten Bibliothek, usw. lernen.

Einfach Standard-**Python**.

Zum Beispiel für ein `int`:

```Python
item_id: int
```

oder für ein komplexeres `Item`-Modell:

```Python
item: Item
```

... und mit dieser einen Deklaration erhalten Sie:

* Editor-Unterstützung, einschließlich:
    * Completion.
    * Typprüfungen.
* Validierung von Daten:
    * Automatische und klare Fehler, wenn die Daten ungültig sind.
    * Validierung sogar für tief verschachtelte JSON-Objekte.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Eingabedaten: vom Netzwerk zu Python-Daten und -Typen. Lesen aus:
    * JSON.
    * Pfad-Parametern.
    * Query-Parametern.
    * Cookies.
    * Headern.
    * Formularen.
    * Dateien.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Ausgabedaten: Umwandeln von Python-Daten und -Typen in Netzwerkdaten (als JSON):
    * Python-Typen konvertieren (`str`, `int`, `float`, `bool`, `list`, usw.).
    * `datetime`-Objekte.
    * `UUID`-Objekte.
    * Datenbankmodelle.
    * ... und viele mehr.
* Automatische interaktive API-Dokumentation, inklusive 2 alternativen Benutzeroberflächen:
    * Swagger UI.
    * ReDoc.

---

Zurück zum vorherigen Codebeispiel – **FastAPI** wird:

* Validieren, dass es einen `item_id` im Pfad für `GET`- und `PUT`-Requests gibt.
* Validieren, dass der `item_id` vom Typ `int` ist für `GET`- und `PUT`-Requests.
    * Falls nicht, sieht der Client einen hilfreichen, klaren Fehler.
* Prüfen, ob es für `GET`-Requests einen optionalen Query-Parameter namens `q` gibt (wie in `http://127.0.0.1:8000/items/foo?q=somequery`).
    * Da der Parameter `q` mit `= None` deklariert ist, ist er optional.
    * Ohne das `None` wäre er erforderlich (so wie der Body im Fall von `PUT`).
* Für `PUT`-Requests auf `/items/{item_id}` den Body als JSON lesen:
    * Prüfen, dass er ein erforderliches Attribut `name` hat, das ein `str` sein sollte.
    * Prüfen, dass er ein erforderliches Attribut `price` hat, das ein `float` sein muss.
    * Prüfen, dass er ein optionales Attribut `is_offer` hat, das ein `bool` sein sollte, falls vorhanden.
    * All dies funktioniert auch für tief verschachtelte JSON-Objekte.
* Automatisch von und nach JSON konvertieren.
* Alles mit OpenAPI dokumentieren, das verwendet werden kann von:
    * Interaktiven Dokumentationssystemen.
    * Systemen zur automatischen Client-Code-Generierung, für viele Sprachen.
* Direkt 2 interaktive Dokumentations-Weboberflächen bereitstellen.

---

Wir haben hier nur an der Oberfläche gekratzt, aber Sie bekommen bereits eine Vorstellung davon, wie alles funktioniert.

Versuchen Sie, die Zeile zu ändern:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

... von:

```Python
        ... "item_name": item.name ...
```

... zu:

```Python
        ... "item_price": item.price ...
```

... und sehen Sie, wie Ihr Editor die Attribute automatisch vervollständigt und ihre Typen kennt:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Ein vollständigeres Beispiel mit mehr Features finden Sie im <a href="https://fastapi.tiangolo.com/de/tutorial/">das Tutorial – Benutzerhandbuch</a>.

**Spoilerwarnung**: das Tutorial – Benutzerhandbuch umfasst:

* Deklaration von **Parametern** aus verschiedenen Quellen wie: **Header**, **Cookies**, **Formularfelder** und **Dateien**.
* Wie **Validierungs-Constraints** wie `maximum_length` oder `regex` gesetzt werden.
* Ein sehr mächtiges und leicht zu nutzendes System für **<abbr title="auch bekannt als: Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>**.
* Security und Authentifizierung, inklusive Support für **OAuth2** mit **JWT-Token** und **HTTP Basic**-Auth.
* Fortgeschrittene (aber ebenso einfache) Techniken für die Deklaration **tief verschachtelter JSON-Modelle** (dank Pydantic).
* **GraphQL**-Integration mit <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> und anderen Bibliotheken.
* Viele zusätzliche Features (dank Starlette), wie:
    * **WebSockets**
    * extrem einfache Tests auf Basis von HTTPX und `pytest`
    * **CORS**
    * **Cookie-Sessions**
    * ... und mehr.

## Performanz { #performance }

Unabhängige TechEmpower-Benchmarks zeigen, dass **FastAPI**-Anwendungen unter Uvicorn als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks</a> laufen, nur unterhalb von Starlette und Uvicorn selbst (intern von FastAPI verwendet). (*)

Um mehr darüber zu verstehen, sehen Sie den Abschnitt <a href="https://fastapi.tiangolo.com/de/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Abhängigkeiten { #dependencies }

FastAPI hängt von Pydantic und Starlette ab.

### `standard`-Abhängigkeiten { #standard-dependencies }

Wenn Sie FastAPI mit `pip install "fastapi[standard]"` installieren, kommt es mit der `standard`-Gruppe optionaler Abhängigkeiten:

Verwendet von Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> – für E-Mail-Validierung.

Verwendet von Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> – Erforderlich, wenn Sie den `TestClient` verwenden möchten.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> – Erforderlich, wenn Sie die Default-Template-Konfiguration verwenden möchten.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> – Erforderlich, wenn Sie Formular-<abbr title="Konvertieren des Strings eines HTTP-Requests in Python-Daten">„parsing“</abbr> mit `request.form()` unterstützen möchten.

Verwendet von FastAPI:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> – für den Server, der Ihre Anwendung lädt und bereitstellt. Dies umfasst `uvicorn[standard]`, das einige Abhängigkeiten (z. B. `uvloop`) beinhaltet, die für eine Bereitstellung mit hoher Performanz benötigt werden.
* `fastapi-cli[standard]` – um den Befehl `fastapi` bereitzustellen.
    * Dies umfasst `fastapi-cloud-cli`, womit Sie Ihre FastAPI-Anwendung auf <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> deployen können.

### Ohne `standard`-Abhängigkeiten { #without-standard-dependencies }

Wenn Sie die optionalen `standard`-Abhängigkeiten nicht einschließen möchten, können Sie mit `pip install fastapi` statt `pip install "fastapi[standard]"` installieren.

### Ohne `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Wenn Sie FastAPI mit den Standardabhängigkeiten, aber ohne das `fastapi-cloud-cli` installieren möchten, können Sie mit `pip install "fastapi[standard-no-fastapi-cloud-cli]"` installieren.

### Zusätzliche optionale Abhängigkeiten { #additional-optional-dependencies }

Es gibt einige zusätzliche Abhängigkeiten, die Sie installieren möchten.

Zusätzliche optionale Pydantic-Abhängigkeiten:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> – für Settings-Management.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> – für zusätzliche Typen zur Verwendung mit Pydantic.

Zusätzliche optionale FastAPI-Abhängigkeiten:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> – Erforderlich, wenn Sie `ORJSONResponse` verwenden möchten.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> – Erforderlich, wenn Sie `UJSONResponse` verwenden möchten.

## Lizenz { #license }

Dieses Projekt ist unter den Bedingungen der MIT-Lizenz lizenziert.

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
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package-Version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Unterstützte Python-Versionen">
</a>
</p>

---

**Dokumentation**: <a href="https://fastapi.tiangolo.com/de" target="_blank">https://fastapi.tiangolo.com/de</a>

**Quellcode**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI ist ein modernes, schnelles (hoch performantes) Webframework zur Erstellung von APIs mit Python auf Basis von Standard-Python-Typhinweisen.

Seine Schlüssel-Merkmale sind:

* **Schnell**: Sehr hohe Performanz, auf Augenhöhe mit **NodeJS** und **Go** (dank Starlette und Pydantic). [Eines der schnellsten verfügbaren Python-Frameworks](#performance).
* **Schnell zu entwickeln**: Erhöhen Sie die Geschwindigkeit bei der Entwicklung von Features um etwa 200 % bis 300 %. *
* **Weniger Bugs**: Verringern Sie die von Menschen (Entwicklern) verursachten Fehler um etwa 40 %. *
* **Intuitiv**: Hervorragende Editor-Unterstützung. <abbr title="auch bekannt als Auto-Complete, Autovervollständigung, IntelliSense">Code-Vervollständigung</abbr> überall. Weniger Zeit mit Debuggen verbringen.
* **Einfach**: So konzipiert, dass es einfach zu benutzen und zu erlernen ist. Weniger Zeit mit dem Lesen von Dokumentation verbringen.
* **Kurz**: Minimieren Sie die Verdoppelung von Code. Mehrere Features aus jeder Parameterdeklaration. Weniger Bugs.
* **Robust**: Erhalten Sie produktionsreifen Code. Mit automatischer, interaktiver Dokumentation.
* **Standards-basiert**: Basierend auf (und vollständig kompatibel mit) den offenen Standards für APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (früher bekannt als Swagger) und <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Schätzung basierend auf Tests in einem internen Entwicklungsteam, das Produktionsanwendungen erstellt.</small>

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

<a href="https://fastapi.tiangolo.com/de/fastapi-people/#sponsors" class="external-link" target="_blank">Andere Sponsoren</a>

## Meinungen { #opinions }

„_[...] Ich verwende **FastAPI** heutzutage sehr oft. [...] Ich habe tatsächlich vor, es für alle **ML-Services meines Teams bei Microsoft** zu verwenden. Einige davon werden in das Kernprodukt **Windows** und einige **Office**-Produkte integriert._“

<div style="text-align: right; margin-right: 10%;">Kabir Khan – <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(Ref.)</small></a></div>

---

„_Wir haben die **FastAPI**-Bibliothek übernommen, um einen **REST**-Server zu erstellen, der für **Vorhersagen** abgefragt werden kann. [für Ludwig]_“

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, und Sai Sumanth Miryala – <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(Ref.)</small></a></div>

---

„_**Netflix** freut sich, die Open-Source-Veröffentlichung unseres **Krisenmanagement**-Orchestrierung-Frameworks bekannt zu geben: **Dispatch**! [erstellt mit **FastAPI**]_“

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen – <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(Ref.)</small></a></div>

---

„_Ich bin hellauf begeistert von **FastAPI**. Es macht so viel Spaß!_“

<div style="text-align: right; margin-right: 10%;">Brian Okken – <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> Podcast-Host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(Ref.)</small></a></div>

---

„_Ehrlich, was Du gebaut hast, sieht super solide und poliert aus. In vielerlei Hinsicht ist es so, wie ich **Hug** haben wollte – es ist wirklich inspirierend, jemanden so etwas bauen zu sehen._“

<div style="text-align: right; margin-right: 10%;">Timothy Crosley – <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a>-Autor</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(Ref.)</small></a></div>

---

„_Wenn Sie ein **modernes Framework** zum Erstellen von REST-APIs erlernen möchten, schauen Sie sich **FastAPI** an. [...] Es ist schnell, einfach zu verwenden und leicht zu lernen [...]_“

„_Wir haben zu **FastAPI** für unsere **APIs** gewechselt [...] Ich denke, es wird Ihnen gefallen [...]_“

<div style="text-align: right; margin-right: 10%;">Ines Montani – Matthew Honnibal – <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a>-Gründer – <a href="https://spacy.io" target="_blank">spaCy</a>-Autoren</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(Ref.)</small></a> – <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(Ref.)</small></a></div>

---

„_Falls irgendjemand eine Produktions-Python-API erstellen möchte, kann ich **FastAPI** wärmstens empfehlen. Es ist **wunderschön konzipiert**, **einfach zu verwenden** und **hoch skalierbar**; es ist zu einer **Schlüsselkomponente** unserer API-First-Entwicklungsstrategie geworden und treibt viele Automatisierungen und Services an, wie etwa unseren Virtual TAC Engineer._“

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury – <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(Ref.)</small></a></div>

---

## **Typer**, das FastAPI der CLIs { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Wenn Sie eine <abbr title="Command Line Interface – Kommandozeilen-Schnittstelle">CLI</abbr>-Anwendung für das Terminal erstellen, anstelle einer Web-API, schauen Sie sich <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> an.

**Typer** ist die kleine Schwester von FastAPI. Und es soll das **FastAPI der CLIs** sein. ⌨️ 🚀

## Anforderungen { #requirements }

FastAPI steht auf den Schultern von Giganten:

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> für die Webanteile.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> für die Datenanteile.

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

### Erstellung { #create-it }

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
<summary>Oder verwenden Sie <code>async def</code> ...</summary>

Wenn Ihr Code `async` / `await` verwendet, benutzen Sie `async def`:

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

Wenn Sie das nicht kennen, schauen Sie sich den Abschnitt _„In Eile?“_ über <a href="https://fastapi.tiangolo.com/de/async/#in-a-hurry" target="_blank">`async` und `await` in der Dokumentation</a> an.

</details>

### Starten { #run-it }

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
<summary>Was der Befehl <code>fastapi dev main.py</code> macht ...</summary>

Der Befehl `fastapi dev` liest Ihre `main.py`-Datei, erkennt die **FastAPI**-App darin und startet einen Server mit <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Standardmäßig wird `fastapi dev` mit aktiviertem Auto-Reload für die lokale Entwicklung gestartet.

Sie können mehr darüber in der <a href="https://fastapi.tiangolo.com/de/fastapi-cli/" target="_blank">FastAPI CLI Dokumentation</a> lesen.

</details>

### Es testen { #check-it }

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Sie sehen die JSON-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> als:

```JSON
{"item_id": 5, "q": "somequery"}
```

Sie haben bereits eine API erstellt, welche:

* HTTP-<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> auf den _Pfaden_ `/` und `/items/{item_id}` entgegennimmt.
* Beide _Pfade_ nehmen `GET` <em>Operationen</em> (auch bekannt als HTTP-_Methoden_) entgegen.
* Der _Pfad_ `/items/{item_id}` hat einen _Pfad-Parameter_ `item_id`, der ein `int` sein sollte.
* Der _Pfad_ `/items/{item_id}` hat einen optionalen `str`-_Query-Parameter_ `q`.

### Interaktive API-Dokumentation { #interactive-api-docs }

Gehen Sie nun auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen die automatische interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation { #alternative-api-docs }

Und jetzt gehen Sie auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Sie sehen die alternative automatische Dokumentation (bereitgestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Beispiel Aktualisierung { #example-upgrade }

Ändern Sie jetzt die Datei `main.py`, um den <abbr title="Body – Körper, Inhalt: Der eigentliche Inhalt einer Nachricht, nicht die Metadaten">Body</abbr> eines `PUT`-Requests zu empfangen.

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

Gehen Sie jetzt auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Die interaktive API-Dokumentation wird automatisch aktualisiert, einschließlich des neuen Bodys:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klicken Sie auf den Button „Try it out“, damit können Sie die Parameter ausfüllen und direkt mit der API interagieren:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klicken Sie dann auf den Button „Execute“, die Benutzeroberfläche wird mit Ihrer API kommunizieren, sendet die Parameter, holt die Ergebnisse und zeigt sie auf dem Bildschirm an:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API-Dokumentation aktualisieren { #alternative-api-docs-upgrade }

Und jetzt gehen Sie auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Die alternative Dokumentation wird ebenfalls den neuen Query-Parameter und Body widerspiegeln:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Zusammenfassung { #recap }

Zusammengefasst deklarieren Sie **einmal** die Typen von Parametern, Body, usw. als Funktionsparameter.

Das machen Sie mit modernen Standard-Python-Typen.

Sie müssen keine neue Syntax, Methoden oder Klassen einer bestimmten Bibliothek usw. lernen.

Nur Standard-**Python**.

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
    * Code-Vervollständigung.
    * Typprüfungen.
* Validierung von Daten:
    * Automatische und eindeutige Fehler, wenn die Daten ungültig sind.
    * Validierung sogar für tief verschachtelte JSON-Objekte.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Eingabedaten: Aus dem Netzwerk kommend, zu Python-Daten und -Typen. Lesen von:
    * JSON.
    * Pfad-Parametern.
    * Query-Parametern.
    * Cookies.
    * Headern.
    * Formularen.
    * Dateien.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Ausgabedaten: Konvertierung von Python-Daten und -Typen zu Netzwerkdaten (als JSON):
    * Konvertieren von Python-Typen (`str`, `int`, `float`, `bool`, `list`, usw.).
    * `datetime`-Objekte.
    * `UUID`-Objekte.
    * Datenbankmodelle.
    * ... und viele mehr.
* Automatische interaktive API-Dokumentation, einschließlich zwei alternativer Benutzeroberflächen:
    * Swagger UI.
    * ReDoc.

---

Um auf das vorherige Codebeispiel zurückzukommen, **FastAPI** wird:

* Validieren, dass es eine `item_id` im Pfad für `GET`- und `PUT`-Requests gibt.
* Validieren, ob die `item_id` vom Typ `int` für `GET`- und `PUT`-Requests ist.
    * Falls nicht, sieht der Client einen hilfreichen, klaren Fehler.
* Prüfen, ob es einen optionalen Query-Parameter namens `q` (wie in `http://127.0.0.1:8000/items/foo?q=somequery`) für `GET`-Requests gibt.
    * Da der `q`-Parameter mit `= None` deklariert ist, ist er optional.
    * Ohne das `None` wäre er erforderlich (wie der Body im Fall von `PUT`).
* Bei `PUT`-Requests an `/items/{item_id}` den Body als JSON lesen:
    * Prüfen, ob er ein erforderliches Attribut `name` hat, das ein `str` sein muss.
    * Prüfen, ob er ein erforderliches Attribut `price` hat, das ein `float` sein muss.
    * Prüfen, ob er ein optionales Attribut `is_offer` hat, das ein `bool` sein muss, falls vorhanden.
    * All dies würde auch für tief verschachtelte JSON-Objekte funktionieren.
* Automatisch von und nach JSON konvertieren.
* Alles mit OpenAPI dokumentieren, welches verwendet werden kann von:
    * Interaktiven Dokumentationssystemen.
    * Automatisch Client-Code generierenden Systemen für viele Sprachen.
* Zwei interaktive Dokumentations-Weboberflächen direkt bereitstellen.

---

Wir haben nur an der Oberfläche gekratzt, aber Sie bekommen schon eine Vorstellung davon, wie das Ganze funktioniert.

Versuchen Sie, diese Zeile zu ändern:

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

![Editor Unterstützung](https://fastapi.tiangolo.com/img/vscode-completion.png)

Für ein vollständigeres Beispiel, mit weiteren Funktionen, siehe das <a href="https://fastapi.tiangolo.com/de/tutorial/">Tutorial – Benutzerhandbuch</a>.

**Spoiler-Alarm**: Das Tutorial – Benutzerhandbuch enthält:

* Deklaration von **Parametern** von anderen verschiedenen Stellen wie: **Header**, **Cookies**, **Formularfelder** und **Dateien**.
* Wie man **Validierungs-Constraints** wie `maximum_length` oder `regex` setzt.
* Ein sehr leistungsfähiges und einfach zu bedienendes System für **<abbr title="Dependency Injection – Einbringen von Abhängigkeiten: Auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>**.
* Sicherheit und Authentifizierung, einschließlich Unterstützung für **OAuth2** mit **JWT-Tokens** und **HTTP Basic** Authentifizierung.
* Fortgeschrittenere (aber ebenso einfache) Techniken zur Deklaration **tief verschachtelter JSON-Modelle** (dank Pydantic).
* **GraphQL**-Integration mit <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> und anderen Bibliotheken.
* Viele zusätzliche Features (dank Starlette) wie:
    * **WebSockets**
    * extrem einfache Tests auf Basis von HTTPX und `pytest`
    * **CORS**
    * **Cookie-Sessions**
    * ... und mehr.

## Performanz { #performance }

Unabhängige TechEmpower-Benchmarks zeigen **FastAPI**-Anwendungen, die unter Uvicorn laufen, als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks</a>, nur hinter Starlette und Uvicorn selbst (intern von FastAPI verwendet). (*)

Um mehr darüber zu erfahren, siehe den Abschnitt <a href="https://fastapi.tiangolo.com/de/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Abhängigkeiten { #dependencies }

FastAPI hängt von Pydantic und Starlette ab.

### `standard`-Abhängigkeiten { #standard-dependencies }

Wenn Sie FastAPI mit `pip install "fastapi[standard]"` installieren, kommt es mit der `standard`-Gruppe optionaler Abhängigkeiten:

Verwendet von Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> – für E-Mail-Validierung.

Verwendet von Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> – erforderlich, wenn Sie den `TestClient` verwenden möchten.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> – erforderlich, wenn Sie die Default-Template-Konfiguration verwenden möchten.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> – erforderlich, wenn Sie Formulare mittels `request.form()` <abbr title="Konvertieren des Strings, der aus einem HTTP-Request stammt, nach Python-Daten">„parsen“</abbr> möchten.

Verwendet von FastAPI:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> – für den Server, der Ihre Anwendung lädt und bereitstellt. Dies umfasst `uvicorn[standard]`, das einige Abhängigkeiten (z. B. `uvloop`) beinhaltet, die für eine Bereitstellung mit hoher Performanz benötigt werden.
* `fastapi-cli[standard]` – um den `fastapi`-Befehl bereitzustellen.
    * Dies beinhaltet `fastapi-cloud-cli`, das es Ihnen ermöglicht, Ihre FastAPI-Anwendung auf <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> bereitzustellen.

### Ohne `standard`-Abhängigkeiten { #without-standard-dependencies }

Wenn Sie die `standard` optionalen Abhängigkeiten nicht einschließen möchten, können Sie mit `pip install fastapi` statt `pip install "fastapi[standard]"` installieren.

### Ohne `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Wenn Sie FastAPI mit den Standardabhängigkeiten, aber ohne das `fastapi-cloud-cli` installieren möchten, können Sie mit `pip install "fastapi[standard-no-fastapi-cloud-cli]"` installieren.

### Zusätzliche optionale Abhängigkeiten { #additional-optional-dependencies }

Es gibt einige zusätzliche Abhängigkeiten, die Sie installieren möchten.

Zusätzliche optionale Pydantic-Abhängigkeiten:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> – für die Verwaltung von Einstellungen.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> – für zusätzliche Typen zur Verwendung mit Pydantic.

Zusätzliche optionale FastAPI-Abhängigkeiten:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> – erforderlich, wenn Sie `ORJSONResponse` verwenden möchten.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> – erforderlich, wenn Sie `UJSONResponse` verwenden möchten.

## Lizenz { #license }

Dieses Projekt ist unter den Bedingungen der MIT-Lizenz lizenziert.

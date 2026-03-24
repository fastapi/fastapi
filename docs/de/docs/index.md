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
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Testabdeckung">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package-Version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Unterstützte Python-Versionen">
</a>
</p>

---

**Dokumentation**: [https://fastapi.tiangolo.com/de](https://fastapi.tiangolo.com/de)

**Quellcode**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI ist ein modernes, schnelles (hoch performantes) Webframework zur Erstellung von APIs mit Python auf Basis von Standard-Python-Typhinweisen.

Seine Schlüssel-Merkmale sind:

* **Schnell**: Sehr hohe Performanz, auf Augenhöhe mit **NodeJS** und **Go** (dank Starlette und Pydantic). [Eines der schnellsten verfügbaren Python-Frameworks](#performance).
* **Schnell zu entwickeln**: Erhöhen Sie die Geschwindigkeit bei der Entwicklung von Features um etwa 200 % bis 300 %. *
* **Weniger Bugs**: Verringern Sie die von Menschen (Entwicklern) verursachten Fehler um etwa 40 %. *
* **Intuitiv**: Hervorragende Editor-Unterstützung. <dfn title="auch bekannt als Auto-Complete, Autovervollständigung, IntelliSense">Code-Vervollständigung</dfn> überall. Weniger Zeit mit Debuggen verbringen.
* **Einfach**: So konzipiert, dass es einfach zu benutzen und zu erlernen ist. Weniger Zeit mit dem Lesen von Dokumentation verbringen.
* **Kurz**: Minimieren Sie die Verdoppelung von Code. Mehrere Features aus jeder Parameterdeklaration. Weniger Bugs.
* **Robust**: Erhalten Sie produktionsreifen Code. Mit automatischer, interaktiver Dokumentation.
* **Standards-basiert**: Basierend auf (und vollständig kompatibel mit) den offenen Standards für APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (früher bekannt als Swagger) und [JSON Schema](https://json-schema.org/).

<small>* Schätzung basierend auf Tests, die von einem internen Entwicklungsteam durchgeführt wurden, das Produktionsanwendungen erstellt.</small>

## Sponsoren { #sponsors }

<!-- sponsors -->

### Keystone-Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold- und Silber-Sponsoren { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[Andere Sponsoren](https://fastapi.tiangolo.com/de/fastapi-people/#sponsors)

## Meinungen { #opinions }

„_[...] Ich verwende **FastAPI** heutzutage sehr oft. [...] Ich habe tatsächlich vor, es für alle **ML-Services meines Teams bei Microsoft** zu verwenden. Einige davon werden in das Kernprodukt **Windows** und einige **Office**-Produkte integriert._“

<div style="text-align: right; margin-right: 10%;">Kabir Khan – <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(Ref.)</small></a></div>

---

„_Wir haben die **FastAPI**-Bibliothek übernommen, um einen **REST**-Server zu erstellen, der für **Vorhersagen** abgefragt werden kann. [für Ludwig]_“

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, und Sai Sumanth Miryala – <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(Ref.)</small></a></div>

---

„_**Netflix** freut sich, die Open-Source-Veröffentlichung unseres **Krisenmanagement**-Orchestrierung-Frameworks bekannt zu geben: **Dispatch**! [erstellt mit **FastAPI**]_“

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen – <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(Ref.)</small></a></div>

---

„_Ich bin hellauf begeistert von **FastAPI**. Es macht so viel Spaß!_“

<div style="text-align: right; margin-right: 10%;">Brian Okken – <strong>[Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855) Podcast-Host</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(Ref.)</small></a></div>

---

„_Ehrlich, was Du gebaut hast, sieht super solide und poliert aus. In vielerlei Hinsicht ist es so, wie ich **Hug** haben wollte – es ist wirklich inspirierend, jemanden so etwas bauen zu sehen._“

<div style="text-align: right; margin-right: 10%;">Timothy Crosley – <strong>[Hug](https://github.com/hugapi/hug)-Autor</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(Ref.)</small></a></div>

---

„_Wenn Sie ein **modernes Framework** zum Erstellen von REST-APIs erlernen möchten, schauen Sie sich **FastAPI** an. [...] Es ist schnell, einfach zu verwenden und leicht zu lernen [...]_“

„_Wir haben zu **FastAPI** für unsere **APIs** gewechselt [...] Ich denke, es wird Ihnen gefallen [...]_“

<div style="text-align: right; margin-right: 10%;">Ines Montani – Matthew Honnibal – <strong>[Explosion AI](https://explosion.ai)-Gründer – [spaCy](https://spacy.io)-Autoren</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(Ref.)</small></a> – <a href="https://x.com/honnibal/status/1144031421859655680"><small>(Ref.)</small></a></div>

---

„_Falls irgendjemand eine Produktions-Python-API erstellen möchte, kann ich **FastAPI** wärmstens empfehlen. Es ist **wunderschön konzipiert**, **einfach zu verwenden** und **hoch skalierbar**; es ist zu einer **Schlüsselkomponente** unserer API-First-Entwicklungsstrategie geworden und treibt viele Automatisierungen und Services an, wie etwa unseren Virtual TAC Engineer._“

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury – <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(Ref.)</small></a></div>

---

## FastAPI Mini-Dokumentarfilm { #fastapi-mini-documentary }

Es gibt einen [FastAPI-Mini-Dokumentarfilm](https://www.youtube.com/watch?v=mpR8ngthqiE), veröffentlicht Ende 2025, Sie können ihn online ansehen:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini-Dokumentarfilm"></a>

## **Typer**, das FastAPI der CLIs { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Wenn Sie eine <abbr title="Command Line Interface - Kommandozeilen-Schnittstelle">CLI</abbr>-Anwendung für das Terminal erstellen, anstelle einer Web-API, schauen Sie sich [**Typer**](https://typer.tiangolo.com/) an.

**Typer** ist die kleine Schwester von FastAPI. Und es soll das **FastAPI der CLIs** sein. ⌨️ 🚀

## Anforderungen { #requirements }

FastAPI steht auf den Schultern von Giganten:

* [Starlette](https://www.starlette.dev/) für die Webanteile.
* [Pydantic](https://docs.pydantic.dev/) für die Datenanteile.

## Installation { #installation }

Erstellen und aktivieren Sie eine [virtuelle Umgebung](https://fastapi.tiangolo.com/de/virtual-environments/) und installieren Sie dann FastAPI:

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
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Oder verwenden Sie <code>async def</code> ...</summary>

Wenn Ihr Code `async` / `await` verwendet, benutzen Sie `async def`:

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Hinweis**:

Wenn Sie das nicht kennen, schauen Sie sich den Abschnitt _„In Eile?“_ über [`async` und `await` in der Dokumentation](https://fastapi.tiangolo.com/de/async/#in-a-hurry) an.

</details>

### Starten { #run-it }

Starten Sie den Server mit:

<div class="termy">

```console
$ fastapi dev

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
<summary>Über den Befehl <code>fastapi dev</code> ...</summary>

Der Befehl `fastapi dev` liest Ihre `main.py`-Datei, erkennt die **FastAPI**-App darin und startet einen Server mit [Uvicorn](https://www.uvicorn.dev).

Standardmäßig wird `fastapi dev` mit aktiviertem Auto-Reload für die lokale Entwicklung gestartet.

Sie können mehr darüber in der [FastAPI CLI Dokumentation](https://fastapi.tiangolo.com/de/fastapi-cli/) lesen.

</details>

### Es testen { #check-it }

Öffnen Sie Ihren Browser unter [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

Sie sehen die JSON-<abbr title="Response - Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr> als:

```JSON
{"item_id": 5, "q": "somequery"}
```

Sie haben bereits eine API erstellt, welche:

* HTTP-<abbr title="Request - Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> auf den _Pfaden_ `/` und `/items/{item_id}` entgegennimmt.
* Beide _Pfade_ nehmen `GET` <em>Operationen</em> (auch bekannt als HTTP-_Methoden_) entgegen.
* Der _Pfad_ `/items/{item_id}` hat einen _Pfad-Parameter_ `item_id`, der ein `int` sein sollte.
* Der _Pfad_ `/items/{item_id}` hat einen optionalen `str`-_Query-Parameter_ `q`.

### Interaktive API-Dokumentation { #interactive-api-docs }

Gehen Sie nun auf [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Sie sehen die automatische interaktive API-Dokumentation (bereitgestellt von [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation { #alternative-api-docs }

Und jetzt gehen Sie auf [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Sie sehen die alternative automatische Dokumentation (bereitgestellt von [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Beispielaktualisierung { #example-upgrade }

Ändern Sie jetzt die Datei `main.py`, um den <abbr title="Body - Körper, Inhalt: Der eigentliche Inhalt einer Nachricht, nicht die Metadaten">Body</abbr> eines `PUT`-Requests zu empfangen.

Deklarieren Sie den Body mit Standard-Python-Typen, dank Pydantic.

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Der `fastapi dev`-Server sollte automatisch neu laden.

### Interaktive API-Dokumentation aktualisieren { #interactive-api-docs-upgrade }

Gehen Sie jetzt auf [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* Die interaktive API-Dokumentation wird automatisch aktualisiert, einschließlich des neuen Bodys:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klicken Sie auf den Button „Try it out“, damit können Sie die Parameter ausfüllen und direkt mit der API interagieren:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klicken Sie dann auf den Button „Execute“, die Benutzeroberfläche wird mit Ihrer API kommunizieren, die Parameter senden, die Ergebnisse erhalten und sie auf dem Bildschirm anzeigen:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API-Dokumentation aktualisieren { #alternative-api-docs-upgrade }

Und jetzt gehen Sie auf [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

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
    * Vervollständigung.
    * Typprüfungen.
* Validierung von Daten:
    * Automatische und eindeutige Fehler, wenn die Daten ungültig sind.
    * Validierung sogar für tief verschachtelte JSON-Objekte.
* <dfn title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</dfn> von Eingabedaten: Aus dem Netzwerk kommend, zu Python-Daten und -Typen. Lesen von:
    * JSON.
    * Pfad-Parametern.
    * Query-Parametern.
    * Cookies.
    * Headern.
    * Formularen.
    * Dateien.
* <dfn title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</dfn> von Ausgabedaten: Konvertierung von Python-Daten und -Typen zu Netzwerkdaten (als JSON):
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
* Ein sehr leistungsfähiges und einfach zu bedienendes System für **<dfn title="auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</dfn>**.
* Sicherheit und Authentifizierung, einschließlich Unterstützung für **OAuth2** mit **JWT-Tokens** und **HTTP Basic** Authentifizierung.
* Fortgeschrittenere (aber ebenso einfache) Techniken zur Deklaration **tief verschachtelter JSON-Modelle** (dank Pydantic).
* **GraphQL**-Integration mit [Strawberry](https://strawberry.rocks) und anderen Bibliotheken.
* Viele zusätzliche Features (dank Starlette) wie:
    * **WebSockets**
    * extrem einfache Tests auf Basis von HTTPX und `pytest`
    * **CORS**
    * **Cookie-Sessions**
    * ... und mehr.

### Ihre App deployen (optional) { #deploy-your-app-optional }

Optional können Sie Ihre FastAPI-App in die [FastAPI Cloud](https://fastapicloud.com) deployen, gehen Sie und treten Sie der Warteliste bei, falls noch nicht geschehen. 🚀

Wenn Sie bereits ein **FastAPI Cloud**-Konto haben (wir haben Sie von der Warteliste eingeladen 😉), können Sie Ihre Anwendung mit einem einzigen Befehl deployen.

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Das war’s! Jetzt können Sie unter dieser URL auf Ihre App zugreifen. ✨

#### Über FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** wird vom selben Autor und Team hinter **FastAPI** entwickelt.

Es vereinfacht den Prozess des **Erstellens**, **Deployens** und **Zugreifens** auf eine API mit minimalem Aufwand.

Es bringt die gleiche **Developer-Experience** beim Erstellen von Apps mit FastAPI auch zum **Deployment** in der Cloud. 🎉

FastAPI Cloud ist der Hauptsponsor und Finanzierer der *FastAPI and friends* Open-Source-Projekte. ✨

#### Bei anderen Cloudanbietern deployen { #deploy-to-other-cloud-providers }

FastAPI ist Open Source und basiert auf Standards. Sie können FastAPI-Apps bei jedem Cloudanbieter Ihrer Wahl deployen.

Folgen Sie den Anleitungen Ihres Cloudanbieters, um FastAPI-Apps dort bereitzustellen. 🤓

## Performanz { #performance }

Unabhängige TechEmpower-Benchmarks zeigen **FastAPI**-Anwendungen, die unter Uvicorn laufen, als [eines der schnellsten verfügbaren Python-Frameworks](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), nur hinter Starlette und Uvicorn selbst (intern von FastAPI verwendet). (*)

Um mehr darüber zu erfahren, siehe den Abschnitt [Benchmarks](https://fastapi.tiangolo.com/de/benchmarks/).

## Abhängigkeiten { #dependencies }

FastAPI hängt von Pydantic und Starlette ab.

### `standard`-Abhängigkeiten { #standard-dependencies }

Wenn Sie FastAPI mit `pip install "fastapi[standard]"` installieren, kommt es mit der `standard`-Gruppe optionaler Abhängigkeiten:

Verwendet von Pydantic:

* [`email-validator`](https://github.com/JoshData/python-email-validator) – für E-Mail-Validierung.

Verwendet von Starlette:

* [`httpx`](https://www.python-httpx.org) – erforderlich, wenn Sie den `TestClient` verwenden möchten.
* [`jinja2`](https://jinja.palletsprojects.com) – erforderlich, wenn Sie die Default-Template-Konfiguration verwenden möchten.
* [`python-multipart`](https://github.com/Kludex/python-multipart) – erforderlich, wenn Sie Formulare mittels `request.form()` <dfn title="Konvertieren des Strings, der aus einem HTTP-Request stammt, nach Python-Daten">„parsen“</dfn> möchten.

Verwendet von FastAPI:

* [`uvicorn`](https://www.uvicorn.dev) – für den Server, der Ihre Anwendung lädt und bereitstellt. Dies umfasst `uvicorn[standard]`, das einige Abhängigkeiten (z. B. `uvloop`) beinhaltet, die für eine Bereitstellung mit hoher Performanz benötigt werden.
* `fastapi-cli[standard]` – um den `fastapi`-Befehl bereitzustellen.
    * Dies beinhaltet `fastapi-cloud-cli`, das es Ihnen ermöglicht, Ihre FastAPI-Anwendung auf [FastAPI Cloud](https://fastapicloud.com) bereitzustellen.

### Ohne `standard`-Abhängigkeiten { #without-standard-dependencies }

Wenn Sie die `standard` optionalen Abhängigkeiten nicht einschließen möchten, können Sie mit `pip install fastapi` statt `pip install "fastapi[standard]"` installieren.

### Ohne `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Wenn Sie FastAPI mit den Standardabhängigkeiten, aber ohne das `fastapi-cloud-cli` installieren möchten, können Sie mit `pip install "fastapi[standard-no-fastapi-cloud-cli]"` installieren.

### Zusätzliche optionale Abhängigkeiten { #additional-optional-dependencies }

Es gibt einige zusätzliche Abhängigkeiten, die Sie installieren möchten.

Zusätzliche optionale Pydantic-Abhängigkeiten:

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) – für die Verwaltung von Einstellungen.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) – für zusätzliche Typen zur Verwendung mit Pydantic.

Zusätzliche optionale FastAPI-Abhängigkeiten:

* [`orjson`](https://github.com/ijl/orjson) – erforderlich, wenn Sie `ORJSONResponse` verwenden möchten.
* [`ujson`](https://github.com/esnme/ultrajson) – erforderlich, wenn Sie `UJSONResponse` verwenden möchten.

## Lizenz { #license }

Dieses Projekt ist unter den Bedingungen der MIT-Lizenz lizenziert.

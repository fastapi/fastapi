# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI Framework, hochperformant, leicht zu erlernen, schnell zu programmieren, einsatzbereit</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package-Version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Unterstützte Python-Versionen">
</a>
</p>

---

**Dokumentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Quellcode**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI ist ein modernes, schnelles (hoch performantes) Webframework zur Erstellung von APIs mit Python auf Basis von Standard-Python-Typhinweisen.

Seine Schlüssel-Merkmale sind:

* **Schnell**: Sehr hohe Leistung, auf Augenhöhe mit **NodeJS** und **Go** (Dank Starlette und Pydantic). [Eines der schnellsten verfügbaren Python-Frameworks](#performanz).

* **Schnell zu programmieren**: Erhöhen Sie die Geschwindigkeit bei der Entwicklung von Funktionen um etwa 200 % bis 300 %. *
* **Weniger Bugs**: Verringern Sie die von Menschen (Entwicklern) verursachten Fehler um etwa 40 %. *
* **Intuitiv**: Exzellente Editor-Unterstützung. <abbr title="auch bekannt als Autovervollständigung, Autocompletion, IntelliSense">Code-Vervollständigung</abbr> überall. Weniger Debuggen.
* **Einfach**: So konzipiert, dass es einfach zu benutzen und zu erlernen ist. Weniger Zeit für das Lesen der Dokumentation.
* **Kurz**: Minimieren Sie die Verdoppelung von Code. Mehrere Funktionen aus jeder Parameterdeklaration. Weniger Bugs.
* **Robust**: Erhalten Sie produktionsreifen Code. Mit automatischer, interaktiver Dokumentation.
* **Standards-basiert**: Basierend auf (und vollständig kompatibel mit) den offenen Standards für APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (früher bekannt als Swagger) und <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Schätzung auf Basis von Tests in einem internen Entwicklungsteam, das Produktionsanwendungen erstellt.</small>

## Sponsoren

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

<a href="https://fastapi.tiangolo.com/de/fastapi-people/#sponsoren" class="external-link" target="_blank">Andere Sponsoren</a>

## Meinungen

„_[...] Ich verwende **FastAPI** heutzutage sehr oft. [...] Ich habe tatsächlich vor, es für alle **ML-Dienste meines Teams bei Microsoft** zu verwenden. Einige davon werden in das Kernprodukt **Windows** und einige **Office**-Produkte integriert._“

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(Ref)</small></a></div>

---

„_Wir haben die **FastAPI**-Bibliothek genommen, um einen **REST**-Server zu erstellen, der abgefragt werden kann, um **Vorhersagen** zu erhalten. [für Ludwig]_“

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, und Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(Ref)</small></a></div>

---

„_**Netflix** freut sich, die Open-Source-Veröffentlichung unseres **Krisenmanagement**-Orchestrierung-Frameworks bekannt zu geben: **Dispatch**! [erstellt mit **FastAPI**]_“

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(Ref)</small></a></div>

---

„_Ich bin überglücklich mit **FastAPI**. Es macht so viel Spaß!_“

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>Host des <a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> Podcast</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(Ref)</small></a></div>

---

„_Ehrlich, was Du gebaut hast, sieht super solide und poliert aus. In vielerlei Hinsicht ist es so, wie ich **Hug** haben wollte – es ist wirklich inspirierend, jemanden so etwas bauen zu sehen._“

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>Autor von <a href="https://www.hug.rest/" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(Ref)</small></a></div>

---

„_Wenn Sie ein **modernes Framework** zum Erstellen von REST-APIs erlernen möchten, schauen Sie sich **FastAPI** an. [...] Es ist schnell, einfach zu verwenden und leicht zu erlernen [...]_“

„_Wir haben zu **FastAPI** für unsere **APIs** gewechselt [...] Ich denke, es wird Ihnen gefallen [...]_“

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Gründer von <a href="https://explosion.ai" target="_blank">Explosion AI</a> - Autoren von <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(Ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(Ref)</small></a></div>

---

„_Falls irgendjemand eine Produktions-Python-API erstellen möchte, kann ich **FastAPI** wärmstens empfehlen. Es ist **wunderschön konzipiert**, **einfach zu verwenden** und **hoch skalierbar**; es ist zu einer **Schlüsselkomponente** in unserer API-First-Entwicklungsstrategie geworden und treibt viele Automatisierungen und Dienste an, wie etwa unseren virtuellen TAC-Ingenieur._“

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(Ref)</small></a></div>

---

## **Typer**, das FastAPI der CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Wenn Sie eine <abbr title="Command Line Interface – Kommandozeilen-Schnittstelle">CLI</abbr>-Anwendung für das Terminal erstellen, anstelle einer Web-API, schauen Sie sich <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> an.

**Typer** ist die kleine Schwester von FastAPI. Und es soll das **FastAPI der CLIs** sein. ⌨️ 🚀

## Anforderungen

FastAPI steht auf den Schultern von Giganten:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> für die Webanteile.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> für die Datenanteile.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Sie benötigen außerdem einen <abbr title="Asynchronous Server Gateway Interface – Asynchrone Server-Verbindungsschnittstelle">ASGI</abbr>-Server. Für die Produktumgebung beispielsweise <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> oder <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Beispiel

### Erstellung

* Erstellen Sie eine Datei `main.py` mit:

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

**Anmerkung**:

Wenn Sie das nicht kennen, schauen Sie sich den Abschnitt _„In Eile?“_ über <a href="https://fastapi.tiangolo.com/de/async/#in-eile" target="_blank">`async` und `await` in der Dokumentation</a> an.
</details>

### Starten

Führen Sie den Server aus:

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
<summary>Was macht der Befehl <code>uvicorn main:app --reload</code> ...</summary>

Der Befehl `uvicorn main:app` bezieht sich auf:

* `main`: die Datei `main.py` (das Python-„Modul“).
* `app`: das Objekt, das innerhalb von `main.py` mit der Zeile `app = FastAPI()` erzeugt wurde.
* `--reload`: lässt den Server nach Codeänderungen neu starten. Tun Sie das nur während der Entwicklung.

</details>

### Testen

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Sie erhalten die JSON-Response:

```JSON
{"item_id": 5, "q": "somequery"}
```

Damit haben Sie bereits eine API erstellt, welche:

* HTTP-Anfragen auf den _Pfaden_ `/` und `/items/{item_id}` entgegennimmt.
* Beide _Pfade_ erhalten `GET` <em>Operationen</em> (auch bekannt als HTTP _Methoden_).
* Der _Pfad_ `/items/{item_id}` hat einen _Pfadparameter_ `item_id`, der ein `int` sein sollte.
* Der _Pfad_ `/items/{item_id}` hat einen optionalen `str` _Query Parameter_ `q`.

### Interaktive API-Dokumentation

Gehen Sie nun auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen die automatische interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation

Gehen Sie jetzt auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Sie sehen die alternative automatische Dokumentation (bereitgestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Beispiel Aktualisierung

Ändern Sie jetzt die Datei `main.py`, um den <abbr title="Body – Körper, Inhalt: Der eigentliche Inhalt einer Nachricht, nicht die Metadaten">Body</abbr> einer `PUT`-Anfrage zu empfangen.

Deklarieren Sie den Body mithilfe von Standard-Python-Typen, dank Pydantic.

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

Der Server sollte automatisch neu geladen werden (weil Sie oben `--reload` zum Befehl `uvicorn` hinzugefügt haben).

### Aktualisierung der interaktiven API-Dokumentation

Gehen Sie jetzt auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Die interaktive API-Dokumentation wird automatisch aktualisiert, einschließlich des neuen Bodys:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klicken Sie auf die Taste „Try it out“, damit können Sie die Parameter ausfüllen und direkt mit der API interagieren:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klicken Sie dann auf die Taste „Execute“, die Benutzeroberfläche wird mit Ihrer API kommunizieren, sendet die Parameter, holt die Ergebnisse und zeigt sie auf dem Bildschirm an:

![Swagger UI Interaktion](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Aktualisierung der alternativen API-Dokumentation

Und nun gehen Sie auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Die alternative Dokumentation wird ebenfalls den neuen Abfrageparameter und -inhalt widerspiegeln:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Zusammenfassung

Zusammengefasst deklarieren Sie **einmal** die Typen von Parametern, Body, etc. als Funktionsparameter.

Das machen Sie mit modernen Standard-Python-Typen.

Sie müssen keine neue Syntax, Methoden oder Klassen einer bestimmten Bibliothek usw. lernen.

Nur Standard-**Python+**.

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
    * Validierung auch für tief verschachtelte JSON-Objekte.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Eingabedaten: Aus dem Netzwerk kommend, zu Python-Daten und -Typen. Lesen von:
    * JSON.
    * Pfad-Parametern.
    * Abfrage-Parametern.
    * Cookies.
    * Header-Feldern.
    * Formularen.
    * Dateien.
* <abbr title="auch bekannt als: Serialisierung, Parsen, Marshalling">Konvertierung</abbr> von Ausgabedaten: Konvertierung von Python-Daten und -Typen zu Netzwerkdaten (als JSON):
    * Konvertieren von Python-Typen (`str`, `int`, `float`, `bool`, `list`, usw.).
    * `Datetime`-Objekte.
    * `UUID`-Objekte.
    * Datenbankmodelle.
    * ... und viele mehr.
* Automatische interaktive API-Dokumentation, einschließlich 2 alternativer Benutzeroberflächen:
    * Swagger UI.
    * ReDoc.

---

Um auf das vorherige Codebeispiel zurückzukommen, **FastAPI** wird:

* Überprüfen, dass es eine `item_id` im Pfad für `GET`- und `PUT`-Anfragen gibt.
* Überprüfen, ob die `item_id` vom Typ `int` für `GET`- und `PUT`-Anfragen ist.
    * Falls nicht, wird dem Client ein nützlicher, eindeutiger Fehler angezeigt.
* Prüfen, ob es einen optionalen Abfrageparameter namens `q` (wie in `http://127.0.0.1:8000/items/foo?q=somequery`) für `GET`-Anfragen gibt.
    * Da der `q`-Parameter mit `= None` deklariert ist, ist er optional.
    * Ohne das `None` wäre er erforderlich (wie der Body im Fall von `PUT`).
* Bei `PUT`-Anfragen an `/items/{item_id}` den Body als JSON lesen:
    * Prüfen, ob er ein erforderliches Attribut `name` hat, das ein `str` sein muss.
    * Prüfen, ob er ein erforderliches Attribut `price` hat, das ein `float` sein muss.
    * Prüfen, ob er ein optionales Attribut `is_offer` hat, das ein `bool` sein muss, falls vorhanden.
    * All dies würde auch für tief verschachtelte JSON-Objekte funktionieren.
* Automatisch von und nach JSON konvertieren.
* Alles mit OpenAPI dokumentieren, welches verwendet werden kann von:
    * Interaktiven Dokumentationssystemen.
    * Automatisch Client-Code generierenden Systemen für viele Sprachen.
* Zwei interaktive Dokumentation-Webschnittstellen direkt zur Verfügung stellen.

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

... und sehen Sie, wie Ihr Editor die Attribute automatisch ausfüllt und ihre Typen kennt:

![Editor Unterstützung](https://fastapi.tiangolo.com/img/vscode-completion.png)

Für ein vollständigeres Beispiel, mit weiteren Funktionen, siehe das <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Benutzerhandbuch</a>.

**Spoiler-Alarm**: Das Tutorial - Benutzerhandbuch enthält:

* Deklaration von **Parametern** von anderen verschiedenen Stellen wie: **Header-Felder**, **Cookies**, **Formularfelder** und **Dateien**.
* Wie man **Validierungseinschränkungen** wie `maximum_length` oder `regex` setzt.
* Ein sehr leistungsfähiges und einfach zu bedienendes System für **<abbr title="Dependency Injection – Einbringen von Abhängigkeiten: Auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>**.
* Sicherheit und Authentifizierung, einschließlich Unterstützung für **OAuth2** mit **JWT-Tokens** und **HTTP-Basic**-Authentifizierung.
* Fortgeschrittenere (aber ebenso einfache) Techniken zur Deklaration **tief verschachtelter JSON-Modelle** (dank Pydantic).
* **GraphQL** Integration mit <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> und anderen Bibliotheken.
* Viele zusätzliche Funktionen (dank Starlette) wie:
    * **WebSockets**
    * extrem einfache Tests auf Basis von `httpx` und `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ... und mehr.

## Performanz

Unabhängige TechEmpower-Benchmarks zeigen **FastAPI**-Anwendungen, die unter Uvicorn laufen, als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks</a>, nur noch hinter Starlette und Uvicorn selbst (intern von FastAPI verwendet).

Um mehr darüber zu erfahren, siehe den Abschnitt <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Optionale Abhängigkeiten

Wird von Pydantic verwendet:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - für E-Mail-Validierung.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - für die Verwaltung von Einstellungen.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - für zusätzliche Typen, mit Pydantic zu verwenden.

Wird von Starlette verwendet:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - erforderlich, wenn Sie den `TestClient` verwenden möchten.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - erforderlich, wenn Sie die Standardkonfiguration für Templates verwenden möchten.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - erforderlich, wenn Sie Formulare mittels `request.form()` <abbr title="Konvertieren des Strings, der aus einer HTTP-Anfrage stammt, nach Python-Daten">„parsen“</abbr> möchten.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - erforderlich für `SessionMiddleware` Unterstützung.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - erforderlich für Starlette's `SchemaGenerator` Unterstützung (Sie brauchen das wahrscheinlich nicht mit FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - erforderlich, wenn Sie `UJSONResponse` verwenden möchten.

Wird von FastAPI / Starlette verwendet:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - für den Server, der Ihre Anwendung lädt und serviert.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - erforderlich, wenn Sie `ORJSONResponse` verwenden möchten.

Sie können diese alle mit `pip install "fastapi[all]"` installieren.

## Lizenz

Dieses Projekt ist unter den Bedingungen der MIT-Lizenz lizenziert.

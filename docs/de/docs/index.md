<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, hochperformant, leicht zu erlernen, schnell zu programmieren, einsatzbereit</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Dokumentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Quellcode**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI ist ein modernes, schnelles (High-Performance) Web-Framework zur Erstellung von APIs mit Python 3.6+ auf Basis von Python type hints.
Die Haupteigenschaften sind:

* **Schnell**: Sehr hohe Leistung, auf dem Niveau von **NodeJS** und **Go** (Dank an Starlette und Pydantic) [Eines der schnellsten verfügbaren Python-Frameworks](#performance).

* **Schnell zu programmieren**: Erhöhen Sie die Geschwindigkeit bei der Entwicklung von Funktionen um etwa 200% bis 300%. *
* **Weniger Bugs**: Reduzieren Sie etwa 40% der von Menschen (Entwicklern) verursachten Fehler. *
* **Intuitiv**: Großartige Editorunterstützung. <abbr title="auch bekannt als Autovervollständigung, Autocompletion, IntelliSense">Vervollständigung</abbr> überall. Weniger Debuggen.
* **Einfach**: Entworfen, um einfach zu bedienen und zu erlernen zu sein. Weniger Zeit für das Lesen von Dokumentationen.
* **Kurz**: Minimieren Sie Code-Duplizierung. Mehrere Funktionen aus jeder Parameterdeklaration. Weniger Bugs.
* **Robust**: Erhalten Sie produktionsreifen Code. Mit automatischer interaktiver Dokumentation.
* **Standardbasiert**: Basierend auf (und vollständig kompatibel mit) den offenen Standards für APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (früher bekannt als Swagger) und <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Andere Sponsors</a>

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

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, the FastAPI of CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

If you are building a <abbr title="Command Line Interface">CLI</abbr> app to be used in the terminal instead of a web API, check out <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** ist das kleine Schwesterchen von FastAPI. Und es soll die **FastAPI der CLIs** sein. ⌨️ 🚀

## Anforderungen

Python 3.6+

FastAPI basiert auf den Projekten:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> für die Webteile.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> für die Datenteile.

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Sie benötigen außerdem einen ASGI-Server, für die Produktivumgebung beispielsweise <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> oder <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Beispiel

### Erstellung

* Erstellen Sie eine Datei `main.py` mit:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Oder verwende <code>async def</code>...</summary>

Wenn Ihr Code `async` / `await` verwendet, benutzen Sie `async def`:

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Anmerkung**:

Wenn Sie es nicht wissen, lesen Sie den Abschnitt _"In a hurry?"_ über <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` und `await` in der Dokumentation</a>.
</details>

### Starten

Führen Sie den Server mit aus:

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
<summary>Über den Befehl <code>uvicorn main:app --reload</code>...</summary>

Der Befehl `uvicorn main:app` bezieht sich auf:

* `main`: die Datei `main.py` (das Python-"Modul").
* `app`: das Objekt, das innerhalb von `main.py` mit der Zeile `app = FastAPI()` erzeugt wurde.
* `--reload`: lässt den Server nach Codeänderungen neu starten. Tun Sie dies nur während der Entwicklung.

</details>

### Testen

Öffnen Sie Ihren Browser unter <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Sie erhalten die JSON-Rückmeldung:

```JSON
{"item_id": 5, "q": "somequery"}
```

Damit haben Sie bereits eine API erstellt:

* Empfängt HTTP-Anfragen in den _Pfaden_ `/` und `/items/{item_id}`.
* Beide _Pfade_ nehmen `GET` <em>Operationen</em> (auch bekannt als HTTP _Methoden_).
* Der _Pfad_ `/items/{item_id}` hat einen _Pfadparameter_ `item_id`, der ein `int` sein sollte.
* Der _Pfad_ `/items/{item_id}` hat einen optionalen `str` _query Parameter_ `q`.

### Interaktive API-Dokumentation

Gehen Sie nun auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen dann die automatische interaktive API-Dokumentation (bereitgestellt von <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API-Dokumentation

Und nun gehen Sie auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Sie sehen dann die alternative automatische Dokumentation (bereitgestellt von <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Beispiel Upgrade

Ändern Sie nun die Datei `main.py`, um einen Body von einer `PUT`-Anfrage zu erhalten.

Deklarieren Sie den Body mit Standard-Python-Typen, dank Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Der Server sollte automatisch neu geladen werden (weil Sie oben `--reload` zum Befehl `uvicorn` hinzugefügt haben).

### Upgrade der interaktiven API-Dokumentation

Gehen Sie nun auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Die interaktive API-Dokumentation wird automatisch aktualisiert, einschließlich des neuen Body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klicken Sie auf die Taste "Try it out", damit können Sie die Parameter ausfüllen und direkt mit der API interagieren:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klicken Sie dann auf die Taste "Execute", die Benutzeroberfläche kommuniziert mit Ihrer API, sendet die Parameter, holt die Ergebnisse ab und zeigt sie auf dem Bildschirm an:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Upgrade der alternativen API-Dokumentation

Und nun gehen Sie auf <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Die alternative Dokumentation wird auch den neuen Abfrageparameter und -inhalt widerspiegeln:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Zusammenfassung

Zusammengefasst deklarieren Sie **einmal** die Typen von Parametern, Body, etc. als Funktionsparameter.

Das machen Sie mit modernen Standard-Python-Typen.

Sie müssen keine neue Syntax, die Methoden oder Klassen einer bestimmten Bibliothek usw. lernen.

Nur Standard **Python 3.6+**.

Zum Beispiel für einen `int`:

```Python
item_id: int
```

oder für ein komplexeres `Item`-Modell:

```Python
item: Item
```

...und mit dieser einen Anweisung erhalten Sie:

* Editor-Unterstützung, einschließlich:
  * Vervollständigung.
  * Typprüfungen.
* Validierung von Daten:
  * Automatische und eindeutige Fehler, wenn die Daten ungültig sind.
  * Validierung auch für tief verschachtelte JSON-Objekte.
* <abbr title="auch bekannt als: serialization, parsing, marshalling">Konvertierung</abbr> von Eingabedaten: aus dem Netzwerk kommend in Python-Daten und -Typen. Lesen von:
  * JSON.
  * Pfad-Parameter.
  * Abfrage-Parameter.
  * Cookies.
  * Kopfzeilen.
  * Formulare.
  * Dateien.
* <abbr title="auch bekannt als: serialization, parsing, marshalling">Konvertierung</abbr> von Ausgabedaten: Konvertierung von Python-Daten und -Typen in Netzwerkdaten (als JSON):
  * Konvertieren von Python-Typen (`str`, `int`, `float`, `bool`, `list`, etc).
  * `Datetime`-Objekte.
  * `UUID`-Objekte.
  * Datenbank-Modelle.
  * ...und viele mehr.
* Automatische interaktive API-Dokumentation, einschließlich 2 alternativer Benutzeroberflächen:
  * Swagger UI.
  * ReDoc.

---

Um auf das vorherige Codebeispiel zurückzukommen, **FastAPI** wird:

* Überprüfen Sie, dass es eine `item_id` im Pfad für `GET`- und `PUT`-Anfragen gibt.
* Überprüfen Sie, ob die `item_id` vom Typ `int` für `GET`- und `PUT`-Anfragen ist.
  * Ist dies nicht der Fall, wird dem Client ein nützlicher, eindeutiger Fehler angezeigt.
* Prüfen Sie, ob es einen optionalen Abfrageparameter namens `q` (wie in `http://127.0.0.1:8000/items/foo?q=somequery`) für `GET`-Anfragen gibt.
  * Da der `q`-Parameter mit `= None` deklariert ist, ist er optional.
  * Ohne das `None` wäre er erforderlich (wie der Body im Fall von `PUT`).
* Bei `PUT`-Anfragen an `/items/{item_id}` wird der Body als JSON gelesen:
  * Prüfen Sie, ob er ein erforderliches Attribut `name` hat, das ein `str` sein sollte.
  * Prüfen Sie, ob er ein erforderliches Attribut `price` hat, das ein `float` sein muss.
  * Prüfen Sie, ob es ein optionales Attribut `is_offer` hat, das ein `bool` sein sollte, falls vorhanden.
  * All dies würde auch für tief verschachtelte JSON-Objekte funktionieren.
* Konvertiert automatisch von und nach JSON.
* Alles mit OpenAPI dokumentieren, das kann von:
  * Interaktive Dokumentationssysteme.
  * Automatische Client-Code-Generierung, für viele Sprachen.
* 2 interaktive Dokumentation-Webschnittstellen direkt zur Verfügung stellen.

---

Wir haben nur an der Oberfläche gekratzt, aber Sie bekommen schon eine Vorstellung davon, wie das Ganze funktioniert.

Versuchen Sie, diese Zeile zu ändern mit:

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

...und sehen Sie, wie Ihr Editor die Attribute automatisch ausfüllt und ihre Typen kennt:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Ein vollständigeres Beispiel mit weiteren Funktionen finden Sie im <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Benutzerhandbuch</a>.

**Spoiler-Alarm**: Das Tutorial - Benutzerhandbuch enthält:

* Deklaration von **Parametern** von anderen verschiedenen Stellen wie: **Kopfzeilen**, **Cookies**, **Formularfelder** und **Dateien**.
* Wie man **Validierungseinschränkungen** als `maximum_length` oder `regex` setzt.
* Ein sehr leistungsfähiges und einfach zu bedienendes **<abbr title="auch bekannt als Komponenten, Ressourcen, Provider, Services, Injectables">Dependency Injection</abbr>** System.
* Sicherheit und Authentifizierung, einschließlich Unterstützung für **OAuth2** mit **JWT-Tokens** und **HTTP Basic** auth.
* Fortgeschrittenere (aber ebenso einfache) Techniken zur Deklaration **tief verschachtelter JSON-Modelle** (Dank an Pydantic).
* Viele zusätzliche Funktionen (dank Starlette) wie:
  * **WebSockets**
  * **GraphQL**
  * extrem einfache Tests auf Basis von `requests` und `pytest`
  * **CORS**
  * **Cookie Sessions**
  * ...und mehr.

## Performance

Unabhängige TechEmpower-Benchmarks zeigen **FastAPI**-Anwendungen, die unter Uvicorn laufen, als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks</a>, nur noch hinter Starlette und Uvicorn selbst (intern von FastAPI verwendet). (*)

Um mehr darüber zu erfahren, lesen Sie den Abschnitt <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Optionale Abhängigkeiten

Wird von Pydantic verwendet:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - für schnelleres JSON <abbr title="Konvertieren des Strings, der von einer HTTP-Anfrage kommt, in Python-Daten">"Parsen"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - für die E-Mail-Validierung.

Wird von Starlette verwendet:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Erforderlich, wenn Sie den `TestClient` verwenden wollen.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Erforderlich, wenn Sie `FileResponse` oder `StaticFiles` verwenden wollen.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Erforderlich, wenn Sie die Vorlagen Konfiguration verwenden möchten.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Erforderlich, wenn Sie das Formular <abbr title="Konvertieren der Zeichenkette, die von einer HTTP-Anfrage kommt, in Python-Daten">"parsen"</abbr>, mit `request.form()` unterstützen wollen.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Erforderlich für `SessionMiddleware`-Unterstützung.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Erforderlich für die Unterstützung von Starlettes `SchemaGenerator` (mit FastAPI brauchen Sie es wahrscheinlich nicht).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Erforderlich für die Unterstützung von `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Erforderlich, wenn Sie `UJSONResponse` verwenden möchten.

Wird von FastAPI / Starlette verwendet:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - für den Server, der Ihre Anwendung lädt und bedient.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Erforderlich, wenn Sie `ORJSONResponse` verwenden möchten.

Sie können diese alle mit `pip install fastapi[all]` installieren.

## Lizenz

Dieses Projekt ist unter den Bedingungen der MIT-Lizenz lizenziert.
# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, zeer goede prestaties, eenvoudig te leren, snel te programmeren, klaar voor productie</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentatie**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Broncode**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI is een modern, snel (zeer goede prestaties), web framework voor het bouwen van API's in Python, gebruikmakend van standaard Python type-hints.

De belangrijkste kenmerken zijn:

* **Snel**: Zeer goede prestaties, vergelijkbaar met **NodeJS** en **Go** (dankzij Starlette en Pydantic). [Een van de snelste beschikbare Python frameworks](#prestaties).
* **Snel te programmeren**: Verhoog de snelheid om functionaliteit te ontwikkelen met ongeveer 200% tot 300%. *
* **Minder bugs**: Verminder ongeveer 40% van de door mensen (ontwikkelaars) veroorzaakte fouten. *
* **Intuïtief**: Buitengewoon goede ondersteuning voor editors. <abbr title="ook bekend als automatisch aanvullen, automatisch aanvullen, IntelliSense">Overal automische code aanvulling</abbr>. Minder tijd kwijt aan debuggen.
* **Eenvoudig**: Ontworpen om gemakkelijk te gebruiken en te leren. Minder tijd nodig om documentatie te lezen.
* **Kort**: Minimaliseer codeduplicatie. Elke parameterdeclaratie ondersteunt meerdere functionaliteiten. Minder bugs.
* **Robust**: Code gereed voor productie. Met automatische interactieve documentatie.
* **Standards-based**: Gebaseerd op (en volledig verenigbaar met) open standaarden voor API's: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (voorheen bekend als Swagger) en <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* schatting op basis van testen met een intern ontwikkelteam en bouwen van productieapplicaties.</small>

## Sponsors

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Overige sponsoren</a>

## Meningen

"_[...] Ik gebruik **FastAPI** heel vaak tegenwoordig. [...] Ik ben van plan om het te gebruiken voor alle **ML-services van mijn team bij Microsoft**. Sommige van deze worden geïntegreerd in het kernproduct van **Windows** en sommige **Office**-producten._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We hebben de **FastAPI** library gebruikt om een **REST** server te maken die bevraagd kan worden om **voorspellingen** te maken. [voor Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin en Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is verheugd om een open-source release aan te kondigen van ons **crisismanagement**-orkestratieframework: **Dispatch**! [gebouwd met **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Ik ben super enthousiast over **FastAPI**. Het is zo leuk!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast presentator</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Wat je hebt gebouwd ziet er echt super solide en gepolijst uit. In veel opzichten is het wat ik wilde dat **Hug** kon zijn - het is echt inspirerend om iemand dit te zien bouwen._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"Wie geïnteresseerd is in een **modern framework** voor het bouwen van REST API's, bekijkt best eens **FastAPI** [...] Het is snel, gebruiksvriendelijk en gemakkelijk te leren [...]_"

"_We zijn overgestapt naar **FastAPI** voor onze **API's** [...] Het gaat jou vast ook bevallen [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> oprichters - <a href="https://spacy.io" target="_blank">spaCy</a> ontwikkelaars</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Wie een Python API wil bouwen voor productie, kan ik ten stelligste **FastAPI** aanraden. Het is **prachtig ontworpen**, **eenvoudig te gebruiken** en **gemakkelijk schaalbaar**, het is een **cruciale component** geworden in onze strategie om API's centraal te zetten, en het vereenvoudigt automatisering en diensten zoals onze Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, de FastAPI van CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Als je een <abbr title="Command Line Interface">CLI</abbr>-app bouwt die in de terminal moet worden gebruikt in plaats van een web-API, gebruik dan <a href="https://typer.tiangolo.com/ " class="external-link" target="_blank">**Typer**</a>.

**Typer** is het kleine broertje van FastAPI. En het is bedoeld als de **FastAPI van CLI's**. ️

## Vereisten

FastAPI staat op de schouders van reuzen:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> voor de webonderdelen.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> voor de datadelen.

## Installatie

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Opmerking**: Zet `"fastapi[standard]"` tussen aanhalingstekens om ervoor te zorgen dat het werkt in alle terminals.

## Voorbeeld

### Creëer het

* Maak het bestand `main.py` aan met daarin:

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
<summary>Of maak gebruik van <code>async def</code>...</summary>

Als je code gebruik maakt van `async` / `await`, gebruik dan `async def`:

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

**Opmerking**:

Als je het niet weet, kijk dan in het gedeelte _"Heb je haast?"_ over <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` en `await` in de documentatie</a>.

</details>

### Voer het uit

Run de server met:

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
<summary>Over het commando <code>fastapi dev main.py</code>...</summary>

Het commando `fastapi dev` leest het `main.py` bestand, detecteert de **FastAPI** app, en start een server met <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Standaard zal dit commando `fastapi dev` starten met "auto-reload" geactiveerd voor ontwikkeling op het lokale systeem.

Je kan hier meer over lezen in de <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI documentatie</a>.

</details>

### Controleer het

Open je browser op <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Je zult een JSON response zien:

```JSON
{"item_id": 5, "q": "somequery"}
```

Je hebt een API gemaakt die:

* HTTP verzoeken kan ontvangen op de _paden_ `/` en `/items/{item_id}`.
* Beide _paden_ hebben `GET` <em>operaties</em> (ook bekend als HTTP _methoden_).
* Het _pad_ `/items/{item_id}` heeft een _pad parameter_ `item_id` dat een `int` moet zijn.
* Het _pad_ `/items/{item_id}` heeft een optionele `str` _query parameter_ `q`.

### Interactieve API documentatie

Ga naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Je ziet de automatische interactieve API documentatie (verstrekt door <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatieve API documentatie

Ga vervolgens naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Je ziet de automatische interactieve API documentatie (verstrekt door <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Voorbeeld upgrade

Pas nu het bestand `main.py` aan om de body van een `PUT` request te ontvangen.

Dankzij Pydantic kunnen we de body declareren met standaard Python types.

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

De `fastapi dev` server zou automatisch moeten herladen.

### Interactieve API documentatie upgrade

Ga nu naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* De interactieve API-documentatie wordt automatisch bijgewerkt, inclusief de nieuwe body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik op de knop "Try it out", hiermee kan je de parameters invullen en direct met de API interacteren:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klik vervolgens op de knop "Execute", de gebruikersinterface zal communiceren met jouw API, de parameters verzenden, de resultaten ophalen en deze op het scherm tonen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternatieve API documentatie upgrade

Ga vervolgens naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* De alternatieve documentatie zal ook de nieuwe queryparameter en body weergeven:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Samenvatting

Samengevat declareer je **eenmalig** de types van parameters, body, etc. als functieparameters.

Dat doe je met standaard moderne Python types.

Je hoeft geen nieuwe syntax te leren, de methods of klassen van een specifieke bibliotheek, etc.

Gewoon standaard **Python**.

Bijvoorbeeld, voor een `int`:

```Python
item_id: int
```

of voor een complexer `Item` model:

```Python
item: Item
```

...en met die ene verklaring krijg je:

* Editor ondersteuning, inclusief:
    * Code aanvulling.
    * Type validatie.
* Validatie van data:
    * Automatische en duidelijke foutboodschappen wanneer de data ongeldig is.
    * Validatie zelfs voor diep geneste JSON objecten.
* <abbr title="ook bekend als: serialisatie, parsing, marshalling">Conversie</abbr> van invoergegevens: afkomstig van het netwerk naar Python-data en -types. Zoals:
    * JSON.
    * Pad parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Formulieren.
    * Bestanden.
* <abbr title="ook bekend als: serialisatie, parsing, marshalling">Conversie</abbr> van uitvoergegevens: converstie van Python-data en -types naar netwerkgegevens (zoals JSON):
    * Converteer Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` objecten.
    * `UUID` objecten.
    * Database modellen.
    * ...en nog veel meer.
* Automatische interactieve API-documentatie, inclusief 2 alternatieve gebruikersinterfaces:
    * Swagger UI.
    * ReDoc.

---

Terugkomend op het vorige code voorbeeld, **FastAPI** zal:

* Valideren dat er een `item_id` bestaat in het pad voor `GET` en `PUT` verzoeken.
* Valideren dat het `item_id` van het type `int` is voor `GET` en `PUT` verzoeken.
    * Wanneer dat niet het geval is, krijgt de cliënt een nuttige, duidelijke foutmelding.
* Controleren of er een optionele query parameter is met de naam `q` (zoals in `http://127.0.0.1:8000/items/foo?q=somequery`) voor `GET` verzoeken.
    * Aangezien de `q` parameter werd gedeclareerd met `= None`, is deze optioneel.
    * Zonder de `None` declaratie zou deze verplicht zijn (net als bij de body in het geval met `PUT`).
* Voor `PUT` verzoeken naar `/items/{item_id}`, lees de body als JSON:
    * Controleer of het een verplicht attribuut `naam` heeft en dat dat een `str` is.
    * Controleer of het een verplicht attribuut `price` heeft en dat dat een`float` is.
    * Controleer of het een optioneel attribuut `is_offer` heeft, dat een `bool` is wanneer het aanwezig is.
    * Dit alles werkt ook voor diep geneste JSON objecten.
* Converteer automatisch van en naar JSON.
* Documenteer alles met OpenAPI, dat gebruikt kan worden door:
    * Interactieve documentatiesystemen.
    * Automatische client code generatie systemen, voor vele talen.
* Biedt 2 interactieve documentatie-webinterfaces aan.

---

Dit was nog maar een snel overzicht, maar je zou nu toch al een idee moeten hebben over hoe het allemaal werkt.

Probeer deze regel te veranderen:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...van:

```Python
        ... "item_name": item.name ...
```

...naar:

```Python
        ... "item_price": item.price ...
```

...en zie hoe je editor de attributen automatisch invult en hun types herkent:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Voor een vollediger voorbeeld met meer mogelijkheden, zie de <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Gebruikershandleiding</a>.

**Spoiler alert**: de tutorial - gebruikershandleiding bevat:

* Declaratie van **parameters** op andere plaatsen zoals: **headers**, **cookies**, **formuliervelden** en **bestanden**.
* Hoe stel je **validatie restricties** in zoals `maximum_length` of een `regex`.
* Een zeer krachtig en eenvoudig te gebruiken **<abbr title="ook bekend als componenten, middelen, verstrekkers, diensten, injectables">Dependency Injection</abbr>** systeem.
* Beveiliging en authenticatie, inclusief ondersteuning voor **OAuth2** met **JWT-tokens** en **HTTP Basic** auth.
* Meer geavanceerde (maar even eenvoudige) technieken voor het declareren van **diep geneste JSON modellen** (dankzij Pydantic).
* **GraphQL** integratie met <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> en andere packages.
* Veel extra functies (dankzij Starlette) zoals:
    * **WebSockets**
    * uiterst gemakkelijke tests gebaseerd op HTTPX en `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...en meer.

## Prestaties

Onafhankelijke TechEmpower benchmarks tonen **FastAPI** applicaties draaiend onder Uvicorn aan als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">een van de snelste Python frameworks beschikbaar</a>, alleen onder Starlette en Uvicorn zelf (intern gebruikt door FastAPI). (*)

Zie de sectie <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> om hier meer over te lezen.

## Afhankelijkheden

FastAPI maakt gebruik van Pydantic en Starlette.

### `standard` Afhankelijkheden

Wanneer je FastAPI installeert met `pip install "fastapi[standard]"`, worden de volgende `standard` optionele afhankelijkheden geïnstalleerd:

Gebruikt door Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - voor email validatie.

Gebruikt door Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Vereist indien je de `TestClient` wil gebruiken.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Vereist als je de standaard templateconfiguratie wil gebruiken.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Vereist indien je <abbr title="het omzetten van de string die uit een HTTP verzoek komt in Python data">"parsen"</abbr> van formulieren wil ondersteunen met `requests.form()`.

Gebruikt door FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - voor de server die jouw applicatie laadt en bedient.
* `fastapi-cli` - om het `fastapi` commando te voorzien.

### Zonder `standard` Afhankelijkheden

Indien je de optionele `standard` afhankelijkheden niet wenst te installeren, kan je installeren met `pip install fastapi` in plaats van `pip install "fastapi[standard]"`.

### Bijkomende Optionele Afhankelijkheden

Er zijn nog een aantal bijkomende afhankelijkheden die je eventueel kan installeren.

Bijkomende optionele afhankelijkheden voor Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - voor het beheren van settings.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - voor extra data types die gebruikt kunnen worden met Pydantic.

Bijkomende optionele afhankelijkheden voor FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Vereist indien je `ORJSONResponse` wil gebruiken.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Vereist indien je `UJSONResponse` wil gebruiken.

## Licentie

Dit project is gelicenseerd onder de voorwaarden van de MIT licentie.

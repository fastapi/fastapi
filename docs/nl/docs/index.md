# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, hoge prestaties, makkelijk te leren, snel te coderen, klaar voor productie</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
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

**Broncode**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI is een modern, snel (high-performance) webframework voor het bouwen van API's met Python, gebaseerd op standaard Python type hints.

De belangrijkste kenmerken zijn:

* **Snel**: Zeer hoge prestaties, vergelijkbaar met **NodeJS** en **Go** (dankzij Starlette en Pydantic). [Een van de snelste Python frameworks beschikbaar](#performance).
* **Snel te coderen**: Verhoog de snelheid om functies te ontwikkelen met ongeveer 200% tot 300%. *
* **Minder bugs**: Verminder ongeveer 40% van de door mensen (ontwikkelaars) veroorzaakte fouten. *
* **Intuïtief**: Geweldige editor-ondersteuning. <abbr title="ook bekend als auto-complete, autocompletion, IntelliSense">Completion</abbr> overal. Minder tijd debuggen.
* **Gemakkelijk**: Ontworpen om gemakkelijk te gebruiken en te leren. Minder tijd documentatie lezen.
* **Kort**: Minimaliseer code duplicatie. Meerdere functies per parameter declaratie. Minder bugs.
* **Robuust**: Krijg productie-klare code. Met automatische interactieve documentatie.
* **Gebaseerd op standaarden**: Gebaseerd op (en volledig compatibel met) de open standaarden voor API's: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (voorheen bekend als Swagger) en <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* schatting gebaseerd op tests uitgevoerd door een intern ontwikkelteam, die productie applicaties bouwden.</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gouden en Zilveren Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Andere sponsors</a>

## Meningen { #opinions }

"_[...] Ik gebruik **FastAPI** tegenwoordig enorm veel. [...] Ik ben eigenlijk van plan om het te gebruiken voor alle **ML services van mijn team bij Microsoft**. Sommige daarvan worden geïntegreerd in het core **Windows** product en sommige **Office** producten._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We hebben de **FastAPI** bibliotheek gebruikt om een **REST** server op te zetten die bevraagd kan worden om **voorspellingen** te verkrijgen. [voor Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, en Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is verheugd om de open-source release aan te kondigen van ons **crisis management** orkestratie framework: **Dispatch**! [gebouwd met **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Ik ben dolenthousiast over **FastAPI**. Het is zo leuk!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Eerlijk gezegd, wat je hebt gebouwd ziet er super solide en gepolijst uit. In veel opzichten is het wat ik wilde dat **Hug** zou zijn - het is echt inspirerend om te zien dat iemand dat bouwt._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Als je op zoek bent naar één **modern framework** om REST API's te bouwen, bekijk dan **FastAPI** [...] Het is snel, makkelijk te gebruiken en makkelijk te leren [...]_"

"_We zijn overgestapt naar **FastAPI** voor onze **API's** [...] Ik denk dat je het leuk zult vinden [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> oprichters - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Als iemand op zoek is om een productie Python API te bouwen, zou ik **FastAPI** sterk aanbevelen. Het is **prachtig ontworpen**, **eenvoudig te gebruiken** en **zeer schaalbaar**, het is een **sleutelcomponent** geworden in onze API-first ontwikkelingsstrategie en drijft veel automatiseringen en services aan zoals onze Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI mini documentaire { #fastapi-mini-documentary }

Er is een <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI mini documentaire</a> uitgebracht eind 2025, je kunt hem online bekijken:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, de FastAPI van CLI's { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Als je een <abbr title="Command Line Interface">CLI</abbr> app bouwt voor gebruik in de terminal in plaats van een web API, bekijk dan <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** is FastAPI's kleine broertje. En het is bedoeld om de **FastAPI van CLI's** te zijn. ⌨️ 🚀

## Vereisten { #requirements }

FastAPI staat op de schouders van reuzen:

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> voor de web onderdelen.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> voor de data onderdelen.

## Installatie { #installation }

Maak en activeer een <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">virtuele omgeving</a> en installeer vervolgens FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Opmerking**: Zorg ervoor dat je `"fastapi[standard]"` tussen aanhalingstekens zet om ervoor te zorgen dat het in alle terminals werkt.

## Voorbeeld { #example }

### Maak het aan { #create-it }

Maak een bestand `main.py` met:

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
<summary>Of gebruik <code>async def</code>...</summary>

Als je code `async` / `await` gebruikt, gebruik dan `async def`:

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

Als je het niet weet, bekijk de _"Haast?"_ sectie over <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` en `await` in de docs</a>.

</details>

### Voer het uit { #run-it }

Start de server met:

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

Het commando `fastapi dev` leest je `main.py` bestand, detecteert de **FastAPI** app erin, en start een server met <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Standaard zal `fastapi dev` starten met auto-reload ingeschakeld voor lokale ontwikkeling.

Je kunt er meer over lezen in de <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI docs</a>.

</details>

### Controleer het { #check-it }

Open je browser op <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Je zult de JSON response zien als:

```JSON
{"item_id": 5, "q": "somequery"}
```

Je hebt al een API gemaakt die:

* HTTP verzoeken ontvangt in de _paths_ `/` en `/items/{item_id}`.
* Beide _paths_ nemen `GET` <em>operations</em> (ook bekend als HTTP _methods_).
* De _path_ `/items/{item_id}` heeft een _path parameter_ `item_id` die een `int` moet zijn.
* De _path_ `/items/{item_id}` heeft een optionele `str` _query parameter_ `q`.

### Interactieve API docs { #interactive-api-docs }

Ga nu naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Je zult de automatische interactieve API documentatie zien (geleverd door <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatieve API docs { #alternative-api-docs }

En nu, ga naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Je zult de alternatieve automatische documentatie zien (geleverd door <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Voorbeeld upgrade { #example-upgrade }

Wijzig nu het bestand `main.py` om een body te ontvangen van een `PUT` verzoek.

Declareer de body met standaard Python types, dankzij Pydantic.

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

### Interactieve API docs upgrade { #interactive-api-docs-upgrade }

Ga nu naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* De interactieve API documentatie zal automatisch worden bijgewerkt, inclusief de nieuwe body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik op de knop "Try it out", hiermee kun je de parameters invullen en direct interactie hebben met de API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klik vervolgens op de "Execute" knop, de gebruikersinterface zal communiceren met je API, de parameters verzenden, de resultaten krijgen en ze op het scherm tonen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternatieve API docs upgrade { #alternative-api-docs-upgrade }

En nu, ga naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* De alternatieve documentatie zal ook de nieuwe query parameter en body weerspiegelen:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Samenvatting { #recap }

Samenvattend, je declareert **één keer** de types van parameters, body, etc. als functie parameters.

Je doet dat met standaard moderne Python types.

Je hoeft geen nieuwe syntax te leren, de methoden of classes van een specifieke bibliotheek, etc.

Gewoon standaard **Python**.

Bijvoorbeeld, voor een `int`:

```Python
item_id: int
```

of voor een meer complex `Item` model:

```Python
item: Item
```

...en met die enkele declaratie krijg je:

* Editor ondersteuning, inclusief:
    * Completion.
    * Type checks.
* Validatie van data:
    * Automatische en duidelijke fouten wanneer de data ongeldig is.
    * Validatie zelfs voor diep geneste JSON objecten.
* <abbr title="ook bekend als: serialization, parsing, marshalling">Conversie</abbr> van input data: afkomstig van het netwerk naar Python data en types. Lezen van:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="ook bekend als: serialization, parsing, marshalling">Conversie</abbr> van output data: converteren van Python data en types naar netwerk data (als JSON):
    * Converteer Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` objecten.
    * `UUID` objecten.
    * Database modellen.
    * ...en nog veel meer.
* Automatische interactieve API documentatie, inclusief 2 alternatieve gebruikersinterfaces:
    * Swagger UI.
    * ReDoc.

---

Terug komend op het vorige code voorbeeld, **FastAPI** zal:

* Valideren dat er een `item_id` in het path is voor `GET` en `PUT` verzoeken.
* Valideren dat de `item_id` van het type `int` is voor `GET` en `PUT` verzoeken.
    * Als dat niet zo is, zal de client een nuttige, duidelijke fout zien.
* Controleren of er een optionele query parameter genaamd `q` is (zoals in `http://127.0.0.1:8000/items/foo?q=somequery`) voor `GET` verzoeken.
    * Omdat de `q` parameter is gedeclareerd met `= None`, is het optioneel.
    * Zonder de `None` zou het verplicht zijn (zoals de body in het geval met `PUT`).
* Voor `PUT` verzoeken naar `/items/{item_id}`, lees de body als JSON:
    * Controleer dat het een verplicht attribuut `name` heeft dat een `str` moet zijn.
    * Controleer dat het een verplicht attribuut `price` heeft dat een `float` moet zijn.
    * Controleer dat het een optioneel attribuut `is_offer` heeft, dat een `bool` moet zijn, indien aanwezig.
    * Dit zou ook werken voor diep geneste JSON objecten.
* Automatisch converteren van en naar JSON.
* Documenteer alles met OpenAPI, dat kan worden gebruikt door:
    * Interactieve documentatie systemen.
    * Automatische client code generatie systemen, voor veel talen.
* Lever 2 interactieve documentatie web interfaces direct.

---

We hebben net aan de oppervlakte gekrabd, maar je begrijpt al het idee van hoe het allemaal werkt.

Probeer de regel te veranderen met:

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

...en zie hoe je editor de attributen zal auto-completen en hun types kent:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Voor een completer voorbeeld inclusief meer functies, zie de <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Spoiler alert**: de tutorial - user guide bevat:

* Declaratie van **parameters** van andere verschillende plaatsen als: **headers**, **cookies**, **form fields** en **files**.
* Hoe **validatie beperkingen** in te stellen als `maximum_length` of `regex`.
* Een zeer krachtig en gemakkelijk te gebruiken **<abbr title="ook bekend als components, resources, providers, services, injectables">Dependency Injection</abbr>** systeem.
* Beveiliging en authenticatie, inclusief ondersteuning voor **OAuth2** met **JWT tokens** en **HTTP Basic** auth.
* Meer geavanceerde (maar even gemakkelijke) technieken voor het declareren van **diep geneste JSON modellen** (dankzij Pydantic).
* **GraphQL** integratie met <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> en andere bibliotheken.
* Veel extra functies (dankzij Starlette) zoals:
    * **WebSockets**
    * extreem gemakkelijke tests gebaseerd op HTTPX en `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...en meer.

### Implementeer je app (optioneel) { #deploy-your-app-optional }

Je kunt optioneel je FastAPI app implementeren naar <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>, ga en meld je aan voor de wachtlijst als je dat nog niet hebt gedaan. 🚀

Als je al een **FastAPI Cloud** account hebt (we hebben je uitgenodigd vanaf de wachtlijst 😉), kun je je applicatie implementeren met één commando.

Voordat je implementeert, zorg ervoor dat je bent ingelogd:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Implementeer vervolgens je app:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Dat is het! Nu kun je je app op die URL bereiken. ✨

#### Over FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** is gebouwd door dezelfde auteur en team achter **FastAPI**.

Het stroomlijnt het proces van het **bouwen**, **implementeren** en **toegang krijgen tot** een API met minimale inspanning.

Het brengt dezelfde **ontwikkelaarservaring** van het bouwen van apps met FastAPI naar het **implementeren** ervan naar de cloud. 🎉

FastAPI Cloud is de primaire sponsor en financieringsverstrekker voor de *FastAPI en friends* open source projecten. ✨

#### Implementeer naar andere cloud providers { #deploy-to-other-cloud-providers }

FastAPI is open source en gebaseerd op standaarden. Je kunt FastAPI apps implementeren naar elke cloud provider die je kiest.

Volg de gidsen van je cloud provider om FastAPI apps met hen te implementeren. 🤓

## Prestaties { #performance }

Onafhankelijke TechEmpower benchmarks tonen **FastAPI** applicaties draaiend onder Uvicorn als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">een van de snelste Python frameworks beschikbaar</a>, alleen onder Starlette en Uvicorn zelf (intern gebruikt door FastAPI). (*)

Om meer te begrijpen hierover, zie de sectie <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Afhankelijkheden { #dependencies }

FastAPI is afhankelijk van Pydantic en Starlette.

### `standard` Afhankelijkheden { #standard-dependencies }

Wanneer je FastAPI installeert met `pip install "fastapi[standard]"` komt het met de `standard` groep van optionele afhankelijkheden:

Gebruikt door Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - voor email validatie.

Gebruikt door Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Vereist als je de `TestClient` wilt gebruiken.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Vereist als je de standaard template configuratie wilt gebruiken.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Vereist als je form <abbr title="het converteren van de string die van een HTTP verzoek komt naar Python data">"parsing"</abbr> wilt ondersteunen, met `request.form()`.

Gebruikt door FastAPI:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - voor de server die je applicatie laadt en serveert. Dit bevat `uvicorn[standard]`, wat enkele afhankelijkheden bevat (bijv. `uvloop`) die nodig zijn voor high performance serving.
* `fastapi-cli[standard]` - om het `fastapi` commando te bieden.
    * Dit bevat `fastapi-cloud-cli`, waarmee je je FastAPI applicatie kunt implementeren naar <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

### Zonder `standard` Afhankelijkheden { #without-standard-dependencies }

Als je de `standard` optionele afhankelijkheden niet wilt opnemen, kun je installeren met `pip install fastapi` in plaats van `pip install "fastapi[standard]"`.

### Zonder `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Als je FastAPI wilt installeren met de standaard afhankelijkheden maar zonder de `fastapi-cloud-cli`, kun je installeren met `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Aanvullende Optionele Afhankelijkheden { #additional-optional-dependencies }

Er zijn enkele extra afhankelijkheden die je misschien wilt installeren.

Extra optionele Pydantic afhankelijkheden:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - voor settings management.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - voor extra types om te gebruiken met Pydantic.

Extra optionele FastAPI afhankelijkheden:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Vereist als je `ORJSONResponse` wilt gebruiken.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Vereist als je `UJSONResponse` wilt gebruiken.

## Licentie { #license }

Dit project is gelicenseerd onder de voorwaarden van de MIT licentie.

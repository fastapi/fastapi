<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, hoge prestaties, eenvoudig te leren, snel te programmeren, klaar voor productie</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
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

**Bron Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI is een modern, snel (hoog presterend), web framework voor het bouwen van API's in Python 3.6+ gebruikmakend van standaard Python type hints.

De belangrijkste kenmerken:

* **Snel**: Zeer hoge prestaties, vergelijkbaar met **NodeJS** en **Go** (met dank aan Starlette en Pydantic). [Een van de snelste beschikbare Python frameworks](#prestaties).
* **Snel te programmeren**: Verhoogd de snelheid om functionaliteit te ontwikkelen met ongeveer 200% tot 300%. *
* **Minder bugs**: Verminderd ongeveer 40% van de door mensen (ontwikkelaars) veroorzaakte fouten. *
* **Intuïtief**: Buitegewoon goede ondersteuning voor editors. <abbr title="ook bekend als automatisch aanvullen, automatisch aanvullen, IntelliSense">Overal automische code aanvulling</abbr>. Minder tijd kwijt aan debuggen.
* **Eenvoudig**: Ontworpen om gemakkelijk te gebruiken en te leren. Minder tijd nodig om docs te lezen.
* **Kort**: Minimaliseer codeduplicatie. Meerdere functionaliteit voor elke parameterdeclaratie. Minder bugs.
* **Robust**: Code gereed voor productie. Met automatische interactieve documentatie.
* **Standards-based**: Gebaseerd op (en volledig verenigbaar met) open standaarden voor API's: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (voorheen bekend als Swagger) en <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* schatting op basis van testen op een intern ontwikkelteam en bouwen van productieapplicaties.</small>

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

"_[...] Ik gebruik tegenwoordig heel vaak **FastAPI**. [...] Ik ben van plan om het te gebruiken voor alle **ML-services van mijn team bij Microsoft**. Sommige van deze worden geïntegreerd in het kernproduct van **Windows** en sommige **Office**-producten._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We hebben de **FastAPI** library geadopteerd om een **REST** server te maken die gequeried kan worden om **voorspellingen** op te vragen. [voor Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin en Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is verheugd om een open-source release aan te kondigen van ons **crisismanagement**-orkestratieframework: **Dispatch**! [gebouwd met **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Ik ben super enthousiast over **FastAPI**. Het is zo leuk!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast presentator</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Eerlijk, wat je hebt gebouwd ziet er super solide en gepolijst uit. In veel opzichten is het wat ik wilde dat **Hug** kon zijn - het is echt inspirerend om iemand dit te zien bouwen._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"Als u op zoek bent naar een **modern framework** voor het bouwen van REST API's, bekijk dan **FastAPI** [...] Het is snel, gebruiksvriendelijk en gemakkelijk te leren [...]_"

"_We zijn overgestapt naar **FastAPI** voor onze **API's** [...] Ik denk dat je het leuk zult vinden [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, the FastAPI of CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Als je een <abbr title="Command Line Interface">CLI</abbr>-app bouwt die in de terminal moet worden gebruikt in plaats van een web-API, ga dan naar <a href="https://typer.tiangolo.com/ " class="external-link" target="_blank">**Typer**</a>.

**Typer** is het kleine broertje van FastAPI. En het is bedoeld als de **FastAPI van CLI's**. ️

## RequVereistenirements

Python 3.6+

FastAPI staat op de schouders van reuzen:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> voor de webonderdelen.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> voor de datadelen.

## Installatie

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Je hebt ook een ASGI-server nodig voor productie, zoals <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> of <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Voorbeeld

### Creëer het

* Maak het bestand `main.py` met:

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

### Run it

Run de server met:

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
<summary>Over het commando <code>uvicorn main:app --reload</code>...</summary>

Het commando `uvicorn main:app` verwijst naar:

* `main`: het bestand `main.py` (de Python "module").
* `app`: het object gemaakt in `main.py` met de regel `app = FastAPI()`.
* `--reload`: laat de server herstarten nadat er veranderingen in de code zijn gemaakt. Doe dit alleen in de ontwikkelings fase.

</details>

### Controleer het

Open je browser op <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Je zult een JSON response zien als:

```JSON
{"item_id": 5, "q": "somequery"}
```

Je hebt een API gemaakt die:

* HTTP verzoeken kan ontvangen op de _paden_ `/` en `/items/{item_id}`.
* Beide _paden_ hebben `GET` <em>bewerkingen</em> (ook bekend als HTTP _methoden_).
* Het _pad_ `/items/{item_id}` heeft een _pad parameter_ `item_id` dat een `int` moet zijn.
* Het _pad_ `/items/{item_id}` heeft een optionele `str` _query parameter_ `q`.

### Interactieve API docs

Ga naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Je ziet de automatische interactieve API docs (verstrekt door <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

Ga vervolgens naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Je ziet de automatische interactieve API docs (verstrekt door <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Voorbeeld upgrade

Pas nu het bestand `main.py` aan om de body van een `PUT` request te ontvangen.

Met dank aan Pydantic kunnen we de body declareren standaard Python types.

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

De server zou automatisch moeten herladen (omdat je `--reload` hebt toegevoegd aan het `uvicorn` commando hierboven).

### Interactive API docs upgrade

Ga nu naar <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* De interactieve API-documentatie wordt automatisch bijgewerkt, inclusief de nieuwe body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Klik op de knop "Try it out", hiermee kunt u de parameters invullen en direct met de API interacteren:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Klik vervolgens op de knop "Execute", de gebruikersinterface zal communiceren met uw API, de parameters verzenden, de resultaten ophalen en deze op het scherm tonen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade

Ga vervolgens naar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* De alternatieve documentatie zal ook de nieuwe queryparameter en body weergeven:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Samenvatting

Samengevat declareer je **eenmalig** de types van parameters, body, etc. als functieparameters.

Dat doe je met standaard moderne Python types.

Je hoeft geen nieuwe syntaxis te leren, de methods of classes van een specifieke bibliotheek, etc.

Gewoon standaard **Python 3.6+**.

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
    * Type checks.
* Validatie van data:
    * Automatic and clear errors when the data is invalid.
    * Validation even for deeply nested JSON objects.
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
* Valideren dat `item_id` van het type `int` is voor `GET` en `PUT` verzoeken.
    * Wanneer dat niet het geval is, krijgt de cliënt een nuttige, duidelijke foutmelding.
* Controleren of er een optionele query parameter is met de naam `q` (zoals in `http://127.0.0.1:8000/items/foo?q=somequery`) voor `GET` verzoeken.
    * Doordat de `q` parameter wordt gedeclareerd met `= None`, is deze optioneel.
    * Zonder de `None` zou het verplicht zijn (net als bij de body in het geval met `PUT`).
* Voor `PUT` verzoeken naar `/items/{item_id}`, lees de body als JSON:
    * Controleer of het een verplicht attribuut `naam` heeft en dat een `str` is.
    * Controleer of het een verplicht attribuut `price` heeft en dat een`float` is.
    * Controleer of het een optioneel attribuut `is_offer` heeft, dat een `bool` is wanneer het aanwezig is.
    * Dit alles zou ook werken voor diep geneste JSON objecten.
* Converteer automatisch van en naar JSON.
* Documenteer alles met OpenAPI, dat gebruikt kan worden door:
    * Interactieve documentatiesystemen..
    * Automatische client code generatie systemen, voor vele talen.
* Biedt 2 interactieve documentatie-webinterfaces aan.

---

We zijn nog maar aan de oppervlakte, maar je hebt al een idee hoe het werkt.

Probeer de lijn te veranderen met:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...en zie hoe je editor de attributen automatisch invult en hun types herkent:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Voor een vollediger voorbeeld met meer mogelijkheden, zie de <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Gebruikershandleiding</a>.

**Spoiler alert**: de tutorial - gebruikershandleiding bevat:

* Declaratie van **parameters** van andere verschillende plaatsen zoals: **headers**, **cookies**, **formuliervelden** en **bestanden**.
* Hoe stel je **validatie restricties** in zoals `maximum_length` of een `regex`.
* Een zeer krachtig en eenvoudig te gebruiken **<abbr title="ook bekend als componenten, middelen, verstrekkers, diensten, injectables">Dependency Injection</abbr>** systeem.
* Beveiliging en authenticatie, inclusief ondersteuning voor **OAuth2** met **JWT-tokens** en **HTTP Basic** auth.
* Meer geavanceerde (maar even eenvoudige) technieken voor het declareren van **diep geneste JSON modellen** (met dank aan Pydantic).
* **GraphQL** integratie met <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> en andere packages.
* Veel extra functies (thanks to Starlette) zoas:
    * **WebSockets**
    * uiterst gemakkelijke tests gebaseerd op `requests` en `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...en meer.

## Prestaties

nafhankelijke TechEmpower benchmarks tonen **FastAPI** applicaties draaiend onder Uvicorn als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">een van de snelste Python frameworks beschikbaar</a>, alleen onder Starlette en Uvicorn zelf (intern gebruikt door FastAPI). (*)

Zie de sectie <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> om hier meer over te lezen.

## Optionele afhankelijkheden

Used by Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - for faster JSON <abbr title="het omzetten van de string uit een HTTP verzoek naar Python data">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - for email validation.

Gebruikt door Pydantic:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Vereist als je de `TestClient` wilt gebruiken.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Vereist als u de standaard templateconfiguratie wilt gebruiken.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Vereist als je het <abbr title="chet omzetten van de string die uit een HTTP verzoek komt in Python data">"parsen"</abbr> van formulieren wil ondersteunen met `requests.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Vereist als voor `SessionMiddleware` ondersteuning.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Nodig voor Starlette's `SchemaGenerator` ondersteuning (je hebt het waarschijnlijk niet nodig met FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Required if you want to use `UJSONResponse`.

Gebruikt door FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - voor de server die uw applicatie laadt en bedient.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Vereist als je `ORJSONResponse` wilt gebruiken.

U kunt deze allemaal installeren met `pip install "fastapi[all]"`.

## License

Dit project is gelicenseerd onder de voorwaarden van de MIT licentie.

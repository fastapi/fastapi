# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**Source Code**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI என்பது Python-இல் standard type hints அடிப்படையில் API-களை உருவாக்க உதவும் ஒரு
நவீன மற்றும் வேகமான (high-performance) web framework ஆகும்.

இதன் முக்கிய அம்சங்கள்:

* **Fast**: மிக அதிக performance,
    **NodeJS** மற்றும் **Go**க்கு சமமாக (Starlette மற்றும் Pydantic காரணமாக).
    [Python frameworks-லேயே மிக வேகமான ஒன்றாக](#performance).
* **Fast to code**: அம்சங்களை உருவாக்கும் வேகம் சுமார் 200% முதல் 300% வரை
    அதிகரிக்கலாம். *
* **Fewer bugs**: மனித (developer) காரணமாக ஏற்படும் தவறுகள் சுமார் 40% வரை
    குறையலாம். *
* **Intuitive**: சிறந்த editor support, எல்லா இடங்களிலும்
    <dfn title="also known as auto-complete, autocompletion, IntelliSense">Completion</dfn>.
    debugging நேரம் குறையும்.
* **Easy**: பயன்படுத்தவும் கற்றுக்கொள்ளவும் எளிதாக வடிவமைக்கப்பட்டுள்ளது.
    documentation-ஐ படிக்கும் நேரம் குறையும்.
* **Short**: code duplication குறையும். ஒவ்வொரு parameter declaration-லேயே பல அம்சங்கள் கிடைக்கும்;
    bugs குறையும்.
* **Robust**: production-ready code வழங்கப்படுகிறது;
    automatic interactive documentation உடன்.
* **Standards-based**: API-களுக்கான open standards அடிப்படையில்...

<small>* production applications உருவாக்கிய ஒரு internal development team செய்த tests அடிப்படையிலான
மதிப்பீடு.</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold and Silver Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[Other sponsors](https://fastapi.tiangolo.com/fastapi-people/#sponsors)

## Opinions { #opinions }

"_[...] இந்த நாட்களில் **FastAPI** ஐ நான் மிகவும் அதிகமாக பயன்படுத்துகிறேன். [...]
உண்மையிலேயே இதை என் team-னுடைய **ML services at Microsoft** எல்லாவற்றுக்கும் பயன்படுத்த திட்டமிட்டுள்ளேன்.
அதில் சில core **Windows** product-லேயே integrate ஆகிறது, சில **Office** products-லையும் ஆகிறது._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_**predictions** பெற query செய்யக்கூடிய ஒரு **REST** server உருவாக்க **FastAPI** library-யை நாம்
பயன்படுத்த தீர்மானித்தோம். [Ludwig காக]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_எங்களின் **crisis management** orchestration framework: **Dispatch**-ஐ open-source ஆக வெளியிட்டதை **Netflix** மகிழ்ச்சியுடன் அறிவிக்கிறது! [**FastAPI** கொண்டு build செய்தது]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_**FastAPI** பற்றி நான் மிகவும் excited. இது மிகவும் fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>[Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855) podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

"_உண்மையிலேயே, நீங்க build செய்தது மிகவும் solid ஆகவும் polished ஆகவும் உள்ளது. பல விதத்தில்,
**Hug** இப்படித்தான் இருக்கணும் என்று நான் நினைத்தது போலவே உள்ளது — இதை ஒருத்தர் build செய்தது பார்க்க
மிகவும் inspiring ஆக உள்ளது._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>[Hug](https://github.com/hugapi/hug) creator</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

"_REST APIs உருவாக்க ஒரு **modern framework** கற்றுக்கணும்னு நினைச்சா, **FastAPI** ஐ பார்க்கவும் [...]
இது வேகமானது, பயன்படுத்த எளிது, கற்றுக்கொள்ள எளிது [...]_"

"_எங்களின் **APIs** காக நாம் **FastAPI** க்கு மாறிட்டோம் [...] உங்களுக்கு இது பிடிக்கும் என்று நினைக்கிறேன் [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>[Explosion AI](https://explosion.ai) founders - [spaCy](https://spacy.io) creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

"_production Python API build செய்ய நினைப்பவர்களுக்கு, **FastAPI** ஐ நான் strongly recommend செய்வேன்.
இது **beautifully designed**, **simple to use**, மற்றும் **highly scalable**. எங்களின் API first development
strategy-ல இது ஒரு **key component** ஆகி, Virtual TAC Engineer போன்ற பல automations மற்றும் services-ஐ
இயக்குது._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## FastAPI mini documentary { #fastapi-mini-documentary }

2025 முடிவில் வெளியான [FastAPI mini documentary](https://www.youtube.com/watch?v=mpR8ngthqiE) ஒன்று இருக்கிறது;
அதை online-ல பார்க்கலாம்:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, the FastAPI of CLIs { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

web APIக்கு பதிலாக terminal-ல் பயன்படுத்த ஒரு <abbr title="Command Line Interface">CLI</abbr> app உருவாக்க விரும்பினால்,
[**Typer**](https://typer.tiangolo.com/) ஐ பார்க்கவும்.

**Typer** என்பது FastAPI-னுடைய small sibling. இது **CLIs கான FastAPI** ஆக இருக்கவே உருவாக்கப்பட்டது. ⌨️ 🚀

## Requirements { #requirements }

FastAPI “giants” மேல் நின்று உருவாக்கப்பட்டது:

* web parts காக [Starlette](https://www.starlette.dev/).
* data parts காக [Pydantic](https://docs.pydantic.dev/).

## Installation { #installation }

[virtual environment](https://fastapi.tiangolo.com/virtual-environments/) ஒன்றை create செய்து activate செய்துவிட்டு,
பிறகு FastAPI ஐ install செய்யுங்கள்:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**குறிப்பு**: எல்லா terminals-லையும் சரியா வேலை செய்ய `"fastapi[standard]"` என்பதை
quotes-க்குள்ளே போடுங்க.

## Example { #example }

### Create it { #create-it }

`main.py` என்ற file ஒன்றை இப்படி உருவாக்குங்கள்:

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
<summary>அல்லது <code>async def</code> பயன்படுத்தலாம்...</summary>

உங்க code-ல `async` / `await` பயன்படுத்துகிறீர்களானால், `async def` பயன்படுத்துங்கள்:

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

**குறிப்பு**:

தெரியலைன்னா, docs-ல இருக்கும் _"In a hurry?"_ section-ல
[`async` மற்றும் `await`](https://fastapi.tiangolo.com/async/#in-a-hurry) பற்றி பார்க்கவும்.

</details>

### Run it { #run-it }

server-ஐ இவ்வாறு இயக்கவும்:

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
<summary><code>fastapi dev</code> command பற்றி...</summary>

`fastapi dev` command உங்க `main.py` file-ஐ automatic-ஆ படிச்சு, அதில் உள்ள **FastAPI** app-ஐ கண்டுபிடிச்சு,
[Uvicorn](https://www.uvicorn.dev) பயன்படுத்தி server-ஐ start செய்யும்.

default-ஆ, local development காக `fastapi dev` auto-reload enabled-ஆ start ஆகும்.

மேலும் விவரங்களுக்கு [FastAPI CLI docs](https://fastapi.tiangolo.com/fastapi-cli/) பார்க்கவும்.

</details>

### Check it { #check-it }

உங்க browser-ல
[http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery) ஐ திறக்கவும்.

JSON response இப்படியே வரும்:

```JSON
{"item_id": 5, "q": "somequery"}
```

இப்போ நீங்கள் ஒரு API உருவாக்கிட்டீங்க, அது:

* `/` மற்றும் `/items/{item_id}` என்ற _paths_-ல HTTP requests-ஐ receive செய்யும்.
* இரண்டு _paths_-க்கும் `GET` <em>operations</em> (அதாவது HTTP _methods_) உள்ளது.
* `/items/{item_id}` _path_-ல `item_id` என்ற _path parameter_ உள்ளது; அது `int` ஆக இருக்கணும்.
* `/items/{item_id}` _path_-ல optional `str` _query parameter_ `q` உள்ளது.

### Interactive API docs { #interactive-api-docs }

இப்போ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) க்கு செல்லவும்.

automatic interactive API documentation (இதை [Swagger UI](https://github.com/swagger-api/swagger-ui) வழங்குகிறது)
உங்களுக்கு தெரியும்:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs { #alternative-api-docs }

அப்புறம் [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) க்கு செல்லவும்.

alternative automatic documentation (இதை [ReDoc](https://github.com/Rebilly/ReDoc) வழங்குகிறது)
இங்கே தெரியும்:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Example upgrade { #example-upgrade }

இப்போ `main.py` file-ஐ மாற்றி, `PUT` request-ல இருந்து body-ஐ receive செய்யுமாறு செய்யுங்கள்.

Pydantic உதவியால், standard Python types பயன்படுத்தி body-யை declare செய்யவும்.

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

`fastapi dev` server automatic-ஆ reload ஆகும்.

### Interactive API docs upgrade { #interactive-api-docs-upgrade }

இப்போ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) க்கு செல்லவும்.

* interactive API documentation automatic-ஆ update ஆகும்; புதிய body உட்பட:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" button-ஐ click செய்யவும்; அதில் parameters fill செய்து
    நேரடியாக API-யோட interact செய்யலாம்:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* அப்புறம் "Execute" button-ஐ click செய்யவும்; user interface உங்க API-யோட பேசும்,
    parameters அனுப்பும், results வாங்கி screen-ல காட்டும்:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade { #alternative-api-docs-upgrade }

அப்புறம் [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) க்கு செல்லவும்.

* alternative documentation-லயும் புதிய query parameter மற்றும் body reflect ஆகும்:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap { #recap }

சுருக்கமாகச் சொன்னால், parameters, body, போன்றவற்றின் types-ஐ function parameters-ஆ **ஒரே முறை**
declare செய்கிறீர்கள்.

அதை standard modern Python types-ஓடு செய்கிறீர்கள்.

புதிய syntax, அல்லது ஒரு specific library-யின் methods/classes போன்றவை தனியா கற்றுக்க வேண்டியதில்லை.

standard **Python** போதும்.

உதாரணத்திற்கு, `int` காக:

```Python
item_id: int
```

அல்லது இன்னும் complex ஆன `Item` model காக:

```Python
item: Item
```

...இப்படி ஒரே declaration-லேயே உங்களுக்கு கிடைப்பது:

* Editor support, இதில்:
    * Completion.
    * Type checks.
* Data validation:
    * data invalid இருந்தா automatic-ஆ தெளிவான errors.
    * deeply nested JSON objects க்கும் validation.
* input data-வின் <dfn title="also known as: serialization, parsing, marshalling">Conversion</dfn>: network-ல இருந்து
    Python data/types-களாக மாற்றுவது. இவற்றிலிருந்து வாசிக்கிறது:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* output data-வின் <dfn title="also known as: serialization, parsing, marshalling">Conversion</dfn>: Python data/types-ல இருந்து
    network data (JSON ஆக) மாற்றுவது:
    * Python types (`str`, `int`, `float`, `bool`, `list`, etc) மாற்றுதல்.
    * `datetime` objects.
    * `UUID` objects.
    * Database models.
    * ...இன்னும் நிறைய.
* Automatic interactive API documentation, இதில் 2 alternative user interfaces:
    * Swagger UI.
    * ReDoc.

---

முந்தைய code example-க்கு திரும்பி பார்த்தா, **FastAPI** இது எல்லாம் செய்யும்:

* `GET` மற்றும் `PUT` requests காக path-ல `item_id` இருக்கிறதா என்று validate செய்யும்.
* `GET` மற்றும் `PUT` requests காக `item_id` type `int` தானா என்று validate செய்யும்.
    * இல்லையென்றால் client-க்கு பயனுள்ள, தெளிவான error தெரியும்.
* `GET` requests காக `q` என்ற optional query parameter இருக்கிறதா என்று check செய்யும்
    (`http://127.0.0.1:8000/items/foo?q=somequery` போல).
    * `q` parameter `= None` உடன் declare செய்யப்பட்டது காரணமாக அது optional.
    * `None` இல்லையென்றால் அது required (PUT-ல body போல).
* `/items/{item_id}` க்கு `PUT` requests வந்தா, body-யை JSON ஆக வாசிக்கும்:
    * `name` என்ற required attribute இருக்கிறதா, அது `str` தானா என்று check.
    * `price` என்ற required attribute இருக்கிறதா, அது `float` தானா என்று check.
    * `is_offer` என்ற optional attribute இருந்தா, அது `bool` தானா என்று check.
    * இதெல்லாம் deeply nested JSON objects க்கும் வேலை செய்யும்.
* JSON-க்கு/JSON-ல இருந்து automatic-ஆ convert செய்யும்.
* எல்லாத்தையும் OpenAPI-யோட document செய்யும்; இதை பயன்படுத்த முடியும்:
    * Interactive documentation systems.
    * பல languages-க்கு automatic client code generation systems.
* நேரடியாக 2 interactive documentation web interfaces கொடுக்கும்.

---

இது இன்னும் தொடக்கம் மட்டுமே; ஆனாலும் இது எப்படி செயல்படுகிறது என்பது பற்றிய ஒரு தெளிவான புரிதல் இப்போது
உங்களுக்கு கிடைத்திருக்கும்.

இந்த line-ஐ மாற்றிப் பார்க்கவும்:

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

...அப்போ உங்க editor எப்படி attributes-ஐ auto-complete செய்யுது, அவற்றின் types-ஐ எப்படி தெரிஞ்சுக்குது என்று
பார்க்கவும்:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

இன்னும் நிறைய features உடன் ஒரு complete example காக
<a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a> பார்க்கவும்.

**Spoiler alert**: tutorial - user guide-ல இதில் எல்லாம் இருக்கு:

* வேறு பல இடங்களிலிருந்து **parameters** declare செய்வது: **headers**, **cookies**, **form fields** மற்றும்
    **files**.
* `maximum_length` அல்லது `regex` போன்ற **validation constraints** எப்படி set செய்வது.
* மிகவும் powerful, பயன்படுத்த எளிதான
    **<dfn title="also known as components, resources, providers, services, injectables">Dependency Injection</dfn>** system.
* Security மற்றும் authentication, இதில் **OAuth2** + **JWT tokens** மற்றும் **HTTP Basic** auth support.
* **deeply nested JSON models** declare செய்ய இன்னும் advanced (ஆனா அதே மாதிரி easy) techniques
    (Pydantic காரணமாக).
* [Strawberry](https://strawberry.rocks) மற்றும் பிற libraries உடன் **GraphQL** integration.
* Starlette காரணமாக கிடைக்கும் பல extra features:
    * **WebSockets**
    * HTTPX மற்றும் `pytest` அடிப்படையில் மிகவும் easy tests
    * **CORS**
    * **Cookie Sessions**
    * ...and more.

### Deploy your app (optional) { #deploy-your-app-optional }

[FastAPI Cloud](https://fastapicloud.com) க்கு உங்க FastAPI app-ஐ optional-ஆ deploy செய்யலாம்;
இன்னும் join செய்யலன்னா waiting list-ல சேருங்க. 🚀

உங்கிடம் ஏற்கனவே **FastAPI Cloud** account இருந்தா (waiting list-ல இருந்து நாம் invite செய்திருப்போம் 😉),
ஒரு command-லேயே app-ஐ deploy செய்யலாம்.

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

அவ்வளவுதான்! இப்போ அந்த URL-ல் உங்க app-ஐ access செய்யலாம். ✨

#### About FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)**-ஐ **FastAPI**-யை உருவாக்கிய அதே author மற்றும் team தான்
build செய்தாங்க.

ஒரு API-யை **building**, **deploying**, **accessing** செய்வதைக் குறைந்த முயற்சியில் smooth-ஆ மாற்றுகிறது.

FastAPI-யோட app build செய்யும்போது கிடைக்கும் அதே **developer experience**-ஐ cloud-க்கு **deploying**
செய்யும்போதும் கொண்டு வருகிறது. 🎉

*FastAPI and friends* open source projects-க்கு FastAPI Cloud தான் primary sponsor மற்றும்
funding provider. ✨

#### Deploy to other cloud providers { #deploy-to-other-cloud-providers }

FastAPI open source, மேலும் standards அடிப்படையிலானது. நீங்க விரும்பும் எந்த cloud provider-லையாவது
FastAPI apps-ஐ deploy செய்யலாம்.

FastAPI apps-ஐ deploy செய்ய உங்க cloud provider-ன் guides-ஐ follow செய்யவும். 🤓

## Performance { #performance }

Independent TechEmpower benchmarks-ல், Uvicorn-ல் ஓடும் **FastAPI** applications
[Python frameworks-லேயே மிகவும் வேகமான ஒன்றாக](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)
காட்டப்படுது; Starlette மற்றும் Uvicorn தங்களுக்குக் கீழே மட்டும் (FastAPI உள்ளே பயன்படுத்துவது). (*)

மேலும் புரிஞ்சுக்க [Benchmarks](https://fastapi.tiangolo.com/benchmarks/) section பார்க்கவும்.

## Dependencies { #dependencies }

FastAPI, Pydantic மற்றும் Starlette மீது depend ஆகிறது.

### `standard` Dependencies { #standard-dependencies }

FastAPI-யை `pip install "fastapi[standard]"` மூலம் install செய்தால், `standard` group-ல உள்ள optional
dependencies உடன் வரும்:

Pydantic பயன்படுத்துவது:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - email validation காக.

Starlette பயன்படுத்துவது:

* [`httpx`](https://www.python-httpx.org) - `TestClient` பயன்படுத்தணும்னா required.
* [`jinja2`](https://jinja.palletsprojects.com) - default template configuration பயன்படுத்தணும்னா required.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - `request.form()` உடன் form
    <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn>
    support வேணும்னா required.

FastAPI பயன்படுத்துவது:

* [`uvicorn`](https://www.uvicorn.dev) - உங்க application-ஐ load செய்து serve செய்யும் server காக.
    இதில் `uvicorn[standard]` அடங்கும்; அதில் high performance serving காக தேவையான சில dependencies
    (எ.கா. `uvloop`) இருக்கிறது.
* `fastapi-cli[standard]` - `fastapi` command வழங்க.
    * இதில் `fastapi-cloud-cli` அடங்கும்; இதனால் உங்க FastAPI application-ஐ
        [FastAPI Cloud](https://fastapicloud.com) க்கு deploy செய்யலாம்.

### Without `standard` Dependencies { #without-standard-dependencies }

`standard` optional dependencies வேண்டாம் என்றால், `pip install "fastapi[standard]"` க்கு பதிலாக
`pip install fastapi` மூலம் install செய்யலாம்.

### Without `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

standard dependencies உடன் ஆனால் `fastapi-cloud-cli` இல்லாமல் install செய்யணும்னா,
`pip install "fastapi[standard-no-fastapi-cloud-cli]"` பயன்படுத்தலாம்.

### Additional Optional Dependencies { #additional-optional-dependencies }

நீங்கள் install செய்ய விரும்பக்கூடிய சில additional dependencies-வும் உள்ளது.

Additional optional Pydantic dependencies:

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - settings management காக.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - Pydantic உடன் பயன்படுத்த
    extra types காக.

Additional optional FastAPI dependencies:

* [`orjson`](https://github.com/ijl/orjson) - `ORJSONResponse` பயன்படுத்தணும்னா required.
* [`ujson`](https://github.com/esnme/ultrajson) - `UJSONResponse` பயன்படுத்தணும்னா required.

## License { #license }

இந்த project, MIT license விதிமுறைகளின் கீழ் licensed ஆகிறது.


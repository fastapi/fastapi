
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI வரைச்சட்டம், அதிக வீரியம், கற்பதற்க்கு எளியது, வேகமாக குறிமுறையாக்கல், உடன் பயனுக்கு தயாரானது</em>
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

**ஆவணம் (docuemntation - doubtful)**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**முலக்குறியீடு**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI ஒரு நவீன, வேகமான (அதிக செயல் திறன்), வலைத்தள வரைச்சட்டம். இது பைத்தான் 3.7+ல் APIக்களை பைத்தான் வகை குறிப்புகள் (type hints) மூலமாக உருவாக்க உதவுகிறது.

இதன் முக்கய அம்சங்கள்:

* **வேகம்**: அதிக செயல் திறன், **NodeJS** மற்றும் **Go**விற்க்கு ஒப்பிடாக (ஸ்டார்லெட் மற்றும் பைடான்டிக்கு நன்றிகள்). [பைத்தான் கட்டமைப்புகளிள் மிக வேகமான ஒன்று](#செயல்-திறன்)
* **வேகமாக குறியீடாக்குதல்**: பண்புகூறுகள் (features) உருவாக்கும் வேகத்தை 200% முதல் 300% அதிகரிக்கிறது. *
* **குறைவான பிழைகள்**: ஏறக்குறைய 40% உருவாக்குனர்களால் வரும் பிழைகளை குறைக்கிறது.
* **உள்ளுணர்வு**: சிறந்த தொகுப்பி ஆதரவு. எங்கும்<abbr title="autocompletion"> பரிந்துரைகள் </abbr>. குறைவான தவறு நீக்குதல்(debugging) நேரம்.
* **எளியது**: கற்பதற்கும் பயன்பாட்டிற்க்கும் எளியது. குறைவான ஆவணப்படித்தல் நேரம்.
* **குட்டி**: குறைவான குறீயிடு(code) நகல்கள். ஒவ்வொரு அளவுருவின் (parameter) அறிவிப்பிலும் பண்முக பண்புகூறுகள். குறைவான தவறுகள்
* **வீரியம்**: உற்பத்திக்கு தயாரான குறியீடு பெறுங்கள். கூடுதலாக தானியக்க ஊடாடும் ஆவணம்.
* **நிலையானது**: OpenAPI அடிப்படையிலான <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (முன்னர் Swagger என்று அழைக்கப்பட்டது) மற்றும் <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>வை சார்ந்த்து (மற்றும் முழுமையாக ஒற்றுமைக்கொண்டது.)
<small>* உத்தேசங்கள், உற்பத்தி-பயன்பாட்டு மென்பொருள் உருவாக்கும் உள்ளணியின் நடத்தப்பட்ட தேர்வுகள் சார்ந்தது.</small>

## ஆதரவாளர்கள்

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">பிற ஆதரவாளர்கள்</a>

## கருத்துகள்

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

நீங்கள் ஒரு வலைய APIக்கு பதிலாக, முணையத்தில் (terminal) வேலை செய்யும் <abbr title="கட்டளை கொடு இடைமுகப்பு">க.கொ.இ</abbr> (CLI) செயலி செய்கிறிர் என்றால், <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>ஐ பார்க்கவும்.

**Typer** FastAPIயின் குட்டி தம்பி. அது **CLIயில் FastAPI** போன்றது.

## தேவைப்பாடுகள்

பைத்தான் 3.7+

FastAPI இக்கருவிகளின் தோள்களிள் நிற்க்கிறது

* வலைய பாகங்களுக்காக<a href="https://www.starlette.io/" class="external-link" target="_blank">ஸ்டார்லெட்</a>.
* தரவு பாகங்களுக்காக<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">பைடான்டிக்</a>.

## நிறுவுதல்

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

உற்பத்திக்கு, உங்களுக்கு <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> (அ) <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> போன்ற ஒரு நேரச்சீரற்ற சேவையக நுழைவாயில் இடைமுகப்பு (ASGI server) தேவைப்படும்.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## உதாரணம்

### உருவாக்குக

* `main.py` என ஒரு கோப்பையை உருவாக்கி, அதில் இதனை எழுதுக:

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
<summary> அல்லது <code>async def</code> பயன்படுத்துக...</summary>

உங்கள் குறீயிடு `async` / `await` பயன்படுத்தினால், `async def` பயன்படுத்துக:

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

**குறிப்பு**:

உங்களுக்கு தெரியவில்லை என்றால், <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` மற்றும் `await` ஆவணத்தில்</a> _"அவசரத்தில்?"_ பகுதியை பார்க்கவும்.

</details>

### இயக்குக

சேவையகத்தை இவ்வாறு இயக்குக:

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
<summary><code>uvicorn main:app --reload</code> என்கிற கட்டளையை பற்றி...</summary>

`uvicorn main:app` என்கிற கட்டளை இதனை குறிக்கின்றன:

* `main`: `main.py` என்கிற கோப்பை (பைத்தான் "தொகுதி" (module)).
* `app`: `main.py` கோப்பையில் `app = FastAPI()` என்கிற வரியால் உருவாக்கிய பொருள் (object).
* `--reload`: சேவையகத்தை குறீயிடுமாறிய பிறகு மறுபிடியும் தொடக்க செய்யும். இதை உருவாக்குதலின் பொழுது மட்டுமே பயன்படுத்தவும்.

</details>

### சரிபார்க்க

உங்கள் மேலோடியில் <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> தளத்தில் திறக்கவும்.

ஒரு JSON பதிலை காண்பிர்:

```JSON
{"item_id": 5, "q": "somequery"}
```

நீங்கள் ஒரு API உருவாக்கியுள்ளிர். அது:

* HTTP வேண்டுதலை `/` மற்றும் `/items/{item_id}` _பாதையில்_ வாங்கும்.
* இரண்டு _பாதைகளும்_ `GET` <em>செயல்பாடுகள் (operations)</em> (HTTP _முறை_ (method) என்றும் கூறுவர்).
* `/items/{item_id}` பாதை `item_id` _பாதை அளவுருவி_ (path parameter) கொண்டுள்ளது. `item_id`, `int` ஆக இருக்க வேண்டும்.
* `/items/{item_id}` _பாதை_, ஒரு `str` _கேட்டறி அளவுருவி_ (query parameter) `q` கொண்டுள்ளது.

### ஊடாடும் API ஆவணம்

இப்பொழுது <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> தளத்திற்க்கு செல்லுங்கள்.

அங்கு தானியங்கி ஊடாடும் API ஆவணம் (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>யால் வழங்கப்படுகிறது) பார்ப்பிர்கள்:
![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### மாற்று API ஆவணம்

<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> தளத்திற்க்கு சென்றால், (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>க்கால் வழங்கப்படுகிறது) மாற்று தானியங்கி ஆவணத்தை காண்பீர்:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## உதாரண மேம்படுத்தல்

இப்பொழுது, `main.py` கோப்பையை ஒரு `PUT` வேண்டுதலில் இருந்து உடலை பெறுவதற்க்கு மாற்றியமைக்கலாம்.

உடலை பைத்தான் வகைகளை அடிப்படையில் அறிவிக்கலாம், பைடான்டிக்கு நன்றி.

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

சேவையகம் தானாகவே புதுப்பிக்கும் (ஏனென்றால், முன்பு `uvicorn` கட்டளையில் `--reload` சேர்த்திறிக்கிறோம்).

### ஊடாடும் API ஆவணம் மேம்படுத்தல்

இப்பொழுது <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> தளத்திற்க்கு செல்லுங்கள்.

* ஊடாடும் API ஆவணம், தானாகவே புதுப்பதிற்க்கும், புது உடலுடன்::

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" பட்டனை சொடக்கினால், அளவுருவிக்களை நிரப்பி, APIயுடன் தொடர்புக்கொள்ள அனுமதிக்கும்:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* "Execute" பட்டனை சொடக்கினால், பயனாளர் இடைமுகப்பு APIயுடன் தொடர்புக்கொண்டு, அளவுருவிகளை அனுப்பி, முடிவுகளை பெற்று திரையில் காண்பிக்கும்.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### மாற்று API ஆவணம் மேம்படுத்தல்

 இப்பொழுது <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>  தளத்திற்க்கு செல்லுங்கள்.

* மாற்று ஆவணமும் புது உடல் மற்றும் கேட்டறி அளவுருவி காண்பிக்கும்:  

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### மீண்டும்

சுருக்கமாக, அளவுருவியின் வகை, உடல் போன்றவற்றை **ஒரு முறை** செயல் கூறு அளவுருவியாக அறிவித்தல்.

அதை சாதாரணமான நவீன பைத்தான் வகைகள் மூலமாக செய்ய வேண்டும்.

புதிய இலக்கணமோ, ஒரு நூலகத்ததை சேர்ந்த முறை (அ) வகுப்பு கற்க அவசியமில்லை.

அடிப்படையில் வெரும் **பைத்தான் 3.7+**.

உதாரணத்திற்க்கு, `int`ற்க்கு:

```Python
item_id: int
```

அல்லது கலவையான `Item` மாதிரிக்கு:

```Python
item: Item
```

...அந்த ஒரு அறிவிப்பில் நீங்கள் பெறுவிர்:

* தொகுப்பி ஆதரவு, கூடவே:
    * நிறைவு.
    * வகை சரி பார்த்தல்.
* தரவு சரி பார்த்தல்:
    * தரவு சரியில்லாத பொழுது, தானாகவே தெளிவாக பிழை காண்பித்தல்.
    * கூடாய் இருக்கும் JSON பொருட்ககளிலும் சோதனை செய்யும்.
* பணையத்திலிருந்து வரும் உள்ளீட்டு தரவுகளை, பைத்தான் தரவாகவும் வகையாகவும் <abbr title="வரிசையாக்குதல், பாகுபடுத்துதல் என்றும் அழைப்பர்">மாற்றுதல்.</abbr>. உள்ளீட்டு முறை
    * JSON.
    * வழி அளவுருவி.
    * கேட்டறி அளவுருவி.
    * Cookies.
    * தலைப்புகள் (Headers).
    * பதிவுகள் (Forms).
    * கோப்பைகள்.
* பணையத்திற்க்கு செல்லும் வெளியீட்டு தரவுகளை, பைத்தான் தரவு வகையில் இருந்து பணைய தரவாக <abbr title="வரிசையாக்குதல், பாகுபடுத்துதல் என்றும் அழைப்பர்">மாற்றுதல்</abbr> (JSON ஆக):
    *  பைத்தான் வகைகளை (`str`, `int`, `float`, `bool`, `list`, etc) மாற்றுதல்.
    * `datetime` பொருட்கள்.
    * `UUID` பொருட்கள்.
    * தரவுத்தள மாதிரிகள்.
    * ...மேலும் சில.
* தானியங்கி ஊடாடும் API ஆவணம், 2 மாற்று பயனாளர் இடைமுகப்புடன்:
    * Swagger UI.
    * ReDoc.

---

முன்னர் இருக்கும் குறீயிடு உதாரணத்தில், **FastAPI**
* `item_id` `GET` மற்றும் `PUT` வேண்டுதலில் இருக்கிறதா என்று பார்க்கும்.
* `item_id` `int` வகையை சேர்ந்ததா என்று பார்க்கும்.
    * `item_id` `int` வகையை சேர்ந்தது இல்லை என்றால், தவறு காண்பிக்கும்.
* `GET` வேண்டுதலில் `q` என்ற ஏதாவது விருப்ப கேட்டறி அளவுருவி (`http://127.0.0.1:8000/items/foo?q=somequery`யில் இருப்பது போல்) என இருக்கிறதா என்று பார்க்கும்.
    * `q` அளவுருவியை `= None` என்று அறிவித்திருப்பதால், அது விருப்ப அளவுருவி.
    * `None` இல்லை என்றால் அது கண்டிப்பாக தேவைப்படும் அளவுருவி.
* `/items/{item_id}` க்கு `PUT` வேண்டுதலில், உடலை ஜசோனாக ஏற்று:
    * `name` என்ற தேவையான பண்பு `str` வகையை கொண்டுருக்கிறதா என்று பார்க்கும்.
    * `price` என்ற தேவையான பண்பு `float` வகையை கொண்டுருக்கிறதா என்று பார்க்கும்.
    * `is_offer` என்ற விருப்ப பண்பு `bool` வகையை கொண்டுருக்கிறதா என்று பார்க்கும்.
    * இவை அனைத்தும் ஆழ்க்கூடாய் இருக்கும் ஜசோன் பொருட்களுக்கும் பொருந்தும்.
* JSON இலிருந்து மற்றும் JSON ஆக தானாகவே மாற்றும்.
* அனைத்தையும் OpenAPI கொண்டு ஆவணப்படுத்துதல். இதனை:
    * ஊடாடும் ஆவணமாக்கும் அமைப்புகள் பயன்படுத்தலாம்.
    * பல மொழிகளில், தானாகவே வழங்குபவர் குறீயிடு உருவாக்கும் அமைப்புகள் பயன்படுத்தலாம்.
* வலைய இடைபரிமாற்றத்திற்க்கு, 2 ஊடாடும் ஆவணங்கள் வழங்கும்.

---

உங்களுக்கு இப்பொழுது மேலோட்டமாக அனைத்தும் எப்படி வேலை செய்கிறது என்று தெரிந்திருக்கும்.

பின் வரும் வரிகளை,

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...இதிலிருந்து:

```Python
        ... "item_name": item.name ...
```

...இவ்வாறாக:

```Python
        ... "item_price": item.price ...
```

மாற்றுக. தொகுப்பி பண்புகளை தானாகவே முடித்து, வகையை அறியும்:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

மேலும் பண்புகளுடன் விரிவான உதாரணத்திற்க்கு, <a href="https://fastapi.tiangolo.com/tutorial/">பயிற்சி - பயனர் கையேடு</a> பார்க்கலாம்.

**சுறுக்கமாக**: பயிற்சி - பயனர் கையேடுல்:

* **headers**, **cookies**, **form fields** மற்றும் **files** களில் **அளவுருவி** அறிவிப்புகள்.
* `maximum_length` (அ) `regex` போன்ற **சரிபார்ப்பு கட்டுப்பாடுகள்** அமைப்பது.
* மிகவும் வலிமையான மற்றும் எளிதாக பயன்படுத்தக்குடிய **தேவைகள் செலுத்தும்** (Dependency Injection) அமைப்பு.
* பாதுகாப்பு மற்றும் அங்கீகாரம், **JWT tokens** உடன் **OAuth2** மற்றும் **HTTP Basic** அங்கீகாரத்திற்க்கு ஆதரவு.
* Pydantic மூலம் **ஆழ்க்கூடு ஜசோன் மாதிரிகள்** அறிவிப்பதற்க்கு வழிகள்.
* <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> மற்றும் பிற நூலகங்கள் மூலம் **GraphQL** ஒருங்கினைப்பு.
* மேலும் சில பண்புகள் (ஸ்டார்லெட் மூலமாக):
    * **WebSockets**
    * `requests` மற்றும் `pytest` சான்ற தேர்வுகள்
    * **CORS**
    * **Cookie Sessions**
    * ...மேலும் சில.

## செயல் திறன்

TechEmpower என்ற சார்பற்ற திறன் மதிப்பு அமைப்பு, யுவிகார்னில் இயங்கும் **FastAPI** செயலிகள் <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">பைத்தான் கட்டமைப்புகளில் வேகமான ஒன்று</a> என்றும், இதன் வேகம் ஸ்டார்லெட் மற்றும் யுவிகார்ன் (FastAPIயால் உள்ளே பயன்படுத்தபடுகிறது) வேகத்தைவிட சற்றே குறையது என்கிறது. (*)

இதனை பற்றி மேலும் அறிய, <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">திறன் மதிப்பு</a> பகுதியை பார்க்கலாம்.

## விருப்ப தேவைகள்

பைடான்டிக் பயன்படுத்துவது:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - வேகமான ஜசான் <abbr title="HTTP வேண்டுதலில் வரும் சரத்ததை பைத்தான் தரவாக மாற்றுதல்">"பாகுபடுத்துதல்"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - மின் அஞ்சல் முகவரி சரி பார்கத்தல்.

ஸ்டார்லெட் பயன்படுத்துவது:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - `TestClient` பயன்படுத்துவிர்கள் என்றால் தேவை.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - இயல்புநிலை டெம்ப்ளேட் பயன்படுத்துவிர்கள் என்றால் தேவை.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - `request.form()` மூலம் <abbr title="HTTP வேண்டுதலில் வரும் சரத்ததை பைத்தான் தரவாக மாற்றுதல்">"பாகுபடுத்துதல்"</abbr> துனை தேவை என்றால் பயன்படுத்துங்கள்.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>அபாயமானது</code></a> - `SessionMiddleware` துனைக்கு தேவை.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - ஸ்டார்லெட்டின் `SchemaGenerator` துனைக்கு தேவை (பெரும்பாலான சமையங்களில் FastAPIயுடன் தேவையில்லை).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` பயன்படுத்துவிர்கள் என்றால் தேவை.

FastAPI / ஸ்டார்லெட் பயன்படுத்துவது::

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - சேவகம் செயழியை ஏற்றி மற்றும் சேவை செய்வதற்க்கு.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` பயன்படுத்துவிர்கள் என்றால் தேவை..

இவை அனைத்தையும் `pip install "fastapi[all]"` கட்டளை மூலம் நிறுவலாம்.

## உரிமம்

இந்த வேலை MIT உரிமம் கொண்டுள்ளது.
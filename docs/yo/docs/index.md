# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Ìlànà wẹ́ẹ́bù FastAPI, iṣẹ́ gíga, ó rọrùn láti kọ̀, o yára láti kóòdù, ó sì ṣetán fún iṣelọpọ ní lílo</em>
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

**Àkọsílẹ̀**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Orisun Kóòdù**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI jẹ́ ìgbàlódé, tí ó yára (iṣẹ-giga), ìlànà wẹ́ẹ́bù fún kikọ àwọn API pẹ̀lú Python èyí tí ó da lori àwọn ìtọ́kasí àmì irúfẹ́ Python.

Àwọn ẹya pàtàkì ni:

* **Ó yára**: Iṣẹ tí ó ga púpọ̀, tí ó wa ni ibamu pẹ̀lú **NodeJS** àti **Go** (ọpẹ si Starlette àti Pydantic). [Ọkan nínú àwọn ìlànà Python ti o yára jùlọ ti o wa](#isesi).
* **Ó yára láti kóòdù**: O mu iyara pọ si láti kọ àwọn ẹya tuntun kóòdù nipasẹ "Igba ìdá ọgọ́rùn-ún" (i.e. 200%) si "ọ̀ọ́dúrún ìdá ọgọ́rùn-ún" (i.e. 300%).
* **Àìtọ́ kékeré**: O n din aṣiṣe ku bi ọgbon ìdá ọgọ́rùn-ún (i.e. 40%) ti eda eniyan (oṣiṣẹ kóòdù) fa. *
* **Ọgbọ́n àti ìmọ̀**: Atilẹyin olootu nla. <abbr title="a tun le pe ni olùrànlọ́wọ́ alaifiọwọkan alaifọwọyi, olùpari iṣẹ-ṣiṣe, Oloye">Ìparí</abbr> nibi gbogbo. Àkókò díẹ̀ nipa wíwá ibi tí ìṣòro kóòdù wà.
* **Irọrun**: A kọ kí ó le rọrun láti lo àti láti kọ ẹkọ nínú rè. Ó máa fún ọ ní àkókò díẹ̀ látı ka àkọsílẹ.
* **Ó kúkurú ní kikọ**: Ó dín àtúnkọ àti àtúntò kóòdù kù. Ìkéde àṣàyàn kọ̀ọ̀kan nínú rẹ̀ ní ọ̀pọ̀lọpọ̀ àwọn ìlò. O ṣe iranlọwọ láti má ṣe ní ọ̀pọ̀lọpọ̀ àṣìṣe.
* **Ó lágbára**: Ó ń ṣe àgbéjáde kóòdù tí ó ṣetán fún ìṣelọ́pọ̀. Pẹ̀lú àkọsílẹ̀ tí ó máa ṣàlàyé ara rẹ̀ fún ẹ ní ìbáṣepọ̀ aládàáṣiṣẹ́ pẹ̀lú rè.
* **Ajohunše/Ìtọ́kasí**: Ó da lori (àti ibamu ni kikun pẹ̀lú) àwọn ìmọ ajohunše/ìtọ́kasí fún àwọn API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (èyí tí a mọ tẹlẹ si Swagger) àti <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* iṣiro yi da lori àwọn idanwo tí ẹgbẹ ìdàgbàsókè FastAPI ṣe, nígbàtí wọn kọ àwọn ohun elo iṣelọpọ kóòdù pẹ̀lú rẹ.</small>

## Àwọn onígbọ̀wọ́

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Àwọn onígbọ̀wọ́ míràn</a>

## Àwọn ero àti èsì

"_[...] Mò ń lo **FastAPI** púpọ̀ ní lẹ́nu àìpẹ́ yìí. [...] Mo n gbero láti lo o pẹ̀lú àwọn ẹgbẹ mi fún gbogbo iṣẹ **ML wa ni Microsoft**. Diẹ nínú wọn ni afikun ti ifilelẹ àwọn ẹya ara ti ọja **Windows** wa pẹ̀lú àwọn ti **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_A gba àwọn ohun èlò ìwé afọwọkọ **FastAPI** tí kò yí padà láti ṣẹ̀dá olùpín **REST** tí a lè béèrè lọ́wọ́ rẹ̀ láti gba **àsọtẹ́lẹ̀**. [fún Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** ni inudidun láti kede itusilẹ orisun kóòdù ti ìlànà iṣọkan **iṣakoso Ìṣòro** wa: **Ìfiránṣẹ́**! [a kọ pẹ̀lú **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Inú mi dùn púpọ̀ nípa **FastAPI**. Ó mú inú ẹnì dùn púpọ̀!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Ní tòótọ́, ohun tí o kọ dára ó sì tún dán. Ní ọ̀pọ̀lọpọ̀ ọ̀nà, ohun tí mo fẹ́ kí **Hug** jẹ́ nìyẹn - ó wúni lórí gan-an láti rí ẹnìkan tí ó kọ́ nǹkan bí èyí._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Ti o ba n wa láti kọ ọkan **ìlànà igbalode** fún kikọ àwọn REST API, ṣayẹwo **FastAPI** [...] Ó yára, ó rọrùn láti lò, ó sì rọrùn láti kọ́[...]_"

"_A ti yipada si **FastAPI** fún **APIs** wa [...] Mo lérò pé wà á fẹ́ràn rẹ̀ [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Ti ẹnikẹni ba n wa láti kọ iṣelọpọ API pẹ̀lú Python, èmi yóò ṣe'dúró fún **FastAPI**. Ó jẹ́ ohun tí **àgbékalẹ̀ rẹ̀ lẹ́wà**, **ó rọrùn láti lò** àti wipe ó ni **ìwọ̀n gíga**, o tí dí **bọtini paati** nínú alakọkọ API ìdàgbàsókè kikọ fún wa, àti pe o ni ipa lori adaṣiṣẹ àti àwọn iṣẹ gẹ́gẹ́ bíi Onímọ̀-ẹ̀rọ TAC tí órí Íńtánẹ́ẹ̀tì_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI ti CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Ti o ba n kọ ohun èlò <abbr title="Command Line Interface">CLI</abbr> láti ṣeé lọ nínú ohun èlò lori ebute kọmputa dipo API, ṣayẹwo <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** jẹ́ àbúrò ìyá FastAPI kékeré. Àti pé wọ́n kọ́ láti jẹ́ **FastAPI ti CLIs**. ⌨️ 🚀

## Èròjà

FastAPI dúró lórí àwọn èjìká tí àwọn òmíràn:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> fún àwọn ẹ̀yà ayélujára.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> fún àwọn ẹ̀yà àkójọf'áyẹ̀wò.

## Fifi sórí ẹrọ

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>
Iwọ yóò tún nílò olupin ASGI, fún iṣelọpọ bii <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> tabi <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Àpẹẹrẹ

### Ṣẹ̀dá rẹ̀

* Ṣẹ̀dá fáìlì `main.py (èyí tíí ṣe, akọkọ.py)` pẹ̀lú:

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
<summary>Tàbí lò <code>async def</code>...</summary>

Tí kóòdù rẹ̀ bá ń lò `async` / `await`, lò `async def`:

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

**Akiyesi**:

Tí o kò bá mọ̀, ṣàyẹ̀wò ibi tí a ti ní _"In a hurry?"_ (i.e. _"Ní kíákíá?"_) nípa <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` and `await` nínú àkọsílẹ̀</a>.

</details>

### Mu ṣiṣẹ

Mú olupin ṣiṣẹ pẹ̀lú:

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
<summary>Nipa aṣẹ kóòdù náà <code>uvicorn main:app --reload</code>...</summary>

Àṣẹ `uvicorn main:app` ń tọ́ka sí:

* `main`: fáìlì náà 'main.py' (Python "module").
* `app` jẹ object( i.e. nǹkan) tí a ṣẹ̀dá nínú `main.py` pẹ̀lú ilà `app = FastAPI()`.
* `--reload`: èyí yóò jẹ́ ki olupin tún bẹ̀rẹ̀ lẹ́hìn àwọn àyípadà kóòdù. Jọ̀wọ́, ṣe èyí fún ìdàgbàsókè kóòdù nìkan, má ṣe é ṣe lori àgbéjáde kóòdù tabi fún iṣelọpọ kóòdù.


</details>

### Ṣayẹwo rẹ

Ṣii aṣàwákiri kọ̀ǹpútà rẹ ni <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Ìwọ yóò sì rí ìdáhùn JSON bíi:

```JSON
{"item_id": 5, "q": "somequery"}
```

O tí ṣẹ̀dá API èyí tí yóò:

* Gbà àwọn ìbéèrè HTTP ni àwọn _ipa ọ̀nà_ `/` àti `/items/{item_id}`.
* Èyí tí àwọn _ipa ọ̀nà_ (i.e. _paths_) méjèèjì gbà àwọn <em>iṣẹ</em> `GET` (a tun mọ si _àwọn ọna_ HTTP).
* Èyí tí _ipa ọ̀nà_  (i.e. _paths_) `/items/{item_id}` ní _àwọn ohun-ini ipa ọ̀nà_ tí ó yẹ kí ó jẹ́ `int` i.e. `ÒǸKÀ`.
* Èyí tí _ipa ọ̀nà_  (i.e. _paths_) `/items/{item_id}` ní àṣàyàn `str` _àwọn ohun-ini_ (i.e. _query parameter_) `q`.

### Ìbáṣepọ̀ àkọsílẹ̀ API

Ní báyìí, lọ sí <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Lẹ́yìn náà, iwọ yóò rí ìdáhùn àkọsílẹ̀ API tí ó jẹ́ ìbáṣepọ̀ alaifọwọyi/aládàáṣiṣẹ́ (tí a pèṣè nípaṣẹ̀ <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Ìdàkejì àkọsílẹ̀ API

Ní báyìí, lọ sí <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Wà á rí àwọn àkọsílẹ̀ aládàáṣiṣẹ́ mìíràn (tí a pese nipasẹ <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Àpẹẹrẹ ìgbésókè mìíràn

Ní báyìí ṣe àtúnṣe fáìlì `main.py` láti gba kókó èsì láti inú ìbéèrè `PUT`.

Ní báyìí, ṣe ìkéde kókó èsì API nínú kóòdù rẹ nipa lílo àwọn ìtọ́kasí àmì irúfẹ́ Python, ọpẹ́ pàtàkìsi sí Pydantic.

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

Olupin yóò tún ṣe àtúnṣe laifọwọyi/aládàáṣiṣẹ́ (nítorí wípé ó se àfikún `-reload` si àṣẹ kóòdù `uvicorn` lókè).

### Ìbáṣepọ̀ ìgbésókè àkọsílẹ̀ API

Ní báyìí, lọ sí <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Ìbáṣepọ̀ àkọsílẹ̀ API yóò ṣe imudojuiwọn àkọsílẹ̀ API laifọwọyi, pẹ̀lú kókó èsì ìdáhùn API tuntun:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Tẹ bọtini "Gbiyanju rẹ" i.e. "Try it out", yóò gbà ọ́ láàyè láti jẹ́ kí ó tẹ́ àlàyé tí ó nílò kí ó le sọ̀rọ̀ tààrà pẹ̀lú API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Lẹhinna tẹ bọtini "Ṣiṣe" i.e. "Execute", olùmúlò (i.e. user interface) yóò sọrọ pẹ̀lú API rẹ, yóò ṣe afiranṣẹ àwọn èròjà, pàápàá jùlọ yóò gba àwọn àbájáde yóò si ṣafihan wọn loju ìbòjú:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Ìdàkejì ìgbésókè àkọsílẹ̀ API

Ní báyìí, lọ sí <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Ìdàkejì àkọsílẹ̀ API yóò ṣ'afihan ìbéèrè èròjà/pàrámítà tuntun àti kókó èsì ti API:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Àtúnyẹ̀wò

Ni akopọ, ìwọ yóò kéde ni **kete** àwọn iru èròjà/pàrámítà, kókó èsì API, abbl (i.e. àti bẹbẹ lọ), bi àwọn èròjà iṣẹ.

O ṣe ìyẹn pẹ̀lú irúfẹ́ àmì ìtọ́kasí ìgbàlódé Python.

O ò nílò láti kọ́ síńtáàsì tuntun, ìlànà tàbí ọ̀wọ́ kíláàsì kan pàtó, abbl (i.e. àti bẹbẹ lọ).

Ìtọ́kasí **Python**

Fún àpẹẹrẹ, fún `int`:

```Python
item_id: int
```

tàbí fún àwòṣe `Item` tí ó nira díẹ̀ síi:

```Python
item: Item
```

... àti pẹ̀lú ìkéde kan ṣoṣo yẹn ìwọ yóò gbà:

* Atilẹyin olootu, pẹ̀lú:
    * Pipari.
    * Àyẹ̀wò irúfẹ́ àmì ìtọ́kasí.
* Ìfọwọ́sí àkójọf'áyẹ̀wò (i.e. data):
    * Aṣiṣe alaifọwọyi/aládàáṣiṣẹ́ àti aṣiṣe ti ó hàn kedere nígbàtí àwọn àkójọf'áyẹ̀wò (i.e. data) kò wulo tabi tí kò fẹsẹ̀ múlẹ̀.
    * Ìfọwọ́sí fún ohun elo JSON tí ó jìn gan-an.
* <abbr title="also known as: serialization, parsing, marshalling">Ìyípadà</abbr> tí input àkójọf'áyẹ̀wò: tí ó wà láti nẹtiwọọki si àkójọf'áyẹ̀wò àti irúfẹ́ àmì ìtọ́kasí Python. Ó ń ka láti:
    * JSON.
    * èròjà ọ̀nà tí ò gbé gbà.
    * èròjà ìbéèrè.
    * Àwọn Kúkì
    * Àwọn Àkọlé
    * Àwọn Fọọmu
    * Àwọn Fáìlì
* <abbr title="a tún má ń pè ni: serialization, parsing, marshalling">Ìyípadà</abbr> èsì àkójọf'áyẹ̀wò: yíyípadà láti àkójọf'áyẹ̀wò àti irúfẹ́ àmì ìtọ́kasí Python si nẹtiwọọki (gẹ́gẹ́ bí JSON):
    * Yí irúfẹ́ àmì ìtọ́kasí padà (`str`, `int`, `float`, `bool`, `list`, abbl i.e. àti bèbè ló).
    * Àwọn ohun èlò `datetime`.
    * Àwọn ohun èlò `UUID`.
    * Àwọn awoṣẹ́ ibi ìpamọ́ àkójọf'áyẹ̀wò.
    * ...àti ọ̀pọ̀lọpọ̀ díẹ̀ síi.
* Ìbáṣepọ̀ àkọsílẹ̀ API aládàáṣiṣẹ́, pẹ̀lú ìdàkejì àgbékalẹ̀-àwọn-olùmúlò (i.e user interfaces) méjì:
    * Àgbékalẹ̀-olùmúlò Swagger.
    * ReDoc.

---

Nisinsin yi, tí ó padà sí àpẹẹrẹ ti tẹ́lẹ̀, **FastAPI** yóò:

* Fọwọ́ sí i pé `item_id` wà nínú ọ̀nà ìbéèrè HTTP fún `GET` àti `PUT`.
* Fọwọ́ sí i pé `item_id` jẹ́ irúfẹ́ àmì ìtọ́kasí `int` fún ìbéèrè HTTP `GET` àti `PUT`.
    * Tí kìí bá ṣe bẹ, oníbàárà yóò ríi àṣìṣe tí ó wúlò, kedere.
* Ṣàyẹ̀wò bóyá ìbéèrè àṣàyàn pàrámítà kan wà tí orúkọ rẹ̀ ń jẹ́ `q` (gẹ́gẹ́ bíi `http://127.0.0.1:8000/items/foo?q=somequery`) fún ìbéèrè HTTP `GET`.
    * Bí wọ́n ṣe kéde pàrámítà `q` pẹ̀lú `= None`, ó jẹ́ àṣàyàn (i.e optional).
    * Láìsí `None` yóò nílò (gẹ́gẹ́ bí kókó èsì ìbéèrè HTTP ṣe wà pẹ̀lú `PUT`).
* Fún àwọn ìbéèrè HTTP `PUT` sí `/items/{item_id}`, kà kókó èsì ìbéèrè HTTP gẹ́gẹ́ bí JSON:
    * Ṣàyẹ̀wò pé ó ní àbùdá tí ó nílò èyí tíí ṣe `name` i.e. `orúkọ` tí ó yẹ kí ó jẹ́ `str`.
    * Ṣàyẹ̀wò pé ó ní àbùdá tí ó nílò èyí tíí ṣe `price` i.e. `iye` tí ó gbọ́dọ̀ jẹ́ `float`.
    * Ṣàyẹ̀wò pé ó ní àbùdá àṣàyàn `is_offer`, tí ó yẹ kí ó jẹ́ `bool`, tí ó bá wà níbẹ̀.
    * Gbogbo èyí yóò tún ṣiṣẹ́ fún àwọn ohun èlò JSON tí ó jìn gidi gan-an.
* Yìí padà láti àti sí JSON lai fi ọwọ́ yi.
* Ṣe àkọsílẹ̀ ohun gbogbo pẹ̀lú OpenAPI, èyí tí yóò wà ní lílo nípaṣẹ̀:
    * Àwọn ètò àkọsílẹ̀ ìbáṣepọ̀.
    * Aládàáṣiṣẹ́ oníbárà èlètò tíí ṣẹ̀dá kóòdù, fún ọ̀pọ̀lọpọ̀ àwọn èdè.
* Pese àkọsílẹ̀ òní ìbáṣepọ̀ ti àwọn àgbékalẹ̀ ayélujára méjì tààrà.

---

A ń ṣẹ̀ṣẹ̀ ń mú ẹyẹ bọ́ làpò ní, ṣùgbọ́n ó ti ni òye bí gbogbo rẹ̀ ṣe ń ṣiṣẹ́.

Gbiyanju láti yí ìlà padà pẹ̀lú:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...láti:

```Python
        ... "item_name": item.name ...
```

...ṣí:

```Python
        ... "item_price": item.price ...
```

.. kí o sì wo bí olóòtú rẹ yóò ṣe parí àwọn àbùdá náà fúnra rẹ̀, yóò sì mọ irúfẹ́ wọn:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Fún àpẹẹrẹ pípé síi pẹ̀lú àwọn àbùdá mìíràn, wo <a href="https://fastapi.tiangolo.com/tutorial/">Ìdánilẹ́kọ̀ọ́ - Ìtọ́sọ́nà Olùmúlò</a>.

**Itaniji gẹ́gẹ́ bí isọ'ye**: ìdánilẹ́kọ̀ọ́ - itọsọna olùmúlò pẹ̀lú:

* Ìkéde àṣàyàn **pàrámítà** láti àwọn oriṣiriṣi ibòmíràn gẹ́gẹ́ bíi: àwọn **àkọlé èsì API**, **kúkì**, **ààyè fọọmu**, àti **fáìlì**.
* Bíi ó ṣe lé ṣètò **àwọn ìdíwọ́ ìfọwọ́sí** bí `maximum_length` tàbí `regex`.
* Ó lágbára púpọ̀ ó sì rọrùn láti lo ètò **<abbr title="a tún mọ̀ sí ìrìnṣẹ́, àwọn ohun àmúlò iṣẹ́, olupese, àwọn ohun àfikún ">Àfikún Ìgbẹ́kẹ̀lé Kóòdù</abbr>**.
* Ààbò àti ìfọwọ́sowọ́pọ̀, pẹ̀lú àtìlẹ́yìn fún **OAuth2** pẹ̀lú **àmì JWT** àti **HTTP Ipilẹ ìfọwọ́sowọ́pọ̀**.
* Àwọn ìlànà ìlọsíwájú (ṣùgbọ́n tí ó rọrùn bákan náà) fún ìkéde **àwọn àwòṣe JSON tó jinlẹ̀** (ọpẹ́ pàtàkìsi sí Pydantic).
* Iṣọpọ **GraphQL** pẹ̀lú <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> àti àwọn ohun èlò ìwé kóòdù afọwọkọ mìíràn tí kò yí padà.
* Ọpọlọpọ àwọn àfikún àwọn ẹ̀yà (ọpẹ́ pàtàkìsi sí Starlette) bí:
    * **WebSockets**
    * àwọn ìdánwò tí ó rọrùn púpọ̀ lórí HTTPX àti `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...àti síwájú síi.

## Ìṣesí

Àwọn àlá TechEmpower fi hàn pé **FastAPI** ń ṣiṣẹ́ lábẹ́ Uvicorn gẹ́gẹ́ bí <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">ọ̀kan lára àwọn ìlànà Python tí ó yára jùlọ tí ó wà</a>, ní ìsàlẹ̀ Starlette àti Uvicorn fúnra wọn (tí FastAPI ń lò fúnra rẹ̀). (*)

Láti ní òye síi nípa rẹ̀, wo abala àwọn <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Àlá</a>.

## Àṣàyàn Àwọn Àfikún Ìgbẹ́kẹ̀lé Kóòdù

Èyí tí Pydantic ń lò:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - fún ifọwọsi ímeèlì.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - fún ètò ìsàkóso.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - fún àfikún oríṣi láti lọ pẹ̀lú Pydantic.

Èyí tí Starlette ń lò:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Nílò tí ó bá fẹ́ láti lọ `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Nílò tí ó bá fẹ́ láti lọ iṣeto awoṣe aiyipada.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Nílò tí ó bá fẹ́ láti ṣe àtìlẹ́yìn fún <abbr title="tí ó se ìyípadà ọ̀rọ̀-ìyọ̀/òkun-ọ̀rọ̀ tí ó wà láti ìbéèrè HTTP sí inú àkójọf'áyẹ̀wò Python">"àyẹ̀wò"</abbr> fọọmu, pẹ̀lú `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Nílò fún àtìlẹ́yìn `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Nílò fún àtìlẹ́yìn Starlette's `SchemaGenerator` (ó ṣe ṣe kí ó má nílò rẹ̀ fún FastAPI).

Èyí tí FastAPI / Starlette ń lò:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Fún olupin tí yóò sẹ́ àmúyẹ àti tí yóò ṣe ìpèsè fún iṣẹ́ rẹ tàbí ohun èlò rẹ.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Nílò tí ó bá fẹ́ láti lọ `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Nílò tí ó bá fẹ́ láti lọ `UJSONResponse`.

Ó lè fi gbogbo àwọn wọ̀nyí sórí ẹrọ pẹ̀lú `pip install "fastapi[all]"`.

## Iwe-aṣẹ

Iṣẹ́ yìí ni iwe-aṣẹ lábẹ́ àwọn òfin tí iwe-aṣẹ MIT.

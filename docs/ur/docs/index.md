# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework، اعلیٰ کارکردگی، سیکھنے میں آسان، تیز کوڈنگ، پروڈکشن کے لیے تیار</em>
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

**دستاویزات**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**سورس کوڈ**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI ایک جدید، تیز رفتار (اعلیٰ کارکردگی والا) web framework ہے جو معیاری Python type hints کی بنیاد پر Python کے ساتھ APIs بنانے کے لیے بنایا گیا ہے۔

اہم خصوصیات یہ ہیں:

* **تیز**: بہت اعلیٰ کارکردگی، **NodeJS** اور **Go** کے برابر (Starlette اور Pydantic کی بدولت)۔ [دستیاب تیز ترین Python frameworks میں سے ایک](#performance)۔
* **تیز کوڈنگ**: فیچرز بنانے کی رفتار تقریباً 200% سے 300% بڑھائیں۔ *
* **کم غلطیاں**: انسانی (ڈویلپر) غلطیوں میں تقریباً 40% کمی۔ *
* **بدیہی**: بہترین ایڈیٹر سپورٹ۔ ہر جگہ <dfn title="also known as auto-complete, autocompletion, IntelliSense">Completion</dfn>۔ debugging میں کم وقت۔
* **آسان**: استعمال اور سیکھنے میں آسان بنایا گیا ہے۔ دستاویزات پڑھنے میں کم وقت۔
* **مختصر**: code کی تکرار کم سے کم۔ ہر parameter کے اعلان سے متعدد خصوصیات۔ کم غلطیاں۔
* **مضبوط**: پروڈکشن کے لیے تیار code حاصل کریں۔ خودکار تعاملی دستاویزات کے ساتھ۔
* **معیارات پر مبنی**: APIs کے کھلے معیارات پر مبنی (اور مکمل طور پر ہم آہنگ): [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (پہلے Swagger کے نام سے جانا جاتا تھا) اور [JSON Schema](https://json-schema.org/)۔

<small>* اندرونی ترقیاتی ٹیم کے ذریعے پروڈکشن ایپلیکیشنز بناتے ہوئے کیے گئے ٹیسٹس پر مبنی تخمینہ۔</small>

## سپانسرز { #sponsors }

<!-- sponsors -->

### کلیدی سپانسر { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### گولڈ اور سلور سپانسرز { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[دیگر سپانسرز](https://fastapi.tiangolo.com/fastapi-people/#sponsors)

## آراء { #opinions }

"_[...] میں ان دنوں **FastAPI** بہت زیادہ استعمال کر رہا ہوں۔ [...] میں دراصل اسے اپنی ٹیم کی **Microsoft میں تمام ML services** کے لیے استعمال کرنے کا ارادہ رکھتا ہوں۔ ان میں سے کچھ بنیادی **Windows** پروڈکٹ اور کچھ **Office** پروڈکٹس میں شامل ہو رہی ہیں۔_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_ہم نے **FastAPI** لائبریری اپنائی تاکہ ایک **REST** server بنایا جا سکے جس سے **predictions** حاصل کی جا سکیں۔ [Ludwig کے لیے]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** اپنے **بحران کے انتظام** کے آرکیسٹریشن framework: **Dispatch** کی اوپن سورس ریلیز کا اعلان کرتے ہوئے خوش ہے! [**FastAPI** سے بنایا گیا]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_میں **FastAPI** سے بے حد خوش ہوں۔ یہ بہت مزے کا ہے!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

"_سچ میں، جو آپ نے بنایا ہے وہ بہت مضبوط اور چمکدار لگتا ہے۔ کئی طرح سے، یہ وہی ہے جو میں **Hug** کو بنانا چاہتا تھا - کسی کو یہ بناتے دیکھنا واقعی حوصلہ افزا ہے۔_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug">Hug</a> کے خالق</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

"_اگر آپ REST APIs بنانے کے لیے ایک **جدید framework** سیکھنا چاہتے ہیں، تو **FastAPI** دیکھیں [...] یہ تیز، استعمال میں آسان اور سیکھنے میں آسان ہے [...]_"

"_ہم نے اپنی **APIs** کے لیے **FastAPI** اپنا لیا ہے [...] مجھے لگتا ہے آپ کو یہ پسند آئے گا [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai">Explosion AI</a> بانی - <a href="https://spacy.io">spaCy</a> تخلیق کار</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

"_اگر کوئی پروڈکشن Python API بنانا چاہتا ہے، تو میں **FastAPI** کی بہت سفارش کروں گا۔ یہ **خوبصورتی سے ڈیزائن کیا گیا** ہے، **استعمال میں آسان** اور **انتہائی قابل توسیع** ہے، یہ ہماری API first ترقیاتی حکمت عملی کا **اہم جزو** بن گیا ہے اور بہت سی automations اور services جیسے ہمارا Virtual TAC Engineer چلا رہا ہے۔_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## FastAPI مختصر دستاویزی فلم { #fastapi-mini-documentary }

2025 کے آخر میں ریلیز ہونے والی [FastAPI مختصر دستاویزی فلم](https://www.youtube.com/watch?v=mpR8ngthqiE) ہے، آپ اسے آن لائن دیکھ سکتے ہیں:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**، CLIs کا FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

اگر آپ web API کے بجائے ٹرمینل میں استعمال ہونے والی <abbr title="Command Line Interface">CLI</abbr> ایپ بنا رہے ہیں، تو [**Typer**](https://typer.tiangolo.com/) دیکھیں۔

**Typer** FastAPI کا چھوٹا بھائی ہے۔ اور اس کا مقصد **CLIs کا FastAPI** بننا ہے۔ ⌨️ 🚀

## تقاضے { #requirements }

FastAPI دیو ہیکل ہستیوں کے کندھوں پر کھڑا ہے:

* ویب حصوں کے لیے [Starlette](https://www.starlette.dev/)۔
* ڈیٹا حصوں کے لیے [Pydantic](https://docs.pydantic.dev/)۔

## انسٹالیشن { #installation }

ایک [virtual environment](https://fastapi.tiangolo.com/virtual-environments/) بنائیں اور فعال کریں اور پھر FastAPI انسٹال کریں:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**نوٹ**: یقینی بنائیں کہ آپ `"fastapi[standard]"` کو quotes میں لکھیں تاکہ یہ تمام ٹرمینلز میں کام کرے۔

## مثال { #example }

### بنائیں { #create-it }

ایک فائل `main.py` بنائیں:

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
<summary>یا <code>async def</code> استعمال کریں...</summary>

اگر آپ کا code `async` / `await` استعمال کرتا ہے، تو `async def` استعمال کریں:

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

**نوٹ**:

اگر آپ نہیں جانتے، تو دستاویزات میں [`async` اور `await`](https://fastapi.tiangolo.com/async/#in-a-hurry) کے بارے میں _"جلدی میں ہیں؟"_ سیکشن دیکھیں۔

</details>

### چلائیں { #run-it }

server کو اس کمانڈ سے چلائیں:

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
<summary><code>fastapi dev</code> کمانڈ کے بارے میں...</summary>

`fastapi dev` کمانڈ خودکار طور پر آپ کی `main.py` فائل پڑھتی ہے، اس میں **FastAPI** ایپ تلاش کرتی ہے، اور [Uvicorn](https://www.uvicorn.dev) استعمال کر کے server شروع کرتی ہے۔

بطور ڈیفالٹ، `fastapi dev` مقامی ترقی کے لیے auto-reload فعال کر کے شروع ہوگا۔

آپ اس کے بارے میں [FastAPI CLI دستاویزات](https://fastapi.tiangolo.com/fastapi-cli/) میں مزید پڑھ سکتے ہیں۔

</details>

### دیکھیں { #check-it }

اپنا براؤزر [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery) پر کھولیں۔

آپ کو JSON response اس طرح نظر آئے گا:

```JSON
{"item_id": 5, "q": "somequery"}
```

آپ نے پہلے ہی ایک API بنا لیا ہے جو:

* _paths_ `/` اور `/items/{item_id}` پر HTTP requests وصول کرتا ہے۔
* دونوں _paths_ `GET` <em>operations</em> (جنہیں HTTP _methods_ بھی کہا جاتا ہے) لیتے ہیں۔
* _path_ `/items/{item_id}` میں ایک _path parameter_ `item_id` ہے جو `int` ہونا چاہیے۔
* _path_ `/items/{item_id}` میں ایک اختیاری `str` _query parameter_ `q` ہے۔

### تعاملی API دستاویزات { #interactive-api-docs }

اب [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر جائیں۔

آپ کو خودکار تعاملی API دستاویزات نظر آئیں گی ([Swagger UI](https://github.com/swagger-api/swagger-ui) کی فراہم کردہ):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### متبادل API دستاویزات { #alternative-api-docs }

اور اب، [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) پر جائیں۔

آپ کو متبادل خودکار دستاویزات نظر آئیں گی ([ReDoc](https://github.com/Rebilly/ReDoc) کی فراہم کردہ):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## مثال کی اپ گریڈ { #example-upgrade }

اب فائل `main.py` میں ترمیم کریں تاکہ `PUT` request سے body وصول کیا جا سکے۔

Pydantic کی بدولت معیاری Python types استعمال کر کے body بیان کریں۔

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

`fastapi dev` server خودکار طور پر reload ہو جائے گا۔

### تعاملی API دستاویزات کی اپ گریڈ { #interactive-api-docs-upgrade }

اب [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) پر جائیں۔

* تعاملی API دستاویزات خودکار طور پر اپ ڈیٹ ہو جائیں گی، نئی body سمیت:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" بٹن پر کلک کریں، یہ آپ کو parameters بھرنے اور API کے ساتھ براہ راست تعامل کرنے کی اجازت دیتا ہے:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* پھر "Execute" بٹن پر کلک کریں، یوزر انٹرفیس آپ کی API سے بات کرے گا، parameters بھیجے گا، نتائج حاصل کرے گا اور انہیں اسکرین پر دکھائے گا:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### متبادل API دستاویزات کی اپ گریڈ { #alternative-api-docs-upgrade }

اور اب، [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) پر جائیں۔

* متبادل دستاویزات بھی نئے query parameter اور body کی عکاسی کریں گی:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### خلاصہ { #recap }

خلاصہ یہ کہ، آپ parameters، body وغیرہ کی types **ایک بار** function parameters کے طور پر بیان کرتے ہیں۔

آپ یہ معیاری جدید Python types کے ساتھ کرتے ہیں۔

آپ کو کوئی نئی syntax، کسی مخصوص لائبریری کے methods یا classes سیکھنے کی ضرورت نہیں۔

بس معیاری **Python**۔

مثال کے طور پر، ایک `int` کے لیے:

```Python
item_id: int
```

یا ایک زیادہ پیچیدہ `Item` model کے لیے:

```Python
item: Item
```

...اور اس ایک اعلان کے ساتھ آپ کو ملتا ہے:

* ایڈیٹر سپورٹ، بشمول:
    * Completion۔
    * Type checks۔
* ڈیٹا کی توثیق:
    * ڈیٹا غلط ہونے پر خودکار اور واضح غلطیاں۔
    * گہرائی سے nested JSON objects کی بھی توثیق۔
* ان پٹ ڈیٹا کی <dfn title="also known as: serialization, parsing, marshalling">تبدیلی</dfn>: نیٹ ورک سے Python ڈیٹا اور types میں۔ پڑھنا:
    * JSON۔
    * Path parameters۔
    * Query parameters۔
    * Cookies۔
    * Headers۔
    * Forms۔
    * Files۔
* آؤٹ پٹ ڈیٹا کی <dfn title="also known as: serialization, parsing, marshalling">تبدیلی</dfn>: Python ڈیٹا اور types سے نیٹ ورک ڈیٹا (بطور JSON) میں:
    * Python types تبدیل کریں (`str`, `int`, `float`, `bool`, `list`, وغیرہ)۔
    * `datetime` objects۔
    * `UUID` objects۔
    * Database models۔
    * ...اور بہت کچھ۔
* خودکار تعاملی API دستاویزات، بشمول 2 متبادل یوزر انٹرفیسز:
    * Swagger UI۔
    * ReDoc۔

---

پچھلی code مثال کی طرف واپس آتے ہوئے، **FastAPI** یہ کرے گا:

* `GET` اور `PUT` requests کے لیے path میں `item_id` ہونے کی توثیق کرے گا۔
* `GET` اور `PUT` requests کے لیے `item_id` کی type `int` ہونے کی توثیق کرے گا۔
    * اگر نہیں ہے، تو client کو ایک مفید، واضح غلطی نظر آئے گی۔
* `GET` requests کے لیے چیک کرے گا کہ کوئی اختیاری query parameter بنام `q` ہے (جیسا کہ `http://127.0.0.1:8000/items/foo?q=somequery`)۔
    * چونکہ `q` parameter کو `= None` کے ساتھ بیان کیا گیا ہے، اس لیے یہ اختیاری ہے۔
    * `None` کے بغیر یہ لازمی ہوتا (جیسا کہ `PUT` کے معاملے میں body ہے)۔
* `/items/{item_id}` کے لیے `PUT` requests میں، body کو بطور JSON پڑھے گا:
    * چیک کرے گا کہ اس میں لازمی attribute `name` ہے جو `str` ہونا چاہیے۔
    * چیک کرے گا کہ اس میں لازمی attribute `price` ہے جو `float` ہونا ضروری ہے۔
    * چیک کرے گا کہ اس میں اختیاری attribute `is_offer` ہے، جو اگر موجود ہو تو `bool` ہونا چاہیے۔
    * یہ سب گہرائی سے nested JSON objects کے لیے بھی کام کرے گا۔
* خودکار طور پر JSON سے اور JSON میں تبدیل کرے گا۔
* OpenAPI کے ساتھ ہر چیز کی دستاویز بنائے گا، جو استعمال ہو سکتی ہے:
    * تعاملی دستاویزاتی نظاموں سے۔
    * کئی زبانوں کے لیے خودکار client code generation نظاموں سے۔
* 2 تعاملی دستاویزاتی ویب انٹرفیسز براہ راست فراہم کرے گا۔

---

ہم نے ابھی صرف سطح کو چھوا ہے، لیکن آپ کو پہلے سے اندازہ ہو گیا ہے کہ یہ سب کیسے کام کرتا ہے۔

اس لائن کو تبدیل کر کے دیکھیں:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...اس سے:

```Python
        ... "item_name": item.name ...
```

...اس میں:

```Python
        ... "item_price": item.price ...
```

...اور دیکھیں کہ آپ کا ایڈیٹر attributes کو خود مکمل کرے گا اور ان کی types جانے گا:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

مزید خصوصیات سمیت ایک زیادہ مکمل مثال کے لیے، <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a> دیکھیں۔

**اسپائلر الرٹ**: tutorial - user guide میں شامل ہے:

* مختلف جگہوں سے **parameters** کا اعلان جیسے: **headers**، **cookies**، **form fields** اور **files**۔
* `maximum_length` یا `regex` جیسی **توثیقی حدود** مقرر کرنے کا طریقہ۔
* ایک بہت طاقتور اور استعمال میں آسان **<dfn title="also known as components, resources, providers, services, injectables">Dependency Injection</dfn>** سسٹم۔
* سیکیورٹی اور تصدیق، بشمول **OAuth2** بمع **JWT tokens** اور **HTTP Basic** auth کی سپورٹ۔
* **گہرائی سے nested JSON models** بیان کرنے کی مزید ایڈوانسڈ (لیکن اتنی ہی آسان) تکنیکیں (Pydantic کی بدولت)۔
* [Strawberry](https://strawberry.rocks) اور دیگر لائبریریز کے ساتھ **GraphQL** انضمام۔
* (Starlette کی بدولت) بہت سی اضافی خصوصیات جیسے:
    * **WebSockets**
    * HTTPX اور `pytest` پر مبنی انتہائی آسان ٹیسٹس
    * **CORS**
    * **Cookie Sessions**
    * ...اور مزید۔

### اپنی ایپ deploy کریں (اختیاری) { #deploy-your-app-optional }

آپ اختیاری طور پر اپنی FastAPI ایپ کو [FastAPI Cloud](https://fastapicloud.com) پر deploy کر سکتے ہیں، اگر ابھی تک نہیں کیا تو ویٹنگ لسٹ میں شامل ہو جائیں۔ 🚀

اگر آپ کے پاس پہلے سے **FastAPI Cloud** اکاؤنٹ ہے (ہم نے آپ کو ویٹنگ لسٹ سے مدعو کیا تھا 😉)، تو آپ ایک کمانڈ سے اپنی ایپلیکیشن deploy کر سکتے ہیں۔

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

بس! اب آپ اس URL پر اپنی ایپ تک رسائی حاصل کر سکتے ہیں۔ ✨

#### FastAPI Cloud کے بارے میں { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** وہی مصنف اور ٹیم بنا رہی ہے جو **FastAPI** کے پیچھے ہے۔

یہ کم سے کم محنت کے ساتھ API **بنانے**، **deploy کرنے**، اور **تک رسائی** حاصل کرنے کے عمل کو آسان بناتا ہے۔

یہ FastAPI کے ساتھ ایپس بنانے کا وہی **ڈویلپر تجربہ** انہیں کلاؤڈ پر **deploy** کرنے میں لاتا ہے۔ 🎉

FastAPI Cloud *FastAPI اور دوستوں* کے اوپن سورس پراجیکٹس کا بنیادی سپانسر اور فنڈنگ فراہم کنندہ ہے۔ ✨

#### دوسرے کلاؤڈ فراہم کنندگان پر Deploy کریں { #deploy-to-other-cloud-providers }

FastAPI اوپن سورس ہے اور معیارات پر مبنی ہے۔ آپ FastAPI ایپس کسی بھی کلاؤڈ فراہم کنندہ پر deploy کر سکتے ہیں جو آپ چاہیں۔

اپنے کلاؤڈ فراہم کنندہ کی رہنمائی کے مطابق FastAPI ایپس deploy کریں۔ 🤓

## کارکردگی { #performance }

آزاد TechEmpower بینچ مارکس دکھاتے ہیں کہ Uvicorn کے تحت چلنے والی **FastAPI** ایپلیکیشنز [دستیاب تیز ترین Python frameworks میں سے ایک](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7) ہیں، صرف Starlette اور خود Uvicorn سے پیچھے ہیں (جو FastAPI اندرونی طور پر استعمال کرتا ہے)۔ (*)

اس کے بارے میں مزید سمجھنے کے لیے، [بینچ مارکس](https://fastapi.tiangolo.com/benchmarks/) سیکشن دیکھیں۔

## Dependencies { #dependencies }

FastAPI کا انحصار Pydantic اور Starlette پر ہے۔

### `standard` Dependencies { #standard-dependencies }

جب آپ `pip install "fastapi[standard]"` سے FastAPI انسٹال کرتے ہیں تو یہ اختیاری dependencies کے `standard` گروپ کے ساتھ آتا ہے:

Pydantic کے استعمال کردہ:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - email کی توثیق کے لیے۔

Starlette کے استعمال کردہ:

* [`httpx`](https://www.python-httpx.org) - اگر آپ `TestClient` استعمال کرنا چاہتے ہیں تو ضروری ہے۔
* [`jinja2`](https://jinja.palletsprojects.com) - اگر آپ ڈیفالٹ template ترتیب استعمال کرنا چاہتے ہیں تو ضروری ہے۔
* [`python-multipart`](https://github.com/Kludex/python-multipart) - اگر آپ `request.form()` کے ساتھ form <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn> کی سپورٹ چاہتے ہیں تو ضروری ہے۔

FastAPI کے استعمال کردہ:

* [`uvicorn`](https://www.uvicorn.dev) - اس server کے لیے جو آپ کی ایپلیکیشن لوڈ اور سرو کرتا ہے۔ اس میں `uvicorn[standard]` شامل ہے، جس میں اعلیٰ کارکردگی سرونگ کے لیے ضروری کچھ dependencies (مثلاً `uvloop`) شامل ہیں۔
* `fastapi-cli[standard]` - `fastapi` کمانڈ فراہم کرنے کے لیے۔
    * اس میں `fastapi-cloud-cli` شامل ہے، جو آپ کو اپنی FastAPI ایپلیکیشن [FastAPI Cloud](https://fastapicloud.com) پر deploy کرنے کی اجازت دیتا ہے۔

### `standard` Dependencies کے بغیر { #without-standard-dependencies }

اگر آپ `standard` اختیاری dependencies شامل نہیں کرنا چاہتے، تو `pip install "fastapi[standard]"` کے بجائے `pip install fastapi` سے انسٹال کریں۔

### `fastapi-cloud-cli` کے بغیر { #without-fastapi-cloud-cli }

اگر آپ FastAPI معیاری dependencies کے ساتھ انسٹال کرنا چاہتے ہیں لیکن `fastapi-cloud-cli` کے بغیر، تو `pip install "fastapi[standard-no-fastapi-cloud-cli]"` سے انسٹال کریں۔

### اضافی اختیاری Dependencies { #additional-optional-dependencies }

کچھ اضافی dependencies ہیں جو آپ شاید انسٹال کرنا چاہیں۔

اضافی اختیاری Pydantic dependencies:

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - settings management کے لیے۔
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - Pydantic کے ساتھ استعمال کے لیے اضافی types۔

اضافی اختیاری FastAPI dependencies:

* [`orjson`](https://github.com/ijl/orjson) - اگر آپ `ORJSONResponse` استعمال کرنا چاہتے ہیں تو ضروری ہے۔
* [`ujson`](https://github.com/esnme/ultrajson) - اگر آپ `UJSONResponse` استعمال کرنا چاہتے ہیں تو ضروری ہے۔

## لائسنس { #license }

یہ پراجیکٹ MIT لائسنس کی شرائط کے تحت لائسنس یافتہ ہے۔

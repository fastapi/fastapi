---
include_yaml:
  sponsors: data/sponsors.yml
---

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/bn"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, শেখা সহজ, দ্রুত code লেখা যায়, production-এর জন্য প্রস্তুত</em>
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

**Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/bn)

**Source Code**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI হলো Python দিয়ে API তৈরি করার জন্য একটি আধুনিক, দ্রুত (high-performance) web framework, যেটা standard Python type hints-এর উপর ভিত্তি করে বানানো।

<!-- agent-banner -->

এর প্রধান feature-গুলো হলো:

* **দ্রুত**: খুবই high performance, **NodeJS** আর **Go**-এর সমান (Starlette আর Pydantic-এর কারণে)। [সবচেয়ে দ্রুত Python framework-গুলোর একটি](#performance)।
* **দ্রুত code লেখা**: feature develop করার গতি প্রায় 200% থেকে 300% বেড়ে যায়। *
* **কম bug**: মানুষের (developer-এর) হাতে হওয়া ভুল প্রায় 40% কমে যায়। *
* **সহজে বোঝা যায়**: দারুণ editor support। সব জায়গায় <dfn title="auto-complete, autocompletion, IntelliSense নামেও পরিচিত">Completion</dfn>। debugging-এ কম সময় লাগে।
* **সহজ**: ব্যবহার করা আর শেখা যেন সহজ হয়, সেভাবেই design করা। docs পড়তে কম সময় লাগে।
* **ছোট code**: code duplication কম। প্রতিটি parameter declaration থেকে একাধিক feature। কম bug।
* **মজবুত**: production-ready code পাবেন। সাথে automatic interactive documentation।
* **Standards-ভিত্তিক**: API-এর open standards-এর উপর ভিত্তি করে বানানো (এবং পুরোপুরি compatible): [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (আগে Swagger নামে পরিচিত) এবং [JSON Schema](https://json-schema.org/)।

<small>* একটি internal development team production application বানানোর সময় যে test করেছিল, তার ভিত্তিতে অনুমান।</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

<div class="fastapi-sponsors fastapi-sponsors--keystone">
{% for sponsor in sponsors.keystone -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--keystone" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}"></a>
{% endfor -%}
</div>

### Gold Sponsors { #gold-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--gold">
{% for sponsor in sponsors.gold -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--gold" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor -%}
</div>

### Silver Sponsors { #silver-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--silver">
{% for sponsor in sponsors.silver -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--silver" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor %}
</div>

<!-- /sponsors -->

[অন্যান্য sponsors](https://fastapi.tiangolo.com/bn/fastapi-people/#sponsors)

## মতামত { #opinions }

<!-- only-mkdocs -->
<div class="fastapi-opinions" data-fastapi-opinions>
  <div class="fastapi-opinions__tabs" role="tablist" aria-label="যেসব company FastAPI ব্যবহার করে">
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-microsoft" aria-controls="fo-panel-microsoft" aria-selected="true" tabindex="0">
      <span class="fastapi-opinions__mark"><img src="/img/logos/microsoft.svg" alt="Microsoft" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-uber" aria-controls="fo-panel-uber" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/uber.svg" alt="Uber" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-netflix" aria-controls="fo-panel-netflix" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/netflix.svg" alt="Netflix" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-cisco" aria-controls="fo-panel-cisco" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/cisco.svg" alt="Cisco" loading="lazy"></span>
    </button>
  </div>

  <div class="fastapi-opinions__panel" id="fo-panel-microsoft" role="tabpanel" aria-labelledby="fo-tab-microsoft" tabindex="0">
    <blockquote class="fastapi-opinions__quote">"আমি আজকাল প্রচুর <strong>FastAPI</strong> ব্যবহার করছি। আসলে আমি আমার team-এর সব <strong>Microsoft-এর ML services</strong>-এর জন্য এটি ব্যবহার করার পরিকল্পনা করছি। এগুলোর কিছু core <strong>Windows</strong> product-এ এবং কিছু <strong>Office</strong> product-এ integrate করা হচ্ছে।"</blockquote>
    <div class="fastapi-opinions__attr">— Kabir Khan, <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-uber" role="tabpanel" aria-labelledby="fo-tab-uber" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"একটি <strong>REST</strong> server চালু করতে আমরা <strong>FastAPI</strong> library বেছে নিয়েছি, যেটাতে query করে <strong>predictions</strong> পাওয়া যায়।" <em>[Ludwig-এর জন্য]</em></blockquote>
    <div class="fastapi-opinions__attr">— Piero Molino, Yaroslav Dudin, Sai Sumanth Miryala, <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-netflix" role="tabpanel" aria-labelledby="fo-tab-netflix" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"<strong>Netflix</strong> আনন্দের সাথে আমাদের <strong>crisis management</strong> orchestration framework <strong>Dispatch</strong>-এর open-source release ঘোষণা করছে!" <em>[FastAPI দিয়ে তৈরি]</em></blockquote>
    <div class="fastapi-opinions__attr">— Kevin Glisson, Marc Vilanova, Forest Monsen, <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-cisco" role="tabpanel" aria-labelledby="fo-tab-cisco" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">"কেউ যদি production-এর জন্য Python API তৈরি করতে চান, আমি তাকে জোরালোভাবে <strong>FastAPI</strong>-এর সুপারিশ করব। এটি <strong>সুন্দরভাবে design করা</strong>, <strong>ব্যবহার করা সহজ</strong> এবং <strong>খুবই scalable</strong> — এটি আমাদের API-first development strategy-র একটি <strong>মূল অংশ</strong> হয়ে উঠেছে।"</blockquote>
    <div class="fastapi-opinions__attr">— Deon Pillsbury, <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/">(ref)</a></div>
  </div>
</div>
<!-- /only-mkdocs -->

<div class="only-github" markdown="1">

"_[...] আমি আজকাল প্রচুর **FastAPI** ব্যবহার করছি। [...] আসলে আমি আমার team-এর সব **Microsoft-এর ML services**-এর জন্য এটি ব্যবহার করার পরিকল্পনা করছি। এগুলোর কিছু core **Windows** product-এ এবং কিছু **Office** product-এ integrate করা হচ্ছে।_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_একটি **REST** server চালু করতে আমরা **FastAPI** library বেছে নিয়েছি, যেটাতে query করে **predictions** পাওয়া যায়। [Ludwig-এর জন্য]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, এবং Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** আনন্দের সাথে আমাদের **crisis management** orchestration framework **Dispatch**-এর open-source release ঘোষণা করছে! [**FastAPI** দিয়ে তৈরি]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_কেউ যদি production-এর জন্য Python API তৈরি করতে চান, আমি তাকে জোরালোভাবে **FastAPI**-এর সুপারিশ করব। এটি **সুন্দরভাবে design করা**, **ব্যবহার করা সহজ** এবং **খুবই scalable**, এটি আমাদের API-first development strategy-র একটি **মূল অংশ** হয়ে উঠেছে এবং আমাদের Virtual TAC Engineer-এর মতো অনেক automation ও service চালাচ্ছে।_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

</div>

## FastAPI mini documentary { #fastapi-mini-documentary }

2025 সালের শেষে একটি [FastAPI mini documentary](https://www.youtube.com/watch?v=mpR8ngthqiE) বের হয়েছে, আপনি এটা online দেখতে পারেন:

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, CLI-এর FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

আপনি যদি web API-এর বদলে terminal-এ ব্যবহারের জন্য একটি <abbr title="Command Line Interface">CLI</abbr> app তৈরি করেন, তাহলে [**Typer**](https://typer.tiangolo.com/) দেখুন।

**Typer** হলো FastAPI-এর ছোট ভাইবোন। আর এটা বানানো হয়েছে **CLI-এর FastAPI** হওয়ার জন্য। ⌨️ 🚀

## যা যা লাগবে { #requirements }

FastAPI দুটি শক্তিশালী ভিত্তির উপর দাঁড়িয়ে আছে:

* web অংশের জন্য [Starlette](https://starlette.dev/)।
* data অংশের জন্য [Pydantic](https://pydantic.dev/docs/)।

## Installation { #installation }

প্রথমে [`uv` install করুন](https://docs.astral.sh/uv/getting-started/installation/), তারপর আপনার project-এ FastAPI যোগ করুন:

<div class="termy">

```console
$ uv add "fastapi[standard]"

---> 100%
```

</div>

**Note**: সব terminal-এ যেন কাজ করে, তাই `"fastapi[standard]"` অবশ্যই quotes-এর ভেতরে লিখবেন।

আপনি যদি `pip` ব্যবহার করতে পছন্দ করেন, তাহলে একটি virtual environment-এর ভেতরে `fastapi[standard]` install করুন। অন্য উপায়ের ধাপগুলো [installation guide](tutorial/#install-fastapi)-এ দেখুন।

## উদাহরণ { #example }

### এটি তৈরি করুন { #create-it }

`main.py` নামে একটি file বানান, তাতে লিখুন:

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
<summary>অথবা <code>async def</code> ব্যবহার করুন...</summary>

আপনার code যদি `async` / `await` ব্যবহার করে, তাহলে `async def` ব্যবহার করুন:

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

**Note**:

না জানলে docs-এ [`async` এবং `await` সম্পর্কে](https://fastapi.tiangolo.com/bn/async/#in-a-hurry) _"In a hurry?"_ section-টি দেখুন।

</details>

### এটি চালান { #run-it }

server চালান:

<div class="termy">

```console
$ uv run fastapi dev

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
<summary><code>fastapi dev</code> command সম্পর্কে...</summary>

`fastapi dev` command নিজে থেকেই আপনার `main.py` file পড়ে, এর ভেতরের **FastAPI** app খুঁজে নেয়, এবং [Uvicorn](https://uvicorn.dev) ব্যবহার করে একটি server চালু করে।

default-ভাবে, local development-এর জন্য `fastapi dev` auto-reload চালু রেখেই start হয়।

এ নিয়ে আরও জানতে [FastAPI CLI docs](https://fastapi.tiangolo.com/bn/fastapi-cli/) পড়ুন।

</details>

### ফলাফল দেখুন { #check-it }

আপনার browser-এ খুলুন [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)।

আপনি এই JSON response দেখতে পাবেন:

```JSON
{"item_id": 5, "q": "somequery"}
```

আপনি এরই মধ্যে একটি API বানিয়ে ফেলেছেন, যেটা:

* _paths_ `/` এবং `/items/{item_id}`-এ HTTP request নেয়।
* দুটি _path_-ই `GET` <em>operations</em> নেয় (যা HTTP _methods_ নামেও পরিচিত)।
* _path_ `/items/{item_id}`-এ একটি _path parameter_ `item_id` আছে, যা একটি `int` হওয়া উচিত।
* _path_ `/items/{item_id}`-এ একটি optional `str` _query parameter_ `q` আছে।

### Interactive API docs { #interactive-api-docs }

এখন যান [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)-এ।

আপনি automatic interactive API documentation দেখতে পাবেন ([Swagger UI](https://github.com/swagger-api/swagger-ui) দিয়ে তৈরি):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### বিকল্প API docs { #alternative-api-docs }

আর এখন যান [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)-এ।

আপনি আরেকটি automatic documentation দেখতে পাবেন ([ReDoc](https://github.com/Redocly/redoc) দিয়ে তৈরি):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## উদাহরণটি upgrade করুন { #example-upgrade }

এবার `main.py` file-টি বদলান, যাতে এটা একটি `PUT` request থেকে body নিতে পারে।

Pydantic-এর সুবাদে, standard Python types দিয়েই body declare করুন।

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

`fastapi dev` server নিজে থেকেই reload হয়ে যাওয়ার কথা।

### Interactive API docs-এর upgrade { #interactive-api-docs-upgrade }

এখন যান [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)-এ।

* interactive API documentation নিজে থেকেই update হয়ে যাবে, নতুন body সহ:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" button-এ click করুন, এতে parameter-গুলো পূরণ করে সরাসরি API-এর সাথে interact করতে পারবেন:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* তারপর "Execute" button-এ click করুন, user interface আপনার API-এর সাথে যোগাযোগ করবে, parameter-গুলো পাঠাবে, ফলাফল নিয়ে screen-এ দেখাবে:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### বিকল্প API docs-এর upgrade { #alternative-api-docs-upgrade }

আর এখন যান [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)-এ।

* বিকল্প documentation-ও নতুন query parameter এবং body দেখাবে:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap { #recap }

সংক্ষেপে, আপনি parameter, body ইত্যাদির types function parameter হিসেবে **একবারই** declare করেন।

এটা করেন standard, আধুনিক Python types দিয়েই।

নতুন কোনো syntax, বা কোনো নির্দিষ্ট library-এর methods বা classes শেখার দরকার নেই।

শুধু standard **Python**।

উদাহরণস্বরূপ, একটি `int`-এর জন্য:

```Python
item_id: int
```

অথবা আরও জটিল একটি `Item` model-এর জন্য:

```Python
item: Item
```

...আর সেই একটি declaration দিয়েই আপনি পাবেন:

* Editor support, যার মধ্যে আছে:
    * Completion।
    * Type checks।
* Data-এর validation:
    * data invalid হলে automatic, পরিষ্কার errors।
    * deeply nested JSON objects-এর জন্যও validation।
* Input data-এর <dfn title="এগুলো নামেও পরিচিত: serialization, parsing, marshalling">Conversion</dfn>: network থেকে আসা data-কে Python data ও types-এ। যেখান থেকে পড়া হয়:
    * JSON।
    * Path parameters।
    * Query parameters।
    * Cookies।
    * Headers।
    * Forms।
    * Files।
* Output data-এর <dfn title="এগুলো নামেও পরিচিত: serialization, parsing, marshalling">Conversion</dfn>: Python data ও types থেকে network data-তে (JSON হিসেবে) convert করা:
    * Python types convert করা (`str`, `int`, `float`, `bool`, `list`, ইত্যাদি)।
    * `datetime` objects।
    * `UUID` objects।
    * Database models।
    * ...এবং আরও অনেক কিছু।
* Automatic interactive API documentation, 2টি আলাদা user interface সহ:
    * Swagger UI।
    * ReDoc।

---

আগের code উদাহরণে ফিরে গেলে, **FastAPI**:

* `GET` এবং `PUT` request-এর জন্য path-এ একটি `item_id` আছে কিনা validate করবে।
* `GET` এবং `PUT` request-এর জন্য `item_id`-এর type `int` কিনা validate করবে।
    * না হলে client একটি কাজে লাগার মতো, পরিষ্কার error দেখতে পাবে।
* `GET` request-এর জন্য `q` নামে একটি optional query parameter আছে কিনা দেখবে (যেমন `http://127.0.0.1:8000/items/foo?q=somequery`)।
    * যেহেতু `q` parameter-টি `= None` দিয়ে declare করা হয়েছে, এটি optional।
    * `None` ছাড়া এটি required হতো (যেমন `PUT`-এর ক্ষেত্রে body required)।
* `/items/{item_id}`-এ `PUT` request-এর জন্য, body-কে JSON হিসেবে পড়বে:
    * দেখবে এতে `name` নামে একটি required attribute আছে কিনা, যা একটি `str` হওয়া উচিত।
    * দেখবে এতে `price` নামে একটি required attribute আছে কিনা, যা অবশ্যই একটি `float` হতে হবে।
    * দেখবে এতে `is_offer` নামে একটি optional attribute আছে কিনা, যা থাকলে একটি `bool` হওয়া উচিত।
    * এই সবকিছু deeply nested JSON objects-এর জন্যও কাজ করবে।
* নিজে থেকেই JSON-এ এবং JSON থেকে convert করবে।
* OpenAPI দিয়ে সবকিছু document করবে, যা ব্যবহার করা যায়:
    * Interactive documentation systems-এ।
    * অনেক language-এর জন্য automatic client code generation systems-এ।
* সরাসরি 2টি interactive documentation web interface দেবে।

---

এটা তো কেবল শুরু, কিন্তু সবকিছু কীভাবে কাজ করে তা আপনি এরই মধ্যে বুঝে গেছেন।

এই line-টা বদলে দেখুন:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...এখান থেকে:

```Python
        ... "item_name": item.name ...
```

...এখানে:

```Python
        ... "item_price": item.price ...
```

...আর দেখুন আপনার editor কীভাবে attributes auto-complete করে এবং তাদের types জানে:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

আরও feature সহ একটি পুরো উদাহরণ দেখতে <a href="https://fastapi.tiangolo.com/bn/tutorial/">Tutorial - User Guide</a> দেখুন।

**Spoiler alert**: tutorial - user guide-এ আছে:

* অন্যান্য বিভিন্ন জায়গা থেকে **parameters** declare করা, যেমন: **headers**, **cookies**, **form fields** এবং **files**।
* `maximum_length` বা `regex`-এর মতো **validation constraints** কীভাবে set করতে হয়।
* একটি খুবই শক্তিশালী আর ব্যবহারে সহজ **<dfn title="এগুলো নামেও পরিচিত: components, resources, providers, services, injectables">Dependency Injection</dfn>** system।
* Security এবং authentication, **JWT tokens** সহ **OAuth2** এবং **HTTP Basic** auth-এর support সহ।
* **deeply nested JSON models** declare করার আরও advanced (কিন্তু একই রকম সহজ) উপায় (Pydantic-এর সুবাদে)।
* [Strawberry](https://strawberry.rocks) এবং অন্যান্য library-এর সাথে **GraphQL** integration।
* আরও অনেক extra feature (Starlette-এর সুবাদে), যেমন:
    * **WebSockets**
    * HTTPX আর `pytest` দিয়ে খুবই সহজ tests
    * **CORS**
    * **Cookie Sessions**
    * ...এবং আরও অনেক কিছু।

### আপনার app deploy করুন (optional) { #deploy-your-app-optional }

আপনি চাইলে একটি মাত্র command দিয়ে আপনার FastAPI app [FastAPI Cloud](https://fastapicloud.com)-এ deploy করতে পারেন। 🚀

<div class="termy">

```console
$ uv run fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

CLI নিজে থেকেই আপনার FastAPI application খুঁজে নিয়ে cloud-এ deploy করবে। login করা না থাকলে authentication শেষ করার জন্য আপনার browser খুলে যাবে।

ব্যস, এতটুকুই! এখন ওই URL-এ গিয়ে আপনার app ব্যবহার করতে পারবেন। ✨

#### FastAPI Cloud সম্পর্কে { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** বানিয়েছেন **FastAPI**-এর সেই একই author আর team।

খুব কম ঝামেলায় একটি API-এর **building**, **deploying** আর **accessing** সহজ করে দেয়।

FastAPI দিয়ে app বানানোর যে **developer experience**, সেটাই এটা cloud-এ **deploy** করার সময়ও এনে দেয়। 🎉

FastAPI Cloud হলো *FastAPI and friends* open source project-গুলোর প্রধান sponsor এবং funding provider। ✨

#### অন্যান্য cloud provider-এ deploy করুন { #deploy-to-other-cloud-providers }

FastAPI open source এবং standards-ভিত্তিক। আপনার পছন্দের যেকোনো cloud provider-এ FastAPI apps deploy করতে পারবেন।

আপনার cloud provider-এর guide দেখে সেখানে FastAPI apps deploy করুন। 🤓

## Performance { #performance }

নিরপেক্ষ TechEmpower benchmarks দেখায়, Uvicorn-এ চলা **FastAPI** applications [সবচেয়ে দ্রুত Python framework-গুলোর একটি](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), শুধু Starlette আর Uvicorn-এর পরেই (যেগুলো FastAPI নিজেই ভেতরে ব্যবহার করে)। (*)

এ নিয়ে আরও জানতে [Benchmarks](https://fastapi.tiangolo.com/bn/benchmarks/) section দেখুন।

## Dependencies { #dependencies }

FastAPI চলে Pydantic আর Starlette-এর উপর।

### `standard` Dependencies { #standard-dependencies }

আপনি যখন `uv add "fastapi[standard]"` দিয়ে FastAPI install করেন, তখন এর সাথে optional dependencies-এর `standard` group-টাও চলে আসে:

Pydantic যেগুলো ব্যবহার করে:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - email validation-এর জন্য।

Starlette যেগুলো ব্যবহার করে:

* [`httpx2`](https://pydantic.dev/docs/httpx2/) (অথবা `httpx`) - `TestClient` এটি ব্যবহার করে।
* [`jinja2`](https://jinja.palletsprojects.com) - default template configuration ব্যবহার করতে চাইলে প্রয়োজন।
* [`python-multipart`](https://github.com/Kludex/python-multipart) - `request.form()` দিয়ে form <dfn title="HTTP request থেকে আসা string-কে Python data-তে convert করা">"parsing"</dfn> support করতে চাইলে প্রয়োজন।

FastAPI যেগুলো ব্যবহার করে:

* [`uvicorn`](https://uvicorn.dev) - সেই server-এর জন্য, যেটা আপনার application load করে আর serve করে। এর মধ্যে `uvicorn[standard]` আছে, যাতে high performance serving-এর জন্য প্রয়োজনীয় কিছু dependencies (যেমন `uvloop`) আছে।
* `fastapi-cli[standard]` - `fastapi` command দেওয়ার জন্য।
    * এর মধ্যে `fastapi-cloud-cli` আছে, যেটা দিয়ে আপনি আপনার FastAPI application [FastAPI Cloud](https://fastapicloud.com)-এ deploy করতে পারেন।

### `standard` Dependencies ছাড়া { #without-standard-dependencies }

আপনি যদি `standard` optional dependencies না রাখতে চান, তাহলে `uv add "fastapi[standard]"`-এর বদলে `uv add fastapi` দিয়ে install করতে পারেন।

### `fastapi-cloud-cli` ছাড়া { #without-fastapi-cloud-cli }

আপনি যদি standard dependencies সহ কিন্তু `fastapi-cloud-cli` ছাড়া FastAPI install করতে চান, তাহলে `uv add "fastapi[standard-no-fastapi-cloud-cli]"` দিয়ে install করতে পারেন।

### অতিরিক্ত Optional Dependencies { #additional-optional-dependencies }

আরও কিছু extra dependencies আছে, যেগুলো আপনার কাজে লাগতে পারে।

Pydantic-এর অতিরিক্ত optional dependencies:

* [`pydantic-settings`](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/) - settings management-এর জন্য।
* [`pydantic-extra-types`](https://github.com/pydantic/pydantic-extra-types) - Pydantic-এর সাথে ব্যবহারের জন্য অতিরিক্ত types।

FastAPI-এর অতিরিক্ত optional dependencies:

* [`orjson`](https://github.com/ijl/orjson) - `ORJSONResponse` ব্যবহার করতে চাইলে প্রয়োজন।
* [`ujson`](https://github.com/ultrajson/ultrajson) - `UJSONResponse` ব্যবহার করতে চাইলে প্রয়োজন।

## License { #license }

এই project-টি MIT license-এর অধীনে প্রকাশিত।

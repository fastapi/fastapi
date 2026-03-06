# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/bn"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI ফ্রেমওয়ার্ক, উচ্চ পারফরম্যান্স সম্পন্ন, শেখা সহজ, দ্রুত কোড করা যায়, প্রোডাকশনের জন্য প্রস্তুত</em>
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

**ডকুমেন্টেশন**: <a href="https://fastapi.tiangolo.com/bn" target="_blank">https://fastapi.tiangolo.com/bn</a>

**সোর্স কোড**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI হলো Python দিয়ে API তৈরির একটি আধুনিক, দ্রুত (উচ্চ-পারফরম্যান্স সম্পন্ন) ওয়েব ফ্রেমওয়ার্ক, যা স্ট্যান্ডার্ড Python টাইপ হিন্টের উপর ভিত্তি করে তৈরি।

মূল বৈশিষ্ট্যগুলো হলো:

* **দ্রুত**: **NodeJS** এবং **Go**-এর সমতুল্য অত্যন্ত উচ্চ পারফরম্যান্স সম্পন্ন (Starlette এবং Pydantic-এর কল্যাণে)। [সবচেয়ে দ্রুত Python ফ্রেমওয়ার্কগুলোর একটি](#performance)।
* **দ্রুত কোড করা যায়**: ফিচার ডেভেলপমেন্টের গতি প্রায় ২০০% থেকে ৩০০% বৃদ্ধি পায়। *
* **কম বাগ**: ডেভেলপারদের করা ভুল বা কোডিং ত্রুটি প্রায় ৪০% কমে যায়। *
* **স্বজ্ঞাত**: চমৎকার এডিটর সাপোর্ট। <dfn title="also known as auto-complete, autocompletion, IntelliSense">Completion</dfn> সর্বত্র। ডিবাগিং-এ কম সময়।
* **সহজ**: ব্যবহার এবং শেখা সহজ হওয়ার জন্য ডিজাইন করা হয়েছে। ডকস পড়তে কম সময়।
* **সংক্ষিপ্ত**: কোড ডুপ্লিকেশন কম। প্রতিটি প্যারামিটার ডিক্লারেশন থেকে একাধিক ফিচার। কম বাগ।
* **শক্তিশালী**: প্রোডাকশন-রেডি কোড পান। স্বয়ংক্রিয় ইন্টারেক্টিভ ডকুমেন্টেশনসহ।
* **স্ট্যান্ডার্ড-ভিত্তিক**: API-এর জন্য উন্মুক্ত মানদণ্ডের উপর ভিত্তি করে (এবং সম্পূর্ণ সামঞ্জস্যপূর্ণ): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (পূর্বে Swagger নামে পরিচিত) এবং <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>।

<small>* একটি অভ্যন্তরীণ ডেভেলপমেন্ট টিম দ্বারা পরিচালিত পরীক্ষার উপর ভিত্তি করে অনুমান, যারা প্রোডাকশন অ্যাপ্লিকেশন তৈরি করছিল।</small>

## স্পনসর { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold and Silver Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">অন্যান্য স্পনসর</a>

## মতামত { #opinions }

"_[...] আজকাল আমি **FastAPI** অনেক বেশি ব্যবহার করছি। [...] আমি আসলে আমার টিমের **Microsoft-এর ML সার্ভিস**গুলোর জন্য এটি ব্যবহার করার পরিকল্পনা করছি। তাদের কেউ কেউ মূল **Windows** প্রোডাক্ট এবং কিছু **Office** প্রোডাক্টে একীভূত হচ্ছে।_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_আমরা **predictions** পেতে query করার জন্য একটি **REST** সার্ভার চালু করতে **FastAPI** লাইব্রেরিটি গ্রহণ করেছি। [Ludwig-এর জন্য]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** আমাদের **crisis management** অর্কেস্ট্রেশন ফ্রেমওয়ার্কের ওপেন-সোর্স রিলিজ ঘোষণা করতে পেরে আনন্দিত: **Dispatch**! [**FastAPI** দিয়ে তৈরি]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_**FastAPI** নিয়ে আমি অত্যন্ত উত্তেজিত। এটি এত মজার!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_সৎভাবে বলতে গেলে, আপনি যা তৈরি করেছেন তা সত্যিই শক্ত এবং পালিশ দেখাচ্ছে। অনেক দিক থেকে, এটাই আমি **Hug** হতে চেয়েছিলাম — কেউ সেটি তৈরি করছে দেখা সত্যিই অনুপ্রেরণাদায়ক।_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_যদি আপনি REST API তৈরির জন্য একটি **আধুনিক ফ্রেমওয়ার্ক** শিখতে চান, তাহলে **FastAPI** দেখুন [...] এটি দ্রুত, ব্যবহার করা সহজ এবং শেখা সহজ [...]_"

"_আমরা আমাদের **API**গুলোর জন্য **FastAPI**-তে স্যুইচ করেছি [...] আমি মনে করি আপনিও এটি পছন্দ করবেন [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_যদি কেউ একটি প্রোডাকশন Python API তৈরি করতে চান, আমি দৃঢ়ভাবে **FastAPI** সুপারিশ করব। এটি **সুন্দরভাবে ডিজাইন করা**, **ব্যবহার করা সহজ** এবং **অত্যন্ত স্কেলযোগ্য**, এটি আমাদের API first ডেভেলপমেন্ট কৌশলে একটি **মূল উপাদান** হয়ে উঠেছে এবং আমাদের Virtual TAC Engineer-সহ অনেক অটোমেশন এবং সার্ভিস পরিচালনা করছে।_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI মিনি ডকুমেন্টারি { #fastapi-mini-documentary }

২০২৫ সালের শেষে একটি <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI মিনি ডকুমেন্টারি</a> প্রকাশিত হয়েছে, আপনি এটি অনলাইনে দেখতে পারেন:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## CLI-এর FastAPI — **Typer** { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

যদি আপনি একটি ওয়েব API-এর পরিবর্তে টার্মিনালে ব্যবহারের জন্য একটি <abbr title="Command Line Interface">CLI</abbr> অ্যাপ তৈরি করছেন, তাহলে <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> দেখুন।

**Typer** হলো FastAPI-এর ছোট ভাই। এবং এটি **CLI-এর FastAPI** হতে উদ্দেশ্যপ্রণোদিত। ⌨️ 🚀

## প্রয়োজনীয়তা { #requirements }

FastAPI দিগগজদের কাঁধে দাঁড়িয়ে আছে:

* ওয়েব অংশের জন্য <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>।
* ডেটা অংশের জন্য <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>।

## ইনস্টলেশন { #installation }

একটি <a href="https://fastapi.tiangolo.com/bn/virtual-environments/" class="external-link" target="_blank">virtual environment</a> তৈরি ও সক্রিয় করুন, তারপর FastAPI ইনস্টল করুন:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**নোট**: সমস্ত টার্মিনালে সঠিকভাবে কাজ করার জন্য `"fastapi[standard]"` কোটেশনের মধ্যে রাখুন।

## উদাহরণ { #example }

### তৈরি করুন { #create-it }

`main.py` নামে একটি ফাইল তৈরি করুন:

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

যদি আপনার কোড `async` / `await` ব্যবহার করে, তাহলে `async def` ব্যবহার করুন:

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

**নোট**:

যদি আপনি না জানেন, ডকসে <a href="https://fastapi.tiangolo.com/bn/async/#in-a-hurry" target="_blank">`async` এবং `await` সম্পর্কে _"তাড়া আছে?"_ বিভাগটি</a> দেখুন।

</details>

### চালান { #run-it }

সার্ভার চালান:

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
<summary><code>fastapi dev main.py</code> কমান্ড সম্পর্কে...</summary>

`fastapi dev` কমান্ড আপনার `main.py` ফাইল পড়ে, সেখানে **FastAPI** অ্যাপটি শনাক্ত করে এবং <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> ব্যবহার করে একটি সার্ভার শুরু করে।

ডিফল্টভাবে, `fastapi dev` লোকাল ডেভেলপমেন্টের জন্য auto-reload সক্ষম করে শুরু হবে।

আরও তথ্যের জন্য <a href="https://fastapi.tiangolo.com/bn/fastapi-cli/" target="_blank">FastAPI CLI ডকস</a> পড়ুন।

</details>

### পরীক্ষা করুন { #check-it }

<a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>-এ ব্রাউজার খুলুন।

আপনি JSON response দেখতে পাবেন:

```JSON
{"item_id": 5, "q": "somequery"}
```

আপনি ইতিমধ্যে একটি API তৈরি করেছেন যা:

* _paths_ `/` এবং `/items/{item_id}`-তে HTTP request গ্রহণ করে।
* উভয় _path_-ই `GET` <em>operations</em> (HTTP _methods_ নামেও পরিচিত) নেয়।
* _path_ `/items/{item_id}`-এ একটি _path parameter_ `item_id` আছে যা `int` হওয়া উচিত।
* _path_ `/items/{item_id}`-এ একটি ঐচ্ছিক `str` _query parameter_ `q` আছে।

### ইন্টারেক্টিভ API ডকস { #interactive-api-docs }

এখন <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>-এ যান।

আপনি স্বয়ংক্রিয় ইন্টারেক্টিভ API ডকুমেন্টেশন দেখতে পাবেন (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> দ্বারা প্রদত্ত):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### বিকল্প API ডকস { #alternative-api-docs }

এখন <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>-এ যান।

আপনি বিকল্প স্বয়ংক্রিয় ডকুমেন্টেশন দেখতে পাবেন (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> দ্বারা প্রদত্ত):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## উদাহরণ আপগ্রেড { #example-upgrade }

এখন `PUT` request থেকে একটি body গ্রহণ করতে `main.py` ফাইলটি পরিবর্তন করুন।

Pydantic-এর কল্যাণে স্ট্যান্ডার্ড Python type ব্যবহার করে body ডিক্লেয়ার করুন।

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

`fastapi dev` সার্ভার স্বয়ংক্রিয়ভাবে রিলোড হবে।

### ইন্টারেক্টিভ API ডকস আপগ্রেড { #interactive-api-docs-upgrade }

এখন <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>-এ যান।

* ইন্টারেক্টিভ API ডকুমেন্টেশন স্বয়ংক্রিয়ভাবে আপডেট হবে, নতুন body সহ:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" বাটনে ক্লিক করুন, এটি আপনাকে parameter পূরণ করতে এবং সরাসরি API-এর সাথে ইন্টারেক্ট করতে দেয়:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* তারপর "Execute" বাটনে ক্লিক করুন, ইউজার ইন্টারফেস আপনার API-এর সাথে যোগাযোগ করবে, parameter পাঠাবে, ফলাফল পাবে এবং স্ক্রিনে দেখাবে:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### বিকল্প API ডকস আপগ্রেড { #alternative-api-docs-upgrade }

এখন <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>-এ যান।

* বিকল্প ডকুমেন্টেশনও নতুন query parameter এবং body প্রতিফলিত করবে:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### সারসংক্ষেপ { #recap }

সংক্ষেপে, আপনি **একবার** parameter, body ইত্যাদির type ফাংশন parameter হিসেবে ডিক্লেয়ার করেন।

আপনি এটি স্ট্যান্ডার্ড আধুনিক Python type দিয়ে করেন।

আপনাকে কোনো নতুন সিনট্যাক্স, কোনো নির্দিষ্ট লাইব্রেরির পদ্ধতি বা ক্লাস শিখতে হবে না।

শুধু স্ট্যান্ডার্ড **Python**।

উদাহরণস্বরূপ, একটি `int`-এর জন্য:

```Python
item_id: int
```

অথবা আরও জটিল `Item` মডেলের জন্য:

```Python
item: Item
```

...এবং সেই একটি ডিক্লারেশনের মাধ্যমে আপনি পান:

* এডিটর সাপোর্ট, যার মধ্যে রয়েছে:
    * Completion।
    * Type check।
* ডেটা যাচাইকরণ:
    * ডেটা অবৈধ হলে স্বয়ংক্রিয় এবং স্পষ্ট ত্রুটি।
    * গভীরভাবে নেস্টেড JSON অবজেক্টের জন্যও যাচাইকরণ।
* ইনপুট ডেটার <dfn title="also known as: serialization, parsing, marshalling">রূপান্তর</dfn>: নেটওয়ার্ক থেকে Python ডেটা এবং type-এ রূপান্তর। নিচ থেকে পড়া:
    * JSON।
    * Path parameter।
    * Query parameter।
    * Cookie।
    * Header।
    * Form।
    * File।
* আউটপুট ডেটার <dfn title="also known as: serialization, parsing, marshalling">রূপান্তর</dfn>: Python ডেটা এবং type থেকে নেটওয়ার্ক ডেটায় (JSON হিসেবে) রূপান্তর:
    * Python type (`str`, `int`, `float`, `bool`, `list`, ইত্যাদি) রূপান্তর।
    * `datetime` অবজেক্ট।
    * `UUID` অবজেক্ট।
    * ডেটাবেস মডেল।
    * ...এবং আরও অনেক।
* স্বয়ংক্রিয় ইন্টারেক্টিভ API ডকুমেন্টেশন, ২টি বিকল্প ইউজার ইন্টারফেস সহ:
    * Swagger UI।
    * ReDoc।

---

আগের কোড উদাহরণে ফিরে আসি, **FastAPI** করবে:

* `GET` এবং `PUT` request-এর জন্য path-এ `item_id` আছে কিনা যাচাই করবে।
* `GET` এবং `PUT` request-এর জন্য `item_id`-এর type `int` কিনা যাচাই করবে।
    * যদি না হয়, ক্লায়েন্ট একটি উপযোগী, স্পষ্ট ত্রুটি দেখবে।
* `GET` request-এর জন্য `q` নামে একটি ঐচ্ছিক query parameter আছে কিনা পরীক্ষা করবে (যেমন `http://127.0.0.1:8000/items/foo?q=somequery`)।
    * `q` parameter `= None` দিয়ে ডিক্লেয়ার করা হয়েছে বলে এটি ঐচ্ছিক।
    * `None` ছাড়া এটি প্রয়োজনীয় হতো (যেমন `PUT`-এর ক্ষেত্রে body)।
* `/items/{item_id}`-এ `PUT` request-এর জন্য, JSON হিসেবে body পড়বে:
    * একটি প্রয়োজনীয় attribute `name` আছে কিনা যাচাই করবে যা `str` হওয়া উচিত।
    * একটি প্রয়োজনীয় attribute `price` আছে কিনা যাচাই করবে যা `float` হতে হবে।
    * একটি ঐচ্ছিক attribute `is_offer` আছে কিনা যাচাই করবে, যদি থাকে তাহলে `bool` হওয়া উচিত।
    * এটি গভীরভাবে নেস্টেড JSON অবজেক্টের জন্যও কাজ করবে।
* স্বয়ংক্রিয়ভাবে JSON থেকে এবং JSON-এ রূপান্তর করবে।
* OpenAPI দিয়ে সবকিছু ডকুমেন্ট করবে, যা ব্যবহার করা যেতে পারে:
    * ইন্টারেক্টিভ ডকুমেন্টেশন সিস্টেম।
    * অনেক ভাষার জন্য স্বয়ংক্রিয় ক্লায়েন্ট কোড জেনারেশন সিস্টেম।
* সরাসরি ২টি ইন্টারেক্টিভ ডকুমেন্টেশন ওয়েব ইন্টারফেস প্রদান করবে।

---

আমরা শুধু উপরিভাগ দেখলাম, কিন্তু আপনি ইতিমধ্যে এটি কীভাবে কাজ করে তার ধারণা পেয়েছেন।

নিচের লাইনটি পরিবর্তন করার চেষ্টা করুন:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...থেকে:

```Python
        ... "item_name": item.name ...
```

...এতে:

```Python
        ... "item_price": item.price ...
```

...এবং দেখুন কীভাবে আপনার এডিটর attribute স্বয়ংক্রিয়ভাবে সম্পূর্ণ করবে এবং তাদের type জানবে:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

আরও বৈশিষ্ট্য সহ আরও সম্পূর্ণ উদাহরণের জন্য, <a href="https://fastapi.tiangolo.com/bn/tutorial/">Tutorial - User Guide</a> দেখুন।

**স্পয়লার সতর্কতা**: tutorial - user guide-এ রয়েছে:

* **header**, **cookie**, **form field** এবং **file** সহ বিভিন্ন জায়গা থেকে **parameter** ডিক্লারেশন।
* `maximum_length` বা `regex`-এর মতো **validation constraint** কীভাবে সেট করবেন।
* একটি অত্যন্ত শক্তিশালী এবং ব্যবহার করা সহজ **<dfn title="also known as components, resources, providers, services, injectables">Dependency Injection</dfn>** সিস্টেম।
* **JWT token** এবং **HTTP Basic** auth সহ **OAuth2** সাপোর্ট সহ নিরাপত্তা এবং প্রমাণীকরণ।
* গভীরভাবে **nested JSON model** ডিক্লেয়ার করার আরও উন্নত (কিন্তু সমানভাবে সহজ) কৌশল (Pydantic-এর কল্যাণে)।
* <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> এবং অন্যান্য লাইব্রেরির সাথে **GraphQL** ইন্টিগ্রেশন।
* Starlette-এর কল্যাণে অনেক অতিরিক্ত বৈশিষ্ট্য:
    * **WebSocket**
    * HTTPX এবং `pytest`-এর উপর ভিত্তি করে অত্যন্ত সহজ test
    * **CORS**
    * **Cookie Session**
    * ...এবং আরও।

### আপনার অ্যাপ ডিপ্লয় করুন (ঐচ্ছিক) { #deploy-your-app-optional }

আপনি ঐচ্ছিকভাবে আপনার FastAPI অ্যাপ <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>-এ ডিপ্লয় করতে পারেন, যদি না করে থাকেন তাহলে waiting list-এ যোগ দিন। 🚀

যদি আপনার ইতিমধ্যে একটি **FastAPI Cloud** অ্যাকাউন্ট থাকে (আমরা আপনাকে waiting list থেকে আমন্ত্রণ জানিয়েছি 😉), আপনি একটি কমান্ড দিয়ে আপনার অ্যাপ ডিপ্লয় করতে পারেন।

ডিপ্লয় করার আগে, নিশ্চিত করুন যে আপনি লগইন করেছেন:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

তারপর আপনার অ্যাপ ডিপ্লয় করুন:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

এটুকুই! এখন আপনি সেই URL-এ আপনার অ্যাপ অ্যাক্সেস করতে পারবেন। ✨

#### FastAPI Cloud সম্পর্কে { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** **FastAPI**-এর পেছনে থাকা একই লেখক এবং টিম দ্বারা তৈরি।

এটি ন্যূনতম প্রচেষ্টায় একটি API **তৈরি**, **ডিপ্লয়** এবং **অ্যাক্সেস** করার প্রক্রিয়াকে সহজ করে।

এটি FastAPI দিয়ে অ্যাপ তৈরির একই **ডেভেলপার এক্সপেরিয়েন্স** ক্লাউডে **ডিপ্লয়** করার ক্ষেত্রেও নিয়ে আসে। 🎉

FastAPI Cloud হলো *FastAPI এবং বন্ধুরা* ওপেন সোর্স প্রজেক্টগুলোর প্রাথমিক স্পনসর এবং ফান্ডিং প্রদানকারী। ✨

#### অন্যান্য ক্লাউড প্রোভাইডারে ডিপ্লয় করুন { #deploy-to-other-cloud-providers }

FastAPI ওপেন সোর্স এবং মানদণ্ড-ভিত্তিক। আপনি যেকোনো ক্লাউড প্রোভাইডারে FastAPI অ্যাপ ডিপ্লয় করতে পারেন।

তাদের সাথে FastAPI অ্যাপ ডিপ্লয় করতে আপনার ক্লাউড প্রোভাইডারের গাইড অনুসরণ করুন। 🤓

## পারফরম্যান্স { #performance }

স্বাধীন TechEmpower বেঞ্চমার্ক দেখায় যে Uvicorn-এর অধীনে চলা **FastAPI** অ্যাপ্লিকেশন <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">সবচেয়ে দ্রুত Python ফ্রেমওয়ার্কগুলোর একটি হিসেবে চলছে</a>, শুধুমাত্র Starlette এবং Uvicorn-এর নিচে (FastAPI দ্বারা অভ্যন্তরীণভাবে ব্যবহৃত)। (*)

আরও জানতে, <a href="https://fastapi.tiangolo.com/bn/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> বিভাগটি দেখুন।

## নির্ভরতা { #dependencies }

FastAPI Pydantic এবং Starlette-এর উপর নির্ভর করে।

### `standard` নির্ভরতা { #standard-dependencies }

যখন আপনি `pip install "fastapi[standard]"` দিয়ে FastAPI ইনস্টল করেন, তখন এটি ঐচ্ছিক নির্ভরতার `standard` গ্রুপের সাথে আসে:

Pydantic দ্বারা ব্যবহৃত:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - ইমেইল যাচাইকরণের জন্য।

Starlette দ্বারা ব্যবহৃত:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - `TestClient` ব্যবহার করতে চাইলে প্রয়োজনীয়।
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - ডিফল্ট template কনফিগারেশন ব্যবহার করতে চাইলে প্রয়োজনীয়।
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - `request.form()` দিয়ে form <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn> সাপোর্ট করতে চাইলে প্রয়োজনীয়।

FastAPI দ্বারা ব্যবহৃত:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - আপনার অ্যাপ্লিকেশন লোড করা এবং পরিবেশন করার সার্ভারের জন্য। এতে `uvicorn[standard]` অন্তর্ভুক্ত, যেখানে উচ্চ-পারফরম্যান্স সার্ভিংয়ের জন্য প্রয়োজনীয় কিছু নির্ভরতা রয়েছে (যেমন `uvloop`)।
* `fastapi-cli[standard]` - `fastapi` কমান্ড প্রদান করতে।
    * এতে `fastapi-cloud-cli` অন্তর্ভুক্ত, যা আপনাকে আপনার FastAPI অ্যাপ্লিকেশন <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>-এ ডিপ্লয় করতে দেয়।

### `standard` নির্ভরতা ছাড়া { #without-standard-dependencies }

যদি আপনি `standard` ঐচ্ছিক নির্ভরতা অন্তর্ভুক্ত করতে না চান, তাহলে `pip install "fastapi[standard]"` এর পরিবর্তে `pip install fastapi` দিয়ে ইনস্টল করতে পারেন।

### `fastapi-cloud-cli` ছাড়া { #without-fastapi-cloud-cli }

যদি আপনি standard নির্ভরতা সহ কিন্তু `fastapi-cloud-cli` ছাড়া FastAPI ইনস্টল করতে চান, তাহলে `pip install "fastapi[standard-no-fastapi-cloud-cli]"` দিয়ে ইনস্টল করতে পারেন।

### অতিরিক্ত ঐচ্ছিক নির্ভরতা { #additional-optional-dependencies }

কিছু অতিরিক্ত নির্ভরতা আছে যা আপনি ইনস্টল করতে চাইতে পারেন।

অতিরিক্ত ঐচ্ছিক Pydantic নির্ভরতা:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - settings management-এর জন্য।
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic-এর সাথে ব্যবহারের জন্য অতিরিক্ত type।

অতিরিক্ত ঐচ্ছিক FastAPI নির্ভরতা:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` ব্যবহার করতে চাইলে প্রয়োজনীয়।
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` ব্যবহার করতে চাইলে প্রয়োজনীয়।

## লাইসেন্স { #license }

এই প্রজেক্টটি MIT লাইসেন্সের শর্তে লাইসেন্সপ্রাপ্ত।

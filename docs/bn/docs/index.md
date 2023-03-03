<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI সেরা-পারফরম্যান্সের, সহজে শেখার এবং দ্রুত কোড করে প্রডাকশনের জন্য ফ্রামওয়ার্ক।</em>
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

**ডকুমেন্টেশন**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**সোর্স কোড**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI একটি আধুনিক, দ্রুততম এবং সেরা-পারফরম্যান্স সম্পন্ন, Python 3.6+ দিয়ে API তৈরির জন্য স্ট্যান্ডার্ড পাইথন টাইপ ইঙ্গিতের ভিত্তিতে ওয়েব ফ্রেমওয়ার্ক।

এর মূল বৈশিষ্ট্য গুলো হলঃ

- **গতি**: এটি **NodeJS** এবং **Go** এর মত সেরা-পারফরম্যান্স সম্পন্ন (Starlette এবং Pydantic এর সাহায্যে)। [পাইথন দ্রুততম ফ্রেমওয়ার্ক গুলোর মধ্যে এটি একটি](#পারফরম্যান্স)।
- **দ্রুত কোড করা**: ফিচার ডেভেলপ করার গতি ২০০% থেকে ৩০০% বৃদ্ধি করে৷ \*
- **স্বল্প bugs**: মানুব (ডেভেলপার) সৃষ্ট ত্রুটির প্রায় 40% হ্রাস করুন। \*
- **স্বজ্ঞাত**: দুর্দান্ত এডিটর সাপোর্ট। সর্বত্র <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> নামেও পরিচিত। দ্রুত ডিবাগ করা যায়।

- **সহজ**: এটি এমন ভাবের সজানো হয়েছে যেন দ্রুত ডকুমেন্টেশন পড়ে সহজে শেখা এবং ব্যবহার করা যায়।
- **সংক্ষিপ্ত**: কোড ডুপ্লিকেশন কমায়। প্রতিটি প্যারামিটার ঘোষণা থেকে একাধিক ফিচার পাওয়া যাবে। কম bug হবে।
- **জোরালো**: স্বয়ংক্রিয় ইন্টারেক্টিভ ডকুমেন্টেশন সহ, উৎপাদনের জন্য প্রস্তুত কোড পাওয়া যাবে।
- **মান-ভিত্তিক**: API-এর জন্য উন্মুক্ত মানগুলির উপর ভিত্তি করে (এবং সম্পূর্ণরূপে সামঞ্জস্যপূর্ণ): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (যাহা পূর্বে Swagger নামে পরিচিত ছিল) এবং <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>\* এক দল প্রোডাকশন এপ্লিকেশন বানানো অভ্যন্তরীণ ডেভেলপার এর ওপর নিরীক্ষন ভিত্তিক অনুমান।</small>

## স্পনসর গণ

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">অন্যান্য স্পনসর গণ</a>

## মতামত সমূহ

"_[...] আমি আজকাল প্রচণ্ড পরিমানে **FastAPI** ব্যবহার করছি। [...] আমি ভাবছি মাইক্রোসফ্টে **ML সার্ভিস** এ আমার সকল দলের জন্য এটি ব্যবহার করব। যার মধ্যে কিছু পণ্য **Windows** এ সংযোযন হয় এবং কিছু **Office** এর সাথে সংযোযন হচ্ছে।_"

<div style="text-align: right; margin-right: 10%;">কবির খান - <strong>মাইক্রোসফ্টে</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_আমরা **FastAPI** লাইব্রেরি গ্রহণ করেছি একটি **REST** সার্ভার তৈরি করতে, যা **ভবিষ্যদ্বাণী** পাওয়ার জন্য কুয়েরি করা যেতে পারে। [লুডউইগের জন্য]_"

<div style="text-align: right; margin-right: 10%;">পিয়েরো মোলিনো, ইয়ারোস্লাভ দুদিন, এবং সাই সুমন্থ মিরিয়ালা - <strong>উবার</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** আমাদের **ক্রাইসিস ম্যানেজমেন্ট** অর্কেস্ট্রেশন ফ্রেমওয়ার্ক: **ডিসপ্যাচ** এর ওপেন সোর্স রিলিজ ঘোষণা করতে পেরে আনন্দিত! [যাকিনা **FastAPI** দিয়ে নির্মিত]_"

<div style="text-align: right; margin-right: 10%;">কেভিন গ্লিসন, মার্ক ভিলানোভা, ফরেস্ট মনসেন - <strong>নেটফ্লিক্স</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_আমি **FastAPI** নিয়ে চাঁদের সমান উৎসাহিত। এটি খুবই মজার!_"

<div style="text-align: right; margin-right: 10%;">ব্রায়ান ওকেন - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">পাইথন বাইটস</a> পডকাস্ট হোস্ট</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_সত্যিই, আপনি যা তৈরি করেছেন তা খুব মজবুত এবং পরিপূর্ন দেখায়৷ অনেক উপায়ে, আমি যা **Hug** করতে চেয়েছিলাম - কাউকে তাঁহাই তৈরি করতে দেখে আমি সত্যিই অনুপ্রানিত৷_"

<div style="text-align: right; margin-right: 10%;">টিমোথি ক্রসলে - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> স্রষ্টা</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"আপনি যদি REST API তৈরির জন্য একটি **আধুনিক ফ্রেমওয়ার্ক** শিখতে চান, তাহলে **FastAPI** দেখুন [...] এটি দ্রুত, ব্যবহার করা সহজ এবং শিখতেও সহজ [...]\_"

"_আমরা আমাদের **APIs** [...] এর জন্য **FastAPI**- তে এসেছি [...] আমি মনে করি আপনিও এটি পছন্দ করবেন [...]_"

<div style="text-align: right; margin-right: 10%;">ইনেস মন্টানি - ম্যাথিউ হোনিবাল - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> প্রতিষ্ঠাতা - <a href="https://spacy.io" target="_blank">spaCy</a> স্রষ্টা</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLI এর জন্য FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

আপনি যদি <abbr title="Command Line Interface">CLI</abbr> অ্যাপ বানাতে চান, যাকিনা ওয়েব API এর পরিবর্তে টার্মিনালে ব্যবহার হবে, তাহলে চেক আউট করুন<a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**টাইপার** হল FastAPI এর ছোট ভাইয়ের মত। এবং এটির উদ্দেশ্য ছিল **CLIs এর FastAPI** হওয়া। ⌨️ 🚀

## প্রয়োজনীয়তা গুলো

Python 3.7+

FastAPI দানবেদের কাঁধে দাঁড়িয়ে আছে:

- <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> ওয়েব অংশের জন্য.
- <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> ডেটা অংশগুলির জন্য.

## ইনস্টলেশন প্রক্রিয়া

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

আপনার একটি ASGI সার্ভারেরও প্রয়োজন হবে, প্রডাকশনের জন্য <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> অথবা <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## উদাহরণ

### তৈরি

- `main.py` নামে একটি ফাইল তৈরি করুন:

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
<summary>অথবা ব্যবহার করুন <code>async def</code>...</summary>

যদি আপনার কোড `async` / `await`, ব্যবহার করে তাহলে `async def` ব্যবহার করুন:

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

**টীকা**:

আপনি যদি না জানেন, _"তাড়াহুড়ো?"_ বিভাগটি দেখুন <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` এবং `await` ডকের মধ্যে দেখুন </a>.

</details>

### এটি চালান

সার্ভার চালু করুন:

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
<summary>কমান্ড সম্পর্কে <code>uvicorn main:app --reload</code>...</summary>

`uvicorn main:app` কমান্ডটি দ্বারা বোঝায়:

- `main`: ফাইল `main.py` (পাইথন "মডিউল")।
- `app`: `app = FastAPI()` লাইন দিয়ে `main.py` এর ভিতরে তৈরি করা অবজেক্ট।
- `--reload`: কোড পরিবর্তনের পরে সার্ভার পুনরায় চালু করুন। এটি শুধুমাত্র ডেভেলপমেন্ট এর সময় ব্যবহার করুন।

</details>

### এটা চেক করুন

আপনার ব্রাউজার খুলুন <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> এ।

আপনি JSON রেসপন্স দেখতে পাবেন:

```JSON
{"item_id": 5, "q": "somequery"}
```

আপনি ইতিমধ্যে একটি API তৈরি করেছেন যা:

- `/` এবং `/items/{item_id}` _paths_ এ HTTP অনুরোধ গ্রহণ করে।
- Both _paths_ take `GET` <em>operations</em> (also known as HTTP _methods_).
- The _path_ `/items/{item_id}` has a _path parameter_ `item_id` that should be an `int`.
- The _path_ `/items/{item_id}` has an optional `str` _query parameter_ `q`.

### ইন্টারেক্টিভ API ডকুমেন্টেশন

এখন যান <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

আপনি স্বয়ংক্রিয় ভাবে প্রস্তুত ইন্টারেক্টিভ API ডকুমেন্টেশন দেখতে পাবেন (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> প্রদত্ত):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### বিকল্প API ডকুমেন্টেশন

এবং এখন <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> এ যান.

আপনি স্বয়ংক্রিয় ভাবে প্রস্তুত বিকল্প ডকুমেন্টেশন দেখতে পাবেন (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> প্রদত্ত):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## উদাহরণস্বরূপ আপগ্রেড

এখন `main.py` ফাইলটি পরিবর্তন করুন যেন এটি `PUT` রিকুয়েস্ট থেকে বডি পেতে পারে।

Python স্ট্যান্ডার্ড লাইব্রেরি, Pydantic এর সাহায্যে বডি ঘোষণা করুন।

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

সার্ভারটি স্বয়ংক্রিয়ভাবে পুনরায় লোড হওয়া উচিত (কারণ আপনি উপরের `uvicorn` কমান্ডে `--reload` যোগ করেছেন)।

### ইন্টারেক্টিভ API ডকুমেন্টেশন আপগ্রেড

এখন <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> এডড্রেসে যান.

- ইন্টারেক্টিভ API ডকুমেন্টেশনটি স্বয়ংক্রিয়ভাবে আপডেট হযে যাবে, নতুন বডি সহ:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- "Try it out" বাটনে ক্লিক করুন, এটি আপনাকে পেরামিটারগুলো পূরণ করতে এবং API এর সাথে সরাসরি ইন্টারঅ্যাক্ট করতে দেয়:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

- তারপরে "Execute" বাটনে ক্লিক করুন, ইউজার ইন্টারফেসটি আপনার API এর সাথে যোগাযোগ করবে, পেরামিটার পাঠাবে, ফলাফলগুলি পাবে এবং সেগুলি স্ক্রিনে দেখাবে:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### বিকল্প API ডকুমেন্টেশন আপগ্রেড

এবং এখন <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> এ যান।

- বিকল্প ডকুমেন্টেশনও নতুন কুয়েরি প্যারামিটার এবং বডি প্রতিফলিত হবে:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### সংক্ষিপ্তকরণ

সংক্ষেপে, আপনি **শুধু একবার** প্যারামিটারের ধরন, বডি ইত্যাদি ফাংশন প্যারামিটার হিসেবে ঘোষণা করেন।

আপনি সেটি আধুনিক স্ট্যান্ডার্ড পাইথন টিপের সাথে করেন।

আপনাকে নতুন করে নির্দিষ্ট কোন লাইব্রেরির সিনট্যাক্স, ফাংশন বা ক্লাস কিছুই শিখতে হচ্ছে না।

শুধুই স্ট্যান্ডার্ড **Python 3.6+**

উদাহরণস্বরূপ, `int` এর জন্য:

```Python
item_id: int
```

অথবা আরও জটিল `Item` মডেলের জন্য:

```Python
item: Item
```

...এবং সেই একই ঘোষণার সাথে আপনি পাবেন:

- এডিটর সাপোর্ট, যেমন
  - সমাপ্তি।
  - টাইপ চেক।
- তথ্য যাচাইকরণ:
  - ডেটা অবৈধ হলে স্বয়ংক্রিয় এবং পরিষ্কার ত্রুটি।
  - এমনকি গভীরভাবে নেস্ট করা JSON অবজেক্টের জন্য বৈধতা।
- ইনপুট ডেটায় <abbr title="যা পরিচিত: serialization, parsing, marshalling">রূপান্তর</abbr>: যা নেটওয়ার্ক থেকে পাইথন ডেটা এবং টাইপে আসে, এবং সেখান থেকে পড়া:

  - JSON।
  - পাথ প্যারামিটার।
  - কুয়েরি প্যারামিটার।
  - কুকিজ
  - হেডার
  - ফর্ম
  - ফাইল

- আউটপুট ডেটার <abbr title="যা পরিচিত: serialization, parsing, marshalling">রূপান্তর</abbr>: পাইথন ডেটা এবং টাইপ থেকে নেটওয়ার্ক ডেটাতে রূপান্তর করা (JSON হিসাবে):
  -পাইথন টাইপে রূপান্তর করুন (`str`, `int`, `float`, `bool`, `list`, ইত্যাদি)।
  - `datetime` অবজেক্ট।
  - `UUID` objeঅবজেক্টcts।
  - ডাটাবেস মডেল।
  - ...এবং আরো অনেক।
- স্বয়ংক্রিয় ইন্টারেক্টিভ API ডকুমেন্টেশন, 2টি বিকল্প ব্যবহারকারীর ইন্টারফেস সহ:
  - সোয়াগার ইউ আই (Swagger UI)।
  - রিডক (ReDoc)।

---

পূর্ববর্তী কোড উদাহরণে ফিরে আসা যাক, **FastAPI** যা করবে:

- `GET` এবং `PUT` অনুরোধের জন্য পথে `item_id` আছে কিনা তা যাচাই করবে।
- `GET` এবং `PUT` অনুরোধের জন্য `item_id` টাইপ `int` এর হতে হবে তা যাচাই করবে।
  - যদি না হয় তবে ক্লায়েন্ট একটি উপযুক্ত, পরিষ্কার ত্রুটি দেখতে পাবেন।
- `GET` অনুরোধের জন্য একটি ঐচ্ছিক ক্যুয়েরি প্যারামিটার নামক `q` (যেমন `http://127.0.0.1:8000/items/foo?q=somequery`) আছে কি তা চেক করবে।
  - যেহেতু `q` প্যারামিটারটি `= None` দিয়ে ঘোষণা করা হয়েছে, তাই এটি ঐচ্ছিক।
  - `None` ছাড়া এটি প্রয়োজনীয় হতো (যেমন `PUT` এর ক্ষেত্রে হয়েছে)।
- `/items/{item_id}` এর জন্য `PUT` অনুরোধের বডি JSON হিসাবে পড়ুন:
  - লক্ষ করুন, `name` একটি প্রয়োজনীয় অ্যাট্রিবিউট হিসাবে বিবেচনা করেছে এবং এটি `str` হতে হবে।
  - লক্ষ করুন এখানে, `price` অ্যাট্রিবিউটটি আবশ্যক এবং এটি `float` হতে হবে।
  - লক্ষ করুন `is_offer` একটি ঐচ্ছিক অ্যাট্রিবিউট এবং এটি `bool` হতে হবে যদি উপস্থিত থাকে।
  - এই সবটি গভীরভাবে নেস্টড JSON অবজেক্টগুলিতেও কাজ করবে।
- স্বয়ংক্রিয়ভাবে জেএসওএন হতে এবং জেএসওএন থেকে কনভার্ট করুন।
- OpenAPI দিয়ে সবকিছু ডকুমেন্ট করুন, যা ব্যবহার করা যেতে পারে:
  - ইন্টারাক্টিভ ডকুমেন্টেশন সিস্টেম।
  - অনেক ভাষার জন্য স্বয়ংক্রিয় ক্লায়েন্ট কোড জেনারেশন সিস্টেম।
- সরাসরি 2টি ইন্টারেক্টিভ ডকুমেন্টেশন ওয়েব ইন্টারফেস প্রদান করা হয়েছে।

---

আমরা এতক্ষন শুধু এর পৃষ্ঠ তৈরি করেছি, কিন্তু আপনি ইতমধ্যেই এটি কিভাবে কাজ করে তার ধারণা পেয়ে গিয়েছেন।

Try changing the line with:
নিম্নোক্ত লাইন গুলো পরিবর্তন করার চেষ্টা করুন:

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

...এবং দেখুন কিভাবে আপনার এডিটর এট্রিবিউটগুলি অটো-কমপ্লিট করবে এবং তাদের ধরন জানতে পারবে:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

আরও বৈশিষ্ট্য সম্পন্ন উদাহরণের জন্য, দেখুন <a href="https://fastapi.tiangolo.com/tutorial/">টিউটোরিয়াল - ব্যবহারকারীর গাইড</a>.

**স্পয়লার সতর্কতা**: টিউটোরিয়াল - ব্যবহারকারীর গাইড নিম্নোক্ত বিষয়গুলি অন্তর্ভুক্ত করে:

- **হেডার**, **কুকিজ**, **ফর্ম ফিল্ড** এবং **ফাইলগুলি** এমন অন্যান্য জায়গা থেকে প্যারামিটার ঘোষণা করা।
- `maximum_length` বা `regex` এর মতো **যাচাইকরণ বাধামুক্তি** সেট করা হয় কিভাবে, তা নিয়ে আলোচনা করা হবে।
- একটি খুব শক্তিশালী এবং ব্যবহার করা সহজ <abbr title="also known as components, resources, providers, services, injectables">ডিপেন্ডেন্সি ইনজেকশন</abbr> সিস্টেম।
- **OAuth2** এবং **JWT টোকেন** এবং **HTTP Basic** auth সহ নিরাপত্তা এবং অনুমোদনপ্রাপ্তি সম্পর্কিত বিষয়সমূহের উপর।
- **গভীরভাবে নেস্টেড JSON মডেল** ঘোষণা করার জন্য আরও উন্নত (কিন্তু সমান সহজ) কৌশল (Pydantic কে ধন্যবাদ)।
- আরো অনেক অতিরিক্ত বৈশিষ্ট্য (স্টারলেটকে ধন্যবাদ) হিসাবে:
  - **WebSockets**
  - **GraphQL**
  - HTTPX এবং `pytest` ভিত্তিক অত্যন্ত সহজ পরীক্ষা
  - **CORS**
  - **Cookie Sessions**
  - ...এবং আরো।

## কর্মক্ষমতা

স্বাধীন TechEmpower বেঞ্চমার্কগুলি দেখায় যে **FastAPI** অ্যাপ্লিকেশনগুলি Uvicorn-এর অধীনে চলমান দ্রুততম<a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">পাইথন ফ্রেমওয়ার্কগুলির মধ্যে একটি,</a> শুধুমাত্র Starlette এবং Uvicorn-এর পর (FastAPI দ্বারা অভ্যন্তরীণভাবে ব্যবহৃত)। (\*)

এটি সম্পর্কে আরও বুঝতে, বিভাগটি দেখুন <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">বেঞ্চমার্কগুলি</a>.

## ঐচ্ছিক ডিপেনডেন্সি

Pydantic দ্বারা ব্যবহৃত:

- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - দ্রুত JSON এর জন্য <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
- <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - ইমেল যাচাইকরণের জন্য।

স্টারলেট দ্বারা ব্যবহৃত:

- <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - আপনি যদি `TestClient` ব্যবহার করতে চান তাহলে আবশ্যক।
- <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - আপনি যদি ডিফল্ট টেমপ্লেট কনফিগারেশন ব্যবহার করতে চান তাহলে প্রয়োজন।
- <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - আপনি যদি ফর্ম সমর্থন করতে চান তাহলে প্রয়োজন <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, `request.form()` সহ।
- <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - `SessionMiddleware` সমর্থনের জন্য প্রয়োজন।
- <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - স্টারলেটের SchemaGenerator সাপোর্ট এর জন্য প্রয়োজন (আপনার সম্ভাবত FastAPI প্রয়োজন নেই)।
- <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - `GraphQLApp` সমর্থনের জন্য প্রয়োজন।
- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - আপনি `UJSONResponse` ব্যবহার করতে চাইলে প্রয়োজন।

FastAPI / Starlette দ্বারা ব্যবহৃত:

- <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - সার্ভারের জন্য যা আপনার অ্যাপ্লিকেশন লোড করে এবং পরিবেশন করে।
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - আপনি `ORJSONResponse` ব্যবহার করতে চাইলে প্রয়োজন।

আপনি এই সব ইনস্টল করতে পারেন `pip install fastapi[all]` দিয়ে.

## লাইসেন্স

এই প্রজেক্ট MIT লাইসেন্সের শর্তাবলীর অধীনে লাইসেন্সপ্রাপ্ত।

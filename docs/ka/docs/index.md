---
hide:
  - navigation
---

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI ფრეიმვორქი, მაღალი წარმადობა, ასათვისებლად მარტივი, ეფექტური, წარმოებაში ჩაშვებისათვის გამზადებული</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**დოკუმენტაცია**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**პროგრამული კოდი**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
FastAPI არის თანამედროვე, სწრაფი (მაღალი წარმადობის მქონე), Python-ზე დაფუძნებული ვებფრეიმვორქი, რომელიც იყენებს Python-ის სტანდარტულ ტიპთა ინდიკატორებს და საშუალებას გვაძლევს შევქმნათ API-ები.

The key features are:
ძირითადი მახასიათებლები გახლავთ:

* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance).
* **სისწრაფე**: აქვს ძალიან მაღალი წარმადობა, როგორც **NodeJS**-სა და **Go**-ს (მადლობა Starlette-სა და Pydantic-ს). [ერთ-ერთი უსწრაფესი ფრეიმვორქია Python-ის არსებულ ფრეიმვორქებს შორის](#performance).
* **Fast to code**: Increase the speed to develop features by about 200% to 300%. *
* **ეფექტურობა**: დეველოპმენტის პროცესს აჩქარებს დაახლოებით 200-300 პროცენტით. *
* **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *
* **ნაკლები პროგრამული ხარვეზი**: ადამიანის (დეველოპერის) მიერ გამოწვეული ხარვეზების ალბათობას ამცირებს დაახლოებით 40 პროცენტით. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **ინტუიციურობა**: შესანიშნავი თავსებადობა ტექსტურ რედაქტორებთან. <abbr title="also known as auto-complete, autocompletion, IntelliSense">კოდის ავტოდასრულების</abbr> ფუნქციონალი ხელმისაწვდომია ყველგან. ნაკლებ დროს დახარჯავთ ხარვეზების აღმოფხვრაში.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **სიმარტივე**: ტექნოლოგია შემუშავებულია იმგვარად, რომ მარტივად გამოსაყენებელი და ასათვისებელი იყოს. დოკუმენტაციის კითხვაში ნაკლებ დროს დახარჯავთ.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
* **კომპაქტური**: კოდის დუბლიკაციის საჭიროება მინიმუმამდეა დაყვანილი. თითოეული პარამეტრის განსაზღვრით აქტიურდება მრავალი ფუნქციონალი. პროგრამული ხარვეზების წარმოქმნის ალბათობა მინიმუმამდეა დაყვანილი.
* **Robust**: Get production-ready code. With automatic interactive documentation.
* **მდგრადობა**: მიიღებთ წარმოებაში ჩაშვებისათვის გამზადებულ კოდს. ამას გარდა, მიიღებთ ავტომატურად გენერირებულ ინტერაქციულ დოკუმენტაციას.
* **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (previously known as Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
* **სტანდარტებზე დაფუძნებულობა**: დაფუძნებულია (და სრულად თავსებადია) API-ებისთვის განსაზღვრულ ღია სტანდარტებზე: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (ადრე ცნობილი იყო, როგორც Swagger) და <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation based on tests on an internal development team, building production applications.</small>
<small>* ზემოთ მოცემული შეფასებები ეფუძნება შიდა დეველოპმენტის გუნდის ტესტებს, რომლებიც მუშაობენ წარმოებაში მყოფ (რეალურ) აპლიკაციებზე.</small>

## Sponsors
## სპონსორები

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Other sponsors</a>
<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">სხვა სპონსორები</a>

## Opinions
## მოსაზრებები

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

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, the FastAPI of CLIs
## **Typer**: ბრძანებათა სტრიქონების FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

If you are building a <abbr title="Command Line Interface">CLI</abbr> app to be used in the terminal instead of a web API, check out <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.
თუკი მუშაობთ <abbr title="ბრძანებათა სტრიქონი">CLI</abbr> აპლიკაციაზე, რომელიც გამოყენებულ იქნება ტერმინალში, - ნაცვლად ვებ API-ისა, თვალი შეავლეთ <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**-ს</a>.

**Typer** is FastAPI's little sibling. And it's intended to be the **FastAPI of CLIs**. ⌨️ 🚀
**Typer** არის FastAPI-ის პატარა ძამიკო. და ჩაფიქრებულია, რომ იგი იყოს **CLI-ების FastAPI**. ⌨️ 🚀

## Requirements
## მოთხოვნები

FastAPI stands on the shoulders of giants:
FastAPI მხრებზე შემოსდგომია შემდეგ გიგანტებს:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> for the web parts.
* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>-ს ვებთან დაკავშირებულ საკითხებში.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> for the data parts.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>-ს მონაცემებთან დაკავშირებულ საკითხებში.

## Installation
## ინსტალაცია

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

## Example
## მაგალითი

### Create it
### შევქმნათ

* Create a file `main.py` with:
* შექმენით `main.py` ფაილი შემდეგი შიგთავსით:

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
<summary>Or use <code>async def</code>...</summary>
<summary>ან გამოიყენეთ <code>async def</code>...</summary>

If your code uses `async` / `await`, use `async def`:
თუკი თქვენი კოდი იყენებს `async` / `await`-ს, გამოიყენეთ `async def`:

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

**Note**:
**შენიშვნა**:

If you don't know, check the _"In a hurry?"_ section about <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` and `await` in the docs</a>.
თუკი ჯერ არ ერკვევით აღნიშნულ საკითხში, <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async`-ისა და `await`-ის შესახებ</a> დოკუმენტაციაში თვალი გადაავლეთ განყოფილებას _„გეჩქარებათ?“_.

</details>

### Run it
### გავუშვათ

Run the server with:
გაუშვით სერვერი შემდეგი ბრძანებით:

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
<summary>About the command <code>fastapi dev main.py</code>...</summary>
<summary><code>fastapi dev main.py</code> ბრძანების შესახებ...</summary>

The command `fastapi dev` reads your `main.py` file, detects the **FastAPI** app in it, and starts a server using <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.
`fastapi dev` ბრძანება კითხულობს თქვენს `main.py` ფაილს, მასში **FastAPI** აპლიკაციას აიდენტიფიცირებს და <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>-ის გამოყენებით უშვებს სერვერს.

By default, `fastapi dev` will start with auto-reload enabled for local development.
ნაგულისხმევად, ლოკალური დეველოპმენტისთვის, `fastapi dev` ბრძანებით გაშვებული სერვერისათვის აქტივირებული იქნება ავტომატური გადატვირთვის ფუნქცია.

You can read more about it in the <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI docs</a>.
ამ საკითხზე დეტალური ინფორმაცია შეგიძლიათ წაიკითხოთ <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI-ის დოკუმენტაციაში</a>.

</details>

### Check it
### შევამოწმოთ

Open your browser at <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.
თქვენს ბრაუზერში გახსენით შემდეგი ბმული: <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

You will see the JSON response as:
დაინახავთ შემდეგნაირ JSON ტიპის მონაცემს:

```JSON
{"item_id": 5, "q": "somequery"}
```

You already created an API that:
ამგვარად, თქვენ უკვე შექმენით API, რომელიც:

* Receives HTTP requests in the _paths_ `/` and `/items/{item_id}`.
* იღებს HTTP მოთხოვნებს შემდეგ _მისამართებზე_: `/` და `/items/{item_id}`.
* Both _paths_ take `GET` <em>operations</em> (also known as HTTP _methods_).
* ორივე _მისამართი_ ამუშავებს `GET` <em>ოპერაციას</em> (ასევე ცნობილს, როგორც HTTP _მეთოდი_).
* The _path_ `/items/{item_id}` has a _path parameter_ `item_id` that should be an `int`.
* `/items/{item_id}` _მისამართს_ გააჩნია _მარშრუტის პარამეტრი_ `item_id`, რომელიც უნდა იყოს მთელი რიცხვის (`int`) ტიპის.
* The _path_ `/items/{item_id}` has an optional `str` _query parameter_ `q`.
* `/items/{item_id}` მისამართს გააჩნია არასავალდებულო სტრიქონის (`str`) ტიპის _საძიებო (query) პარამეტრი_ `q`.

### Interactive API docs
### ინტერაქციული API-დოკუმენტაცია

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.
ახლა კი, თქვენს ბრაუზერში გახსენით შემდეგი ბმული: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):
დაინახავთ ავტომატურად გენერირებულ ინტერაქციულ API-დოკუმენტაციას (რომელიც უზრუნველყოფილია <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>-ის მიერ):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs
### ალტერნატიული API-დოკუმენტაცია

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.
თქვენს ბრაუზერში გახსენით შემდეგი ბმული: <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):
დაინახავთ ალტერნატიულ ავტომატურად გენერირებულ დოკუმენტაციას (რომელიც უზრუნველყოფილია <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>-ის მიერ):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Example upgrade
## გაუმჯობესების მაგალითი

Now modify the file `main.py` to receive a body from a `PUT` request.
მოდით, შევცვალოთ `main.py` ფაილის შიგთავსი იმგვარად, რომ `PUT` ტიპის მოთხოვნით მივიღოთ და დავამუშავოთ მონაცემები.

Declare the body using standard Python types, thanks to Pydantic.
მოვახდინოთ მოთხოვნის შიგთავსის პროტოტიპის დეკლარაცია Python-ის სტანდარტული ტიპების გამოყენებით. ამ შესაძლებლობას Pydantic-ს უნდა ვუმადლოდეთ.

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

The `fastapi dev` server should reload automatically.
ცვლილებების შენახვის შემდეგ, `fastapi dev` ბრძანებით გაშვებული სერვერი, წესით და რიგით, ავტომატურად გადაიტვირთება.

### Interactive API docs upgrade
### გავაუმჯობესოთ ინტერაქციული API-დოკუმენტაცია

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.
თქვენს ბრაუზერში გახსენით შემდეგი ბმული: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.


* The interactive API documentation will be automatically updated, including the new body:
* ინტერაქციული API-დოკუმენტაცია, ახლად დამატებული პროტოტიპის ჩათვლით, განახლდება ავტომატურად:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Click on the button "Try it out", it allows you to fill the parameters and directly interact with the API:
* დააკლიკეთ "Try it out" ღილაკს. ეს საშუალებას მოგცემთ, განსაზღვროთ პარამეტრები და API-სთან უშუალო ინტერაქციით დაკავდეთ:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Then click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:
* შემდგომ ამისა, დააკლიკეთ "Execute" ღილაკს, რითაც თქვენ მიერ გახსნილი ინტერფეისი დაუკავშირდება API-ს, გაგზავნის თქვენ მიერ განსაზღვრულ პარამეტრებს, მიიღებს მოთხოვნის შედეგებს და გამოიტანს ეკრანზე:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade
### გავაუმჯობესოთ ალტერნატიული API-დოკუმენტაცია

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.
ახლა კი, თქვენს ბრაუზერში გახსენით შემდეგი ბმული: <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* The alternative documentation will also reflect the new query parameter and body:
* ახლად დამატებული საძიებო პარამეტრი და შიგთავსის პროტოტიპი ალტერნატიულ დოკუმენტაციაშიც აისახება:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap
### შეჯამება

In summary, you declare **once** the types of parameters, body, etc. as function parameters.
მაშასადამე, პარამეტრების, შიგთავსის პროტოტიპებისა და სხვა ტიპების დეკლარირებას ახორციელებთ **ერთჯერადად**. როგორც ეს ხდება ფუნქციისათვის პარამეტრების განსაზღვრისას.

You do that with standard modern Python types.
ამას აკეთებთ Python-ის თანამედროვე, სტანდარტული ტიპების გამოყენებით.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.
არ გჭირდებათ რომელიმე ცალკეული ბიბლიოთეკისთვის დამახასიათებელი თავისებური სინტაქსის, მეთოდების ან კლასების შესწავლა.

Just standard **Python**.
იყენებთ მხოლოდ და მხოლოდ სტანდარტულ **Python**-ს. 

For example, for an `int`:
მაგალითად, `int`-ის შემთხვევაში:

```Python
item_id: int
```

or for a more complex `Item` model:
ან შედარებით რთული `Item` მოდელისთვის:

```Python
item: Item
```

...and with that single declaration you get:
...და ამ ერთი დეკლარაციით თქვენ მიიღებთ:

* Editor support, including:
    * Completion.
    * Type checks.
* რედაქტორის მხარდაჭერას. მათ შორის:
    * კოდის ავტოდასრულებას.
    * ტიპთა ვალიდურობის შემოწმებას.
* Validation of data:
    * Automatic and clear errors when the data is invalid.
    * Validation even for deeply nested JSON objects.
* მონაცემთა ვალიდაციას:
    * ავტომატურად გენერირებულ და მარტივად გასაგებ ცდომილების შეტყობინებებს, როდესაც მონაცემები ვალიდური არ არის.
    * ვალიდაციას თუნდაც უკიდურესად კომპლექსური JSON მონაცემებისათვის.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of input data: coming from the network to Python data and types. Reading from:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* შემავალ მონაცემთა <abbr title="ასევე ცნობილია, როგორც: სერიალიზება, პარსირება, კლასიფიცირება">გარდაქმნას: ქსელიდან შემომავალი მონაცემების გადათარგმნას Python-ისთვის გასაგებ მონაცემებად და ტიპებად. შესაძლებელია შემდეგი სახის მონაცემების წაკითხვა და გარდაქმნა:
    * JSON.
    * მარშრუტის (Path) პარამეტრები.
    * საძიებო (Query) პარამეტრები.
    * Cookie-ები.
    * თავსართები (Headers).
    * ფორმები.
    * ფაილები.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of output data: converting from Python data and types to network data (as JSON):
    * Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` objects.
    * `UUID` objects.
    * Database models.
    * ...and many more.
* გამომავალ მონაცემთა <abbr title="ასევე ცნობილია, როგორც: სერიალიზება, პარსირება, კლასიფიცირება">გარდაქმნას: Python-ის მონაცემებისა და ტიპების გადათარგმნას ქსელურ მონაცემებად (JSON-ად). შესაძლებელია შემდეგი სახის მონაცემების გარდაქმნა:
    * Python-ის ტიპები (`str`, `int`, `float`, `bool`, `list` და სხვ.).
    * `datetime` ობიექტები.
    * `UUID` ობიექტები.
    * მონაცემთა ბაზის მოდელები.
    * ...და მრავალი სხვა.
* Automatic interactive API documentation, including 2 alternative user interfaces:
    * Swagger UI.
    * ReDoc.
* ავტომატურად გენერირებულ ინტერაქციულ API-დოკუმენტაციას, რომელიც მოიცავს 2 ალტერნატიულ ინტერფეისს. ესენია:
    * Swagger UI.
    * ReDoc.

---

Coming back to the previous code example, **FastAPI** will:
მოდით, მივუბრუნდეთ წინა მაგალითს და გავაანალიზოთ, რას და როგორ გააკეთებს **FastAPI**:

* Validate that there is an `item_id` in the path for `GET` and `PUT` requests.
* `GET` და `PUT` ოპერაციებისათვის შეამოწმებს, არის თუ არა მისამართში განსაზღვრული `item_id` პარამეტრი.
* Validate that the `item_id` is of type `int` for `GET` and `PUT` requests.
    * If it is not, the client will see a useful, clear error.
* `GET` და `PUT` ოპერაციებისათვის გადაამოწმებს, არის თუ არა `item_id` პარამეტრი `int` ტიპის.
    * თუ ეს ასე არ იქნება, კლიენტი იხილავს გამოსადეგ, მარტივად გასაგებ ცდომილების შეტყობინებას.
* Check if there is an optional query parameter named `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) for `GET` requests.
    * As the `q` parameter is declared with `= None`, it is optional.
    * Without the `None` it would be required (as is the body in the case with `PUT`).
* `GET` ოპერაციებისათვის შეამოწმებს, არის თუ არა წარმოდგენილი არასავალდებულო საძიებო (query) პარამეტრი სახელად `q` (მაგ.: `http://127.0.0.1:8000/items/foo?q=somequery`).
    * ვინაიდან `q` პარამეტრი განსაზღვრულია `= None` ბოლოსართით, იგი არასავალდებულოა.
    * `None`-ის არარსებობის შემთხვევაში, იგი იქნებოდა სავალდებულო (როგორც მოთხოვნის შიგთავსი `PUT` ოპერაციის შემთხვევაში).
* For `PUT` requests to `/items/{item_id}`, Read the body as JSON:
    * Check that it has a required attribute `name` that should be a `str`.
    * Check that it has a required attribute `price` that has to be a `float`.
    * Check that it has an optional attribute `is_offer`, that should be a `bool`, if present.
    * All this would also work for deeply nested JSON objects.
* `/items/{item_id}` მისამართზე `PUT` ოპერაციისას, წაიკითხავს მოთხოვნის შიგთავსს როგორც JSON მონაცემს. ამასთან:
    * შეამოწმებს, არის თუ არა განსაზღვრული `str` ტიპის სავალდებულო `name` ატრიბუტი.
    * შეამოწმებს, არის თუ არა განსაზღვრული `float` ტიპის სავალდებულო `price` ატრიბუტი.
    * შეამოწმებს, მოთხოვნის შიგთავსში არის თუ არა წარმოდგენილი `bool` ტიპის არასავალდებულო `is_offer` ატრიბუტი.
    * ყველაფერი ეს იმუშავებს ნებისმიერი სახის (მაგ.: მრავალშრიანი) JSON მონაცემისათვის. 
* Convert from and to JSON automatically.
* ავტომატურად გარდაქმნის JSON-ს სხვა სახის მონაცემად და პირიქით.
* Document everything with OpenAPI, that can be used by:
    * Interactive documentation systems.
    * Automatic client code generation systems, for many languages.
* OpenAPI-ით მოახდენს ყველაფრის დოკუმენტირებას, რაც გამოსადეგი იქნება:
    * ინტერაქციული დოკუმენტაციის სისტემებისათვის.
    * კლიენტის კოდის ავტომატიზირებული გენერირების სისტემებისათვის სხვადასხვა ენაში. 
* Provide 2 interactive documentation web interfaces directly.
* უშუალოდ უზრუნველყოფს 2 ალტერნატიულ ინტერაქციულ დოკუმენტაციის ვებინტერფეისს.

---

We just scratched the surface, but you already get the idea of how it all works.
ჯერჯერობით ჩვენ რაც განვიხილეთ, მხოლოდ და მხოლოდ ზედაპირია აისბერგისა, მაგრამ, ასე თუ ისე, ალბათ გაიაზრეთ ზოგადი პრინციპი, თუ როგორ მუშაობს ეს ყველაფერი.

Try changing the line with:
სცადეთ შემდეგ ხაზში ცვლილების შეტანა:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:
...ძველი:

```Python
        ... "item_name": item.name ...
```

...to:
...ახალი:

```Python
        ... "item_price": item.price ...
```

...and see how your editor will auto-complete the attributes and know their types:
...და დააკვირდით, როგორ მოახდენს თქვენი ტექსტური რედაქტორი ატრიბუტების ავტოდასრულებას და მათი ტიპების იდენტიფიცირებას:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

For a more complete example including more features, see the <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.
მეტად სრულყოფილი მაგალითის სანახავად, სადაც განხილული იქნება უფრო მეტი საკითხი, იხილეთ <a href="https://fastapi.tiangolo.com/tutorial/">სახელმძღვანელო - მომხმარებლის გზამკვლევი</a>.

**Spoiler alert**: the tutorial - user guide includes:
**გაფრთხილება სპოილერის შესახებ**: მომხმარებლის გზამკვლევი მოიცავს შემდეგ საკითხებს:

* Declaration of **parameters** from other different places as: **headers**, **cookies**, **form fields** and **files**.
* **პარამეტრების** დეკლარირება სხვა წყაროებიდან, როგორებიცაა: **თავსართები (headers)**, **cookie-ები**, **ფორმის ველები** და **ფაილები**.
* How to set **validation constraints** as `maximum_length` or `regex`.
* **შემმოწმებლებისათვის (ვალიდატორებისათვის) შეზღუდვების** დაწესება, როგორებიცაა: `maximum_length` ან `regex`.
* A very powerful and easy to use **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** system.
* ძალიან მძლავრი და მარტივად გამოსაყენებელი **<abbr title="ასევე ცნობილი, როგორც კომპონენტები, რესურსები, პროვაიდერები, სერვისები, injectable-ები">პაკეტების ინექციის</abbr>** სისტემა.
* Security and authentication, including support for **OAuth2** with **JWT tokens** and **HTTP Basic** auth.
* უსაფრთხოება და ავთენტიკაცია, მათ შორის **OAuth2**-ის მხარდაჭერა **JWT ტოკენებით** და **HTTP Basic** ავთენტიკაცია.
* More advanced (but equally easy) techniques for declaring **deeply nested JSON models** (thanks to Pydantic).
* მეტად სიღრმისეული (მაგრამ ისეთივე მარტივი) მეთოდოლოგიები **კომპლექსური (მრავალშრიანი) JSON მოდელების** დეკლარირებისათვის (მადლობა Pydantic-ს).
* **GraphQL** integration with <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> and other libraries.
* **GraphQL**-ის ინტეგრირება <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a>-სთან და სხვა ბიბლიოთეკებთან.
* Many extra features (thanks to Starlette) as:
    * **WebSockets**
    * extremely easy tests based on HTTPX and `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...and more.
* არაერთი სხვა თავისებურება (მადლობა Starlette-ს), როგორებიცაა:
    * **ვებსოკეტები**
    * HTTPX-ზე და `pytest`-ზე დაფუძნებული უმარტივესი ტესტები
    * **CORS**
    * **Cookie სესიები**
    * ...და მრავალი სხვა.

## Performance
## წარმადობა

Independent TechEmpower benchmarks show **FastAPI** applications running under Uvicorn as <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">one of the fastest Python frameworks available</a>, only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)
TechEmpower-ის მიუკერძოებელი ტესტები ცხადყოფენ, რომ Uvicorn-ით გაშვებული **FastAPI**-ზე დაფუძნებული აპლიკაციები <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">წარმოაჩენენ FastAPI-ს, როგორც ერთ-ერთ უსწრაფეს ფრეიმვორქს Python-ის არსებულ ფრეიმვორქებს შორის</a>. მას წინ უსწრებენ მხოლოდ Starlette-ი და Uvicorn-ი (რომლებსაც თავის მხრივ, FastAPI-ი იყენებს). (*)

To understand more about it, see the section <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.
ამ ყველაფრის უკეთ გასააზრებლად იხილეთ შემდეგი განყოფილება: <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">წარმადობის ტესტები (Benchmarks)</a>.

## Dependencies

Used by Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - for email validation.
* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - for settings management.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - for extra types to be used with Pydantic.

Used by Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Required if you want to use the `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Required if you want to use the default template configuration.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Required if you want to support form <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, with `request.form()`.

Used by FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - for the server that loads and serves your application.
* `fastapi-cli` - to provide the `fastapi` command.

When you install `fastapi` it comes these standard dependencies.

Additional optional dependencies:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Required if you want to use `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Required if you want to use `UJSONResponse`.

## `fastapi-slim`

If you don't want the extra standard optional dependencies, install `fastapi-slim` instead.

When you install with:

```bash
pip install fastapi
```

...it includes the same code and dependencies as:

```bash
pip install "fastapi-slim[standard]"
```

The standard extra dependencies are the ones mentioned above.

## License

This project is licensed under the terms of the MIT license.

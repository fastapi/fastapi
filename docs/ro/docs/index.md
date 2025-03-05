
{!../../docs/missing-translation.md!}


# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework-ul FastAPI: perfromanță superioară, ușor de învățat, rapid de codat, pregătit pentru producție</em>
    
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

**Documentație**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Cod sursă**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI este un *framework web* modern, foarte performant (rapid), pentru implementarea de API-uri în Python care se bazează pe *type hints*-urile standard din Python.

Caractersticile cheie sunt:

* **Rapid**: Performanță foarte ridicată, la paritate cu **NodeJS** și **Go**, datorită librăriilor Starlette și Pydantic. [Una dintre cele mai rapide librării Python disponbile](#performance).
* **Rapid de codat**: Accelerează viteza de implementare a funcționalităților cu aproape 200% până la 300%. *
* **Mai puține *bug*-uri**: Reduce cu până la 40% erorile cauzate de programator. *
* **Intuitiv**: Suport excelent pentru editoare de cod. <abbr title="cunoscut și ca IntelliSense">Completare automata a codului.</abbr>. Mai puțin timp petrecut cu <abbr title="cunoscut și ca debugging">depanarea</abbr>.
* **Facil**: Proiectat astfel încât să fie ușor de folosit și învățat. Mai puțin timp cu citirea documentației.
* **Scurt**: Minimizează duplicarea de code. Funcționalități multiple din fiecare parametru declarat. Mai puține *bug*-uri.
* **Robust**: Cod gata pentru producție, cu documentație interactiva generată automat.
* **Standardizat**: Se bazeaza și este in totalitate compatibil cu specificațiile <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (cunoscut în trecut ca Swagger) și <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimare bazată pe testele efectuate de o echipa internă, construind aplicații pentru producție.</small>

## Sponsori

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Alți sponsori</a>

## Opinii

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

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

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, <abbr title="Command Line Interface (CLI)">interfața linie de comanda pentru FastAPI</abbr>

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Dacă dezvolți o aplicație în <abbr title="Command Line Interface (CLI)">interfațâ linie de comandă</abbr> pe care să o folosești in terminal în loc de *browser*, verifică <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.
**Typer** este fratele mai mic al FastAPI și este <abbr title="Command Line Interface (CLI)">**interfața linie de comanda pentru FastAPI**</abbr>. ⌨️ 🚀

## Cerințe

FastAPI se bazează pe doi giganți:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> pentru procesarea *web*.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> pentru procesarea datelor.

## Instalare

Crează și activează un <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">mediu virtual</a>, după care instalează FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Notă**: Asigură-te ca pui `"fastapi[standard]"` intre ghilimele, ca să te asiguri ca functionează în orice terminal.

## Exemplu

### Crează

* Crează un fișier `main.py` care va conține:

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
<summary>Sau folosește <code>async def</code>...</summary>

Dacă ai în cod `async` / `await`, folosește `async def`:

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

**Notă**:

Dacă nu ești sigur, verifică documentația la secțiunea _"În grabă?"_ pentru mai multe detalii pentru <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` și `await`</a>.

</details>

### Execută

Pornește *server*-ul web cu:

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
<summary>Despre instrucțiunea <code>fastapi dev main.py</code>...</summary>

Instrucțiunea `fastapi dev` citește fișierul `main.py`, detectează prezența **FastAPI** și pornește un *server web* bazat pe <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Implicit, `fastapi dev` va porni cu modul auto-încărcare activat pentru dezvolatre locală.

Poți afla mai multe în <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">Documentație FastAPI ILC docs</a>.

</details>

### Verifică

Deschide *browser*-ul la <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

În format JSON, vei vedea următorul răspuns:

```JSON
{"item_id": 5, "q": "somequery"}
```

Asftel, ai creat un API care:

* Primște o cerere HTTP pe ruta _paths_ `/` și `/items/{item_id}`.
* Ambele rute răspund la o operațiune `GET` (cunoscută si ca _verb_ HTTP).
* Ruta _path_ `/items/{item_id}` are un prametru de cale `item_id` care trebuie sa fie un `int`  
* Ruta _path_ `/items/{item_id}` are un _parametru de interogare_ `q` care este un tip de dată `str`.

### Documentație API interactivă

Acum navighează către <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vei observa documentatia API generata interactiv (furnizată de <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentație API alternativă

Dacă navighezi către <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>, vei vedea documentația API alternativa generată cu <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Actualizare (Exemplu)

Acum modifică fișierul `main.py` astfel încât o `PUT` să primească un corp în cerere.

Mulțumită Pydantic, poți declara corpul cererii folosind tipuri standard din Python

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

Server-ul `fastapi dev` se va reîncărca automat.

### Actualizarea documentației API interactive

Navighează catre <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Documentația API interactivă va fi actualizată automat, incluzând noul corp al cererii HTTP:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Dă click pe butonul "Try it out", care iți va permite sa completezi valoarea parametrilor si să interacționezi direct cu *API*-ul:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Acum dă click pe butonul "Execute". Interfața grafică va comunica cu API-ul tău, va trimite parametrii, va primi raspunsul pe care îl va afișa pe ecran:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Actualizarea documentației API alternative

Acum, navighează către <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Documentația API alternativă, reflecta noul parametru de interogare precum și corpul cererii:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recapitulare

Pe scurt, declari **o singură data** tipurile de parametrii, corpul, etc. ca argumente intr-o funcție.

Aceasta este posibil prin intermediul tipurilor moderne de date standard din Python.

Nu este nevoie să înveți o noua sintaxă, metodele sau clasele unui librarări speciale, etc.

Doar **Python** standard.

De examplu, pentru un `int`:

```Python
item_id: int
```

sau pentru un model mai complex precum `Item`:

```Python
item: Item
```

...astfel, cu o singura declarație obții:

* Suport la editare, incluzând:
    * Autocompletare.
    * Verificare de tip.
* Validarea datelor:
    * Errori clare si gestionate automat când datele sunt invalide.
    * Validare disponibilă chiar si pentru obiecte JSON profund imbricate.
* <abbr title=": serializare, parsare, marshalling">Conversia</abbr> datelor de intrare dispre rețea către date și tipuri Python. Citește din:
    * JSON.
    * Parametrii de cale.
    * Parametrii de interogare.
    * Cookie-uri.
    * Anteturi HTTP.
    * Formulare HTML.
    * Fișiere.
* <abbr title="also known as: serialization, parsing, marshalling">Conversia</abbr> datelor de ieșire dinspre date și tipuri Python către date de rețea precum JSON:
    * Conversie de tipuri de date Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Obiecte `datetime`.
    * Obiecte `UUID`.
    * Modele de baze de date.
    * ...și multe altele.
* Documentație API interactivă, generata automat incluzând două interfețe grafice alternative bazate pe:
    * Swagger UI.
    * ReDoc.

---

Revenind la codul din exemplul anterior, **FastAPI** efectuează următoareleȘ

* Validează că există un `item_id` în calea cererilor `GET` și `PUT`.
* Validează că `item_id` este de tip `int` pentru cererile `GET` și `PUT`:
  * Dacă nu este, clientul va primi un mesaj de erorare clar și folositor
* Verifică dacă exista un parametru de interogare opțional numit `q` (așa cum apare in `http://127.0.0.1:8000/items/foo?q=somequery`) pentru cererea `GET` /
  * Deoarece parametrul `q` este declarat cu `= None`, acesta este opțional.
  * Fără `None`, ar fi obligatoriu (așa cum este corpul cererii in cazul `PUT`).
* Pentru cererile `PUT` către `/items/{item_id}`, citește corpul cererii ca JSON:
  * Verifică că acesta conține un atribut obligatoriu `name`, care trebuie să fie de tip `str`.
  * Verifică că acesta conține un atribut obligatoriu `price`, care trebuie să fie de tip `float`.
  * Verifică că acesta conține un atribut opțional `is_offer`, care trebuie să fie de tip `bool`, dacă este prezent.
  * Toate aceste verificări se aplică și pentru obiectele JSON **profund imbricate**.
* Conversia din și în JSON se realizează automat.
* Documentează totul utilizând **OpenAPI**, care poate fi folosit pentru:
  * Sisteme interactive de documentație.
  * Sisteme automate de generare de cod client, pentru multiple limbaje de programare.
* Oferă două interfețe web interactive pentru documentație.

---

Deși am atins doar suprafața subiectului, deja ai o idee despre modul în care functionează totul.

Încearcă să înlocuiești liniile de mai jos:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...de la:

```Python
        ... "item_name": item.name ...
```

...la:

```Python
        ... "item_price": item.price ...
```

...și observă cum editorul tau va completa automat atributele și va recunoaște tipurile acestora:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Pentru un exemplu mai complet, care include mai multe funcționalități, consultă <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Ghidul utilizatorului</a>.

**Atenție, spoiler!** "Tutorialul - Ghidul utilizatorului" include:
* Declararea **parametrilor** din diverse surse, cum ar fi: **anteturi (headers)**, **cookie-uri**, **câmpuri de formular HTML** și **fișiere**.
* Modul de configurare a restricțiilor de validare, precum `maximum_length` sau `regex`.
* Un sistem de **<abbr title="cunoscut și sub denumirea de componente, resurse, furnizori, servicii, injectabile">Injecție de dependențe</abbr>** foarte puternic și ușor de utilizat.
* Securitate și autentificare, inclusiv suport pentru **OAuth2** cu **token-uri JWT** și autentificare **HTTP Basic**.
* Tehnici mai avansate (dar la fel de simple) pentru definirea **modelelor JSON profund imbricate** (datorită Pydantic).
* Integrarea **GraphQL** cu <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> și alte biblioteci.
* Multe funcționalități suplimentare (datorită Starlette), precum:
  * **WebSockets**
  * Teste extrem de simple bazate pe HTTPX și `pytest`
  * **CORS**
  * Sesiuni bazate pe Cookie-uri
  * ...și multe altele.


## Performanța

Benchmark-urile independente realizate de TechEmpower arată că aplicațiile bazate pe FastAPI, rulând sub Uvicorn, sunt <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">printre cele mai rapide aplicații Python disponibile</a>, fiind depășite doar de Starlette și Uvicorn (utilizate intern de FastAPI). (*)

Pentru a înțelege mai bine acest aspect, consultă secțiunea <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmark-uri</a>.

## Dependențe

FastAPI depinde de Pydantic si Starlette.

### Dependențe `standard`

Când instalezi FastAPI cu `pip install "fastapi[standard]"`, acesta include grupul de dependențe opționale standard:

Utilizate de Pydantic:
  * <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> – pentru validarea adreselor de email.

Utilizate de Starlette:
  * <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> – necesar dacă dorești să utilizezi TestClient.
  * <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> – necesar dacă dorești să utilizezi configurația implicită a șabloanelor.
  * <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> – necesar dacă dorești suort pentru <abbr title="convertirea șirului primit într-o cerere HTTP în date Python">"parsing-ul"</abbr> formularelor, utilizând request.form().

Utilizate de FastAPI / Starlette:
  * <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> – pentru serverul care încarcă și servește aplicația. Acesta include uvicorn[standard], care conține unele dependențe (de exemplu, uvloop) necesare pentru un server de înaltă performanță.
  * fastapi-cli – oferă interfața linie de comanda fastapi.

### Fără dependențele standard

Dacă nu dorești să incluzi dependențele opționale standard, poți instala FastAPI cu `pip install fastapi` în loc de `pip install "fastapi[standard]"`.

### Dependențe opționale suplimentare

Există și alte dependențe suplimentare pe care le poți instala, în funcție de necesități.

Dependențe opționale suplimentare pentru Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> – pentru gestionarea configurațiilor și a setărilor.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> – oferă tipuri suplimentare utilizabile cu Pydantic.

Dependențe opționale suplimentare pentru FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> – necesar dacă dorești să utilizezi ORJSONResponse.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> – necesar dacă dorești să utilizezi UJSONResponse.

## Licență

Acest proiect este licențiat sub termenii de licențiere MIT.

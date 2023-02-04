<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI keretrendszer, nagy teljesítményű, könnyen tanulható, gyors fejlesztést lehetővé tevő, production ready</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Teszt">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Csomag verzió">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Támogatott Python verziók">
</a>
</p>

---

**Dokumentáció**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Forráskód**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

A FastAPI egy modern, gyors (nagy teljesítményű) webes keretrendszer API-k készítéséhez Python 3.7+ nyelven, a Python szabványos típusjelöléseire építve.

A főbb jellemzők:

* **Gyors**: Nagyon magas teljesítmény, a **NodeJS**-el és **Go**-val egyenrangú (a Starlette-nek és a Pydantic-nek köszönhetően). [Egyike a leggyorsabb Python keretrendszereknek](#teljesitmeny).
* **Gyors fejlesztés**: Kb. 200% és 300% közötti fejlesztési sebességnövekedés. *
* **Kevesebb hiba**: Kb. 40%-al csökkenthető az emberi tényezők okozta fejlesztői hibák száma. *
* **Intuitív**: Kiváló editor támogatás. <abbr title="más néven auto-complete, autocompletion, IntelliSense">Kiegészítés</abbr> mindenhol. Kevesebb hibakereséssel töltött idő.
* **Egyszerű**: Könnyen tanulható és használható. Kevesebb dokumentációt kell olvasni.
* **Kisméretű**: Kód duplikáció minimalizálása. Több funkció minden paraméter deklarációhoz. Kevesebb hiba.
* **Szilárdság**: Production ready kód. Automatizált interaktív dokumentációval.
* **Szabványos**: Az API-k nyílt forrású szabványaira épít (és azokkal teljesen kompatibilis): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (előtte Swagger néven ismert) és <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* egy belső fejlesztőcsapat tesztjei alapján történő becslés, production alkalmazások építése.</small>

## Támogatók

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">További támogatók</a>

## Vélemények

"_[...] Mostanában nagyon sokat használom a **FastAPI**-t. [...] Tulajdonképpen azt tervezem, hogy a  csapatom összes **ML szolgáltatásához a Microsoftnál** ezt használjuk. Ezek közül néhányat integrálunk is magába a **Windows** termékbe és néhány **Office** termékbe is._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Átvettük a **FastAPI** könyvtárat, hogy olyan **REST** kiszolgálót hozzunk létre, amelyet az **előrejelzések** lekérdezésére lehet használni. [a Ludwig számára]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_A **Netflix** örömmel jelenti be **válságkezelési** orchestration keretrendszerének nyílt forrású változatát: **Dispatch**! [**FastAPI**-val készült]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Nagyon lelkesít a **FastAPI**. Annyira szórakoztató!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Őszintén szólva, amit felépítettél, az nagyon szilárdnak és kifinomultnak tűnik. Sok szempontból olyan, mint amilyennek a **Hug**-ot szeretném látni - nagyon inspiráló, hogy valaki ilyet készít._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Ha szeretnél megtanulni egy **modern keretrendszert** REST API-k létrehozásához, nézd meg a **FastAPI**-t [...] Gyors, egyszerűen használható és könnyen tanulható [...]_"

"_Átálltunk a **FastAPI**-ra az **API**-jainknál [...] Szerintem kedvelni fogod [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, a CLI-k FastAPI-ja

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Ha webes API helyett inkább terminálban használható <abbr title="Command Line Interface">CLI</abbr> alkalmazást készítenél, nézd meg a <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>t.

A **Typer** a FastAPI kistestvére. A **CLI-k FastAPI-ja**. ⌨️ 🚀

## Követelmények

Python 3.7+

A FastAPI óriások vállán áll:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> a webes részekhez.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> az adatokhoz.

## Telepítés

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Szükség van még egy ASGI szerverre is a production-höz, mint a <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> vagy a <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Példa

### Hozd létre

* Hozz létre egy `main.py` fájlt a következő tartalommal:

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
<summary>Vagy az <code>async def</code>-et használva...</summary>

Ha a kódod az `async` / `await` megoldással él, akkor használd az `async def`-et:

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

**Megjegyzés**:

Ha még nem ismered, olvasd el a _"Sietsz?"_ szakaszt a dokumentációban az <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` és `await` használatáról</a>.

</details>

### Futtasd

A szervert a következőképpen futtasd:

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
<summary>Néhány szó a <code>uvicorn main:app --reload</code>-ról...</summary>

A `uvicorn main:app` parancsban az egyes részek jelentése:

* `main`: a `main.py` fájl (a Python "module").
* `app`: a `main.py`-ban, az `app = FastAPI()` sorral létrehozott objektum.
* `--reload`: azt mondja meg a szervernek, hogy az minden változtatáskor újratöltsön. Csak fejlesztéshez használd.

</details>

### Próbáld ki

A böngészőben nyisd meg a <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> hivatkozást.

A következő JSON választ kell látnod:

```JSON
{"item_id": 5, "q": "somequery"}
```

Már létrehoztál egy API-t, ahol:

* HTTP kéréseket fogadunk a `/` és a `/items/{item_id}` _útvonalakon_.
* Mindkét _útvonal_ a `GET` <em>műveletet</em> használja (másik elnevezés: HTTP _metódus_).
* A `/items/{item_id}` _útvonalnak_ van egy _path paramétere_, az `item_id`, aminek `int` típusúnak kell lennie.
* A `/items/{item_id}` _útvonalnak_ még van egy opcionális, `str` típusú _query paramétere_ is, a `q`.

### Interaktív API documentáció

Most nyisd meg a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> linket.

A megjelenő oldal egy interaktív dokumentáció (amit a <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>-val hozunk létre):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatív API dokumentáció

Most pedig a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> linket nyisd meg.

Egy másik, alternatív dokumentációt látsz (ezt a <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> biztosítja):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Frissítési példa

Módosítsuk a `main.py` fájlt úgy, hogy fogadjon egy body-t egy `PUT` kéréstől.

A Pydantic segítségével szabványos Python típusokat használva deklaráljuk a body-t.

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

A szerver automatikusan újratölt (mivel fentebb hozzáadtuk a `--reload`-ot a `uvicorn` parancshoz).

### Az interaktív API dokumentáció frissítése

Most nyisd meg a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> linket.

* Az interaktív API dokumentáció automatikusan frissült, már tartalmazza az új body-t:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Kattints a "Try it out" gombra, ezzel megadhatod a paramétereket, és közvetlenül meghívhatod az API-t:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Most kattints az "Execute" gombra, amivel a felhasználói felület kapcsolatot létesít az API-val, elküldi a paramétereket és visszakapja az eredményt, ami így néz ki a képernyőn:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Az alternatív API dokumentáció frissítése

Kattints a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> linkre.

* Az alternatív dokumentáció szintén frissült az új paraméterrel és body-val:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Összefoglalás

Tehát összefoglalva, **egyszer** kell megadnod a paraméterek, body stb. típusait függvény paraméterként.

Ezt szabványos Python típusokkal megteheted.

Nem kell új szintaktikát vagy speciális könyvtárak metódusait, osztályait megtanulnod.

Csak a szabványos **Python 3.7+**-re van szükséged.

Például, egy `int`-hez:

```Python
item_id: int
```

vagy egy komplexebb  `Item` modellhez:

```Python
item: Item
```

...és ez az egyetlen deklaráció biztosítja számodra:

* A szövegszerkesztő támogatását, beleértve:
    * a kódkiegészítést és a
    * a típusellenőrzést.
* Az adatellenőrzést:
    * Automatikus és tiszta hibaüzeneteket, amikor az adat érvénytelen.
    * Ellenőrzést még mélyen beágyazott JSON objektumok esetén is.
* A hálózatról bejövő adatok <abbr title="ismerős lehet még mint: serialization, parsing, marshalling">konvertálását</abbr> Python adatokra és típusokra. Értelmezi:
    * a JSON-t
    * az útvonal paramétereket
    * a query paramétereket
    * a cookie-kat
    * a fejléceket
    * a formokat és a
    * a fájlokat.
* A kimenő Python adatok és típusok <abbr title="ismerős lehet még mint: serialization, parsing, marshalling">konvertálását</abbr> hálózati adatra (JSON):
    * Python típusok átalakítása (`str`, `int`, `float`, `bool`, `list` stb.)
    * `datetime` objektumok
    * `UUID` objektumok
    * adatbázis modellek
    * ...és még sok minden mást.
* Automatikus, interaktív API dokumentációt, 2 alternatív felhasználói felülettel:
    * Swagger UI és
    * ReDoc.

---

Visszatérve az előző kódra, a **FastAPI**:

* Ellenőrzi, hogy van-e egy `item_id` az útvonal `GET` és `PUT` kéréseiben.
* Ellenőrzi, hogy az `item_id` típusa `int` a `GET` és `PUT` kérésekben.
    * Ha nem, akkor egy könnyen érthető, világos hibaüzenetet kap a kliens.
* Megvizsgálja, van-e opcionális `q` paraméter (mint pl. a `http://127.0.0.1:8000/items/foo?q=somequery`-ben) a `GET` kérésekben.
    * Mivel a `q` paraméter `= None`-al van deklarálva, ezért opcionális.
    * A `None` nélkül kötelező lenne (mint a body a `PUT` kérésben).
* Ad egy `PUT` kérést a `/items/{item_id}`-hez, beolvassa a body-t JSON-ként:
    * Leellenőrzi a kötelező `name` mezőt, hogy az `str`.
    * A kötelező `price` mezőnek pedig `float`-nak kell lennie.
    * Azt is megvizsgálja, hogy az opcionális `is_offer` mező jelen van-e és `bool`-e.
    * És mindez a mélyen beágyazott JSON objektumok esetén is működik.
* Automatikusan konvertál JSON-ba és JSON-ból.
* Mindent dokumentál az OpenAI-val, amit lehet használni:
    * Interaktív dokumentációs rendszerekben
    * Automata kliens kód generáló rendszerekben, sokféle nyelvhez illesztve.
* Közvetlenül kétféle interaktív webes dokumentációs rendszert biztosít.

---

Csak a felszínt karcoljuk meg, és máris jobban érted, hogyan működik az egész.

Próbáld ki, hogy megváltoztatod ebben a sorban:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...ezt:

```Python
        ... "item_name": item.name ...
```

...erre:

```Python
        ... "item_price": item.price ...
```

...és látni fogod, hogy a szerkesztő automatikuasn kiegészíti a mezőt és ismeri a típusát is:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Ha egy részletesebb példát szeretnél látni, amelyik még több funkciót mutat be, nézd meg az <a href="https://fastapi.tiangolo.com/tutorial/">Útmutató - Felhasználói kézikönyvet</a>.

**Spoiler alert**: az útmutató - felhasználói kézikönyv tartalmaz:

* **Paraméterek** deklarációját különféle helyeken: **header**, **cookie**, **form mező** és **fájl**.
* Hogyan állíts be **ellenőrzési megszorításokat**, mint pl. a `maximum_length` vagy a `regex`.
* Hogyan használd a nagyon hatékony és könnyű **<abbr title="más néven komponensek, erőforrások (resources), szolgáltatók (providers), szervízek (services), befecskendezések (injections)">Dependency Injection (Függőség befecskendezése)</abbr>** rendszert.
* Biztonság és autentikáció, **OAuth2** **JWT tokenekkel** és **HTTP Basic** auth támogatása.
* Fejlettebb (de hasonlóan egyszerű) megoldások **mélyen beágyazott JSON modellek** deklarálására (a Pydantic-nak köszönhetően).
* **GraphQL** integráció a <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a>-vel és egyéb könyvtárakkal.
* Rengeteg extra képesség (a Starlette-nek köszönhetően), mint pl.:
    * **WebSocketek**
    * nagyon egyszerű tesztek HTTPX-en és `pytest`-en
    * **CORS**
    * **Cookie Session-ök**
    * ...és még sok minden más.

## Teljesítmény

Uvicorn alatt futtatott **FastAPI** alkalmazások független TechEmpower teljesítménymutatóit láthatod a <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">one of the fastest Python frameworks available</a> linken, csak Starlette és Uvicorn alatt (a FastAPI beépítetten használja). (*)

További információkért, nézd meg a <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> szekciót.

## Opcionális függőségek

Pydantic-ot használva:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - gyorsabb JSON <abbr title="A HTTP kérésből jövő sztringet konvertálja Python adattá">"parsing"</abbr>-hoz.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - email ellenőrzéshez.

Starlette-et használva:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Akkor szükséges, ha `TestClient`-et szeretnél használni.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Az alapértelmezett template-hez szükséges.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Ha <abbr title="A HTTP kérésből jövő sztringet konvertálja Python adattá">"parsing"</abbr> támogatást szeretnél `request.form()`-okkal, akkor szükséged van rá.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - A `SessionMiddleware` támogatáshoz kell.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - A Starlette `SchemaGenerator` támogatáshoz kell (valószínűleg nincs rá szükséged a FastAPI-val).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Ha `UJSONResponse`-t szeretnél használni, akkor szükséges.

FastAPI / Starlette-et használva:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - szerver az alkalmazásod betöltéséhez és a kérések kiszolgálásához.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Ha `ORJSONResponse`-t szeretnél használni, akkor szükséged lesz rá.

Mindezeket együtt a `pip install "fastapi[all]"` paranccsal telepítheted.

## Licenc

Ennek a projektnek a licencelése az MIT licenc alapján történik.
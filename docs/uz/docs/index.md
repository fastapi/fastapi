# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
    <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
        <em>FastAPI frameworki, juda tez, o‘qish oson, tez kod yozish, production ga tayyor</em>
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

**Hujjatlar**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Manba kodi**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI — bu zamonaviy, tez (yuqori samaradorlikka ega), Python uchun API yaratishda ishlatiladigan web-framework bo‘lib, standart Python tip ko‘rsatkichlariga asoslanadi (type hintlar).

Asosiy xususiyatlari:

* **Tez**: Juda yuqori samaradorlik, **NodeJS** va **Go** bilan teng (Starlette va Pydantic tufayli). [Python uchun eng tez frameworklardan biri](#performance).
* **Tez kod yozish**: Funksiyalarni ishlab chiqish tezligini taxminan 200% dan 300% gacha oshiradi. *
* **Kamroq xatolik**: Inson (dasturchi) tomonidan yuzaga keladigan xatolarni taxminan 40% ga kamaytiradi. *
* **Intuitiv**: Ajoyib muharrir yordami. <abbr title="avto-to‘ldirish, autocompletion, IntelliSense">To‘ldirish</abbr> har yerda. Kamroq vaqtni nosozliklarni tuzatishga sarflaysiz.
* **Oson**: Foydalanish va o‘rganish uchun qulay. Kamroq vaqt hujjatlarni o‘qishga ketadi.
* **Qisqa**: Kodni takrorlashni minimallashtiradi. Har bir parametr e’lonidan bir nechta imkoniyatlar. Kamroq xatolik.
* **Barqaror**: Ishlab chiqarishga tayyor kodga ega bo‘lasiz. Avtomatik interaktiv hujjatlar bilan.
* **Standartlarga asoslangan**: API uchun ochiq standartlarga asoslangan (va to‘liq mos): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (ilgari Swagger nomi bilan tanilgan) va <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* ishlab chiqarish ilovalarini yaratishda ichki dasturchilar jamoasida o‘tkazilgan testlar asosida baholangan.</small>

## Homiylar

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Boshqa homiylar</a>

## Fikrlar

"_[...] Men hozirda **FastAPI** dan juda ko‘p foydalanmoqdaman. [...] Aslida, uni jamoamdagi barcha **ML xizmatlari** uchun ishlatishni rejalashtiryapman. Ularning ba’zilari asosiy **Windows** mahsulotiga va ba’zilari **Office** mahsulotlariga integratsiya qilinmoqda._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(manba)</small></a></div>

---

"_Biz **FastAPI** kutubxonasini **REST** serverini ishga tushirish uchun qabul qildik, u orqali **bashoratlar** olish mumkin. [Ludwig uchun]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin va Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(manba)</small></a></div>

---

"_**Netflix** o‘zining **inqiroz boshqaruvi** orkestratsiya frameworki: **Dispatch** ni ochiq manba sifatida chiqarganini mamnuniyat bilan e’lon qiladi! [**FastAPI** yordamida yaratilgan]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(manba)</small></a></div>

---

"_Men **FastAPI** dan juda hayajondaman. Bu juda qiziqarli!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podkast boshlovchisi</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(manba)</small></a></div>

---

"_Rostini aytsam, siz yaratgan narsa juda mustahkam va sayqallangan ko‘rinadi. Ko‘p jihatdan, bu men **Hug** bo‘lishini istagan narsam edi — kimdir bunday narsani yaratganini ko‘rib, ilhomlanaman._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> yaratuvchisi</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(manba)</small></a></div>

---

"_Agar siz **REST API** lar qurish uchun zamonaviy framework o‘rganmoqchi bo‘lsangiz, **FastAPI** ga qarang [...] Bu tez, ishlatish va o‘rganish oson [...]_"

"_Biz **API** larimiz uchun **FastAPI** ga o‘tdik [...] Sizga yoqadi deb o‘ylayman [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> asoschilari - <a href="https://spacy.io" target="_blank">spaCy</a> yaratuvchilari</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(manba)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(manba)</small></a></div>

---

"_Agar kimdir ishlab chiqarish uchun Python API yaratmoqchi bo‘lsa, men **FastAPI** ni tavsiya qilaman. Bu **chiroyli ishlab chiqilgan**, **foydalanish uchun oddiy** va **juda kengaytiriladigan** framework, u bizning API birinchi rivojlanish strategiyamizda asosiy komponentga aylandi va ko‘plab avtomatlashtirishlar va xizmatlarni, jumladan Virtual TAC Engineer’imizni boshqaradi._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(manba)</small></a></div>

---

## **Typer**, CLI lar uchun FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Agar siz web API o‘rniga terminalda ishlatiladigan <abbr title="Command Line Interface">CLI</abbr> dastur yaratmoqchi bo‘lsangiz, <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> ga e’tibor bering.

**Typer** — bu FastAPI ning kichik ukasi. U aynan **CLI lar uchun FastAPI** bo‘lishi uchun yaratilgan. ⌨️ 🚀

## Talablar

FastAPI ulkanlar yelkasida turadi:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> web tomoni uchun.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> data part uchun.

## O‘rnatish

<a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">Virtual atrofni</a> yarating va faollashtiring, so‘ng FastAPI ni o‘rnating:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Eslatma**: `"fastapi[standard]"` ni qo‘shtirnoq ichida yozing, shunda barcha terminallarda to‘g‘ri ishlaydi.

## Misol

### Yarating

`main.py` fayl ni yarating pastdagi kod bilan:

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
<summary>Yoki <code>async def</code>... ni ishlating.</summary>

Agar sizni kodiz `async` / `await` asosiy so‘zlarni ishlatsa, `async def` ni ishlating:

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

**E’tibor bering**:
Agar bilmasangiz, hujjatlardagi <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` va `await` haqida "Shoshilinchmisiz?" bo‘limiga</a> qarang.

</details>

### Uni ishga tushirish

Serverni ishga tushirish uchun:

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
<summary><code>fastapi dev main.py</code>... komanda haqida</summary>

`fastapi dev` buyrug‘i sizning `main.py` faylingizni o‘qiydi, undagi **FastAPI** ilovasini aniqlaydi va <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> yordamida serverni ishga tushiradi.

Standart holatda, `fastapi dev` lokal ishlab chiqish uchun avtomatik qayta yuklash (auto-reload) rejimida ishga tushadi.

Bu haqda batafsil ma’lumotni <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI hujjatlarida</a> o‘qishingiz mumkin.

</details>

### Tekshirish

Browser da <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> ni oching.

Shunga o'xshagan JSON javob ko'rasiz:

```JSON
{"item_id": 5, "q": "somequery"}
```

Siz allaqachon quyidagi API ni yaratdingiz:

* HTTP so‘rovlarini quyidagi _yo‘llar_ da qabul qiladi: `/` va `/items/{item_id}`.
* Har ikkala _yo‘l_ ham `GET` <em>operatsiyalarini</em> (HTTP _usullari_ deb ham ataladi) qabul qiladi.
* `/items/{item_id}` _yo‘li_ da `item_id` nomli _yo‘l parametri_ bor va u `int` bo‘lishi kerak.
* `/items/{item_id}` _yo‘li_ da ixtiyoriy `str` tipidagi _so‘rov parametri_ `q` mavjud.

### Interaktiv API hujjatlar

Endi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> manziliga o'ting.

Siz avtomatik interaktiv API hujjatlarini ( <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tomonidan taqdim etilgan) ko'rasiz:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Muqobil API hujjatlari

Endi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> manziliga o'ting.

Siz muqobil avtomatik hujjatlarni ( <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tomonidan taqdim etilgan) ko'rasiz:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Misolni yangilash

Endi `main.py` faylini `PUT` so‘rovlaridan body (tanani) qabul qiladigan qilib o‘zgartiring.

Body ni Pydantic yordamida, standart Python tiplari orqali e’lon qiling.

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

`fastapi dev` serveri avtomatik tarzda qayta yuklanadi.

### Interaktiv API hujjatlarini yangilash

Endi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> manziliga o'ting.

* Interaktiv API hujjatlari avtomatik tarzda yangilanadi, yangi body ham ko‘rsatiladi:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" tugmasini bosing, bu sizga parametrlarni to‘ldirish va API bilan bevosita ishlash imkonini beradi:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Keyin "Execute" tugmasini bosing, foydalanuvchi interfeysi sizning API’ga so‘rov yuboradi, parametrlarni jo‘natadi, natijalarni oladi va ekranda ko‘rsatadi:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Muqobil API hujjatlarini yangilash

Endi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> manziliga o'ting.

* Muqobil hujjatlar ham yangi so‘rov parametri va body ni aks ettiradi:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Qisqacha takrorlash

Xulosa qilib aytganda, siz **bir marta** parametrlar, body va boshqalar uchun turlarni funksiya parametrlarida e’lon qilasiz.

Buni zamonaviy Python tiplari yordamida qilasiz.

Yangi sintaksis, maxsus kutubxona metodlari yoki klasslarini o‘rganishingiz shart emas.

Faqat oddiy **Python**.

Masalan, `int` uchun:

```Python
item_id: int
```

yoki qiyinroq `Item` model uchun:

```Python
item: Item
```

...va o‘sha bitta bayonot bilan siz quyidagilarni olasiz:

* Muharrir (editor) yordami, jumladan:
    * Avto-to‘ldirish (completion).
    * Tiplarni tekshirish (type checks).
* Ma’lumotlarni tekshirish (validation):
    * Ma’lumotlar noto‘g‘ri bo‘lsa, avtomatik va aniq xatoliklar.
    * Hattoki chuqur joylashgan (deeply nested) JSON obyektlari uchun ham tekshiruv.
* Kiruvchi ma’lumotlarni <abbr title="serializatsiya, parsing, marshalling nomlari bilan ham tanilgan">konvertatsiya qilish</abbr>: tarmoqdan Python ma’lumotlari va turlariga o‘tkazish. Quyidagilardan o‘qish:
    * JSON.
    * Yo‘l (path) parametrlari.
    * So‘rov (query) parametrlari.
    * Cookies.
    * Sarlavhalar (headers).
    * Formalar.
    * Fayllar.
* Chiquvchi ma’lumotlarni <abbr title="serializatsiya, parsing, marshalling nomlari bilan ham tanilgan">konvertatsiya qilish</abbr>: Python ma’lumotlari va turlaridan tarmoq ma’lumotlariga (JSON ko‘rinishida) o‘tkazish:
    * Python turlarini (`str`, `int`, `float`, `bool`, `list` va boshqalar) konvertatsiya qilish.
    * `datetime` obyektlari.
    * `UUID` obyektlari.
    * Ma’lumotlar bazasi modellari.
    * ...va yana ko‘plab turlar.
* Avtomatik interaktiv API hujjatlari, 2 ta muqobil foydalanuvchi interfeysi bilan:
    * Swagger UI.
    * ReDoc.

---

Oldingi kod namunasi bo‘yicha, **FastAPI** quyidagilarni amalga oshiradi:

* `GET` va `PUT` so‘rovlari uchun yo‘lda `item_id` mavjudligini tekshiradi.
* `GET` va `PUT` so‘rovlari uchun `item_id` ning turi `int` ekanligini tekshiradi.
    * Agar u int bo‘lmasa, mijozga aniq va tushunarli xatolik ko‘rsatiladi.
* `GET` so‘rovlari uchun `q` nomli ixtiyoriy so‘rov parametrining mavjudligini tekshiradi (masalan, `http://127.0.0.1:8000/items/foo?q=somequery`).
    * `q` parametri `= None` bilan e’lon qilinganligi sababli, u ixtiyoriy hisoblanadi.
    * Agar `None` bo‘lmasa, u majburiy bo‘lardi (xuddi `PUT` da body majburiy bo‘lgani kabi).
* `/items/{item_id}` ga `PUT` so‘rovlari uchun body ni JSON sifatida o‘qiydi:
    * Unda majburiy `name` atributi borligini va u `str` bo‘lishi kerakligini tekshiradi.
    * Majburiy `price` atributi borligini va u `float` bo‘lishi kerakligini tekshiradi.
    * Ixtiyoriy `is_offer` atributi borligini va u (agar mavjud bo‘lsa) `bool` bo‘lishi kerakligini tekshiradi.
    * Bularning barchasi chuqur joylashgan (deeply nested) JSON obyektlari uchun ham ishlaydi.
* Avtomatik tarzda JSON ga va JSON dan konvertatsiya qiladi.
* Hammasini OpenAPI yordamida hujjatlashtiradi, bu quyidagilar uchun ishlatilishi mumkin:
    * Interaktiv hujjatlash tizimlari.
    * Ko‘plab dasturlash tillari uchun avtomatik mijoz kodi generatsiyasi tizimlari.
* To‘g‘ridan-to‘g‘ri 2 ta interaktiv hujjatlash web interfeysini taqdim etadi.

---

Biz faqat yuzaki ko‘rib chiqdik, lekin siz allaqachon hammasi qanday ishlashini tushundingiz.

Quyidagi qatorni o‘zgartirib ko‘ring:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...bu joyni:

```Python
        ... "item_name": item.name ...
```

...quyidagiga o‘zgartiring:

```Python
        ... "item_price": item.price ...
```

...va muharriringiz atributlarni avtomatik to‘ldirishini va ularning turlarini bilishini ko‘ring:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Ko‘proq imkoniyatlarni o‘z ichiga olgan to‘liqroq misol uchun <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a> bo‘limiga qarang.

**Ogohlantirish (spoiler)**: tutorial - foydalanuvchi qo‘llanmasida quyidagilar mavjud:

* **Parametrlarni** boshqa joylardan e’lon qilish: **headerlar**, **cookie**lar, **forma maydonlari** va **fayllar**.
* **Validatsiya cheklovlarini** o‘rnatish, masalan: `maximum_length` yoki `regex`.
* Juda qulay va kuchli **<abbr title="komponentlar, resurslar, providerlar, servislar, injectables nomi bilan ham tanilgan">Dependency Injection</abbr>** tizimi.
* Xavfsizlik va autentifikatsiya, jumladan **OAuth2** va **JWT tokenlar**, hamda **HTTP Basic** autentifikatsiyasi.
* **Pydantic** yordamida **chuqur joylashgan JSON modellari**ni e’lon qilishning ilg‘or (lekin oson) usullari.
* **GraphQL** integratsiyasi: <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> va boshqa kutubxonalar yordamida.
* Ko‘plab qo‘shimcha imkoniyatlar (Starlette tufayli), jumladan:
    * **WebSocket**lar
    * HTTPX va `pytest` asosidagi juda oson testlar
    * **CORS**
    * **Cookie Session**lar
    * ...va boshqalar.

## Performance

Mustaqil TechEmpower benchmark natijalari shuni ko‘rsatadiki, **FastAPI** ilovalari Uvicorn ostida <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eng tez ishlaydigan Python frameworklaridan biri</a> hisoblanadi, faqat Starlette va Uvicorn (FastAPI ichida ishlatiladi) dan keyin turadi. (*)

Batafsil ma’lumot uchun <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> bo‘limiga qarang.

## Bog‘liqliklar

FastAPI Pydantic va Starlette kutubxonalariga bog‘liq.

### `standard` bog‘liqliklar

Agar siz FastAPI ni `pip install "fastapi[standard]"` orqali o‘rnatsangiz, u `standard` guruhidagi ixtiyoriy bog‘liqliklar bilan birga keladi:

Pydantic tomonidan ishlatiladi:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> — email manzillarini tekshirish uchun.

Starlette tomonidan ishlatiladi:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> — agar siz `TestClient` dan foydalanmoqchi bo‘lsangiz, talab qilinadi.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> — standart shablon konfiguratsiyasidan foydalanish uchun kerak bo‘ladi.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> — forma <abbr title="HTTP so‘rovdan kelgan satrni Python ma’lumotlariga aylantirish">"parsing"</abbr> ni qo‘llab-quvvatlash uchun, `request.form()` bilan ishlatiladi.

FastAPI / Starlette tomonidan ishlatiladi:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> — ilovangizni yuklab, serverda ishga tushirish uchun. Bu `uvicorn[standard]` ni o‘z ichiga oladi, u yuqori samaradorlik uchun kerakli ba’zi bog‘liqliklarni (masalan, `uvloop`) o‘z ichiga oladi.
* `fastapi-cli` — `fastapi` buyrug‘ini taqdim etadi.

### `standard` bog‘liqliklarsiz

Agar siz `standard` ixtiyoriy bog‘liqliklarni o‘rnatishni xohlamasangiz, `pip install fastapi` buyrug‘i orqali o‘rnating (`pip install "fastapi[standard]"` o‘rniga).

### Qo‘shimcha ixtiyoriy bog‘liqliklar

Qo‘shimcha o‘rnatishingiz mumkin bo‘lgan ba’zi bog‘liqliklar mavjud.

Qo‘shimcha ixtiyoriy Pydantic bog‘liqliklari:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> — sozlamalarni boshqarish uchun.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> — Pydantic bilan ishlatish uchun qo‘shimcha turlar.

Qo‘shimcha ixtiyoriy FastAPI bog‘liqliklari:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> — agar siz `ORJSONResponse` dan foydalanmoqchi bo‘lsangiz, talab qilinadi.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> — agar siz `UJSONResponse` dan foydalanmoqchi bo‘lsangiz, talab qilinadi.

## Litsenziya

Ushbu loyiha MIT litsenziyasi shartlariga muvofiq litsenziyalangan.

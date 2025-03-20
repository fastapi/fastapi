
{!../../docs/missing-translation.md!}


# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI фреймворк, өндөр гүйцэтгэлтэй, сурахад хялбар, хурдан кодлох боломжтой, ашиглалтанд оруулахад бэлэн</em>
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

**Документ**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Эх код**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI нь Python type hint стандартад суурилсан, API хөгжүүлэх зориулалттай, орчин үеийн, хурдан (өндөр гүйцэтгэлтэй) вэб фреймворк юм.
{ .annotate }

1. `тайп хинт` - Тохиромжтой Монгол орчуулга байгаагүй тул Англи галигаар нь үлдээв.

Гол онцлогууд нь:

* **Хурд**: **NodeJS** болон **Go**-тэй адил түвшний маш хурдан гүйцэтгэлтэй (Starlette ба Pydantic-ийн ачаар). [Хамгийн хурдан Python фреймворкийн нэг](#_11).
* **Кодлоход хурдан**: Ямар нэгэн шинэ зүйл хөгжүүлэх хурдыг 200-гаас 300% нэмэгдүүлнэ. *
* **Алдааг багасгана**:  Хүнээс үүдэлтэй (инженерээс) алдааг 40% орчим бууруулна. *
* **Ойлгомжтой**: Код эдитэрийн дэмжлэг сайтай. Код эдитэрийн <abbr title="Өөрөөр: auto-complete, autocompletion, IntelliSense">зөвлөгөө</abbr> маш их тул алдааг засахад зарцуулах хугацаа бага.
* **Хялбар**: Сурч, хэрэглэхэд амархан. Документ унших шаардлага бага.
* **Богинохон**: Кодын давхардал багатай. Параметр ашиглан  функцуудыг удирдах боломжтой. Алдаа багатай.
* **Бат бөх**: Интерактив документтэй, борлуулалтанд бэлэн код хөгжүүлэхэд нэн тохиромжтой.
* **Стандартад нийцсэн**: Дараах API-ийн стандартад нийцсэн, бас түүн дээр суурилсан: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (Өмнө нь Swagger гэж нэрлэгддэг байсан), <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Шууд ашиглалтанд оруулахад зориулагдсан програмууд хөгжүүлэх явцад хийгдсэн туршилтуудад үндэслэв.</small>

## Спонсор

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">бусад спонсорууд</a>

## Коммент

"_[...] **FastAPI**-г сүүлийн үед маш их ашиглаж байна. [...] Энэ чигээрээ **Microsoft**-ийн багийнхаа бүх **ML**-д, зарим нь **Windows**-ийн үндсэн бүтээгдэхүүн, зарим нь **Office**-ийн бүтээгдэхүүнүүдэд **FastAPI**-ийг ашиглахаар төлөвлөж байна._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Бид **FastAPI**-г ашиглан **REST** серверийг хөгжүүлж, түүгээр дамжуулан **прогноз/таавар** авч байна. [Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** нь **уналтын менежмент** фремворк буюу **Dispatch**-ийг нээлттэй эх сурвалжтайгаар гаргаснаа зарлаж байгаадаа баяртай байна! [**FastAPI**-ээр бүтээсэн]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Би **FastAPI**-д маш их сэтгэл хангалуун, баяртай байна!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Яг үнэнийг хэлэхэд та бүхний бүтээсэн зүйл маш бат бөх, төгс харагдаж байна. **Hug**-г яг ийм байгаасай гэж төсөөлж байсан. Хэн нэгэн нь үүнийг бүтээж байгааг харахад урам орж байна._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> үүсгэн байгуулагч</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Хэрэв та REST API-г хөгжүүлэхэд зориулагдсан **орчин үеийн фремворк**-г сурахыг хүсэж байгаа бол, **FastAPI**-г шалгаарай [...] Хурдан, хэрэглэхэд хялбар, сурахад амар [...]_"

"_Бид **API**-аа **FastAPI**-гаар хийхээр болсон. [...] Та бүхэн ч бас тэгнэ гэж найдаж байна. [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> үүсгэн байгуулагч - <a href="https://spacy.io" target="_blank">spaCy</a> үүсгэн байгуулагч</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Хэрэв хэн нэгэн нь борлуулалтанд бэлэн Python API хөгжүүлэхийг хүсч байвал, би **FastAPI**-г 100% санал болгоно.  **FastAPI** нь **төгс бүтээгдсэн**, **хэрэглэхэд хялбар** бөгөөд **томсгох, жижигсгэхэд түүртээд байхгүй**. Манай API-н хөгжүүлэлтийн стратегийн **түлхүүр бүрэлдэхүүн** болж, олон автоматаци болон үйлчилгээнд, тухайлбал манай Virtual TAC Engineer-д ашиглагдаж байна._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLI дахь FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Хэрэв та веб интерфейс биш, <abbr title="Command Line Interface">CLI</abbr> интерфейс апп хөгжүүлж байвал <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>-ийг шалгаарай!.

**Typer** нь FastAPI-ийн төрсөн дүү нь юм. **CLI дахь FastAPI** байхад зориулагдсан. ⌨️ 🚀

## Өмнөтгөл

FastAPI-ийн үндсэн тулгуур:

* Bеб-тэй холбоотой зүйлс: <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>.
* Дата болон өгөгдөлтэй холбоотой зүйлс: <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.

## FastAPI-г суулгах

<a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">Виртуал орчинг</a> үүсгэн идэвхижүүлээд FastAPI-г суулгана:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Тэмдэглэл**: Бүх терминал дээр асуудалгүй ажиллуулахын тулд `"fastapi[standard]"`-ийг хашилтад хийж бичихээ мартуузай.
## Жишээ

### Файл үүсгэцгээе

* Доорх код-оор `main.py` файлийг үүсгэнэ үү:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Сайн уу?": "Эх дэлхий минь!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Эсвэл <code>async def</code>-ийг...</summary>

Хэрэв код тань `async` / `await`-ийг ашигладаг бол, `async def`ийг ашиглана уу:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Сайн уу?": "Эх дэлхий минь!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Тэмдэглэл**:

Хэрэв та мэдэхгүй, эргэлзээд байвал, _"Яаралтай хэрэгтэй байна уу?"_ хэсгийг шалгана уу. <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` ба `await`-ийн тухай</a>.

</details>

### Хэрэгжүүлцгээе

Доорх коммандаар серверээ асаана уу:

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
<summary><code>fastapi dev main.py</code> коммандын тухай...</summary>

`fastapi dev` комманд нь `main.py` файлыг уншснаар доторх **FastAPI**-г олон, <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>-ийг ашиглан серверийг асаана.

`fastapi dev` комманд нь нэмэлт тохиргоогүйгээр, локал хөгжүүлэлтийн үе дэх кодны өөрчлөлтийг автоматаар мэдэрч ре-старт хийнэ..

Энэ талаар дэлгэрэнгүйг <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">FastAPI CLI документ</a>-ээс уншина уу.

</details>

### Шалгацгаая

Энэ линк-ээр <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> браузер-аа нээнэ үү.

Доорхтой адил JSON хариу харагдах болно:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ингэснээр та аль хэдийн доорх API-г үүсгэсэн:

* HTTP хүсэлтийг `/` ба `/items/{item_id}`_хаяг_ дээр хүлээн авдаг API.
* 2 _хаяг_ хоёулаа `GET` гэсэн <em>үйл ажиллагаа</em> (HTTP протоколын `GET` _арга_)-тай API.
* `/items/{item_id}` _хаяг_ нь `item_id` гэж нэрлэгдсэн, `int` тайптай, зайлшгүй хэрэгтэй _**хаягийн параметртэй**_ API.
* Мөн `/items/{item_id}` _хаяг_ нь `q` гэж нэрлэгдсэн, `str` тайптай, зайлшгүй бус _**хайлтын параметртай**_ API.

### Интерактив API документ

<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>-г нээснээр та:

<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>-аар бүтээгдсэн, aвтомат интерактив API документ-ийг харах болно:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Хоёр дахь интерактив документ

Мөн <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>-г нээснээр:

<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>-ooр бүтээгдсэн, xоёр дахь автомат документ-ийг олж харах болно:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Дээрх жишээг үргэлжлүүлцгээе

`main.py` файлыг, `PUT` хүсэлтийг хүлээн авах зориулалттай болгон өөрчлье.

Pydantic-ийн ачаар body-г нь Python-ий стандарт тайп-аар зарлах боломжтой.

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
    return {"Сайн уу?": "Эх дэлхий минь!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` сервер нь автоматаар ре-старт хийх ёстой.

### Интерактив API документийн шинчлэлт

Дахин <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>-г нээнэ үү.

* Интерактив API документ маань автоматаар шинэ body-той болж шинэчлэгдсэн байх ёстой:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* "Try it out" гэсэн товчлуурыг дарснаар та API-тай интерактив харилцаа (харилцан нөлөөлөх харилцаа) хийх боломжтой болно:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Дараа нь "Execute" товч дээр дарснаар таны харч буй интерфэйс тань API-тай холбогдож, параметрүүдийг илгээн, хариуг авч, дэлгэцэн дээр харуулна:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Хоёр дахь интерактив API документийн шинчлэлт

Мөн <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>-ийг дахин нээнэ үү.

* Хоёр дахь документ маань ч бас шинэ хайлтын параметр болон шинэ body-г харуулах болно:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Товч дүгнэлт

Товчхондоо, та параметрүүд болон body гэх мэт зүйлсийн тайпыг, функцийн параметр болгон ганц л удаа зарлана.

Үүнийг орчин үеийн стандарт Python тайпаар л хийчихнэ.

Шинэ синтакс, тодорхой нэгэн library-ний аргачлал, класс зэргийг сураад байх шаардлага байхгүй.

Зүгээр л илүү ч үгүй дутуу ч үгүй, ориг Python.

Жишээлбэл, тоо `int` байхад:

```Python
item_id: int
```

Эсвэл комплекс `Item` модел байхад:

```Python
item: Item
```

Дээрх ганц удаагийн зарлалтаар та:

* Kод эдитэрийн тусламж:
    * Код гүйцэтгэлт.
    * Тайп шалгалт.
* Аргументийн шалгалт буюу баталгаажуулалт:
    * Аргумент нь алдаатай өөр үед, автоматaap тодорхой бөгөөд ойлгомжтой алдаат хариуг авна.
    * Аргумент нь маш гүн салаалсан комплекс JSON байсан ч хамаагүй ягш баталгаажуулалт хийгдэнэ.
* Ирэх өгөгдлийн <abbr title="Өөрөөр: сериалчлалт, парсчлах, маршаллах">хөрвүүлэлт</abbr>.<br> Дараах эх сурвалжаас ирсэн өгөгдлийг Python-ий дата ба тайп рүү хөрвүүлнэ:
    * JSON (JSON)
    * Хаягийн параметрүүд (Path parameters)
    * Хайлтын параметрүүд (Query parameters)
    * Күүки (Cookies)
    * Хүсэлтийн хедер (Headers)
    * Форм (Forms)
    * Файл (Files)
* Гарах өгөгдлийн <abbr title="Өөрөөр: сериалчлалт, парсчлах, маршаллах">хөрвүүлэлт</abbr>.<br> Дараах Python-ий дата ба тайпаас гарах өгөдлийг, JSON гэх мэт тайп руу хөрвүүлнэ:
    * Python тайп (`str`, `int`, `float`, `bool`, `list` гэх мэт)
    * `datetime` объект
    * `UUID` объект
    * Database модел
    * ...гэх мэтчилэн
* Дараах 2 төрлийн өөрийн гэсэн интерфэйстэй автомат интерактив API документтой:
    * Swagger UI.
    * ReDoc.

---

Дээрх кодын жишээнээс дурдахад, **FastAPI** нь:

* `GET` болон `PUT` хүсэлтийн хаягнд `item_id` байгаа эсэхийг шалгана.
* `GET` болон `PUT` хүсэлтийн `item_id` нь `int` тайп байхыг шалгана.
    * Хэрэв `int` тайп буюу тоо биш бол ойлгомжтой бөгөөд тодорхой алдаат хариуг илгээнэ.
* `GET` хүсэлтэнд `q` гэж нэрлэгдсэн зайлшгүй бус хайлтын параметр байгаа эсэхийг шалгана. (`http://127.0.0.1:8000/items/foo?q=somequery` гэх мэт)
    *  `q` параметр нь `= None` гэж зарлагдсан учраас байсан ч, байхгүй байсан ч болно. (3айлшгүй бус)
    * `None` биш бол, параметр нь залшгүй хэрэгтэй параметр болно. (Дээрх жишээний `PUT` хүсэлтэнд дурдагдсан body мэт).
* `/items/{item_id}` хаяг дээрх `PUT` хүсэлтийн body-г JSON гэж уншин:
    * `name` гэсэн `str` тайп байх ёстой, зайлшгүй хэрэгтэй атрибут байгаа эсэхийг шалгана.
    * `price` гэсэн `float` тайп байх ёстой, зайлшгүй хэрэгтэй атрибут байгаа эсэхийг шалгана.
    * `is_offer` гэсэн `bool` тайп байх ёстой, зайлшгүй бус атрибут байгаа эсэхийг шалгана.
    * Маш гүн салаалсан, комплекс JSON объект байсан ч үүн шиг шалгалт болон баталгаажуулалт явагдана.
* Автоматаар JSON-г хөрвүүлнэ.
* OpenAPI-аар бүх зүйлийг документчүүлэн:
    * Интерактив документ систэмд,
    * Автоматаар олон төрлийн хэлд зориулсан, клаянт код үүсгэх системд тус тус ашиглана.
* 2 төрлийн веб интерфэйс-тэй интерактив документийг санал болгоно.

---

Ингэснээр бид ердөө л мөсөн уулын оройг л хөндлөө, гэвч та аль хэдий нь яг яаж ажлаад байгааг тодорхой хэмжээгээр ойлгосон байх.

```Python
    return {"item_name": item.name, "item_id": item_id}
```

Дээрх эгнээг:

```Python
        ... "item_name": item.name ...
```
...aaс:

```Python
        ... "item_price": item.price ...
```

...луу солиод үзнэ үү. Таны код эдитэр атрибутын тайп зэргийг аль хэдийн мэдээд, кодыг тань автоматаар гүйцэтгээд өгч байгааг ажиглаарай:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Илүү өргөн хүрээтэй, олон боломжийг харуулсан жишээг үзэхийг хүсвэл <a href="https://fastapi.tiangolo.com/tutorial/">Сургалт – Хэрэглэгчийн гарын авлага</a>-аас хараарай.

**Спойлер**: Сургалт – Хэрэглэгчийн гарын авлага нь:

* **Параметрүүдийг** хэрхэн **хедер**, **күүки**, **форм**, **файл** зэрэг олон төрлийн эх үүсвэрээс хялбархан авч ашиглах талаар дурдана.
* `maximum_length` эсвэл `regex` зэрэг **аргументийн шалгуурыг** хэрхэн тохируулах талаар дурдана.
* Хэрэглэхэд хялбар атлаа маш хүчирхэг **<abbr title="өөрөөр components, resources, providers, services, injectables">Dependency Injection</abbr>** системийн тухай дурдана.
* **JWT токен**-той **OAuth2**-ийн тухай, мөн **HTTP Basic** нотолгоо зэргийг хавсаргасан аюулгүй байдал болон хамгаалалтын тухай дурдана.
* **Гүн салаалсан JSON модел**-ийг хэрхэн зарлах тухай гүнзгий түвшинд авч хэлэлцэнэ. (Гэхдээ нэг их хэцүү биш. Pydantic-ийн ачаар!)
* **GraphQL**-ийг <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> болон бусад library-тай интеграци хийх талаар дурдана.
* Starlette-ийн ачаар дараахи oлон нэмэлт онцлогийн талаар дурдана:
    * **WebSockets**
    * HTTPX and `pytest`  дээр суурилсан тест
    * **CORS**
    * **Cookie Sessions**
    * гэх мэтчилэн...

## Үзүүлэлт

TechEmpower-ийн бие даасан бенчмарк статистикт **FastAPI** нь Starlette болон Uvicorn-ийн дараагаар ордог, <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">хамгийн хурдан Python фреймворкуудын нэг</a> гэдгийг харуулсан байна. (Uvicorn, Starlette нь FastAPI-ийн дотор ашиглагддаг фремворк)

Үүний тухай илүү ихийг мэдэхийг хүсвэл <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Бенчмарк</a>хэсгийг үзнэ үү.

## Хамаарлууд

FastAPI нь Pydantic ба Starlette-ээс хараат фремворк юм.

### `standard` Хамаарлууд

FastAPI-г `pip install "fastapi[standard]"` коммандаар суулгахад, доорх  `standard` хамаарлуудтай хамт суулгагдана:

Pydantic-т ашиглагддаг:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - aргумент нь э-мэйл эсэхийг шалгагч бөгөөд хэрэв хэрэгтэй бол шаардлагатай.

Starlette-т ашиглагддаг:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Хэрэв `TestClient`-ийг ашиглах хэрэгтэй бол шаардлагатай.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Хэрэв дефолт загварын тохиргоог ашиглах хэрэгтэй бол шаардлагатай.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Хэрэв `request.form()`-ийг ашиглаж <abbr title="HTTP хүсэлтээс ирсэн өгөдлийг Python дата болгон хувиргах">"задлан шинжлэгээ"</abbr> хийх хэрэгтэй бол шаардлагатай.

FastAPI / Starlette-т ашиглагддаг:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - веб серверийн төлөөх хамаарал бөгөөд энэ нь `uvicorn[standard]` , улмаар `uvloop` зэрэг өндөр үзүүлэлттэй веб серверт хэрэгтэй хамаарлыг агуулсан.

* `fastapi-cli` - `fastapi` коммандын төлөөх хамаарал.

### `standard` хамаарал хэрэггүй бол:

Хэрэв таны апп-нд `standard` хамаарал хэрэггүй бол `pip install "fastapi[standard]"` биш `pip install fastapi` коммандаар FastAPI-г суулгана уу.

### Нэмэлт, зайлшгүй биш хамаарлууд

Таньд хэрэгтэй нэмэлт хамаарлууд байж магадгүй юм.

Жишээлбэл, нэмэлт Pydantic хамаарлуудаас дурдахад:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - тохиргооны зохицуулалтанд зориулагдсан.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic-т ашиглагдах нэмэлт тайп-нд зориулагдсан.

Hэмэлт FastAPI хамаарлуудаас дурдахад:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse`-г ашиглах хэрэгтэй бол шаардлагатай.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse`-г ашиглах хэрэгтэй бол шаардлагатай.

## Лиценз

Энэхүү төсөл нь MIT лицензийн нөхцлөөр лицензжигдсэн билээ.

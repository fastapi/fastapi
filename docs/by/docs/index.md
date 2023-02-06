
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI фрэймворк, высокая прадукцыйнасць, просты ў вывучэнні, хуткі ў кодаванні, гатовы да вытворчасці</em>
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

**Дакументацыя**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Зыходны код**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI - гэта сучасны, хуткі (высокапрадукцыйны) вэб-фреймворк для стварэння API на Python 3.7+ з выкарыстаннем стандартных анатацыяў тыпаў Python.

Ключавыя асабліваці:

* **Хуткасць**: Вельмі высокая прадукцыйнасць, нароўні з **NodeJS** ды **Go** (дзякуючы Starlette і Pydantic). [Адзін з самых хуткіх з існуючых фрэймворкаў на Python](#performance).
* **Хуткасць распрацоўкі**: Павялічце хуткасць распрацоўкі прыкладна ад 200% да 300%. *
* **Менш памылак**: Скарачае колькасць памылак, выкліканых чалавекам (распрацоўшчыкам), прыкладна на 40%. *
* **Інтуітыўны**: Выдатная падтрымка рэдактарамі. <abbr title="таксама вядомы як аўтадапаўненне, autocompletion, IntelliSense">Завяршэнне</abbr> ўсюды. Менш часу на адладку.
* **Лёгкі**: Распрацаваны, каб быць простым у выкарыстанні і вывучэнні. Патрабуе менш часу на чытанне дакументаў.
* **Кароткі**: Мінімізуйце дубляванне кода. Кожны аб'яўлены параметр мае некалькі функцый.
* **Трывалы**: Атрымайце гатовы да работы код з аўтаматычнай інтэрактыўнай дакументацыяй.
* **На аснове стандартаў**: Заснаваны і цалкам сумяшчальны з адкрытымі стандартамі для API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (раней вядомы як Swagger) ды <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* ацэнка на аснове тэстаў унутранай групы распрацоўшчыкаў, якія ствараюць прадакшн праграмы.</small>

## Спонсары

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

## Меркаванні

"_[...] У апошні час я шмат выкарыстоўваю **FastAPI**. [...]  Насамрэч я планую выкарыстоўваць яго для ўсіх **ML-сервісаў маёй каманды ў Microsoft**. Некаторыя з іх інтэгруюцца ў асноўны прадукт **Windows** і некаторыя прадукты **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Мы прынялі бібліятэку **FastAPI**, каб стварыць **REST** сервер, да якога можна запытвацца для атрымання **прагнозаў**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** рада аб'явіць аб выпуску нашай структуры аркестравання з адкрытым зыходным кодам **крызіснага кіравання**: **Dispatch**! [створаны з дапамогай **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Я ў вялікім захапленні ад **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Шчыра кажучы, тое, што вы пабудавалі, выглядае вельмі трывалым і адшліфаваным. У многім я хацеў, каб **Hug** быў такім - вельмі натхняльна бачыць, як хтосьці стварае гэта._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Калі вы жадаеце вывучыць які-небудзь **сучасны фрэймворк** для стварэння REST API, паспрабуйце **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_Мы перайшлі на **FastAPI** для нашых **API** [...] Я думаю, вам спадабаецца [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, CLIs(інтэрфейс каманднага радка) для FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Калі вы ствараеце праграму <abbr title="Command Line Interface">CLI</abbr> для выкарыстання ў тэрмінале замест вэб-API, паглядзіце на <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** - малодшы брат FastAPI. І ён прызначаны як **FastAPI для CLI**. ⌨️ 🚀

## Залежнасці

Python 3.7+

FastAPI стаіць на плячах такіх гігантаў як:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для частак вэб.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для частак дадзеных.

## Устаноўка

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Вам таксама спатрэбіцца ASGI сервер для прадакшн, напрыклад <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ці <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Прыклад

### Стварэнне

* Стварыце файл `main.py` з наступным кодам:

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
<summary>Або выкарыстоўвайце <code>async def</code>...</summary>

Калі ваш код выкарыстоўвае `async` / `await`, выкарыстоўвайце `async def`:

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

**Нататка**:

Калі вы не ведаеце, праверце раздзел _"Спяшаецеся??"_ пра  <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">пра `async` і `await` у дакументацыі</a>.

</details>

### Запуск

Запусціце сервер наступнай камандай:

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
<summary>Пра каманду<code>uvicorn main:app --reload</code>...</summary>

Каманда `uvicorn main:app` адносіцца да:

* `main`: файл `main.py` (модуль Python).
* `app`: аб'ект, створаны ўнутры `main.py` з дапамогай радка `app = FastAPI()`.
* `--reload`: прымусіць сервер перазагрузіцца пасля змены кода. Выкарыстоўвайце гэта толькі пад час распрацойкі.

</details>

### Праверка

Адкрыйце Ваш браўзер па адрасу <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Вы ўбачыце наступны JSON адказ:

```JSON
{"item_id": 5, "q": "somequery"}
```

Вы ўжо стварылі API, які:

* Атрымлівае HTTP-запыты па _шляхах_ `/` i `/items/{item_id}`.
* Абодва _шляхі_ выконваюць `GET` <em>запыты</em> (таксама вядомыя як HTTP _метады_).
* _Шлях_ `/items/{item_id}` мае _параметр шляху_ `item_id`, які павінен быць `int`.
* _Шлях_ `/items/{item_id}` мае дадатковы `str` _параметр запыту_ `q`.

### Інтэрактыўныя дакументы API

Перайдзіце на <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Вы ўбачыце аўтаматычную інтэрактыўную дакументацыю API (прадастаўленую <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтэрнатыўныя дакументацыя API

А зараз перайдзіце на <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы ўбачыце альтэрнатыўную аўтаматычную дакументацыю (прадастаўленую <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Прыклад пашырэння функцыяналу

Цяпер змяніце файл `main.py`, каб атрымліваць цела з `PUT`-запыту.

Дзякуючы Pydantic, аб'явіце цела з выкарыстаннем стандартных тыпаў Python.

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

Сервер павінен перазагрузіцца аўтаматычна (таму што вы дадалі `--reload` да каманды `uvicorn` вышэй).

### Абнаўленне інтэрактыўнай дакументацыі API

Цяпер перайдзіце да <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Інтэрактыўная дакументацыя API будзе аўтаматычна абнаўляцца, уключаючы новае цела запыта:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Націсніце на кнопку «Try it out», яна дазваляе запоўніць параметры і непасрэдна ўзаемадзейнічаць з API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Затым націсніце на кнопку «Execute», карыстальніцкі інтэрфейс звяжацца з вашым API, адправіць параметры, атрымае вынікі і пакажа іх на экране:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Абнаўленне альтэрнатыўнай дакументацыі API

А зараз, перайдзіце да <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Альтэрнатыўная дакументацыя таксама будзе адлюстроўваць новы параметр і цела запыту:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Падвядзенне вынікаў

Такім чынам, вы аб'яўляеце **адзін раз** тыпы параметраў, цела і г.д. як параметры функцыі.

Вы робіце гэта з дапамогай стандартных сучасных тыпаў Python.

Вам не трэба вывучаць новы сінтаксіс, метады або класы пэўнай бібліятэкі і г.д.

Проста стандартны **Python 3.7+**.

Напрыклад, для тыпу `int`:

```Python
item_id: int
```

або для больш складанай мадэлі "Item":

```Python
item: Item
```

...і з гэтай адзінай дэкларацыяй вы атрымаеце:

* Падтрымка рэдактара, у тым ліку:
    * Падказкі.
    * Праверка тыпаў.
* Праверка даных:
    * Аўтаматычныя і ясныя памылкі, калі дадзеныя несапраўдныя.
    * Праверка нават для глыбока ўкладзеных аб'ектаў JSON.
* <abbr title="таксама вядомы як: серыялізацыя, разбор, маршалінг">Пераўтварэнне</abbr> ўваходных даных, якія паступаюць з сеткі ў даныя і тыпы Python. Чытанне з:
    * JSON.
    * Параметры шляху.
    * Параметры запыту.
    * Cookies.
    * Загалоўкі.
    * Forms.
    * Файлыю
* <abbr title="таксама вядомы як: серыялізацыя, разбор, маршалінг">Пераўтварэнне</abbr> выхадных даных: пераўтварэнне з даных і тыпаў Python у сеткавыя даныя (як JSON):
    * Пераўтварэнне тыпаў Python (`str`, `int`, `float`, `bool`, `list` і г.д. ).
    * `datetime` аб'екты.
    * `UUID` аб'екты.
    * Мадэлі баз даных.
    * ...і многае іншае.
* Аўтаматычная інтэрактыўная дакументацыя API, уключаючая 2 альтэрнатыўныя карыстальніцкія інтэрфейсы:
    * Swagger UI.
    * ReDoc.

---

Вяртаючыся да папярэдняга прыкладу кода, **FastAPI** будзе:

* Правяраць, ці ёсць `item_id` у шляху для `GET` і `PUT` запытаў.
* Правяраць, што `item_id` мае тып `int` для `GET` і `PUT` запытаў.
    * Калі гэта не так, кліент убачыць карысную, зразумелую памылку.
* Правяраць, ці ёсць неабавязковы параметр запыту з назвай `q` (як у `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET` запытаў
    * Паколькі параметр `q` аб'яўлены як `= None`, ён неабавязковы.
    * Без `None` ён быў бы неабходны (як і цела ў выпадку з `PUT`).
* Для `PUT` запытаў да `/items/{item_id}` чытаць цела як JSON:
    * Правяраць, ці ёсць у яго абавязковы атрыбут "name", які павінен быць "str".
    * Правяраць, ці мае абавязковы атрыбут "price", які павінен быць тыпу "float".
    * Правяраць, ці ёсць у яго дадатковы атрыбут "is_offer", які павінен быць "bool", калі ён ёсць.
    * Усё гэта таксама будзе працаваць для глыбока ўкладзеных аб'ектаў JSON.
* Аўтаматычна пераўтвараць з і ў JSON.
* Дакументаваць ўсё з дапамогай OpenAPI, што можа быць выкарыстана для:
    * Інтэрактыўнай сістэмы дакументацыі.
    * Сістэмы аўтаматычнай генерацыі кліенцкага кода для многіх моў.
* Забяспечвае 2 інтэрактыўныя вэб-інтэрфейсы дакументацыі непасрэдна.

---

Мы толькі дакрануліся да паверхні, але вы ўжо разумееце, як усё гэта працуе.

Паспрабуйце змяніць наступны радок:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...з:

```Python
        ... "item_name": item.name ...
```

...на:

```Python
        ... "item_price": item.price ...
```

...і паглядзіце, як ваш рэдактар будзе аўтаматычна запаўняць атрыбуты і ведаць іх тыпы:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для атрымання больш поўнага прыкладу з дадатковымі функцыямі глядзіце <a href="https://fastapi.tiangolo.com/tutorial/">Навучальнае кіраўніцтва - Кіраўніцтва карыстальніка.</a>.

**Спойлер**: кіраўніцтва карыстальніка ўключае:

* Дэкларацыя **параметраў** з іншых розных месцаў, такіх як: **загалоўкі**, **кукі**, **палі формы** і **файлы**.
* Як усталяваць **праверачныя абмежаванні**, такія як `maximum_length` або `regex`.
* Вельмі магутная і простая ў выкарыстанні сістэма **<abbr title="таксама вядомы як кампаненты, рэсурсы, пастаўшчыкі, паслугі, ін'екцыі">Ін'екцыі залежнасцяў</abbr>**.
* Бяспека і аўтэнтыфікацыя, уключаючы падтрымку **OAuth2** з **JWT-токенамі** і **HTTP Basic** аўтэнтыфікацыяй.
* Больш прасунутыя, але аднолькава простыя метады для дэкларацыі **глыбока ўкладзеных мадэляў JSON** (дзякуючы Pydantic).
* **GraphQL** інтэграцыя са <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> і іншымі бібліятэкамі.
* Шмат дадатковых функцый, дзякуючы Starlette, такіх як:
    * **WebSockets**
    * надзвычай простыя тэсты на аснове HTTPX and `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...і шмат чаго яшчэ.

## Прадукцыйнасць

Незалежныя тэсты TechEmpower паказваюць, што **FastAPI**, які працуе пад кіраваннем Uvicorn, <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank"> з'яўляецца аднымі з самых хуткіх даступных фрэймворкаў на Python</a>, саступаючы толькі самім Starlette і Uvicorn, якія выкарыстоўваюцца ўнутры FastAPI. (*)

Каб даведацца больш пра гэта, глядзіце раздзел <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Тэсты</a>.

## Неабавязковыя залежнасці

Выкарыстоўваецца Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для больш хуткага JSON <abbr title="пераўтварэнне радка, які паходзіць з HTTP запыту, у дадзеныя Python">"парсінгу"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для праверкі электроннай пошты.

Выкарыстоўваецца Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> -Патрабуецца, калі вы хочаце выкарыстоўваць `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Патрабуецца, калі вы хочаце выкарыстоўваць канфігурацыю шаблона па змаўчанні.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Патрабуецца, калі вы хочаце падтрымліваць форму <abbr title="пераўтварэнне радка, які паходзіць з HTTP запыту, у дадзеныя Python">"парсінгу"</abbr> з `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Патрабуецца для падтрымкі `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Патрабуецца для падтрымкі `SchemaGenerator` Starlette (яна вам, верагодна, не спатрэбіцца з FastAPI).
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Патрабуецца, калі вы хочаце выкарыстоўваць `UJSONResponse`.

Выкарыстоўваецца FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - для сервера, які загружае і абслугоўвае вашу праграму.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> -Патрабуецца, калі вы хочаце выкарыстоўваць `ORJSONResponse`.

Вы можаце ўсталяваць усё гэта з дапамогай `pip install "fastapi[all]"`.

## Ліцэнзія

Гэты праект ліцэнзаваны ў адпаведнасці з умовамі ліцэнзіі MIT.

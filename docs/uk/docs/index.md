# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/uk"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Фреймворк FastAPI - це висока продуктивність, легко вивчати, швидко писати код, готовий до продакшину</em>
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

**Документація**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/uk)

**Вихідний код**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI - це сучасний, швидкий (високопродуктивний) вебфреймворк для створення API за допомогою Python, що базується на стандартних підказках типів Python.

Ключові особливості:

* **Швидкий**: дуже висока продуктивність, на рівні з **NodeJS** та **Go** (завдяки Starlette та Pydantic). [Один із найшвидших Python-фреймворків](#performance).
* **Швидке написання коду**: пришвидшує розробку функціоналу приблизно на 200%–300%. *
* **Менше помилок**: зменшує приблизно на 40% кількість помилок, спричинених людиною (розробником). *
* **Інтуїтивний**: чудова підтримка редакторами коду. <dfn title="також відоме як: авто-доповнення, автозавершення, IntelliSense">Автодоповнення</dfn> всюди. Менше часу на налагодження.
* **Простий**: спроєктований так, щоб бути простим у використанні та вивченні. Менше часу на читання документації.
* **Короткий**: мінімізує дублювання коду. Кілька можливостей з кожного оголошення параметра. Менше помилок.
* **Надійний**: ви отримуєте код, готовий до продакшину. З автоматичною інтерактивною документацією.
* **Заснований на стандартах**: базується на (і повністю сумісний з) відкритими стандартами для API: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (раніше відомий як Swagger) та [JSON Schema](https://json-schema.org/).

<small>* оцінка на основі тестів, проведених внутрішньою командою розробників, що створює продакшн-застосунки.</small>

## Спонсори { #sponsors }

<!-- sponsors -->

### Ключовий спонсор { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Золоті та срібні спонсори { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[Інші спонсори](https://fastapi.tiangolo.com/uk/fastapi-people/#sponsors)

## Враження { #opinions }

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>[Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855) podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>[Hug](https://github.com/hugapi/hug) creator</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>[Explosion AI](https://explosion.ai) founders - [spaCy](https://spacy.io) creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## Міні-документальний фільм про FastAPI { #fastapi-mini-documentary }

Наприкінці 2025 року вийшов [міні-документальний фільм про FastAPI](https://www.youtube.com/watch?v=mpR8ngthqiE), ви можете переглянути його онлайн:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, FastAPI для CLI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Якщо ви створюєте застосунок <abbr title="Command Line Interface - Інтерфейс командного рядка">CLI</abbr> для використання в терміналі замість веб-API, зверніть увагу на [**Typer**](https://typer.tiangolo.com/).

**Typer** - молодший брат FastAPI. І його задумано як **FastAPI для CLI**. ⌨️ 🚀

## Вимоги { #requirements }

FastAPI стоїть на плечах гігантів:

* [Starlette](https://www.starlette.dev/) для вебчастини.
* [Pydantic](https://docs.pydantic.dev/) для частини даних.

## Встановлення { #installation }

Створіть і активуйте [віртуальне середовище](https://fastapi.tiangolo.com/uk/virtual-environments/), а потім встановіть FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Примітка**: переконайтеся, що ви взяли `"fastapi[standard]"` у лапки, щоб це працювало в усіх терміналах.

## Приклад { #example }

### Створіть { #create-it }

Створіть файл `main.py` з:

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
<summary>Або використайте <code>async def</code>...</summary>

Якщо ваш код використовує `async` / `await`, скористайтеся `async def`:

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

**Примітка**:

Якщо ви не знаєте, перегляньте розділ _"In a hurry?"_ про [`async` та `await` у документації](https://fastapi.tiangolo.com/uk/async/#in-a-hurry).

</details>

### Запустіть { #run-it }

Запустіть сервер за допомогою:

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
<summary>Про команду <code>fastapi dev</code>...</summary>

Команда `fastapi dev` автоматично читає ваш файл `main.py`, знаходить у ньому застосунок **FastAPI** і запускає сервер за допомогою [Uvicorn](https://www.uvicorn.dev).

За замовчуванням `fastapi dev` запускається з авто-перезавантаженням для локальної розробки.

Докладніше читайте в [документації FastAPI CLI](https://fastapi.tiangolo.com/uk/fastapi-cli/).

</details>

### Перевірте { #check-it }

Відкрийте браузер і перейдіть на [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

Ви побачите JSON-відповідь:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ви вже створили API, який:

* Отримує HTTP-запити за _шляхами_ `/` та `/items/{item_id}`.
* Обидва _шляхи_ приймають `GET` <em>операції</em> (також відомі як HTTP _методи_).
* _Шлях_ `/items/{item_id}` містить _параметр шляху_ `item_id`, який має бути типу `int`.
* _Шлях_ `/items/{item_id}` містить необовʼязковий `str` _параметр запиту_ `q`.

### Інтерактивна документація API { #interactive-api-docs }

Тепер перейдіть на [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Ви побачите автоматичну інтерактивну документацію API (надану [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативна документація API { #alternative-api-docs }

А тепер перейдіть на [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Ви побачите альтернативну автоматичну документацію (надану [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Приклад оновлення { #example-upgrade }

Тепер змініть файл `main.py`, щоб отримувати тіло `PUT`-запиту.

Оголосіть тіло, використовуючи стандартні типи Python, завдяки Pydantic.

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

Сервер `fastapi dev` має автоматично перезавантажитися.

### Оновлення інтерактивної документації API { #interactive-api-docs-upgrade }

Тепер перейдіть на [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* Інтерактивна документація API буде автоматично оновлена, включно з новим тілом:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Натисніть кнопку "Try it out", вона дозволяє заповнити параметри та безпосередньо взаємодіяти з API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Потім натисніть кнопку "Execute", інтерфейс користувача зв'яжеться з вашим API, надішле параметри, отримає результати та покаже їх на екрані:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Оновлення альтернативної документації API { #alternative-api-docs-upgrade }

А тепер перейдіть на [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

* Альтернативна документація також відобразить новий параметр запиту та тіло:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Підсумки { #recap }

Отже, ви оголошуєте **один раз** типи параметрів, тіла тощо як параметри функції.

Ви робите це за допомогою стандартних сучасних типів Python.

Вам не потрібно вивчати новий синтаксис, методи чи класи конкретної бібліотеки тощо.

Лише стандартний **Python**.

Наприклад, для `int`:

```Python
item_id: int
```

або для складнішої моделі `Item`:

```Python
item: Item
```

...і з цим єдиним оголошенням ви отримуєте:

* Підтримку редактора, включно з:
    * Автодоповненням.
    * Перевіркою типів.
* Валідацію даних:
    * Автоматичні та зрозумілі помилки, коли дані некоректні.
    * Валідацію навіть для глибоко вкладених JSON-обʼєктів.
* <dfn title="також відоме як: серіалізація, парсинг, маршалінг">Перетворення</dfn> вхідних даних: з мережі до даних і типів Python. Читання з:
    * JSON.
    * Параметрів шляху.
    * Параметрів запиту.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <dfn title="також відоме як: серіалізація, парсинг, маршалінг">Перетворення</dfn> вихідних даних: перетворення з даних і типів Python у мережеві дані (як JSON):
    * Перетворення типів Python (`str`, `int`, `float`, `bool`, `list`, тощо).
    * Обʼєктів `datetime`.
    * Обʼєктів `UUID`.
    * Моделей бази даних.
    * ...та багато іншого.
* Автоматичну інтерактивну документацію API, включно з 2 альтернативними інтерфейсами користувача:
    * Swagger UI.
    * ReDoc.

---

Повертаючись до попереднього прикладу коду, **FastAPI**:

* Перевірить, що `item_id` є у шляху для `GET` та `PUT`-запитів.
* Перевірить, що `item_id` має тип `int` для `GET` та `PUT`-запитів.
    * Якщо це не так, клієнт побачить корисну, зрозумілу помилку.
* Перевірить, чи є необов'язковий параметр запиту з назвою `q` (як у `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET`-запитів.
    * Оскільки параметр `q` оголошено як `= None`, він необов'язковий.
    * Без `None` він був би обов'язковим (як і тіло у випадку з `PUT`).
* Для `PUT`-запитів до `/items/{item_id}` прочитає тіло як JSON:
    * Перевірить, що є обовʼязковий атрибут `name`, який має бути типу `str`.
    * Перевірить, що є обовʼязковий атрибут `price`, який має бути типу `float`.
    * Перевірить, що є необовʼязковий атрибут `is_offer`, який має бути типу `bool`, якщо він присутній.
    * Усе це також працюватиме для глибоко вкладених JSON-обʼєктів.
* Автоматично перетворюватиме з та в JSON.
* Документуватиме все за допомогою OpenAPI, який може бути використано в:
    * Інтерактивних системах документації.
    * Системах автоматичної генерації клієнтського коду для багатьох мов.
* Надаватиме безпосередньо 2 вебінтерфейси інтерактивної документації.

---

Ми лише трішки доторкнулися до поверхні, але ви вже маєте уявлення про те, як усе працює.

Спробуйте змінити рядок:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...із:

```Python
        ... "item_name": item.name ...
```

...на:

```Python
        ... "item_price": item.price ...
```

...і побачите, як ваш редактор автоматично доповнюватиме атрибути та знатиме їхні типи:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для більш повного прикладу, що включає більше можливостей, перегляньте <a href="https://fastapi.tiangolo.com/uk/tutorial/">Навчальний посібник - Посібник користувача</a>.

**Попередження про спойлер**: навчальний посібник - посібник користувача містить:

* Оголошення **параметрів** з інших різних місць, як-от: **headers**, **cookies**, **form fields** та **files**.
* Як встановлювати **обмеження валідації** як `maximum_length` або `regex`.
* Дуже потужну і просту у використанні систему **<dfn title="також відоме як: компоненти, ресурси, провайдери, сервіси, інжектовані залежності">Впровадження залежностей</dfn>**.
* Безпеку та автентифікацію, включно з підтримкою **OAuth2** з **JWT tokens** та **HTTP Basic** auth.
* Досконаліші (але однаково прості) техніки для оголошення **глибоко вкладених моделей JSON** (завдяки Pydantic).
* Інтеграцію **GraphQL** з [Strawberry](https://strawberry.rocks) та іншими бібліотеками.
* Багато додаткових можливостей (завдяки Starlette) як-от:
    * **WebSockets**
    * надзвичайно прості тести на основі HTTPX та `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...та більше.

### Розгортання застосунку (необовʼязково) { #deploy-your-app-optional }

За бажання ви можете розгорнути ваш застосунок FastAPI у [FastAPI Cloud](https://fastapicloud.com), перейдіть і приєднайтеся до списку очікування, якщо ви ще цього не зробили. 🚀

Якщо у вас вже є обліковий запис **FastAPI Cloud** (ми запросили вас зі списку очікування 😉), ви можете розгорнути ваш застосунок однією командою.

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Ось і все! Тепер ви можете отримати доступ до вашого застосунку за цією URL-адресою. ✨

#### Про FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** створено тим самим автором і командою, що стоять за **FastAPI**.

Він спрощує процес **створення**, **розгортання** та **доступу** до API з мінімальними зусиллями.

Він забезпечує той самий **developer experience** створення застосунків на FastAPI під час їх **розгортання** у хмарі. 🎉

FastAPI Cloud - основний спонсор і джерело фінансування open source проєктів *FastAPI and friends*. ✨

#### Розгортання в інших хмарних провайдерів { #deploy-to-other-cloud-providers }

FastAPI - open source проект і базується на стандартах. Ви можете розгортати застосунки FastAPI в будь-якому хмарному провайдері, який ви оберете.

Дотримуйтеся інструкцій вашого хмарного провайдера, щоб розгорнути застосунки FastAPI у нього. 🤓

## Продуктивність { #performance }

Незалежні тести TechEmpower показують застосунки **FastAPI**, які працюють під керуванням Uvicorn, як [одні з найшвидших доступних Python-фреймворків](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), поступаючись лише Starlette та Uvicorn (які внутрішньо використовуються в FastAPI). (*)

Щоб дізнатися більше, перегляньте розділ [Benchmarks](https://fastapi.tiangolo.com/uk/benchmarks/).

## Залежності { #dependencies }

FastAPI залежить від Pydantic і Starlette.

### Залежності `standard` { #standard-dependencies }

Коли ви встановлюєте FastAPI за допомогою `pip install "fastapi[standard]"`, ви отримуєте групу необовʼязкових залежностей `standard`:

Використовується Pydantic:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - для валідації електронної пошти.

Використовується Starlette:

* [`httpx`](https://www.python-httpx.org) - потрібно, якщо ви хочете використовувати `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - потрібно, якщо ви хочете використовувати конфігурацію шаблонів за замовчуванням.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - потрібно, якщо ви хочете підтримувати форми з <dfn title="перетворення строки, що надходить із HTTP-запиту, у дані Python">«парсингом»</dfn> через `request.form()`.

Використовується FastAPI:

* [`uvicorn`](https://www.uvicorn.dev) - для сервера, який завантажує та обслуговує ваш застосунок. Це включає `uvicorn[standard]`, до якого входять деякі залежності (наприклад, `uvloop`), потрібні для високопродуктивної роботи сервера.
* `fastapi-cli[standard]` - щоб надати команду `fastapi`.
    * Це включає `fastapi-cloud-cli`, який дозволяє розгортати ваш застосунок FastAPI у [FastAPI Cloud](https://fastapicloud.com).

### Без залежностей `standard` { #without-standard-dependencies }

Якщо ви не хочете включати необовʼязкові залежності `standard`, ви можете встановити через `pip install fastapi` замість `pip install "fastapi[standard]"`.

### Без `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Якщо ви хочете встановити FastAPI зі стандартними залежностями, але без `fastapi-cloud-cli`, ви можете встановити через `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Додаткові необовʼязкові залежності { #additional-optional-dependencies }

Є ще деякі додаткові залежності, які ви можете захотіти встановити.

Додаткові необовʼязкові залежності Pydantic:

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - для керування налаштуваннями.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - для додаткових типів, що можуть бути використані з Pydantic.

Додаткові необовʼязкові залежності FastAPI:

* [`orjson`](https://github.com/ijl/orjson) - потрібно, якщо ви хочете використовувати `ORJSONResponse`.
* [`ujson`](https://github.com/esnme/ultrajson) - потрібно, якщо ви хочете використовувати `UJSONResponse`.

## Ліцензія { #license }

Цей проєкт ліцензовано згідно з умовами ліцензії MIT.

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
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

**Документація**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Вихідний код**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI це сучасний, швидкий (високопродуктивний), вебфреймворк для створення API за допомогою Python 3.6+ на основі стандартних підказок типу Python.

Ключові особливості:

* **Швидкий**: Дуже висока продуктивність, на рівні з **NodeJS** та **Go** (завдяки Starlette та Pydantic). [Один із найшвидших фреймворків](#performance).

* **Швидке кодування**: Збільшить швидкість розробки функцій приблизно на 200%-300%. *
* **Менше помилок**: Зменшить кількість помилок спричинених людиною (розробником) на 40%. *
* **Інтуїтивний**: Чудова підтримка редакторами. <abbr title="також відоме як автозаповнення, IntelliSense.">Доповнення</abbr> всюди. Зменште час на налагодження.
* **Простий**: Спроектований, для легкого використання та навчання. Знадобиться менше часу на читання документації.
* **Короткий**: Зведе до мінімуму дублювання коду. Кілька функцій кожного оголошення параметра.
* **Документований**: Отримайте готовий код з автоматичною інтерактивною документацією.
* **Стандартизований**: Оснований та повністю сумісний з відкритими стандартами для API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (previously known as Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* оцінка на основі тестів внутрішньої команди розробників, створення продуктових застосунків.</small>

## Спонсори

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

## Враження

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

## **Typer**, FastAPI CLI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Якщо ви створюєте <abbr title="Command Line Interface">CLI</abbr> застосунок для використання в терміналі, замість веб-API перевірте <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** є молодшим братом FastAPI. І це **FastAPI для CLI**. ⌨️ 🚀

## Вимоги

Python 3.6+

FastAPI стоїть на плечах гігантів:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для частин web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для частин даних.

## Інсталяція

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Вам також знадобиться сервер ASGI для продакшину, наприклад <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> або <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Приклад

### Створіть

* Створіть файл `main.py` з:

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
<summary>Або використайте <code>async def</code>...</summary>

Якщо ваш код використовує `async` / `await`, скористайтеся `async def`:

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

**Примітка**:

Якщо ви не розумієте, перегляньте розділ _"In a hurry?"_ про <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` та `await` в документації</a>.

</details>

### Запустіть

Запустіть server з:

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
<summary>Про команди <code>uvicorn main:app --reload</code>...</summary>

Команда `uvicorn main:app` посилається:

* `main`: файл `main.py` (the Python "module").
* `app`: об’єкт створений усередині `main.py` рядком `app = FastAPI()`.
* `--reload`: перезапускає сервер після зміни коду. Використовуйте виключно для розробки.

</details>

### Перевірте

Відкрийте браузер та введіть адресу <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Ви побачите у відповідь подібний JSON:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ви вже створили API який:

* Отримує HTTP запити за _шляхом_ `/` та `/items/{item_id}`.
* Обидва _шляхи_ приймають `GET` <em>операції</em> (також відомі як HTTP _методи_).
* _Шлях_ `/items/{item_id}` має _параметер шляху_ `item_id` це має бути `int`.
* _Шлях_ `/items/{item_id}` має опціональний `str` _параметр запиту_ `q`.

### Інтерактивні документації API

Перейдемо сюди <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Ви побачите автоматичну інтерактивну документацію API (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативні документи API

Тепер, перейдемо сюди <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Ви побачите альтернативну автоматичну документацію (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Приклад оновлення

Тепер модифікуйте файл `main.py` щоб отримати тіло запиту `PUT`.

Оголошуйте тіло запиту за допомогою стандартних типів Python завдяки Pydantic.

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

Сервер повинен автоматично перезавантажуватися (тому що ви додали `--reload` до `uvicorn`).

### Оновлення інтерактивної документації API

Тепер перейдемо сюди <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Інтерактивна документація API буде автоматично оновлена, включаючи нове тіло:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Натисніть кнопку "Try it out", це дозволить вам заповнити параметри та безпосередньо взаємодіяти з API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Потім натисніть кнопку "Execute", інтерфейс користувача зв'яжеться з вашим API, надішле параметри, у відповідь отримає результати та покаже їх на екрані:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Оновлення альтернативної документації API

Зараз перейдемо <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Альтернативна документація також показуватиме новий параметр і тіло запиту:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Підсумки

Таким чином, ви оголошуєте **один раз** типи параметрів, тіло, тощо. як параметри функції.

Ви робите це за допомогою стандартних сучасних типів Python.

Вам не потрібно вивчати новий синтаксис, методи чи класи конкретної бібліотеки тощо.

Використовуючи стандартний **Python 3.6+**.

Наприклад, для `int`:

```Python
item_id: int
```

або для більш складногї моделі `Item`:

```Python
item: Item
```

...і з цією єдиною декларацією ви отримуєте:

* Підтримка редактора, включаючи:
    * Варіанти заповнення.
    * Перевірка типів.
* Перевірка даних:
    * Автоматичне видалення помилок, коли дані недійсні.
    * Перевірка навіть для глибоко вкладених об'єктів JSON.
* <abbr title="також відомий як: serialization, parsing, marshalling">Перетворення</abbr> вхідних даних: з мережі до даних і типів Python. Читання з:
    * JSON.
    * Параметрів шляху.
    * Параметрів запиту.
    * Cookies.
    * Headers.
    * Forms.
    * Файлів.
* <abbr title="також відомий як: serialization, parsing, marshalling">Перетворення</abbr> вихідних даних: converting from Python data and types to network data (as JSON):
    * Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` об'єкти.
    * `UUID` об'єкти.
    * Моделі баз даних.
    * ...та багато іншого.
* Автоматична інтерактивна документація API, включаючи 2 альтернативні інтерфейси користувача:
    * Swagger UI.
    * ReDoc.

---

Повертаючись до попереднього прикладу коду, **FastAPI**:

* Підтвердить наявність `item_id` у шляху для запитів `GET` та `PUT`.
* Підтвердить, що `item_id` має тип `int` для запитів `GET` and `PUT`.
    * Якщо це не так, клієнт побачить корисну, зрозумілу помилку.
* Перевірить, чи є необов'язковий параметр запиту з назвою `q` (а саме `http://127.0.0.1:8000/items/foo?q=somequery`) для запитів `GET`.
    * Оскільки параметр `q` оголошено як `= None`, він необов'язковий.
    * За відсутності `None` це було б обов'язковим (як і тіло у випадку з `PUT`).
* Для запитів `PUT` із `/items/{item_id}`, читає тіло як JSON:
    * Перевірить, чи є обов'язковий атрибут `name` який має бути `str`.
    * Перевірить, чи є обов'язковий атрибут `price` який має бути `float`.
    * Перевірить, чи є необов'язковий атрибут `is_offer`, який має бути `bool`, якщо він є.
    * Усе це також працюватиме для глибоко вкладених об'єктів JSON.
* Автоматично конвертує **із** та **в** JSON.
* Документує все за допомогою OpenAPI, та використовує в:
    * Інтерактивних документаціях системи.
    * Автоматичних системах генерації клієнтського коду для багатьох мов.
* Надає безпосередньо 2 вебінтерфейси інтерактивної документації.

---

Ми лише трошки доторкнулися, але ви вже маєте уявлення про те, як все працює.

Спробуємо змінити рядок:

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

...і побачите, як ваш редактор автоматично заповнюватиме атрибути та знатиме їхні типи:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для більш повного ознайомлення з додатковими функціями, перегляньте the <a href="https://fastapi.tiangolo.com/tutorial/">Підручник - Посібник Користувача</a>.

**Spoiler alert**: підручник - посібник користувача містить:

* Оголошення **параметрів** з інших місць як: **headers**, **cookies**, **form fields** та **files**.
* Як встановити **перевірку обмежень** як `maximum_length` або `regex`.
*Дуже потужна і проста у використанні система **<abbr title="також відомий як: components, resources, providers, services, injectables">Ін'єкції Залежностей</abbr>** system.
* Безпека та автентифікація, включаючи підтримку **OAuth2** з **JWT tokens** та **HTTP Basic** автентифікацією.
* Досконаліші (але однаково прості) техніки для оголошення **глибоко вкладених моделей JSON** (завдяки Pydantic).
* Багато додаткових функцій (завдяки Starlette) як:
    * **WebSockets**
    * **GraphQL**
    * надзвичайно прості тести на основі `requests` та `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...та більше.

## Performance

Незалежні тести TechEmpower показують програми **FastAPI**, що працюють під керуванням Uvicorn є <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">одними з найшвидших доступних фреймворків в Python</a>, поступаючись лише Starlette та Uvicorn (внутрішньо використовуються FastAPI). (*)

Щоб дізнатися більше про це, перегляньте розділ <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Необов'язкові залежності

Використовується Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для швидшого <abbr title="перетворення рядка, який надходить із запиту HTTP, на дані Python">"розбору"</abbr> JSON.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для підтвердження email.

Використовується Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Необхідно, якщо ви хочете використовувати `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Необхідно, якщо ви хочете використовувати шаблонну конфігурацію за замовчуванням.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Потрібний, якщо ви хочете підтримувати <abbr title="перетворення рядка, який надходить із запиту HTTP, на дані Python">"розбір"</abbr>, форми за допомогою `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Необхідно для підтримки `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Необхідно для підтримки `SchemaGenerator` Starlette (ймовірно, вам це не потрібно з FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Необхідно для підтримки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Необхідно, якщо ви хочете використовувати `UJSONResponse`.

Використовується FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - для сервера, який завантажує та обслуговує вашу програму.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Необхідно, якщо ви хочете використовувати `ORJSONResponse`.

Ви можете встановити все це за допомогою `pip install fastapi[all]`.

## Ліцензія

Цей проєкт ліцензовано згідно з умовами ліцензії MIT.

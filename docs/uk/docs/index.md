<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI - швидкісний фреймворк який легко вивчити, швидкісний в написанні, готовий для реальний проектів</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Статус тестів">
</a>
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Publish/badge.svg" alt="Статус білда">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Покриття коду">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Версія пекеджу">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Заходьте в наш чат https://gitter.im/tiangolo/fastapi">
</a>
</p>

---

**Документація**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Вихідний код**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---
FastAPI це сучаний, швидкий фреймворк для будування API з Python 3.6+ з базування на стандартні типи Python.

Ключові особливості:

* **Швидкий**: Джуе велика швидкість, нарівні з **NodeJS** або **Go** (завдяки Starlette та Pydantic). [Одна з найшвидших фреймворків в Python](#performance).

* **Шкидкий в написанні**: Збільши швидкість девелопмента функціональності на 200% до 300%. *
* **Менша кількість багів**: Зменши можливість зробити людські помилки на 40%. *
* **Інтуітивний**: Відмінна підтримка редакторів. <abbr title="також відомий як auto-complete, autocompletion, IntelliSense">Заповнення</abbr> коду. Менше часу для дебагування.
* **Легкий**: Розроблений, щоб бути простим у використанні та навчанні. Менше часу для читання документів.
* **Стислий**: Мінімізуйте дуплікацію коду. Декілька функцій для кожного оголошення параметрів. Менше багів.
* **Міцний**: Отримайте код який готовий до продакшена. З автоматичною інтерактивною документацією.
* **На основі стандартів**: Базовані на (і повністю сумісні з) відкритими стандартами для APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (раніше відомий як Swagger) і <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Схема</a>.

<small>* оцінка базується на тестах у внутрішній команді, будуючи продакш аплікації.</small>


## Думки

"_[...] Цими днями я дуже часто використовую **FastAPI**. [...] Насправді я планую використовувати її для моєї команди для **ML сервісів в Microsoft**. Деякі з них інтегруються в ядро **Windows** продуктів і декілька **Office** продуктів._"


<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(реф)</small></a></div>

---

"_Ми використали **FastAPI** бібліотеку щоб створити **REST** сервер який можна кверіти щоб отримати **прогнози**. [for Ludwig]_"


<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(реф)</small></a></div>

---

"_**Netflix** із задоволенням повідомляє опен-сорс реліз фрейворку для оркестрації **кризової ситуацій**: **Dispatch**! [built with **FastAPI**]_"


<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(реф)</small></a></div>

---

"_Я на сьомому небі від **FastAPI**. Він такий приємний!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> хост подкастів</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(реф)</small></a></div>

---

"_Чесно кажучи, те, що ви створили, виглядає надзвичайно міцно і відшліфовано. У багатьох відношеннях це то що я хотів **Hug** бути - це насправді надихає що таке було зроблено._"


<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a> творець</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(реф)</small></a></div>

---

"_Якщо ти хочеш вивчити одну **сучасну бібліотеку** для будування REST APIs, подивись на **FastAPI** [...] Він швидкий, легкий в використанні та легкий в вивченні [...]_"


"_Ми перейшли на **FastAPI** для наших **APIs** [...] Я думаю що тобі він сподобається [...]_"


<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> засновники - <a href="https://spacy.io" target="_blank">spaCy</a> творці</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(реф)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(реф)</small></a></div>

---

## **Typer**, це FastAPI для CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Якщо ти будуєш <abbr title="Command Line Interface">CLI</abbr> додаток для використання в терміналі замість web API, подивись на <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** це FastAPI's маленький брат. І його призначення це бути **FastAPI для CLIs**. ⌨️ 🚀

## Вимоги

Python 3.6+

FastAPI стоїть на плечах гігантів:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для веб-частин.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для даних.

## Установка

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Вам також знадобиться ASGI сервер для Search Results продакшена, такий як <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> або <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## Приклад

### Створити аплікацію

* Створіть файл з назвою `main.py` який в собі має:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Або використовуй <code>async def</code>...</summary>

Якщо твій код використовує `async` / `await`, тоді використовуй `async def`:

```Python hl_lines="9 14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**Примітка**:

Якщо ти не знаєш, подивись на _"In a hurry?"_ секцію про <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` і `await` в документації</a>.

</details>

### Запусти програму

Запусти сервер з:

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
<summary>Про команду <code>uvicorn main:app --reload</code>...</summary>

Команда `uvicorn main:app` має наувазі:

* `main`: файл `main.py` (пітонівський модуль).
* `app`: об'єкт який створений в `main.py` з лінією `app = FastAPI()`.
* `--reload`: робить щоб сервер перезапускався після зміни коду. Роби це тільки для девелопмента.

</details>

### Перевірь програму

Відкрий свій браузер на <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Ти побачиш такий JSON відповідь:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ти уже створив API який:

* Отримує HTTP реквести в _шлях_ `/` і `/items/{item_id}`.
* Обоє _шляхи_ беруть `GET` <em>операції</em> (також відомі як HTTP _методи_).
* _Шлях_ `/items/{item_id}` має _параметер в шляху_ `item_id` який має бути `int`.
* _Шлях_ `/items/{item_id}` має необов’язковий `str` _квері параметер_ `q`.

### Інтерактивна API документація

А тепер піди до <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Ти побачиш автоматичну інтерактивну API документацію (завдяки <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Алтернативна API документація

А тепер піди до <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Ти побачиш альтернативну документацію (завдяки <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Приклад оновлення

А тепер онови `main.py` щоб він отримав 'body' з `PUT` реквеста.

Декларуй 'body' використовуючи стандартні Python типи, завдяки Pydantic.

```Python hl_lines="4  9 10 11 12  25 26 27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Сервер має сам перезавантажитись автоматично (через те що ти добавив `--reload` до `uvicorn` команди швидше)

### Обновлення інтерекатривного API документації

А тепер піди до <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Інтерактивне API докементація буде автоматично обновлена, включаючи новий 'body':

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Нажми на кнопку "Try it out", він дозволяє тобі заповнити параметри і безпосередньо взаємодіяти з API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Тепер нажми на кнопку "Execute", інтерфейс буде комінукувати з твоїм API, відпрявляти параметри, получати результат і показувати його на екрані:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Обновлення альтернативного API документації

А тепер піди до <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* The alternative documentation will also reflect the new query parameter and body:
* Альтернативна документація також покаже нові 'query parameter' і 'body':

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Коротке повторення

Підсумовуючи, ви оголошуєте **один раз** типи параметрів, 'body', тощо як параметри функції.

Ви це робити з стандартними типами Python.

Вам не потрібно вчити новий синтакс, методи або класи специфічної бібліотеки, тощо.

Просто стандартний **Python 3.6+**.

На приклад, для `int`:

```Python
item_id: int
```

або бля більш складної `Item` моделі:

```Python
item: Item
```

...і з цією єдиною декларацією ви отримаєте:

* Підтримка редактора, включаючи:
    * Завершення коду.
    * Перевірка типів.
* Валідація даних:
    * Автоматичні і понятні помилки коли дані не правильні.
    * Валідація навіть для глибоко вкладених об'єктів JSON
* <abbr title="також відомі як: serialization, parsing, marshalling">Перетворення</abbr> вхідних даних: які приходять з інтернету до Пітонивських даних і типів. Читаючи з:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> вихідних даних: перетворення з Пітонивських даних і типів. До інтернет даних (таких як JSON):
    * Перетвори Пітонівські типи (`str`, `int`, `float`, `bool`, `list`, тощо).
    * `datetime` об'єкти.
    * `UUID` об'єкти.
    * Моделі датабази.
    * ...і багато іншого.
* Автоматичні інтерективні API документації, включаючи 2 альтернативні інтерфейси:
    * Swagger UI.
    * ReDoc.

---

Coming back to the previous code example, **FastAPI** зробить:

* Провалідує що `item_id` існує в 'path' для `GET` і `PUT` реквестах.
* Провалідує що `item_id` має тип `int` для `GET` і `PUT` реквестах.
    * Якщо це не так, клієнт побачить корисну, явну помилку.
* Перевіре чи існує необов'язковий 'query parameter' який називається `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET` реквестів.
    * Томущо `q` параметер був задекларований з `= None`, він є необов'язковий.
    * Якщо `None` не було тобі цей параметр був би потрібний (так як 'body' в екземплярі з `PUT`).
* Для `PUT` реквестів до `/items/{item_id}`, Читайте 'body' як JSON:
    * Перевірь чи він має потрібний атрибув `name` який має бути `str`.
    * Перевірь чи він має потрібний атрибув `price` який має бути `float`.
    * Перевірь чи він має необов’язковий атрибув `is_offer` який має бути `bool`, якщо він існує.
    * Все це би також пряцювло для глибоко вкладених JSON об'єктах.
* Автоматично перетворюй з і в JSON.
* Документуйте все з OpenAPI, якими можуть користуватися: 
    * Інтерактивні системи документації.
    * Системи автоматичного генерування коду клієнта для багатьох мов.
* Надає 2 інтерактивних веб інтерфейсів для документації.

---

Ми тільки пройшли по поверхності, але ти вже маєш їдею як це все працює.

Попробуй поміняти з:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...від:

```Python
        ... "item_name": item.name ...
```

...до:

```Python
        ... "item_price": item.price ...
```

...і подивись як твій редактор автоматично заповнить атрибути і буде знати їх типи:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для більш повного прикладу, що включає більше функцій, подивись на <a href="https://fastapi.tiangolo.com/tutorial/">Посібник</a>.

**Спойлер попередження**: посібник - включає в себе:

* Декларація **parameters** з інших місць таких як: **headers**, **cookies**, **form fields** і **files**.
* Як встановити **validation constraints** як `maximum_length` або `regex`.
* Дуже потужний і легкий в використанні **<abbr title="також відомий як component, resources, providers, services, injectables">Dependency Injection</abbr>** система.
* Безпека і автентифікація, включаючи підтримку для **OAuth2** з **JWT tokens** і **HTTP Basic** автенфікації.
* Вищий рівень функціональності (але однаково лекго) для декларації **глибоко вкладених JSON моделей** (завдяки Pydantic).
    
* Багато додаткових фіч (завдяки Starlette):
    * **WebSockets**
    * **GraphQL**
    * нереально легкі тести базовані на `requests` і `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...і більше.

## Швидкість

Незалежні бенчмарки від TechEmpower показують що програми написані на **FastAPI** які працюють під Uvicorn є <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">одні з найшвидших фреймворків в Python</a>, тільки поступаючись Starlette та Uvicorn (які внутрішньо використовуються в FastAPI). (*)

Щоб зрозуміти більше про це, подивись на ось цю секцію <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Бенчмарки</a>.

## Необов’язкові бібліотеки

Pydantic використовує:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для швидшого JSON <abbr title="converting the string that comes from an HTTP request into Python data">"парсування"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для веріфікації імейлів.

Starlette використовує:

* <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - Потрібен якщо ти хочеш використовувати `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Потрібен якщо ти хочеш використовувати `FileResponse` або `StaticFiles`.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Потрібен якщо ти хочеш використовувати дефолтну конфігурацію темплейтів.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Потрібен якщо ти хочеш підтримувати форму <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, разом з `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Потрібен для підтримки `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Потрібен для Starlette`SchemaGenerator` (тобі це напевно не потрібно).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Потрібен для підтримки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Потрібен якщо ви використовуєте `UJSONResponse`.

FastAPI / Starlette використовують:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Для сервера який загружає і публікує вашу аплікацію.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Потрібен якщо ви використовуєте `ORJSONResponse`.

Ти можеш встановити всі ці бібліотеки з `pip install fastapi[all]`.

## Ліцензія

Цей проект ліцензований на умовах MIT ліцензії.

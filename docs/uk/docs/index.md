<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI високопродуктивний та простий у вивченні фреймворк, з великою швидкістю написання коду та є повністю готовим до реальних проектів</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Тести">
</a>
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Publish/badge.svg" alt="Публікації">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Покриття коду">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Версії пакету">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Приєднуйтесь до нашого чату у https://gitter.im/tiangolo/fastapi">
</a>
</p>

---

**Документація**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Вихідний код**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI це сучасний, швидкий (високопродуктивний) веб-фреймворк для створення API з використанням Python 3.6+, що базується на стандартних Python типах.

Ключові особливості:

* **Швидкий**: Дуже велика продуктивність, нарівні з **NodeJS** та **Go** (завдяки пакетам Starlette та Pydantic). [Один з найшвидших Python фреймворків на сьогоднішній день](#performance).

* **Швидке написання коду**: Збільшує швидкість розробки приблизно на 200 - 300 відсотків. *
* **Менше помилок**: Зменшує можливість виникнення людських помилок майже на 40 відсотків. *
* **Інтуїтивно зрозумілий**: Гарна робота з редактором. <abbr title="також відоме як авто-доповнення, IntelliSense">Автозавершення</abbr> всюди. Потребує менше часу для дебагінгу.
* **Легкий**: Розроблений бути доступним для вивчення та використання. Потребує менше часу для вивчення документації.
* **Компактніший**: Мінімізовано дублювання коду. Багато особливостей для декларування параметрів. Менше шансів виникнення помилок.
* **Завершений**: Готовий до використання код. З автоматично-генерованою та інтерактивною документацією.
* **Стандартизований**: Оснований та повністю сумісний зі стандартами відкритих API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (раніше відомий як Swagger) та <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* оцінка на основі тестів внутрішньої команди розробки, яка створювала реальні застосунки.</small>

## Відгуки

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

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer** - FastAPI для CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Якщо Ви розробляєте <abbr title="Інтерфейс командного рядка">CLI</abbr> застосунок для використання в терміналі замість веб API, загляніть до <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** це менший брат FastAPI. Але за призначенням це **FastAPI для CLIs**. ⌨️ 🚀

## Програмні вимоги

Python 3.6+

FastAPI стоїть на плечах таких гігантів:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для вебу.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для даних.

## Встановлення

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Також Вам потрібен ASGI сервер для реального проекту, наприклад <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> або <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## Приклади

### Створення

* Створіть файл `main.py` з наступним змістом:

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
<summary>Або використовуйте <code>async def</code>...</summary>

Якщо Ваш код містить асинхронність (`async` / `await`), використовуйте `async def`:

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

Якщо Ви не знаєте, перевірте секцію про <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` та `await` в документації</a>.

</details>

### Запуск

Запустіть сервер з:

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

Команда `uvicorn main:app` містить наступну інформацію:

* `main`: файл `main.py` (Python "модуль").
* `app`: об'єкт, створений у файлі `main.py` за допомогою рядка `app = FastAPI()`.
* `--reload`: перезавантажує сервер після кожної зміни в сирцевому коді. Використовується лише при розробці.

</details>

### Перевірка

Відкрийте наступну сторінку в браузері <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Ви побачите наступну JSON відповідь:

```JSON
{"item_id": 5, "q": "somequery"}
```

Наразі Ви створили API, що:

* Отримує HTTP запит на _шляхи_ `/` та `/items/{item_id}`.
* Обидва _шляхи_ отримують `GET` <em>операції</em> (також відомі як HTTP _методи_).
* _Шлях_ `/items/{item_id}` має _GET параметер_ `item_id`, що має бути типом `int`.
* _Шлях_ `/items/{item_id}` має необов'язковий строковий _GET параметер_ `q`, що має бути типом `str`.

### Інтерактивна API документація

Тепер перейдіть до сторінки <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Ви побачити автоматичну та інтерактивну API документацію (надану за допомогою <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативна API документація

Тепер перейдіть на сторінку <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Тут Ви можете побачити альтернативну автоматичну документацію (надану за допомогою <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Приклад внесення змін

Тепер модифікуйте файл `main.py` для отримання тіла `PUT` запиту.

Оголошуйте тіло за допомогою стандартних Python типів, використовуючи Pydantic.

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

Сервер буде перезавантажено автоматично (тому що Ви додали `--reload` до `uvicorn` команди вище).

### Оновлення інтерактивної API документації

Перейдіть до <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Інтерактивна API документація буде автоматично оновлена, включаючи нове тіло запиту:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Натисніть на кнопку "Try it out" - це дозволить Вам заповнити параметри напряму з API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Далі натисніть на кнопку "Execute" та користувацький інтерфейс зробить запит на Ваш API, відправивши параметри, отримає результат і відобразить його на екрані:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Оновлення альтернативної API документації

Тепер перейдіть до <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Альтернативна документація також буде відображати нові параметри та тіло запиту:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Підсумки

В цілому, Ви оголошуєте **один раз** типи параметрів, тіло, тощо., як параметри функції. 

І робите це Ви зі стандартними типами Python.

Немає потреби вивчати новий синтаксис, методи чи класи специфічних бібліотек, тощо.

Лише стандартний **Python 3.6+**.

Наприклад, для `int`:

```Python
item_id: int
```

або для більш складної `Item` моделі:

```Python
item: Item
```

...з цим оголошенням Ви отримуєте:

* Підтримку редактора, включно з:
    * Автозавершенням.
    * Перевіркою типів.
* Валідацією даних:
    * Автоматичні та чисті помилки коли дані недійсні.
    * Валідація навіть глубоко вкладених JSON об'єктів.
* <abbr title="також відоме як: серіалізація, парсинг, форматування">Перетворення</abbr> вхідних даних: що надходять з мережі до Python даних та типів. Читання з:
    * JSON.
    * Параметрів шляху.
    * Параметрів запиту.
    * Cookies.
    * Заголовків.
    * Форм.
    * Файлів.
* <abbr title="також відоме як: серіалізація, парсинг, форматування">Перетворення</abbr> вихідних даних: перетворення з Python даних та типів у мережеві дані (як JSON):
    * Перетворення Python типів (`str`, `int`, `float`, `bool`, `list`, тощо).
    * `datetime` об'єктів.
    * `UUID` об'єктів.
    * Моделей бази даних.
    * ...та багато іншого.
* Автоматична та інтерактивна API документація, включаючи 2 альтернативні користувацькі інтерфейси:
    * Swagger UI.
    * ReDoc.

---

Повертаючись до попереднього прикладу коду, **FastAPI** буде:

* Валідувати наявність `item_id` серед `GET` та `PUT` запитів.
* Валідувати `item_id` як `int` для `GET` та `PUT` запитів.
    * Якщо це не так - клієнту буде відображено інформативну та зрозумілу помилку.
* Перевіряти необов'язковий параметр `q` (як у `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET` запитів.
    * Так як `q` параметр об'явлено з `= None` - він є необов'язковим.
    * Без `None` параметр буде обов'язковим (як і тіло запиту у випадку з `PUT` запитом).
* Для `PUT` запитів до `/items/{item_id}`, читати тіло запіту як JSON:
    * Перевіряти що міститься обов'язковий параметр `name` що має бути типу `str`. 
    * Перевіряти що міститься обов'язковий параметр `price` що має бути типу `float`.
    * Перевіряти що міститься необов'язковий параметр `is_offer`, що має бути типу `bool`, якщо наявний.
    * Все це буде працювати з усіма вкладеними JSON об'єктами.
* Автоматичне перетворення з та в JSON формат.
* Документуйте все з OpenAPI, що може бути використане:
    * Системою інтерактивної документації.
    * Автоматичною системою генерації клієнтського коду для багатьох мов програмування.
* Надає 2 інтерактивні веб інтерфейси документації.

---

Ми розповіли Вам лише про поверхневі можливості, але Ви вже маєте розуміння як це працює.

Спробуйте змінити рядок:

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

...і побачете як Ваш редактор автоматично підставить атрибути та їх типи:

![підтримка редактора](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для більш детального прикладу, що включає більше можливостей - перейдіть до <a href="https://fastapi.tiangolo.com/tutorial/">Посібника користувача</a>.

**Попередження**: посібник користувача вміщує:

* Оголошення **параметрів** з інших місць, таких як: **заголовки**, **cookies**, **поля форми** та **файли**.
* Як задати **правила валідації**, такі як `maximum_length` чи `regex`.
* Дуже потужні та легкі у використанні **<abbr title="також відомі як компоненти, ресурси, постачальники, сервіси, ін'єкції">Ін'єкційно залежні</abbr>** системи.
* Безпека та аутентифікація, включно з підтримкою **OAuth2** з **JWT токенами** та **HTTP Basic** аутентифікацією.
* Більш продвинуті (але однаково легкі) технології для оголошення **глубоко вкладених JSON моделей** (завдяки Pydantic).
* Багато додаткового функціоналу (завдяки Starlette), такого як:
    * **WebSockets**
    * **GraphQL**
    * надзвичайно легкі тести на основі пакетів `requests` та `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...та інше.

## Швидкодія

Незалежні TechEmpower бенчмарки показують, що **FastAPI** додатки, запущені з Uvicorn <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">є одними з найшвидших Python фреймворків на сьогоднішній день</a>, лише запущені з  Starlette та Uvicorn (використовуються в середині FastAPI). (*)

Для більш детального розуміння дивіться секцію <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Бенчмарки</a>.

## Необов'язкові залежності

Використані у Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для швидшого JSON <abbr title="перетворення рядку з HTTP запиту у Python дані">"парсингу"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для email валідації.

Використані у Starlette:

* <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - Обов'язково для використання `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Обов'язково для використання `FileResponse` чи `StaticFiles`.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Обов'язково для використання стандартного шаблону конфігурації.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Обов'язково для підтримки форм <abbr title="перетворення рядку з HTTP запиту у Python дані">"парсингу"</abbr> з `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Обов'язково для підтримки `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Обов'язково для підтримки `SchemaGenerator` Starlette'у (Вам може бути це не потрібно з FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Обов'язково для підтримки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Обов'язково для використання `UJSONResponse`.

Використані у FastAPI / Starlette:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Для розгортання Вашого додатку.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Обов'язково для використання `ORJSONResponse`.

Ви можете встановити все перераховане завдяки `pip install fastapi[all]`.

## Ліцензія

Цей проект поширюється за ліцензією MIT.

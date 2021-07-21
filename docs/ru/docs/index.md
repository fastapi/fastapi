
{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI фреймворк, лучшая производительность, низкий порог входа, высокая скорость разработки, production-ready решение</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/fastapi" target="_blank">
    <img src="https://travis-ci.com/tiangolo/fastapi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Package version">
</a>
</p>

---

**Документация**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Исходный код**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI - это современный, высокопроизводительный веб-фреймворк для построения API на Python 3.6+ в основе которого лежит стандартная аннотация типов.

Ключевые особенности:

* **Эффективность**: Отличная производительность наравне с **NodeJS** и **Go** (благодаря Starlette и Pydantic). [Один из самых быстрых Python фреймворков](#performance).
* **Скорость разработки**: Увеличьте свою скорость разработки на 200–300%. *
* **Меньше багов**: На 40% меньше багов при разработке. *
* **Авто дополнение**: Отличная поддержка IDE – тратьте меньше времени на отладку.
* **Простота**: Низкий порог вхождения. Простая и понятная документация.
* **Лаконичность**: Минимальное дублирование кода. Большое количество готовых решений.
* **Надёжность**: Получите production-ready код с генерацией интерактивной документации.
* **Специфицирован**: Основан, и полностью совместим, на стандартах API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (так же известный как Swagger) и <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Оценка основана на опыте во внутренней команде программистов при разработке приложений.</small>

## Золотые спонсоры

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Все спонсоры</a>

## Что думают о FastAPI разработчики

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

## **Typer** – FastAPI для CLI приложений

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Если вы разрабатываете <abbr title="Command Line Interface">CLI</abbr>-приложение обратите внимание <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** это младший брат FastAPI's. Используйте его вместо **FastAPI** для **CLI-приложений**. ⌨️ 🚀

## Требования

Python 3.6+

FastAPI стоит на плечах гигантов:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для веб части.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для работы с данными.

## Установка

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Вам также понадобится ASGI сервер например <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> или <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Пример

### Создание

* Создайте файл `main.py`:

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
<summary>Или используйте <code>async def</code>...</summary>

Если ваш код использует `async` / `await`, используйте `async def`:

```Python hl_lines="9  14"
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

**Примечание**:

Если вы не понимаете о чем идёт речь, ознакомьтесь с разделом об <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` и `await` в документации</a>.

</details>

### Запуск

Запустите сервер командой:

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
<summary>О команде <code>uvicorn main:app --reload</code>...</summary>

Команда `uvicorn main:app` состоит из:

* `main`: файл `main.py` (Python модуль).
* `app`: объект который мы создаём в `main.py` строчкой `app = FastAPI()`.
* `--reload`: перезапуск сервера при изменении в коде. Используйте этот ключ только во время разработки.

</details>

### Проверка

Откройте в браузере <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Вы увидите JSON-ответ:

```JSON
{"item_id": 5, "q": "somequery"}
```

Мы создали API который:

* Принимать HTTP запросы по _маршрутам_ `/` и `/items/{item_id}`.
* Оба _маршрута_ умеют обрабатывать `GET`-<em>операцию</em> ( HTTP _метод_).
*  _Маршрут_ `/items/{item_id}` имеет _параметр_ `item_id` типа `int`.
*  _Маршрут_ `/items/{item_id}` имеет необязательный _параметр_ `q` типа `str`.

### Интерактивная API документация

Откройте в браузере <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Перед вами автоматически сгенерированная документация нашего API (предоставленная <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативная API документация

Откройте в браузере <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Это документация предоставлена <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Улучшаем пример

Изменим код `main.py`чтобы получить тело `PUT` запроса.

Определим тело запроса стандартными аннотациями типов Python используя Pydantic.

```Python hl_lines="4  9-12  25-27"
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

Сервер должен автоматически перезагрузиться (благодаря ключу `--reload` у команды `uvicorn` выше).

### Изменения в документации

Отройте в браузере <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Интерактивная документация API автоматически обновилась:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Нажмите кнопку "Try it out" и заполните форму. Так вы можете напрямую взаимодействовать с API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* После заполнения формы нажмите "Execute", пользовательский интерфейс документации соединится с API, отошлет параметры, запросит результаты и выведет их вам на экран:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Обновление альтернативной документации

Перейдите по адресу <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* ReDoc документация также обновилась:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Итог

Вы **один раз** задали типы параметров, тела запроса, и т. д. как параметры функции. 

Вы сделали это используя стандартные средства Python.

Вам не пришлось учить новый синтаксис, методы или классы специальной библиотеки.

Только стандартный **Python 3.6+**.

Пример для типа `int`:

```Python
item_id: int
```

Немного более сложная модель `Item`:

```Python
item: Item
```

...и благодаря всего одному описанию вы получаете:

* Поддержку IDE, включая:
    * Авто дополнение.
    * Проверку типов.
* Валидацию данных:
    * Автоматические и понятные ошибки в случае невалидных данных.
    * Валидация для JSON-объектов любой вложенности.
* <abbr title="Сериализацию, парсинг, маршаллинг">Преобразование</abbr> входных данных. Поддерживаемые форматы:
    * JSON.
    * Параметры для маршрутов, например, `/item/{id}`..
    * Параметры запросов.
    * Cookies.
    * Заголовки запросов.
    * Формы.
    * Файлы.
* <abbr title="Сериализацию, парсинг, маршаллинг">Преобразование</abbr> выходных данных:
    * Преобразование Python типов (`str`, `int`, `float`, `bool`, `list`, и другие).
    * `datetime`.
    * `UUID`.
    * Модели для работы с базой данных.
    * ...и многое другое.
* Автоматическая интерактивная документация API, включающая в себя два разных интерфейса:
    * Swagger UI.
    * ReDoc.

---

Если вернуться к примеру кода, **FastAPI** делает следующее:

* Проверяет, существует ли параметр `item_id` в маршрутах для `GET` и `PUT` запросов.
* Проверяет, является ли параметр `item_id` типом `int` для `GET` и `PUT` запросов.
    * Если нет, API отошлет клиенту понятное сообщение об ошибке.
* Проверяет необязательный параметр `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET` запросов.
    * Если параметр `q` объявлен со значением `= None`, он автоматически считается необязательным.
    * Без инструкции `None` параметр считается обязательным (например, как в `PUT`-запросе).
* Для `PUT`-запросов к `/items/{item_id}`, парсит тело запроса как JSON:
    * Проверяет, существует ли обязательный параметр `name` и является ли он строкой `str`. 
    * Проверяет, существует ли обязательный параметр `price` и является ли он типом `float`.
    * Проверяет, существует ли _необязательный_ параметр `is_offer`, который должен быть `bool`, если существует
    * И всё это работает для JSON-объектов любой вложенности.
* Конвертирует данные в/из JSON.
* Документирует всё по стандарту OpenAPI, который легко использовать в:
    * Интерактивных системах документации.
    * Автоматической генерации кода на клиенте, на любом языке.
* Добавляет 2 прямых интерактивных пользовательских интерфейса для документации и проверки методов API.

---

Мы прошлись по верхам, однако вы уже имеете представление о том как работает **FastApi**.

Попробуйте изменить в строке:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...Это:

```Python
        ... "item_name": item.name ...
```

...На:

```Python
        ... "item_price": item.price ...
```

...и вы увидите как ваша IDE будет авто-дополнять атрибуты и знать их типы:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для более комплексных примеров с большим количеством функционала смотрите <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Спойлер**: Туториал содержит информацию:

* Объявление **параметров** из других источников: **заголовков HTTP**, **cookies**, **форм** и  **файлов**.
* Как установить **ограничения валидации**, например `maximum_length` или `regex`.
* Очень мощный и лёгкий в использовании механизм **<abbr title="Внедрение зависимостей">Dependency Injection</abbr>**.
* Авторизации и безопасность, включая поддержку OAuth2 с JWT-токенов и HTTP-авторизации.
* Более продвинутых (но таких же просты) техник для описания **JSON моделей с большой вложенностью** (благодаря  Pydantic).
* Много дополнительного функционала Starlette:
    * **WebSockets**
    * **GraphQL**
    * Невероятно простое тестирование основанное на `requests` и `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...и многое другое.

## Производительность

Независимые тесты производительности от TechEmpower показывают, что приложения **FastAPI** запущенные на Uvicorn сервере, <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">являются одними из самых быстрых Python приложениями</a>, уступая только Starlette и Uvicorn (они используются внутри FastAPI). (*)

Больше информации вы можете узнать тут – <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Необязательные зависимости

Используемые Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для быстрого JSON <abbr title="Преобразование строки из HTTP запроса в Python объект">"парсинга"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для валидации email.

Используемые Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Необходимо при использовании `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Для файловых ответов от сервера `FileResponse` или `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Для стандартных шаблонов jinja.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Для поддержки <abbr title="Преобразование строки из HTTP запроса в Python объект">"парсинга"</abbr>, форм благодаря `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Необходимо для поддержки `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Поддержка `SchemaGenerator` для Starlette (скорее всего в FastAPI вам это не нужно).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Для поддержки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Необходимо чтобы использовать `UJSONResponse`.

Используемые FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - Сервер для асинхронных приложений на Python.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Для использования класса `ORJSONResponse`.

Вы можете установить их все с помощью `pip install fastapi[all]`.

## Лицензия

Проект распространяется под лицензией MIT.
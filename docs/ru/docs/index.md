
<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI — быстрый, понятный фреймворк для реальных проектов</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/fastapi" target="_blank">
    <img src="https://travis-ci.com/tiangolo/fastapi.svg?branch=master" alt="Статус сборки">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi" alt="Покрытие кода">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Версия пакета в pypi">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Заходите в наш чат https://gitter.im/tiangolo/fastapi">
</a>
</p>

---

**Документация**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Исходники**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI — это современный и шустрый веб-фреймворк для создания API на Python 3.6+.

Вот его главные преимущества:

* **Скорость**: FastAPI работает не хуже движков на **NodeJS** или **Go** (спасибо движкам Starlette и Pydantic). Без шуток, это [один из самых быстрых движков на Python в мире](#_9).
* **Понятный**: Помогает программистам делать на 40% ошибок меньше*.
* **Чистый код**: FastAPI без проблем работает в современных редакторах и IDE. Хорошо поддерживает <abbr title="это то же самое, что и автодополнение или IntelliSense">дополнение кода</abbr>. На отладку и чтение кода у вас будет уходить меньше времени.
* **Легкий и понятный**: Мы сделали FastAPI проще для учебы или работы над реальными проектами. Документацию написали простым, понятным языком и сдобрили большим количеством примеров — почаще заходите сюда, если что-то непонятно. 
* **Простой, но не примитивный**: FastAPI поможет писать код без копипасты и багов. Он гибкий и с большим набором фич «из коробки».
* **Сразу на выпуск**: На FastAPI удобно писать полностью готовый к коммерческому использованию код. FastAPI автоматически, без усилий со стороны программиста создаст документацию к API для проекта (см. ниже).
* **Всё по стандартам**: Основан (и полностью совместим) с открытыми стандартами API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (он же Swagger) и <a href="http://json-schema.org/" class="external-link" target="_blank">JSON-схемами</a>.

<small>* эмпирические данные. Основаны на тестах команды разработчиков движка и опыте построения реальных приложений.</small>

## Что думают о FastAPI разработчики

"*[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products.*"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"*I’m over the moon excited about **FastAPI**. It’s so fun!*"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"*Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that.*"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"*If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]*"

"*We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]*"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"*We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]*"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer** — FastAPI для консольных программ

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Если вы создаете <abbr title="CLI-приложение, Command Line Interface">консольную</abbr> программу, которое будет работать в эмуляторе терминала вместо веба, почитайте про <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** — это такой «младший брат» для FastAPI. Если быть точным, это **FastAPI, только для консольных программ** ⌨️ 🚀

## Системные требования для FastAPI

Python 3.6 или выше.

Фрейморку FastAPI нужны две основные зависимости:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для всего, что связано с вебом.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для проверки и сериализации данных.

## Установка

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

FastAPI — асинхронный движок. Для запуска нужен ASGI-сервер и мы советуем использовать <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> или <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a> (он поддерживает HTTP/2).

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## Примеры

### Создание

* Создайте файл `main.py` и скопируйте в него код:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Превед": "медвед"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Либо то же самое, но асинхронно...</summary>

Просто замените `def` на `async def`:

```Python hl_lines="7 12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Превед": "медвед"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**Хозяйке на заметку**:

Если вы не знаете, зачем нужны асинхронные вызовы, гляньте секцию _"In a hurry?"_ в <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">документации</a>.

</details>

### Запуск

Как помните, нашему приложению нужен сервер. Запустите сервер такой командой:

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
<summary>Что делает команда <code>uvicorn main:app --reload</code>...</summary>

Команда `uvicorn main:app` состоит из трех частей:

* `main`: файл `main.py` приложения (модуль в Python).
* `app`: объект, к которому сервер обращается в `main.py`, он создается строчкой `app = FastAPI()`.
* `--reload`: приказывает серверу перезапускаться после изменений в исходниках. Удобно для разработки, но не делайте так в итоговом проекте.

Если вкратце, эта команда указывает `uvicorn` обратиться к файлу `main.py`, найти объект `app` и запустить сервер. Сервер перезапустится, если файл `main.py` будет изменен.

Если хотите узнать больше — советуем почитать <a href="http://www.uvicorn.org" class="external-link" target="_blank">документацию проекта Uvicorn</a>. 

</details>

### Проверяем, всё ли работает

Откройте в браузере URL <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=medved</a>.

Вы увидите ответ от локального сервера в формате JSON:

```JSON
{"item_id": 5, "q": "medved"}
```

Это всё. Не сложно же, а? :)

Вы только что создали API, который умеет:

* Принимать HTTP запросы по маршрутам `/` и `/items/{item_id}`.
* Оба маршрута умеют обрабатывать `GET`-операции (их еще называют _HTTP-методами_).
* Маршрут `/items/{item_id}` имеет параметр `item_id`, который должен быть целочисленной переменной (`int`).
* Маршрут `/items/{item_id}` имеет необязательный строковой (`str`) параметр `q`.

### Интерактивная документация к API

Теперь зайдите по адресу <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Перед вами появится интерактивная документация к только что написанному API (ее создает <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативная реализация документации к API

А теперь проследуйте по адресу <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы увидите альтернативную реализацию документации (ее создает <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

Выбирайте документацию по вкусу. В итоговом проекте ее можно отключить или перенести на другой адрес.

## Апгрейдим код

Теперь измените файл `main.py`, чтобы тот умел принимать `PUT`-запросы.

Для этого нужно немного подправить тело запроса и описать то, как данные
будут сериализироваться и проверяться (спасибо Pydantic).

```Python hl_lines="2  7 8 9 10  23 24 25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Превед": "медвед"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Просто вставьте код и сохраните файл. Сервер перезагрузится автоматически и вы сразу увидите результат (если вы добавили ключ `--reload` к команде запуска `uvicorn`).

### Проверяем изменения в документации

Откройте адрес <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Интерактивная документация обновится сама — в нее добавится новый раздел для метода `PUT`:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Нажмите кнопку "Try it out" и вставьте в поля какие-нибудь данные, согласно схеме:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Затем нажмите кнопку "Execute". Пользовательский интерфейс документации соединится с API, отошлет параметры, запросит результаты и выведет их вам на экран:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Смотрим изменения в ReDoc

Теперь проследуйте по адресу <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Документация в Redoc попросит вас ввести новые параметры и тело запроса:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### В итоге

Вот так вы **один раз** задаете типы параметров, тело запроса и прочее — через обычные функции. 

Это можно сделать со стандартными типами Python.

Для этого не нужно учить новые методы, плодить классы или устанавливать библиотеки по 30 Гб.

Просто используйте стандартный **Python 3.6+**.

Вот простой пример для параметра с типом `int`:

```Python
item_id: int
```

или сложнее — для модели `Item`:

```Python
item: Item
```

Такой способ очень гибкий и позволяет получить сразу несколько ништяков для разработчика:

* Нормальную поддержку типов в редакторах и IDE, включая:
    * Автодополнение.
    * ... и проверки типов.
* Проверку данных:
    * Автоматизированную и с видными ошибками, если API получает данные в неправильном формате.
    * Проверку даже для сложных, вложенных JSON-объектов.
* <abbr title="то же самое, что сериализация или парсинг">Преобразование</abbr> данных на входе: из сети в поддерживаемые Python'ом структуры данных. Например:
    * JSON-документы.
    * Параметры для маршрутов, например, `/item/{id}`.
    * Параметры запросов, вроде `/items?price=400&name="Товар"`.
    * Куки.
    * Заголовки.
    * Формы.
    * ... и даже файлы.
* <abbr title="то же самое, что сериализация или парсинг">Преобразование</abbr> отсылаемых данных: из структур и типов Python'а в веб-форматы (например, JSON):
    * Преобразование типов Python'а (`str`, `int`, `float`, `bool`, `list` и пр).
    * Объекты `datetime`.
    * Объекты `UUID`.
    * Модели баз данных.
    * ...и всё, что умеет Pydantic.
* Автоматическую документацию, с двумя разными интерфейсами на выбор:
    * Swagger UI.
    * ReDoc.

---

Если вернуться в примерам кода, **FastAPI** делает следующее:

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
    * И всё это работает для сложных и вложенных JSON-объектов.
* Конвертирует данные в/из JSON.
* Документирует всё по стандарту OpenAPI, который легко использовать в:
    * Интерактивных системах документации.
    * Автоматической генерации кода на клиенте, на любом языке.
* Добавляет 2 прямых интерактивных пользовательских интерфейса для документации и проверки методов API.

---

На самом деле мы только что немного пробежались по азам FastAPI, но вы наверняка поняли идею того, как всё работает.

Попробуйте изменить строку кода:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...из:

```Python
        ... "item_name": item.name ...
```

...на:

```Python
        ... "item_price": item.price ...
```

...и вы увидите, как ваш редактор или IDE поможет вам с автодополнением:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)
_(скриншот из Visual Studio Code)_

Тут в документации есть продвинутые примеры, и некоторые — не для слабонервных. Заглядывайте на огонек в раздел <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Немного спойлеров**: внутри туториала вы найдете:

* Объявление **параметров** из других источников: **заголовков HTTP**, **куков**, **форм** и даже **файлов**.
* Как расширить **проверки**, например для максимальной длины строк или с помощью регулярных выражений.
* Мощная, но легкая в освоении система **<abbr title="она же компоненты, ресурсы, провайдеры, сервисы">внедрения зависимостей</abbr>**.
* Примочки для авторизации и безопасности, включая поддержку **OAuth2** с **JWT-токерами** и **HTTP-авторизацией**.
* Техники для объявления **продвинутых моделей для сериализации данных** (благослови Линукс человека, придумавшего Pydantic).
* Много дополнительных фичей (спасибо Starlette), вроде:
    * **WebSockets**
    * **GraphQL** API
    * легкие тесты, основанные на модулях `requests` и `pytest`
    * **CORS**
    * **Сессии в куках**
    * ...и так далее.
Это всё есть в документации :-)

## Производительность

Бенчмарки от TechEmpower говорят, что приложения **FastAPI** под Uvicorn <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">являются одними их самых быстрых приложений на Python</a>, только наравне с Starlette и Uvicorn (эти две библиотеки используются внутри FastAPI). (*)

Прочитайте о результатах и сравните сами, в секции <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> есть ссылки.

## Необязательные зависимости

Используются Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для быстрого JSON-<abbr title="преобразование строк из HTTP-запросов в типы Python">парсинга</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - для проверки полей с e-mail.

Используются Starlette:

* <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - нужно, если хотите тестировать ваше приложение с помощью класса `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - для файловых ответов от сервера — `FileResponse` или `StaticFiles`.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - для стандартных шаблонов jinja.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - поддержка <abbr title="преобразование строк из HTTP-запросов в типы Python">"парсинга форм"</abbr>, с помощью `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - поддержка `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - для класса `SchemaGenerator` в Starlette.
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - для поддержки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - альтернативная библиотека (де)сериализации JSON — `UJSONResponse`.

Используют FastAPI / Starlette:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - сервер для асинхронных приложений на Python.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - для использования класса `ORJSONResponse`.

Необязательные зависимости можно установить вручную по-одному или все сразу, командой `pip install fastapi[all]`.

## Лицензия

Проект распространяется под лицензие MIT.


{!../../../docs/missing-translation.md!}


<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI фреймворк, высокая производительность, легкий в изучении, быстрый для написания, готов для работы</em>
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

FastAPI соврменный, быстрый (высоко-производительный), веб фреймворк для создания APIs с Python 3.6+ базируемый на стандартных 
аннотациях типов Python.

Ключевые особенности:

* **Быстрый**: Очень большая производительность, на равне с **NodeJS** и **Go** (спасибо Starlette и Pydantic). [Один из самых быстрых доступных фреймворков Python](#performance).

* **Быстрый для написания**: Увеличьте скорость разработки примерно на 200–300 %.
* **Меньше багов**: Можно сократить около 40% ошибок, вызванных человеком (разработчиком).
* **Понятный**: Отличная поддержка редактора. <abbr title="также известный как, IntelliSense">Автозаполнение</abbr> всегда. Меньше времени на отладку.
* **Легкий**: Разработан, чтобы быть простым в использовании и обучении. Меньше времени на чтение документации.
* **Краткий**: Минимальное повторение кода. Множество функций от каждого объявления параметров. Меньше багов.
* **Надежный**: Получите готовый к работе код. С автоматическим интерактивным документированием.
* **На основе стандартов**: Основан на открытых стандартах API (и полностью совместим с ними): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (ранее известный как Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* оценка на основе тестов внутренней команды разработчиков, создающих производственные приложения.</small>

## Спонсоры

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Остальные спонсоры</a>

## Отзывы

"_[...] В последнее время я часто использую **FastAPI**. [...] На самом деле я планирую использовать его для всех членов моей команды **ML сервисов в Microsoft**. Некоторые из них интегрируются в основной **Windows** продукт и некоторые **Office** продукты._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Мы взяли библиотеку **FastAPI** для создания **REST** сервера, который можно запросить для получения **прогнозов**. [для Людвига]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** рада объявить о выпуске с открытым исходным кодом нашего **кризисного управления**  оркестровки фреймворка: **Dispatch**! [сделано с **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Я в полном восторге от **FastAPI**. Это очень весело_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Честно говоря, то, что вы создали, выглядит очень солидно и отполировано. Во многих отношениях, это то, чем я хотел видеть **Hug** это действительно вдохновляет, когда видишь, как кто-то создает это._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Если вы хотите изучить один **современный фреймворк** для проектирования REST APIs, попробуйте **FastAPI** [...] Он быстрый, простой в использовании и легкий в освоении [...]_"

"_Мы перешли на **FastAPI** для нашего **APIs** [...] Думаю вам понравится [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, FastAPI для CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Если вы создаете <abbr title="Command Line Interface">CLI</abbr> приложение для использования в терминале а не веб-API, попробуйте <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** это  младший брат FastAPI's . И он задуман как **FastAPI для CLIs**. ⌨️ 🚀

## Требования

Python 3.6+

FastAPI стоит на плечах гигантов:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> для веб части.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> для части данных.

## Установка

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Вам также потребуется ASGI сервер для работы, такие как: <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> or <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## Пример

### Создание

* создайте файл `main.py` как:

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
<summary>или используйте <code>async def</code>...</summary>

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

Если вы не знаете проверьте раздел "Торопитесь?" <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` и `await` в документации</a>.

</details>

### Запуск

Запустите сервер с параметрами:

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
<summary>Подробнее о командах <code>uvicorn main:app --reload</code>...</summary>

К команде `uvicorn main:app` относится:

* `main`: файл `main.py` (модуль Python).
* `app`: объект, созданный внутри `main.py` на строке `app = FastAPI()`.
* `--reload`: сделать перезагрузку сервера после изменения. Только для разработки.

</details>

### Проверка

Откройте свой браузер на <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Вы можете увидеть JSON ответ:

```JSON
{"item_id": 5, "q": "somequery"}
```

Вы уже создали API, который:

* Принимает HTTP запросы по пути _пути_ `/` и `/items/{item_id}`.
* Оба _пути_ принимают `GET` <em>операции</em> (также известные как HTTP _методы_).
* _Путь_ `/items/{item_id}`имеет _параметр пути_ `item_id` который должен быть равен `int`.
* _Путь_ `/items/{item_id}` имеет опциональный `str` _параметр запроса_ `q`.

### Интерактивная API документация

Пройдите по адресу <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs<a>

Вы увидете автоматически сделаную документацию (предоставленая <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативная API документация

И теперь перейдите на <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы сможете увидеть альтернативную версию документации (предоставленая <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Пример улучшения

Сейчас изменим файл `main.py` для отправки тела `PUT` запросом.

Объявите тело, используя стандартные типы Python, благодаря Pydantic.

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

Сервер должен перезагрузиться автоматически (потому что вы добавили `--reload` к команде `uvicorn` выше).

### Улучшение интерактивной API документации

Перейдите на <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Документация интерактивного API будет автоматически обновлена, включая новое тело:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Нажмите на кнопку "Попробовать", это позволит вам заполнить параметры и напрямую взаимодействовать с API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Затем нажмите на кнопку "Выполнить", пользовательский интерфейс свяжется с вашим API, отправит параметры, получит результаты и покажет их на экране.:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Улучшение альтернативной документации API

Теперь перейдите на <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Альтернативная документация также будет отражать новый параметр запроса и тело запроса:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Итоги

Вкратце, вы объявляете **один раз** типы параметров, тела и т.д. как параметры функции. 

Вы делаете это с помощью стандартных типов современного Python.

Вам не нужно изучать новый синтаксис, методы или классы конкретной библиотеки и т.д.

Простой стандарт **Python 3.6+**.

Например для  `int`:

```Python
item_id: int
```

или для более сложного `Item` модели:

```Python
item: Item
```

...и с помощью этой единственной декларации вы получаете:

* Поддержку кода включая:
    * Completion.
    * Type checks.
* Валидацию данных:
    * Автоматические и явные ошибки, когда данные недействительны.
    * Валидация даже для глубоко вложенных объектов JSON.
* <abbr title="also known as: serialization, parsing, marshalling">Конверсия</abbr> входных данных: поступающих из сети данных и типов Python. Чтение из:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="также известный как: сериализация, парсинг, маршаллинг">Конверсия</abbr> входных данных: поступающих из сети данных и типов Python. Чтение из (as JSON):
    * Конвертирование Python типов (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` объектов.
    * `UUID` объектов.
    * Database модели.
    * ...и многое другое.
* Автоматическая интерактивная документация по API, включая 2 альтернативных пользовательских интерфейса:
    * Swagger UI.
    * ReDoc.

---

Возвращаясь к предыдущему примеру кода, **FastAPI** будет:

* Проверять наличие `item_id` в пути для запросов `GET` и `PUT`.
* Убеждаться, что `item_id` имеет тип `int` для запросов `GET` и `PUT`.
    * Если это не так, клиент увидит полезную и понятную ошибку.
* Проверять, существует ли дополнительный параметр запроса с именем `q` (в `http://127.0.0.1:8000/items/foo?q=somequery`) для `GET` запроса.
    * Поскольку параметр `q` объявлен с `= None`, он является необязательным.
    * Без `None` оно было бы обязательным (как и тело в случае с `PUT`).
* Для запросов `PUT` к `/items/{item_id}`, считывание тела как JSON:
    * Проверять, что у него есть обязательный атрибут `name`, который должен быть `str`.. 
    * Проверять, что у него есть обязательный атрибут `price`, который должен быть `float`..
    * Проверять, что он имеет необязательный атрибут `is_offer`, который должен быть `bool`, если присутствует.
    * Все это будет работать и для глубоко вложенных объектов JSON.
* Автоматическое преобразование из JSON и в JSON.
* Документируйте все с помощью OpenAPI, что может быть использовано:
    * Интерактивные системы документирования.
    * Системы автоматической генерации клиентского кода для многих языков.
* Обеспечит 2 интерактивных веб-интерфейса документации напрямую.

---

Мы только прощупали почву, но вы уже получили представление о том, как все это работает.

Попробуйте изменить строку:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

....с:

```Python
        ... "item_name": item.name ...
```

...на:

```Python
        ... "item_price": item.price ...
```

...и посмотрите, как ваш редактор будет автоматически заполнять атрибуты и узнавать их типы:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Для более полного примера, включающего больше возможностей, см. <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Внимание, cпойлеры!**: учебник - руководство пользователя включает в себя:

* Объявление **параметров** из других различных мест, таких как: **заголовки**, **куки**, **поля формы** и **файлы**.
* Как установить **validation constraints** в виде `maximum_length` или `regex`.
* Очень мощная и простая в использовании **<abbr title="также известные как компоненты, ресурсы, поставщики, услуги, инъекции">Инъекция зависимостей</abbr>** система.
* Безопасность и аутентификация, включая поддержку **OAuth2** с **JWT tokens** и **HTTP Basic** авторизация.
* Более продвинутые (но не менее простые) техники для объявления **глубоко вложенных моделей JSON** (спасибо Pydantic).
* Множество дополнительных функций (благодаря Starlette), таких как:
    * **WebSockets**
    * **GraphQL**
    * extremely easy tests based on `requests` and `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...и многие другие.

## Производительность

Независимые бенчмарки TechEmpower показывают, что приложения **FastAPI**, работающие под Uvicorn, являются <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">одними из самых быстрых Python-фреймворков</a>, уступая лишь Starlette и самому Uvicorn (используемому внутри FastAPI). (*)

Чтобы узнать об этом больше, см. раздел <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Бенчмарки</a>.

## Необязательные зависимости

Используется Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - для быстрого JSON <abbr title="преобразование строки, полученной из HTTP-запроса, в данные Python">"парсинга"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - валидация почты.

Used by Starlette:

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - Требуется, если вы хотите использовать `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Требуется, если вы хотите использовать `FileResponse` или `StaticFiles`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Требуется, если вы хотите использовать конфигурацию шаблона по умолчанию.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Требуется, если вы хотите поддерживать форму <abbr title="преобразование строки, полученной из HTTP-запроса, в данные Python">"парсинга"</abbr>, с `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Требуется для поддержки `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Требуется для Starlette's `SchemaGenerator`(скорее всего, он вам не понадобится при использовании FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Требуется для поддержки `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Требуется если вы хотите использовать `UJSONResponse`.

Используется FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - для сервера, который загружает и обслуживает ваше приложение.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Требуется, если вы хотите использовать `ORJSONResponse`.

Вы можете установить все это с помощью `pip install fastapi[all]`.

## Лицензия

Этот проект лицензирован на условиях лицензии MIT.

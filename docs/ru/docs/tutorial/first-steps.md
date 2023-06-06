# Первые шаги

Самый простой FastAPI файл может выглядеть так:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Скопируйте в файл `main.py`.

Запустите сервер в режиме реального времени:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! note "Технические детали"
    Команда `uvicorn main:app` обращается к:

    * `main`: файл `main.py` (модуль Python).
    * `app`: объект, созданный внутри файла `main.py` в строке `app = FastAPI()`.
    * `--reload`: перезапускает сервер после изменения кода. Используйте только для разработки.

В окне вывода появится следующая строка:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Эта строка показывает URL-адрес, по которому приложение доступно на локальной машине.

### Проверьте

Откройте браузер по адресу: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Вы увидите JSON-ответ следующего вида:

```JSON
{"message": "Hello World"}
```

### Интерактивная документация API

Перейдите по адресу: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Вы увидите автоматически сгенерированную, интерактивную документацию по API (предоставленную <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативная документация API

Теперь перейдите по адресу <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы увидите альтернативную автоматически сгенерированную документацию (предоставленную <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** генерирует "схему" всего API, используя стандарт **OpenAPI**.

#### "Схема"

"Схема" - это определение или описание чего-либо. Не код, реализующий это, а только абстрактное описание.

#### API "схема"

<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> - это спецификация, которая определяет, как описывать схему API.

Определение схемы содержит пути (paths) API, их параметры и т.п.

#### "Схема" данных

Термин "схема" также может относиться к формату или структуре некоторых данных, например, JSON.

Тогда, подразумеваются атрибуты JSON, их типы данных и т.п.

#### OpenAPI и JSON Schema

OpenAPI описывает схему API. Эта схема содержит определения (или "схемы") данных, отправляемых и получаемых API. Для описания структуры данных в JSON используется стандарт **JSON Schema**.

#### Рассмотрим `openapi.json`

Если Вас интересует, как выглядит исходная схема OpenAPI, то FastAPI автоматически генерирует JSON-схему со всеми описаниями API.

Можете посмотреть здесь: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Вы увидите примерно такой JSON:

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### Для чего нужен OpenAPI

Схема OpenAPI является основой для обеих систем интерактивной документации.

Существуют десятки альтернативных инструментов, основанных на OpenAPI. Вы можете легко добавить любой из них к **FastAPI** приложению.

Вы также можете использовать OpenAPI для автоматической генерации кода для клиентов, которые взаимодействуют с API. Например, для фронтенд-, мобильных или IoT-приложений.

## Рассмотрим поэтапно

### Шаг 1: импортируйте `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` это класс в Python, который предоставляет всю функциональность для API.

!!! note "Технические детали"
    `FastAPI` это класс, который наследуется непосредственно от `Starlette`.

    Вы можете использовать всю функциональность <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> в `FastAPI`.

### Шаг 2: создайте экземпляр `FastAPI`

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Переменная `app` является экземпляром класса `FastAPI`.

Это единая точка входа для создания и взаимодействия с API.

Именно к этой переменной `app` обращается `uvicorn` в команде:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Если создать такое приложение:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

И поместить его в `main.py`, тогда вызов `uvicorn` будет таким:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Шаг 3: определите *операцию пути (path operation)*

#### Путь (path)

"Путь" это часть URL, после первого символа `/`, следующего за именем домена.

Для URL:

```
https://example.com/items/foo
```

...путь выглядит так:

```
/items/foo
```

!!! info "Дополнительная иформация"
    Термин "path" также часто называется "endpoint" или "route".

При создании API, "путь" является основным способом разделения "задач" и "ресурсов".

#### Операция (operation)

"Операция" это один из "методов" HTTP.

Таких, как:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...и более экзотических:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

По протоколу HTTP можно обращаться к каждому пути, используя один (или несколько) из этих "методов".

---

При создании API принято использовать конкретные HTTP-методы для выполнения определенных действий.

Обычно используют:

* `POST`: создать данные.
* `GET`: прочитать.
* `PUT`: изменить (обновить).
* `DELETE`: удалить.

В OpenAPI каждый HTTP метод называется "**операция**".

Мы также будем придерживаться этого термина.

#### Определите *декоратор операции пути (path operation decorator)*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Декоратор `@app.get("/")` указывает **FastAPI**, что функция, прямо под ним, отвечает за обработку запросов, поступающих по адресу:

* путь `/`
* использующих <abbr title="HTTP GET метод"><code>get</code> операцию</abbr>

!!! info "`@decorator` Дополнительная информация"
    Синтаксис `@something` в Python называется "декоратор".

    Вы помещаете его над функцией. Как красивую декоративную шляпу (думаю, что оттуда и происходит этот термин).

    "Декоратор" принимает функцию ниже и выполняет с ней какое-то действие.

    В нашем случае, этот декоратор сообщает **FastAPI**, что функция ниже соответствует **пути** `/` и  **операции** `get`.

    Это и есть "**декоратор операции пути**".

Можно также использовать операции:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

И более экзотические:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip "Подсказка"
    Вы можете использовать каждую операцию (HTTP-метод) по своему усмотрению.

    **FastAPI** не навязывает определенного значения для каждого метода.

    Информация здесь представлена как рекомендация, а не требование.

    Например, при использовании GraphQL обычно все действия выполняются только с помощью POST операций.

### Шаг 4: определите **функцию операции пути**

Вот "**функция операции пути**":

* **путь**: `/`.
* **операция**: `get`.
* **функция**: функция ниже "декоратора" (ниже `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Это обычная Python функция.

**FastAPI** будет вызывать её каждый раз при получении `GET` запроса к URL "`/`".

В данном случае это асинхронная функция.

---

Вы также можете определить ее как обычную функцию вместо `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note "Технические детали"
    Если не знаете в чём разница, посмотрите [Конкурентность: *"Нет времени?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Шаг 5: верните результат

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Вы можете вернуть `dict`, `list`, отдельные значения `str`, `int` и т.д.

Также можно вернуть модели Pydantic (рассмотрим это позже).

Многие объекты и модели будут автоматически преобразованы в JSON (включая ORM). Пробуйте использовать другие объекты, которые предпочтительней для Вас, вероятно, они уже поддерживаются.

## Резюме

* Импортируем `FastAPI`.
* Создаём экземпляр `app`.
* Пишем **декоратор операции пути** (такой как `@app.get("/")`).
* Пишем **функцию операции пути** (`def root(): ...`).
* Запускаем сервер в режиме разработки (`uvicorn main:app --reload`).

# Первые шаги { #first-steps }

Самый простой файл FastAPI может выглядеть так:

{* ../../docs_src/first_steps/tutorial001.py *}

Скопируйте это в файл `main.py`.

Запустите сервер в режиме реального времени:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

В выводе будет строка примерно такого вида:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Эта строка показывает URL, по которому ваше приложение доступно на локальной машине.

### Проверьте { #check-it }

Откройте браузер по адресу: <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Вы увидите JSON-ответ вида:

```JSON
{"message": "Hello World"}
```

### Интерактивная документация API { #interactive-api-docs }

Теперь перейдите по адресу: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Вы увидите автоматически сгенерированную интерактивную документацию по API (предоставлено <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативная документация API { #alternative-api-docs }

И теперь перейдите по адресу <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы увидите альтернативную автоматически сгенерированную документацию (предоставлено <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** генерирует «схему» всего вашего API, используя стандарт **OpenAPI** для описания API.

#### «Схема» { #schema }

«Схема» — это определение или описание чего-либо. Не код, который это реализует, а только абстрактное описание.

#### «Схема» API { #api-schema }

В данном случае <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> — это спецификация, которая определяет, как описывать схему вашего API.

Это определение схемы включает пути вашего API, возможные параметры, которые они принимают, и т. п.

#### «Схема» данных { #data-schema }

Термин «схема» также может относиться к форме некоторых данных, например, к содержимому JSON.

В таком случае это будут атрибуты JSON, их типы данных и т. п.

#### OpenAPI и JSON Schema { #openapi-and-json-schema }

OpenAPI определяет схему API для вашего API. И эта схема включает определения (или «схемы») данных, отправляемых и получаемых вашим API, с использованием стандарта **JSON Schema** для схем данных JSON.

#### Посмотрите `openapi.json` { #check-the-openapi-json }

Если вам интересно, как выглядит исходная схема OpenAPI, FastAPI автоматически генерирует JSON (схему) с описанием всего вашего API.

Вы можете посмотреть её напрямую по адресу: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Вы увидите JSON, начинающийся примерно так:

```JSON
{
    "openapi": "3.1.0",
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

#### Для чего нужен OpenAPI { #what-is-openapi-for }

Схема OpenAPI является основой для обеих включённых систем интерактивной документации.

Есть десятки альтернатив, все основаны на OpenAPI. Вы можете легко добавить любую из них в ваше приложение, созданное с **FastAPI**.

Вы также можете использовать её для автоматической генерации кода для клиентов, которые взаимодействуют с вашим API. Например, для фронтенд-, мобильных или IoT-приложений.

## Рассмотрим поэтапно { #recap-step-by-step }

### Шаг 1: импортируйте `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI` — это класс на Python, который предоставляет всю функциональность для вашего API.

/// note | Технические детали

`FastAPI` — это класс, который напрямую наследуется от `Starlette`.

Вы можете использовать весь функционал <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> и в `FastAPI`.

///

### Шаг 2: создайте экземпляр `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

Здесь переменная `app` будет экземпляром класса `FastAPI`.

Это будет основная точка взаимодействия для создания всего вашего API.

### Шаг 3: создайте *операцию пути (path operation)* { #step-3-create-a-path-operation }

#### Путь (path) { #path }

Здесь «путь» — это последняя часть URL, начиная с первого символа `/`.

Итак, в таком URL:

```
https://example.com/items/foo
```

...путь будет:

```
/items/foo
```

/// info | Информация

«Путь» также часто называют «эндпоинт» или «маршрут».

///

При создании API «путь» — это основной способ разделения «задач» и «ресурсов».

#### Операция (operation) { #operation }

«Операция» здесь — это один из HTTP-«методов».

Один из:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...и более экзотические:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

В протоколе HTTP можно обращаться к каждому пути, используя один (или несколько) из этих «методов».

---

При создании API обычно используют конкретные HTTP-методы для выполнения конкретных действий.

Обычно используют:

* `POST`: создать данные.
* `GET`: прочитать данные.
* `PUT`: обновить данные.
* `DELETE`: удалить данные.

Таким образом, в OpenAPI каждый HTTP-метод называется «операцией».

Мы тоже будем называть их «операциями».

#### Определите *декоратор операции пути (path operation decorator)* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

`@app.get("/")` сообщает **FastAPI**, что функция прямо под ним отвечает за обработку запросов, поступающих:

* по пути `/`
* с использованием <abbr title="метод HTTP GET"><code>get</code> операции</abbr>

/// info | Информация о `@decorator`

Синтаксис `@something` в Python называется «декоратор».

Его размещают над функцией. Как красивая декоративная шляпа (кажется, отсюда и пошёл термин).

«Декоратор» берёт функцию ниже и делает с ней что-то.

В нашем случае этот декоратор сообщает **FastAPI**, что функция ниже соответствует **пути** `/` с **операцией** `get`.

Это и есть «декоратор операции пути».

///

Можно также использовать другие операции:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

И более экзотические:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Подсказка

Вы можете использовать каждый метод (HTTP-операцию) так, как считаете нужным.

**FastAPI** не навязывает какого-либо конкретного смысла.

Эта информация дана как рекомендация, а не требование.

Например, при использовании GraphQL обычно все действия выполняются только с помощью POST-операций.

///

### Шаг 4: определите **функцию операции пути** { #step-4-define-the-path-operation-function }

Вот наша «функция операции пути»:

* **путь**: `/`.
* **операция**: `get`.
* **функция**: функция ниже «декоратора» (ниже `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Это функция на Python.

**FastAPI** будет вызывать её каждый раз, когда получает запрос к URL «`/`» с операцией `GET`.

В данном случае это асинхронная (`async`) функция.

---

Вы также можете определить её как обычную функцию вместо `async def`:

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note | Примечание

Если вы не знаете, в чём разница, посмотрите [Асинхронность: *"Нет времени?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Шаг 5: верните содержимое { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Вы можете вернуть `dict`, `list`, отдельные значения `str`, `int` и т.д.

Также можно вернуть модели Pydantic (подробнее об этом позже).

Многие другие объекты и модели будут автоматически преобразованы в JSON (включая ORM и т. п.). Попробуйте использовать те, что вам привычнее, с высокой вероятностью они уже поддерживаются.

## Резюме { #recap }

* Импортируйте `FastAPI`.
* Создайте экземпляр `app`.
* Напишите **декоратор операции пути**, например `@app.get("/")`.
* Определите **функцию операции пути**; например, `def root(): ...`.
* Запустите сервер разработки командой `fastapi dev`.

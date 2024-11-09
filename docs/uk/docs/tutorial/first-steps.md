# Перші кроки

Найпростіший файл FastAPI може виглядати так:

```Python
{!../../docs_src/first_steps/tutorial001.py!}
```

Скопіюйте це до файлу `main.py`.

Запустіть сервер:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

У консолі буде рядок приблизно такого змісту:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Цей рядок показує URL, за яким додаток запускається на вашій локальній машині.

### Перевірте

Відкрийте браузер та введіть адресу <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Ви побачите у відповідь таке повідомлення у форматі JSON:

```JSON
{"message": "Hello World"}
```

### Інтерактивна API документація

Перейдемо сюди <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Ви побачите автоматичну інтерактивну API документацію (створену завдяки <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативна API документація

Тепер перейдемо сюди <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Ви побачите альтернативну автоматичну документацію (створену завдяки <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** генерує "схему" з усім вашим API, використовуючи стандарт **OpenAPI** для визначення API.

#### "Схема"

"Схема" - це визначення або опис чогось. Це не код, який його реалізує, а просто абстрактний опис.

#### API "схема"

У цьому випадку, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> є специфікацією, яка визначає, як описати схему вашого API.

Це визначення схеми включає шляхи (paths) вашого API, можливі параметри, які вони приймають тощо.

#### "Схема" даних

Термін "схема" також може відноситися до структури даних, наприклад, JSON.

У цьому випадку це означає - атрибути JSON і типи даних, які вони мають тощо.

#### OpenAPI і JSON Schema

OpenAPI описує схему для вашого API. І ця схема включає визначення (або "схеми") даних, що надсилаються та отримуються вашим API за допомогою **JSON Schema**, стандарту для схем даних JSON.

#### Розглянемо `openapi.json`

Якщо вас цікавить, як виглядає вихідна схема OpenAPI, то FastAPI автоматично генерує JSON-схему з усіма описами API.

Ознайомитися можна за посиланням: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Ви побачите приблизно такий JSON:

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

#### Для чого потрібний OpenAPI

Схема OpenAPI є основою для обох систем інтерактивної документації.

Існують десятки альтернативних інструментів, заснованих на OpenAPI. Ви можете легко додати будь-який з них до **FastAPI** додатку.

Ви також можете використовувати OpenAPI для автоматичної генерації коду для клієнтів, які взаємодіють з API. Наприклад, для фронтенд-, мобільних або IoT-додатків

## А тепер крок за кроком

### Крок 1: імпортуємо `FastAPI`

```Python hl_lines="1"
{!../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` це клас у Python, який надає всю функціональність для API.

/// note | Технічні деталі

`FastAPI` це клас, який успадковується безпосередньо від `Starlette`.

Ви також можете використовувати всю функціональність <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> у `FastAPI`.

///

### Крок 2: створюємо екземпляр `FastAPI`

```Python hl_lines="3"
{!../../docs_src/first_steps/tutorial001.py!}
```
Змінна `app` є екземпляром класу `FastAPI`.

Це буде головна точка для створення і взаємодії з API.

### Крок 3: визначте операцію шляху (path operation)

#### Шлях (path)

"Шлях" це частина URL, яка йде одразу після символу `/`.

Отже, у такому URL, як:

```
https://example.com/items/foo
```

...шлях буде:

```
/items/foo
```

/// info | Додаткова інформація

"Шлях" (path) також зазвичай називають "ендпоінтом" (endpoint) або "маршрутом" (route).

///

При створенні API, "шлях" є основним способом розділення "завдань" і "ресурсів".
#### Operation

"Операція" (operation) тут означає один з "методів" HTTP.

Один з:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...та більш екзотичних:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

У HTTP-протоколі можна спілкуватися з кожним шляхом, використовуючи один (або кілька) з цих "методів".

---

При створенні API зазвичай використовуються конкретні методи HTTP для виконання певних дій.

Як правило, використовують:

* `POST`: для створення даних.
* `GET`: для читання даних.
* `PUT`: для оновлення даних.
* `DELETE`: для видалення даних.

В OpenAPI кожен HTTP метод називається "операція".

Ми також будемо дотримуватися цього терміна.

#### Визначте декоратор операції шляху (path operation decorator)

```Python hl_lines="6"
{!../../docs_src/first_steps/tutorial001.py!}
```
Декоратор `@app.get("/")` вказує **FastAPI**, що функція нижче, відповідає за обробку запитів, які надходять до неї:

* шлях `/`
* використовуючи <abbr title="an HTTP GET method"><code>get</code> операцію</abbr>

/// info | `@decorator` Додаткова інформація

Синтаксис `@something` у Python називається "декоратором".

Ви розташовуєте його над функцією. Як гарний декоративний капелюх (мабуть, звідти походить термін).

"Декоратор" приймає функцію нижче і виконує з нею якусь дію.

У нашому випадку, цей декоратор повідомляє **FastAPI**, що функція нижче відповідає **шляху** `/` і **операції** `get`.

Це і є "декоратор операції шляху (path operation decorator)".

///

Можна також використовувати операції:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

І більш екзотичні:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Порада

Ви можете використовувати кожну операцію (HTTP-метод) на свій розсуд.

**FastAPI** не нав'язує жодного певного значення для кожного методу.

Наведена тут інформація є рекомендацією, а не обов'язковою вимогою.

Наприклад, під час використання GraphQL зазвичай усі дії виконуються тільки за допомогою `POST` операцій.

///

### Крок 4: визначте **функцію операції шляху (path operation function)**

Ось "**функція операції шляху**":

* **шлях**: це `/`.
* **операція**: це `get`.
* **функція**: це функція, яка знаходиться нижче "декоратора" (нижче `@app.get("/")`).

```Python hl_lines="7"
{!../../docs_src/first_steps/tutorial001.py!}
```

Це звичайна функція Python.

FastAPI викликатиме її щоразу, коли отримає запит до URL із шляхом "/", використовуючи операцію `GET`.

У даному випадку це асинхронна функція.

---

Ви також можете визначити її як звичайну функцію замість `async def`:

```Python hl_lines="7"
{!../../docs_src/first_steps/tutorial003.py!}
```

/// note | Примітка

Якщо не знаєте в чому різниця, подивіться [Конкурентність: *"Поспішаєш?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Крок 5: поверніть результат

```Python hl_lines="8"
{!../../docs_src/first_steps/tutorial001.py!}
```

Ви можете повернути `dict`, `list`, а також окремі значення `str`, `int`, ітд.

Також можна повернути моделі Pydantic (про це ви дізнаєтесь пізніше).

Існує багато інших об'єктів і моделей, які будуть автоматично конвертовані в JSON (зокрема ORM тощо). Спробуйте використати свої улюблені, велика ймовірність, що вони вже підтримуються.

## Підіб'ємо підсумки

* Імпортуємо `FastAPI`.
* Створюємо екземпляр `app`.
* Пишемо **декоратор операції шляху** як `@app.get("/")`.
* Пишемо **функцію операції шляху**; наприклад, `def root(): ...`.
* Запускаємо сервер у режимі розробки `fastapi dev`.

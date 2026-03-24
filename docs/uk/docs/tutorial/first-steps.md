# Перші кроки { #first-steps }

Найпростіший файл FastAPI може виглядати так:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Скопіюйте це до файлу `main.py`.

Запустіть live-сервер:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

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

У виводі є рядок приблизно такого змісту:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Цей рядок показує URL, за яким ваш застосунок обслуговується на вашій локальній машині.

### Перевірте { #check-it }

Відкрийте браузер за адресою [http://127.0.0.1:8000](http://127.0.0.1:8000).

Ви побачите JSON-відповідь:

```JSON
{"message": "Hello World"}
```

### Інтерактивна API документація { #interactive-api-docs }

Тепер перейдіть сюди [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Ви побачите автоматичну інтерактивну API документацію (надається [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Альтернативна API документація { #alternative-api-docs }

А тепер перейдіть сюди [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Ви побачите альтернативну автоматичну документацію (надається [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** генерує «схему» з усім вашим API, використовуючи стандарт **OpenAPI** для визначення API.

#### «Схема» { #schema }

«Схема» — це визначення або опис чогось. Це не код, який його реалізує, а просто абстрактний опис.

#### API «схема» { #api-schema }

У цьому випадку, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) є специфікацією, яка визначає, як описати схему вашого API.

Це визначення схеми включає шляхи (paths) вашого API, можливі параметри, які вони приймають, тощо.

#### «Схема» даних { #data-schema }

Термін «схема» також може відноситися до форми деяких даних, наприклад, вмісту JSON.

У цьому випадку це означає атрибути JSON і типи даних, які вони мають, тощо.

#### OpenAPI і JSON Schema { #openapi-and-json-schema }

OpenAPI описує схему API для вашого API. І ця схема включає визначення (або «схеми») даних, що надсилаються та отримуються вашим API, за допомогою **JSON Schema**, стандарту для схем даних JSON.

#### Перевірте `openapi.json` { #check-the-openapi-json }

Якщо вас цікавить, як виглядає «сирий» OpenAPI schema, FastAPI автоматично генерує JSON (schema) з описами всього вашого API.

Ви можете побачити це напряму тут: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

Ви побачите JSON, що починається приблизно так:

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

#### Для чого потрібний OpenAPI { #what-is-openapi-for }

OpenAPI schema — це те, на чому працюють дві включені системи інтерактивної документації.

Також існують десятки альтернатив, і всі вони засновані на OpenAPI. Ви можете легко додати будь-яку з цих альтернатив до вашого застосунку, створеного з **FastAPI**.

Ви також можете використовувати його для автоматичної генерації коду для клієнтів, які взаємодіють з вашим API. Наприклад, для фронтенд-, мобільних або IoT-застосунків.

### Налаштуйте `entrypoint` застосунку в `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Ви можете налаштувати, де знаходиться ваш застосунок, у файлі `pyproject.toml`, приблизно так:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Цей `entrypoint` повідомить команді `fastapi`, що вона має імпортувати застосунок так:

```python
from main import app
```

Якщо структура вашого коду виглядала б так:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Тоді ви б задали `entrypoint` як:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

що було б еквівалентно:

```python
from backend.main import app
```

### `fastapi dev` із шляхом { #fastapi-dev-with-path }

Ви також можете передати шлях до файлу в команду `fastapi dev`, і вона вгадає обʼєкт FastAPI app, який слід використовувати:

```console
$ fastapi dev main.py
```

Але вам доведеться щоразу памʼятати передавати правильний шлях під час виклику команди `fastapi`.

Крім того, інші інструменти можуть не знайти його, наприклад [Розширення VS Code](../editor-support.md) або [FastAPI Cloud](https://fastapicloud.com), тому рекомендується використовувати `entrypoint` у `pyproject.toml`.

### Розгорніть ваш застосунок (необовʼязково) { #deploy-your-app-optional }

За бажанням ви можете розгорнути ваш FastAPI-застосунок у [FastAPI Cloud](https://fastapicloud.com), перейдіть і приєднайтеся до списку очікування, якщо ви цього ще не зробили. 🚀

Якщо у вас вже є обліковий запис **FastAPI Cloud** (ми запросили вас зі списку очікування 😉), ви можете розгорнути ваш застосунок однією командою.

Перед розгортанням переконайтеся, що ви увійшли:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Потім розгорніть ваш застосунок:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Ось і все! Тепер ви можете отримати доступ до вашого застосунку за цим URL. ✨

## Підібʼємо підсумки, крок за кроком { #recap-step-by-step }

### Крок 1: імпортуємо `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` — це клас у Python, який надає всю функціональність для вашого API.

/// note | Технічні деталі

`FastAPI` — це клас, який успадковується безпосередньо від `Starlette`.

Ви також можете використовувати всю функціональність [Starlette](https://www.starlette.dev/) у `FastAPI`.

///

### Крок 2: створюємо «екземпляр» `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Тут змінна `app` буде «екземпляром» класу `FastAPI`.

Це буде головна точка взаємодії для створення всього вашого API.

### Крок 3: створіть *операцію шляху* { #step-3-create-a-path-operation }

#### Шлях { #path }

«Шлях» тут означає останню частину URL, починаючи з першого `/`.

Отже, у такому URL, як:

```
https://example.com/items/foo
```

...шлях буде:

```
/items/foo
```

/// info

«Шлях» також зазвичай називають «ендпоінтом» або «маршрутом».

///

Під час створення API «шлях» є основним способом розділити «завдання» і «ресурси».

#### Операція { #operation }

«Операція» тут означає один з HTTP «методів».

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

У протоколі HTTP ви можете спілкуватися з кожним шляхом, використовуючи один (або кілька) з цих «методів».

---

Під час створення API зазвичай використовують ці конкретні HTTP методи, щоб виконати певну дію.

Зазвичай використовують:

* `POST`: щоб створити дані.
* `GET`: щоб читати дані.
* `PUT`: щоб оновити дані.
* `DELETE`: щоб видалити дані.

Отже, в OpenAPI кожен з HTTP методів називається «операцією».

Ми також будемо називати їх «**операціями**».

#### Визначте *декоратор операції шляху* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

Декоратор `@app.get("/")` повідомляє **FastAPI**, що функція одразу нижче відповідає за обробку запитів, які надходять до:

* шляху `/`
* використовуючи <dfn title="HTTP метод GET"><code>get</code> операція</dfn>

/// info | `@decorator` Інформація

Синтаксис `@something` у Python називається «декоратором».

Ви розташовуєте його над функцією. Як гарний декоративний капелюх (мабуть, звідти походить термін).

«Декоратор» бере функцію нижче і виконує з нею якусь дію.

У нашому випадку, цей декоратор повідомляє **FastAPI**, що функція нижче відповідає **шляху** `/` і **операції** `get`.

Це і є «**декоратор операції шляху**».

///

Можна також використовувати інші операції:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

І більш екзотичні:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip

Ви можете використовувати кожну операцію (HTTP-метод) як забажаєте.

**FastAPI** не навʼязує жодного конкретного значення.

Наведена тут інформація подана як настанова, а не вимога.

Наприклад, під час використання GraphQL ви зазвичай виконуєте всі дії, використовуючи лише `POST` операції.

///

### Крок 4: визначте **функцію операції шляху** { #step-4-define-the-path-operation-function }

Ось наша «**функція операції шляху**»:

* **шлях**: це `/`.
* **операція**: це `get`.
* **функція**: це функція нижче «декоратора» (нижче `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

Це функція Python.

**FastAPI** викликатиме її щоразу, коли отримає запит до URL «`/`», використовуючи операцію `GET`.

У цьому випадку це `async` функція.

---

Ви також можете визначити її як звичайну функцію замість `async def`:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note

Якщо ви не знаєте різницю, подивіться [Асинхронність: *«Поспішаєте?»*](../async.md#in-a-hurry).

///

### Крок 5: поверніть вміст { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

Ви можете повернути `dict`, `list`, а також окремі значення `str`, `int` тощо.

Також можна повернути моделі Pydantic (про це ви дізнаєтесь пізніше).

Існує багато інших обʼєктів і моделей, які будуть автоматично конвертовані в JSON (зокрема ORM тощо). Спробуйте використати свої улюблені — велика ймовірність, що вони вже підтримуються.

### Крок 6: розгорніть його { #step-6-deploy-it }

Розгорніть ваш застосунок у **[FastAPI Cloud](https://fastapicloud.com)** однією командою: `fastapi deploy`. 🎉

#### Про FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** створено тим самим автором і командою, які стоять за **FastAPI**.

Він спрощує процес **створення**, **розгортання** та **доступу** до API з мінімальними зусиллями.

Він переносить той самий **досвід розробника** зі створення застосунків на FastAPI на **розгортання** їх у хмарі. 🎉

FastAPI Cloud — основний спонсор і джерело фінансування для open source проєктів *FastAPI and friends*. ✨

#### Розгортання в інших хмарних провайдерах { #deploy-to-other-cloud-providers }

FastAPI — це open source і базується на стандартах. Ви можете розгортати FastAPI-застосунки у будь-якого хмарного провайдера на ваш вибір.

Дотримуйтеся інструкцій вашого хмарного провайдера, щоб розгорнути FastAPI-застосунки з їхньою допомогою. 🤓

## Підібʼємо підсумки { #recap }

* Імпортуйте `FastAPI`.
* Створіть екземпляр `app`.
* Напишіть **декоратор операції шляху**, використовуючи декоратори на кшталт `@app.get("/")`.
* Визначте **функцію операції шляху**; наприклад, `def root(): ...`.
* Запустіть сервер розробки командою `fastapi dev`.
* За бажанням розгорніть ваш застосунок за допомогою `fastapi deploy`.

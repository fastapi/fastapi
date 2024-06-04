# Getting Started

FastAPI is fast web-framework for building APIs. To get started, install FastAPI, set up your main file, run the development server, and view your API's documentation.

## Installing FastAPI

1. Open **Git Bash**. If you don't have it, download <a href="https://git-scm.com/downloads" class="external-link" target="_blank">the latest version of Git Bash.</a>
2. Enter `gh repo clone [your forked repository]`.
3. Open your coding edtor.
4. Create a new **Python workspace**.

## Setting up your main file
A main file (usually named `main.py`) tells your program how to work when launching it for the first time. A main FastAPI file should always contain:
* An `import` command
* A `fastapi` instance
* A path operation decorator
* A path operation function
* An output

To add these components to your file, follow the steps below:

---

### Step 1: Import `FastAPI`
`FastAPI` is a Python class that provides all the functionality for your API.

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

!!! note "Technical Details"
    `FastAPI` is a class that inherits directly from `Starlette`, meaning that you can use all the <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> functionality with `FastAPI` too.

---

### Step 2: Create `fastapi` instance
Define the main point of interaction of your API using the FastAPI class.

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Here the `app` variable is an "instance" of the class `FastAPI`.

---

### Step 3: Define path operation decorator
A **path operation** (also known as an **endpoint** or **route**) tells your API to perform various actions. A **path operation decorator** tells FastAPI that the function below it is in charge of handling requests that go to the path `/` using an HTTP method.

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

!!! info "Vocabulary"
    That `@something` syntax in Python is called a **decorator**. You put it on top of a function like a decorative hat. A **decorator** takes the function below and does something with it.

FastAPI comes with a variety of **HTTP methods**, or **operations**, including:

| HTTP Method | Purpose | Path Operator Decorator |
| --- | --- | --- |
| `POST` | Creates data. | `@app.post()` |
| `GET` | Reads data. | `@app.get()` |
| `PUT` | Updates data. | `@app.put()` |
| `DELETE` | Deletes data. | `@app.delete()` |

To see a full list of HTTP methods, see...

---

### Step 4: Define path operation function

A path operation function is simply the function below a path operation decorator.

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

The function below will be called by FastAPI whenever it receives a request to the URL "`/`" using a `GET` operation. The above function is an `async` function but normal functions defined with `def` work too.

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! info "Learn"
    To learn more about asynchronicity, visit the [Asynchronous code with `async` and `await` page(../async.md){.internal-link target=_blank}.

---

### Step 5: Return output

You can return arrays like `dict` or `list`, singular values like `str` or `int`, or even Pydantic models.

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Other objects and models are automatically converted to JSON (including ORMs). Try using your favourite one—it's most likely already supported by FastAPI.

## Running the development server
In Git Bash, run the live server using the command `fastapi dev`.

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

The output is a line with a URL of where your app is being served within your local machine.

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

To view the JSON response, open the URL <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

```JSON
{"message": "Hello World"}
```

## Interactive API docs

Every good API needs documentation. To view your API's documentation, head to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>. This automatic interactive documentation is provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

Alternatively, you can also view documentation provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> by heading to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

---

### OpenAPI and schemas

API **schemas** are important when creating reference documentation. Schemas are abstract definitions or descriptions of something. FastAPI automatically generates schemas with all your API using the <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> standard for defining APIs.

There are two main types of schemas FastAPI recognizes:
* **Data schema** - The shape of some data, like JSON content. In this case, it also refers to the JSON attributes and the data types they have.
* **OpenAPI and JSON schema** - OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using **JSON Schema**, the standard for JSON data schemas.

!!! info "Technical Details"
    The OpenAPI schema is what powers the two interactive documentation systems included. And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with FastAPI. You could also use it to generate code automatically for clients that communicate with your API (such as frontend, mobile or IoT applications).

If you're curious about how the raw OpenAPI schema looks like, head to <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

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

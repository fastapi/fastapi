# Getting Started

FastAPI's set up aspires to be as simple and intuitive as possible to help you get coding your API faster. This document provides an overview on how to install, set up, run the development server, and view your API's documentation.

## Installation
To install FastAPI, follow the steps below.

1. Open Git Bash. If you haven't downloaded it, visit the Git Bash website to find a download link.
2. Enter `gh repo clone tiangolo/fastapi`.

## Setting up a file
Every FastAPI file should have the following:
* An `import` command
* A `fastapi` instance
* A **path operation decorator**
* A **path operation function**
* An output

To see how to incorporate these components in your file, follow the steps below:

---

### Step 1 - Import `FastAPI`
`FastAPI` is a Python class that provides all the functionality for your API. 

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

!!! note "Technical Details"
    `FastAPI` is a class that inherits directly from `Starlette`, meaning that you can use all the <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> functionality with `FastAPI` too.

---

### Step 2 - Create a **`FastAPI` instance**
Define the main point of interaction to create your API. 

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Here the `app` variable is an "instance" of the class `FastAPI`.

---

### Step 3 - Create a **Path Operation Decorator**
A **path operation** (also known as an **endpoint** or **route**) tells your API to perform various actions. FastAPI already comes with a variety of **HTTP methods** (also known as **operations**) including (but not limited to):

| HTTP Method | Purpose | Path Operator Decorator |
| --- | --- | --- | 
| `POST` | Creates data. | `@app.post()` |
| `GET` | Reads data. | `@app.get()` |
| `PUT` | Updates data. | `@app.put()` |
| `DELETE` | Deletes data. | `@app.delete()` |

!!! tip
    The information here is presented as a guideline, not a requirement. You are free to use each operation as you wish, since **FastAPI** doesn't enforce any specific meaning. For example, when using GraphQL you normally perform all the actions using only `POST` operations. To see a list of more methods, visit...

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Breaking it down, the `@app.get("/")` tells FastAPI that the function below is in charge of handling requests that go to:

* The path `/`
* Using a <abbr title="an HTTP GET method"><code>get</code> operation</abbr>

!!! info "`@decorator` Info"
    That `@something` syntax in Python is called a **decorator**. You put it on top of a function like a decorative hat. A **decorator** takes the function below and does something with it. In our case, this decorator tells **FastAPI** that the function below corresponds to the **path** `/` with an **operation** `get`. It is the "**path operation decorator**".

---

### Step 4 - Define the **Path Operation Function**

A path operation function contains: 
* A **path** using `/`.
* An **operation** such as `get`.
* A **function** that sits below the "decorator" (below `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

This Python function will be called by **FastAPI** whenever it receives a request to the URL "`/`" using a `GET` operation. In this case, the above function is an `async` function but normal functions defined with `def` work too:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note
    To read more about asynchronicity, visit the [Asynchronous code with `async` and `await` page(../async.md#in-a-hurry){.internal-link target=_blank}.

### Step 5 - Return the output

You can return arrays like `dict` or `list`, singular values like `str` or `int`, or even Pydantic models. 

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Other objects and models are automatically converted to JSON (including ORMs). Try using your favourite one. It's most likely already supported by FastAPI.

## Example
To see how to run a Python file in FastAPI, see the example below:

Suppose you have the following Python file called `main.py`.

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

In Git Bash, run the live server.

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

The output would be a line that shows the URL where your app is being served within your local machine.

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

To view the JSON response, open your browser at <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

```JSON
{"message": "Hello World"}
```
---

### Interactive API docs

Every good API needs documentation. To view your API's documentation, head to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>. This automatic interactive documentation is provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

Alternatively, you can also head to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>. This alternative automatic documentation is provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## OpenAPI and schemas

**FastAPI** generates **schemas** with all your API using the **OpenAPI** standard for defining APIs. The OpenAPI schema is what powers the two interactive documentation systems included. And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with **FastAPI**. You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.

To understand the different types of schemas, see the table below:
| Schema type | Definition |
| --- | --- |
| Schema | An abstract definition or description of something (not coded). In this case, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> is a specification that dictates how to define a schema of your API. |
| Data schema | The shape of some data, like JSON content. In this case, it also refers to the JSON attributes and the data types they have. |
| OpenAPI and JSON schema | OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using **JSON Schema**, the standard for JSON data schemas. |

---

### Check `openapi.json`

If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API. You can see it directly at: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

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


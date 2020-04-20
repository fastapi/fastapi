# 第一步

最简单的 FastAPI 文件可能像下面这样：
The simplest FastAPI file could look like this:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

将其复制到 `main.py` 文件中。

运行实时服务器：

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

!!! note
    `uvicorn main:app` 命令含义如下:

    * `main`：`main.py` 文件（一个 Python "模块"）。
    * `app`：在 `main.py` 文件中通过 `app = FastAPI()` 创建的对象。
    * `--reload`：让服务器在更新代码后重新启动。仅在开发时使用该选项。
    

在输出中，有一行的信息会像下面这样：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```


该行显示了在本地计算机上为你的应用提供服务的URL。That line shows the URL where your app is being served, in your local machine.

### 查看

打开浏览器访问 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你将看到如下的 JSON 响应：

```JSON
{"message": "Hello World"}
```

### 交互式 API 文档

现在跳转到 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你将会看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档

那么现在前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你将会看到可选的自动生成文档 （由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供)：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** 使用定义 API 的 **OpenAPI** 标准将你的所有 API 转换成"模式"。

#### "模式"

"模式"是对事物的一种定义或描述。并非具体的实现代码，而只是抽象的描述。

#### API "模式"

在这种场景下，OpenAPI 是一种规定如何定义 API 模式的规范。

定义的 OpenAPI 模式将包括你的 API 路径，以及它们可能使用的参数等等。

#### 数据 "模式"

"模式"这个术语也可能指的是某些数据比如 JSON 的结构。

在这种情况下，它可以表示 JSON 的属性及其具有的数据类型，等等。

#### OpenAPI 和 JSON Schema

OpenAPI 为你的 API 定义了 API 的模式。并且该模式还包括了使用 JSON 数据模式标准 **JSON Schema** 的 API 发送接收数据的定义（或"模式"）。

#### 查看 `openapi.json`

如果你对原始的 OpenAPI 模式长什么样子感到好奇，其实它只是一个自动生成的包含了所有 API 描述的 JSON 文件。

你可以直接在: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 看到它。

它将显示以如下内容开头的 JSON：

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

#### OpenAPI 的用途

驱动内置的 2 个交互式文档系统的正是 OpenAPI 模式。

并且还有数十种替代方案，它们全部都基于 OpenAPI。你可以轻松地将这些替代方案中的任何一种添加到使用 **FastAPI** 构建的应用程序中。

你还可以使用它自动生成与你的 API 进行通信的客户端代码。例如 web 前端，移动端或物联网嵌入程序。

## 逐步回顾

### 步骤 1： 导入 `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` 是一个为你的 API 提供了所有功能的 Python 类。

!!! note "技术细节"
    `FastAPI` 直接从 `Starlette` 继承的类。

    你可以通过 `FastAPI` 使用所有的 Starlette 的功能。

### 步骤 2： 创建一个 `FastAPI` "实例"

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Here the `app` variable will be an "instance" of the class `FastAPI`.

This will be the main point of interaction to create all your API.

This `app` is the same one referred by `uvicorn` in the command:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

If you create your app like:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

And put it in a file `main.py`, then you would call `uvicorn` like:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Step 3: create a *path operation*

#### Path

"Path" here refers to the last part of the URL starting from the first `/`.

So, in a URL like:

```
https://example.com/items/foo
```

...the path would be:

```
/items/foo
```

!!! info
    A "path" is also commonly called an "endpoint" or a "route".

Building an API, the "path" is the main way to separate "concerns" and "resources".

#### Operation

"Operation" here refers to one of the HTTP "methods".

One of:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...and the more exotic ones:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

---

When building APIs, you normally use these specific HTTP methods to perform a specific action.

Normally you use:

* `POST`: to create data.
* `GET`: to read data.
* `PUT`: to update data.
* `DELETE`: to delete data.

So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "**operations**" too.

#### Define a *path operation function*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

The `@app.get("/")` tells **FastAPI** that the function right below is in charge of handling requests that go to:

* the path `/`
* using a <abbr title="an HTTP GET method"><code>get</code> operation</abbr>

!!! info "`@decorator` Info"
    That `@something` syntax in Python is called a "decorator".

    You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

    A "decorator" takes the function below and does something with it.

    In our case, this decorator tells **FastAPI** that the function below corresponds to the **path** `/` with an **operation** `get`.

    It is the "**path operation decorator**".

You can also use the other operations:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

And the more exotic ones:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    You are free to use each operation (HTTP method) as you wish.

    **FastAPI** doesn't enforce any specific meaning.

    The information here is presented as a guideline, not a requirement.

    For example, when using GraphQL you normally perform all the actions using only `post`.

### Step 4: define the **path operation function**

This is our "**path operation function**":

* **path**: is `/`.
* **operation**: is `get`.
* **function**: is the function below the "decorator" (below `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

This is a Python function.

It will be called by **FastAPI** whenever it receives a request to the URL "`/`" using `GET`.

In this case, it is an `async` function.

---

You could also define it as a normal function instead of `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note
    If you don't know the difference, check the [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Step 5: return the content

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

You can return a `dict`, `list`, singular values as `str`, `int`, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.

## Recap

* Import `FastAPI`.
* Create an `app` instance.
* Write a **path operation decorator** (like `@app.get("/")`).
* Write a **path operation function** (like `def root(): ...` above).
* Run the development server (like `uvicorn main:app --reload`).

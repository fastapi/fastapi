# 第一步

最简单的 FastAPI 文件大概长这样：

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

将这些代码复制到 `main.py` 文件中。

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
    `uvicorn main:app` 命令的含义如下:

    * `main`：`main.py` 文件（一个 Python“模块”）。
    * `app`：在 `main.py` 文件中通过 `app = FastAPI()` 创建的对象。
    * `--reload`：让服务器在更新代码后重新启动。仅在开发时使用该选项。

输出中会有一行像下面这样：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

这一行展示了你的应用在本地机器上提供服务的 URL。

### 看看效果

打开浏览器，访问 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你将看到如下的 JSON 响应：

```JSON
{"message": "Hello World"}
```

### 交互式 API 文档

跳转到 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你将会看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 另一种 API 文档

现在，再访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你会看到另一种自动生成的文档 （由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供)：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** 会根据用于定义 API 的 **OpenAPI** 标准为你所有的 API 生成相应“模式”（Schema）。

#### “模式”（Schema）

“模式”是指对事物的定义或者描述。它并非具体的实现代码，而只是抽象的描述。

#### API “模式”

就 API 这一领域而言，<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 给出了一种规定如何定义 API 模式的规范。

API 模式的定义包括 API 的路径以及其可能采用的参数等。

#### 数据“模式”

“模式”这个术语也可能指的是某些数据的“形状”，比如 JSON 的内容结构。

在这种情况下，“模式”会描述 JSON 的属性及其具有的数据类型，等等。

#### OpenAPI 和 JSON 模式

OpenAPI 为你的 API 定义 API 模式。该模式中包含了你的 API 发送和接收的数据的定义（或称为“模式”），这些定义通过 **JSON 模式**（即 JSON 数据模式的标准）所生成。

#### 看看 `openapi.json`

如果您想知道原始OpenAPI模式是什么样子，FastAPI会自动生成一个包含所有 API 的描述的 JSON（模式）。

你可以直接在 <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 看到它。

它将显示以如下内容开头的 JSON：

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

#### OpenAPI 的用途是什么

OpenAPI 模式是 FastAPI 所包含的两个交互文档系统的基础。

此外，还有数十种替代方案，它们全部都基于 OpenAPI。很容易就能将任何一种替代方案添加到使用 **FastAPI** 构建的应用之中。

你还可以使用它自动生成与你的 API 进行通信的客户端代码（例如前端、移动端、物联网应用）。

## 回顾刚才的每一步

### 步骤 1：导入 `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` 是一个为你的 API 提供了所有功能的 Python 类。

!!! note "技术细节"
    `FastAPI` 是直接从 `Starlette` 继承的类。

    你可以通过 `FastAPI` 使用所有的 <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> 的功能。

### 步骤 2：创建 `FastAPI`“实例”

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

这里的变量 `app` 会是 `FastAPI` 类的一个“实例”。

这个实例将是创建你所有 API 的主要交互对象。

此 `app` 与命令中 `uvicorn` 使用的 `app` 是同一对象：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果你像下面这样创建应用：

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

并将代码放入 `main.py` 文件中，然后你可以像下面这样运行 `uvicorn`：

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 步骤 3：创建 *路径操作*

#### 路径（Path）

这里的“路径”指的是 URL 中从第一个 `/` 起的后半部分。

所以，在一个这样的 URL 中：

```
https://example.com/items/foo
```

……路径会是：

```
/items/foo
```

!!! info
    “路径”也通常被称为“端点”（endpoint）或“路由”（route）。

开发 API 时，“路径”是用来分离“关注点”和“资源”的主要手段。

#### 操作（Operation）

这里的“操作”指的是 HTTP“方法”中的一种。

HTTP“方法”主要包括：

* `POST`
* `GET`
* `PUT`
* `DELETE`

……以及更少见的几种：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 协议中，你可以使用以上的其中一种（或多种）“方法”与每个路径进行通信。

---

在开发 API 时，你通常使用特定的 HTTP 方法去执行特定的行为。

通常会使用：

* `POST`：创建数据。
* `GET`：读取数据。
* `PUT`：更新数据。
* `DELETE`：删除数据。

因此，在 OpenAPI 中，每一个 HTTP 方法都被称为“操作”。

我们也打算称呼它们为“操作”。

#### 定义 *路径操作装饰器*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` 告诉 **FastAPI** 在它下方的函数负责处理满足如下要求的请求：

* 路径为 `/`
* 使用 <abbr title="HTTP GET 方法"><code>get</code> 操作</abbr>

!!! info "关于 `@decorator`"
    形如 `@something` 这样语法结构在 Python 中被称为“装饰器”（decorator）。

    装饰器会放在函数的上方，就像一顶漂亮的装饰帽一样（我猜测这个术语就是这么来的）。

    装饰器会接管位于其下方的函数并且用它来完成一些工作。

    在我们的例子中，这个装饰器会告诉 **FastAPI** 位于其下方的函数对应用于处理 使用 `get` **操作** 访问 **路径** `/` 的请求。

    这是一个“**路径操作装饰器**”。

也可以使用其他的操作：

* `@app.post()`
* `@app.put()`
* `@app.delete()`

以及更少见的：

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    您可以随意使用任何一个操作（HTTP方法）。

    **FastAPI** 没有强制要求操作有任何特定的含义。

    此处提供的信息仅作为指导，而不是要求。

    比如，在使用 GraphQL 时通常只使用 `POST` 操作来执行所有动作。

### 步骤 4：定义**路径操作函数**

这是我们的“**路径操作函数**”：

* **路径**：是 `/`。
* **操作**：是 `get`。
* **函数**：是位于“装饰器”下方的函数（位于 `@app.get("/")` 下方）。

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

这是一个 Python 函数。

每当 **FastAPI** 接收一个使用 `GET` 方法访问 URL“`/`”的请求时这个函数会被调用。

在这个例子中，它是一个 `async` 函数。

---

你也可以将其定义为常规函数而不使用 `async def`：

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note
    如果你不知道两者的区别，请查阅 [Async: *"In a hurry?"*](https://fastapi.tiangolo.com/async/#in-a-hurry){.internal-link target=_blank}。

### 步骤 5：返回内容

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

你可以返回一个 `dict`、`list`，亦或者是像 `str`、`int` 这样的单个值，等等。

你还可以返回 Pydantic 模型（这会在后面介绍）。

还有许多其他对象和模型会自动转换为 JSON （包括 ORM 对象等）。试试你最常用的那些对象和模型，很有可能已经支持了。

## 总结

* 导入 `FastAPI`。
* 创建 `app` 实例。
* 写上**路径操作装饰器**（例如 `@app.get("/")`）。
* 编写**路径操作函数**（例如上面的 `def root(): ...`）。
* 运行开发服务器（例如 `uvicorn main:app --reload`）。

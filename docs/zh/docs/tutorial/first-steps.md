# 第一步 { #first-steps }

最简单的 FastAPI 文件长这样：

{* ../../docs_src/first_steps/tutorial001_py310.py *}

复制到 `main.py` 里。

运行开发服务器：

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

输出里有一行像这样：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

这行告诉你本机服务的地址。

### 试一下 { #check-it }

打开浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

会看到这个 JSON 响应：

```JSON
{"message": "Hello World"}
```

### 交互式 API 文档 { #interactive-api-docs }

现在打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 另一个 API 文档 { #alternative-api-docs }

然后访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你会看到另一个自动文档（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

FastAPI 会用 OpenAPI 标准为你的 API 生成一个“schema”（模式）。

#### “Schema” { #schema }

“schema” 是某个东西的定义或描述。不是实现它的代码。只是抽象描述。

#### API 的 “schema” { #api-schema }

这里的 [OpenAPI](https://github.com/OAI/OpenAPI-Specification) 是一个规范。它规定怎么定义你的 API 的 schema。

这个 schema 会包含你的 API 的路径、可用的参数等。

#### 数据的 “schema” { #data-schema }

“schema” 也可以指数据的结构，比如 JSON 内容。

这时指的是 JSON 的属性、它们的数据类型等。

#### OpenAPI 和 JSON Schema { #openapi-and-json-schema }

OpenAPI 定义你的 API 的 schema。这个 schema 里包含数据的定义（也叫 “schemas”）。这些数据是 API 发送和接收的，使用 JSON Schema 这个 JSON 数据模式的标准。

#### 看看 `openapi.json` { #check-the-openapi-json }

想看原始的 OpenAPI schema 怎么样？FastAPI 会自动生成一个包含所有 API 描述的 JSON（schema）。

直接打开：[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)。

你会看到一个 JSON，开头像这样：

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

#### OpenAPI 有什么用 { #what-is-openapi-for }

这份 OpenAPI schema 驱动了上面两个交互式文档。

还有很多基于 OpenAPI 的替代方案。你可以很容易把它们加到用 FastAPI 构建的应用里。

你也可以用它自动生成客户端代码。比如前端、移动端或 IoT 应用。

### 在 `pyproject.toml` 里配置应用的 `entrypoint` { #configure-the-app-entrypoint-in-pyproject-toml }

你可以在 `pyproject.toml` 里配置应用的位置，像这样：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

这个 `entrypoint` 会告诉 `fastapi` 命令按下面方式 import 应用：

```python
from main import app
```

如果你的代码结构是这样：

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

那就把 `entrypoint` 设成：

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

等价于：

```python
from backend.main import app
```

### `fastapi dev` 传文件路径或用 `--entrypoint` 选项 { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

也可以把文件路径传给 `fastapi dev`。它会猜要用的 FastAPI app 对象：

```console
$ fastapi dev main.py
```

或者给 `fastapi dev` 传 `--entrypoint` 选项：

```console
$ fastapi dev --entrypoint main:app
```

但每次跑 `fastapi` 都得记得传对的路径或 entrypoint。

而且其它工具可能找不到它。比如 [VS Code 扩展](../editor-support.md) 或 [FastAPI Cloud](https://fastapicloud.com)。所以推荐在 `pyproject.toml` 里配置 `entrypoint`。

### 部署应用（可选） { #deploy-your-app-optional }

你也可以把 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。还没账号的话去加入候补名单。🚀

如果你已经有 **FastAPI Cloud** 账号（我们从候补名单邀请你了 😉），一条命令就能部署。

部署前，先登录：

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

然后部署应用：

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就这样！现在可以用这个地址访问你的应用了。✨

## 逐步回顾 { #recap-step-by-step }

### 步骤 1：导入 `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` 是个 Python 类。它提供你的 API 所需的一切功能。

/// note | 技术细节

`FastAPI` 直接继承自 `Starlette`。

在 `FastAPI` 里也能用所有的 [Starlette](https://www.starlette.dev/) 功能。

///

### 步骤 2：创建一个 `FastAPI` “实例” { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

这里的 `app` 变量就是 `FastAPI` 类的一个“实例”。

你用它来声明整个 API。

### 步骤 3：创建一个路径操作 { #step-3-create-a-path-operation }

#### 路径 { #path }

这里的 “Path” 指从第一个 `/` 开始的 URL 最后一段。

比如这个 URL：

```
https://example.com/items/foo
```

...它的路径是：

```
/items/foo
```

/// note | 注意

“path” 也常被叫做 “endpoint” 或 “route”。

///

做 API 时，path 是区分不同“职责”和“资源”的主要方式。

#### 操作 { #operation }

这里的 “Operation” 指一种 HTTP “方法”。

比如：

* `POST`
* `GET`
* `PUT`
* `DELETE`

...还有更少用的：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 里，你可以用这些“方法”跟每个路径通信。

---

写 API 时，通常用这些方法表示动作。

一般约定：

* `POST`：创建数据。
* `GET`：读取数据。
* `PUT`：更新数据。
* `DELETE`：删除数据。

所以在 OpenAPI 里，每个 HTTP 方法都叫一个 “operation”。

我们下面也叫它们“操作”。

#### 定义路径操作装饰器 { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")` 告诉 **FastAPI**，下面这个函数负责处理去到：

* 路径 `/`
* 使用一个 <dfn title="一个 HTTP GET 方法"><code>get</code> 操作</dfn>

/// note | `@decorator` 说明

在 Python 里，`@something` 这种语法叫 “decorator”。

你把它放在函数上面。像给函数戴了顶装饰用的帽子（大概名字就这么来的）。

“decorator” 会拿下面那个函数做点事。

这里，这个装饰器告诉 **FastAPI**：下面的函数对应 **路径** `/`，**操作** 是 `get`。

它就是“路径操作装饰器”。

///

你也可以用其他方法：

* `@app.post()`
* `@app.put()`
* `@app.delete()`

还有更少用的：

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | 提示

这些方法怎么用由你决定。

**FastAPI** 不强制语义。

这里说的是常见约定，不是硬性要求。

比如，用 GraphQL 时通常所有操作都用 `POST`。

///

### 步骤 4：定义路径操作函数 { #step-4-define-the-path-operation-function }

这是我们的“路径操作函数”：

* 路径：`/`。
* 操作：`get`。
* 函数：装饰器下面那个函数（在 `@app.get("/")` 下面）。

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

这是个 Python 函数。

**FastAPI** 收到发到 “`/`” 的 `GET` 请求时就会调用它。

这里它是个 `async` 函数。

---

你也可以不用 `async`，写成普通函数：

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | 注意

不清楚区别？看 [Async: *"In a hurry?"*](../async.md#in-a-hurry)。

///

### 步骤 5：返回内容 { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

可以返回 `dict`、`list`，或基础类型，比如 `str`、`int` 等。

也可以返回 Pydantic 模型（后面会讲）。

还有很多对象和模型会被自动转成 JSON（包括 ORMs 等）。用你喜欢的，基本都支持。

### 步骤 6：部署 { #step-6-deploy-it }

用一条命令把应用部署到 **[FastAPI Cloud](https://fastapicloud.com)**：`fastapi deploy`。🎉

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 出自 **FastAPI** 的作者和团队。

它让你几乎不费力地完成 API 的**构建**、**部署**和**访问**。

把用 FastAPI 写应用的**开发体验**，带到**部署**到云上的过程里。🎉

FastAPI Cloud 是 *FastAPI 及其好友* 开源项目的主要赞助方与资金提供者。✨

#### 部署到其他云厂商 { #deploy-to-other-cloud-providers }

FastAPI 是开源的，基于标准。你可以把 FastAPI 应用部署到任何云厂商。

按你的云厂商的文档部署 FastAPI 即可。🤓

## 回顾 { #recap }

* 导入 `FastAPI`。
* 创建一个 `app` 实例。
* 写一个**路径操作装饰器**，比如 `@app.get("/")`。
* 定义**路径操作函数**，比如 `def root(): ...`。
* 用命令 `fastapi dev` 跑开发服务器。
* 需要的话，用 `fastapi deploy` 部署。

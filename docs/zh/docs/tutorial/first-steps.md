# 第一步 { #first-steps }

最简单的 FastAPI 文件可能像下面这样：

{* ../../docs_src/first_steps/tutorial001_py39.py *}

将其复制到 `main.py` 文件中。

运行实时服务器：

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

在输出中，会有一行信息像下面这样：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

该行显示了你的应用在本机所提供服务的 URL 地址。

### 查看 { #check-it }

打开浏览器访问 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你将看到如下的 JSON 响应：

```JSON
{"message": "Hello World"}
```

### 交互式 API 文档 { #interactive-api-docs }

现在跳转到 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你将会看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档 { #alternative-api-docs }

现在，前往 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你将会看到可选的自动生成文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** 使用定义 API 的 **OpenAPI** 标准将你的所有 API 转换成「模式」。

#### 「模式」 { #schema }

「模式」是对事物的一种定义或描述。它并非具体的实现代码，而只是抽象的描述。

#### API「模式」 { #api-schema }

在这种场景下，<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 是一种规定如何定义 API 模式的规范。

「模式」的定义包括你的 API 路径，以及它们可能使用的参数等等。

#### 数据「模式」 { #data-schema }

「模式」这个术语也可能指的是某些数据比如 JSON 的结构。

在这种情况下，它可以表示 JSON 的属性及其具有的数据类型，等等。

#### OpenAPI 和 JSON Schema { #openapi-and-json-schema }

OpenAPI 为你的 API 定义 API 模式。该模式中包含了你的 API 发送和接收的数据的定义（或称为「模式」），这些定义通过 JSON 数据模式标准 **JSON Schema** 所生成。

#### 查看 `openapi.json` { #check-the-openapi-json }

如果你对原始的 OpenAPI 模式长什么样子感到好奇，FastAPI 自动生成了包含所有 API 描述的 JSON（模式）。

你可以直接在：<a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 看到它。

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

#### OpenAPI 的用途 { #what-is-openapi-for }

驱动 FastAPI 内置的 2 个交互式文档系统的正是 OpenAPI 模式。

并且还有数十种替代方案，它们全部都基于 OpenAPI。你可以轻松地将这些替代方案中的任何一种添加到使用 **FastAPI** 构建的应用程序中。

你还可以使用它自动生成与你的 API 进行通信的客户端代码。例如 web 前端，移动端或物联网嵌入程序。

### 部署你的应用（可选） { #deploy-your-app-optional }

你可以选择将 FastAPI 应用部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>，如果你还没加入等待列表，现在就去加入。🚀

如果你已经有 **FastAPI Cloud** 账号（我们已经从等待列表里邀请了你 😉），你可以用一条命令部署你的应用。

在部署之前，确保你已登录：

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

然后部署你的应用：

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就这样！现在你可以通过那个 URL 访问你的应用。✨

## 分步概括 { #recap-step-by-step }

### 步骤 1：导入 `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[1] *}

`FastAPI` 是一个为你的 API 提供了所有功能的 Python 类。

/// note | 技术细节

`FastAPI` 是直接从 `Starlette` 继承的类。

你可以通过 `FastAPI` 使用所有的 <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 的功能。

///

### 步骤 2：创建一个 `FastAPI`「实例」 { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[3] *}

这里的变量 `app` 会是 `FastAPI` 类的一个「实例」。

这个实例将是创建你所有 API 的主要交互对象。

### 步骤 3：创建一个*路径操作* { #step-3-create-a-path-operation }

#### 路径 { #path }

这里的「路径」指的是 URL 中从第一个 `/` 起的后半部分。

所以，在一个这样的 URL 中：

```
https://example.com/items/foo
```

...路径会是：

```
/items/foo
```

/// info | 信息

「路径」也通常被称为「端点」或「路由」。

///

开发 API 时，「路径」是用来分离「关注点」和「资源」的主要手段。

#### 操作 { #operation }

这里的「操作」指的是一种 HTTP「方法」。

下列之一：

* `POST`
* `GET`
* `PUT`
* `DELETE`

...以及更少见的几种：

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

在 HTTP 协议中，你可以使用以上的其中一种（或多种）「方法」与每个路径进行通信。

---

在开发 API 时，你通常使用特定的 HTTP 方法去执行特定的行为。

通常使用：

* `POST`：创建数据。
* `GET`：读取数据。
* `PUT`：更新数据。
* `DELETE`：删除数据。

因此，在 OpenAPI 中，每一个 HTTP 方法都被称为「操作」。

我们也打算称呼它们为「**操作**」。

#### 定义一个*路径操作装饰器* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[6] *}

`@app.get("/")` 告诉 **FastAPI** 在它下方的函数负责处理如下访问请求：

* 请求路径为 `/`
* 使用 <abbr title="an HTTP GET method - HTTP GET 方法"><code>get</code> 操作</abbr>

/// info | `@decorator` Info

`@something` 语法在 Python 中被称为「装饰器」。

像一顶漂亮的装饰帽一样，将它放在一个函数的上方（我猜测这个术语的命名就是这么来的）。

装饰器接收位于其下方的函数并且用它完成一些工作。

在我们的例子中，这个装饰器告诉 **FastAPI** 位于其下方的函数对应着**路径** `/` 加上 `get` **操作**。

它是一个「**路径操作装饰器**」。

///

你也可以使用其他的操作：

* `@app.post()`
* `@app.put()`
* `@app.delete()`

以及更少见的：

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | 提示

你可以随意使用任何一个操作（HTTP方法）。

**FastAPI** 没有强制要求操作有任何特定的含义。

此处提供的信息仅作为指导，而不是要求。

比如，当使用 GraphQL 时通常你所有的动作都通过 `POST` 一种方法执行。

///

### 步骤 4：定义**路径操作函数** { #step-4-define-the-path-operation-function }

这是我们的「**路径操作函数**」：

* **路径**：是 `/`。
* **操作**：是 `get`。
* **函数**：是位于「装饰器」下方的函数（位于 `@app.get("/")` 下方）。

{* ../../docs_src/first_steps/tutorial001_py39.py hl[7] *}

这是一个 Python 函数。

每当 **FastAPI** 接收一个使用 `GET` 方法访问 URL「`/`」的请求时这个函数会被调用。

在这个例子中，它是一个 `async` 函数。

---

你也可以将其定义为常规函数而不使用 `async def`:

{* ../../docs_src/first_steps/tutorial003_py39.py hl[7] *}

/// note | 注意

如果你不知道两者的区别，请查阅 [并发: *赶时间吗？*](../async.md#in-a-hurry){.internal-link target=_blank}。

///

### 步骤 5：返回内容 { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[8] *}

你可以返回一个 `dict`、`list`，像 `str`、`int` 一样的单个值，等等。

你还可以返回 Pydantic 模型（稍后你将了解更多）。

还有许多其他将会自动转换为 JSON 的对象和模型（包括 ORM 对象等）。尝试下使用你最喜欢的一种，它很有可能已经被支持。

### 步骤 6：部署 { #step-6-deploy-it }

用一条命令将你的应用部署到 **<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**：`fastapi deploy`。🎉

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** 由 **FastAPI** 背后的同一位作者和团队构建。

它简化了以最小的工作量来 **构建**、**部署** 和 **访问** API 的流程。

它将使用 FastAPI 构建应用时同样的 **开发者体验** 带到了将它们 **部署** 到云端的过程。🎉

FastAPI Cloud 是 *FastAPI and friends* 开源项目的主要赞助方和资金提供者。✨

#### 部署到其他云服务商 { #deploy-to-other-cloud-providers }

FastAPI 是开源的，并基于标准。你可以将 FastAPI 应用部署到你选择的任何云服务商。

按照你的云服务商提供的指南，将 FastAPI 应用部署到他们的平台上。🤓

## 总结 { #recap }

* 导入 `FastAPI`。
* 创建一个 `app` 实例。
* 编写一个**路径操作装饰器**，如 `@app.get("/")`。
* 定义一个**路径操作函数**，如 `def root(): ...`。
* 使用命令 `fastapi dev` 运行开发服务器。
* 可选地使用 `fastapi deploy` 部署你的应用。

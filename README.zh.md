<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 框架，高性能、易学习、快速编码、生产就绪</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**文档**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**源代码**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI 是一个现代、快速（高性能）的 Python Web 框架，基于标准 Python 类型提示构建 API。

核心特性：

* **快速**：非常高的性能，可与 **NodeJS** 和 **Go** 媲美（得益于 Starlette 和 Pydantic）。[Python 最快的框架之一](#performance)。
* **编码高效**：开发特性的速度提升约 200% 到 300%。*
* **更少 Bug**：减少约 40% 的人为（开发者）错误。*
* **直观**：出色的编辑器支持。随处可见的<dfn title="也称为自动补全、智能感知">代码补全</dfn>。更少的调试时间。
* **简单**：设计为易于使用和学习。花更少时间阅读文档。
* **精简**：最小化代码重复。每个参数声明即包含多个功能。更少的 Bug。
* **健壮**：生成生产就绪的代码。带有自动交互式文档。
* **基于标准**：基于（并完全兼容）API 的开放标准：[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（以前称为 Swagger）和 [JSON Schema](https://json-schema.org/)。

<small>* 基于内部开发团队构建生产应用程序的测试估算。</small>

## 赞助商

<!-- sponsors -->
### Keystone 赞助商

<a href="https://fastapicloud.com" target="_blank" title="FastAPI Cloud. 由 FastAPI 团队打造。你写代码，我们上云。"><img src="https://fastapi.tiangolo.com/img/sponsors/fastapicloud.png"></a>

### Gold 赞助商

<a href="https://blockbee.io?ref=fastapi" target="_blank" title="BlockBee 加密货币支付网关"><img src="https://fastapi.tiangolo.com/img/sponsors/blockbee.png"></a>
<a href="https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=main-badge" target="_blank" title="Scalar: 基于 Swagger/OpenAPI 的精美开源 API 参考文档"><img src="https://fastapi.tiangolo.com/img/sponsors/scalar.svg"></a>
<a href="https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=mainbadge" target="_blank" title="为你的 B2B 产品提供认证和用户管理"><img src="https://fastapi.tiangolo.com/img/sponsors/propelauth.png"></a>
<a href="https://liblab.com?utm_source=fastapi" target="_blank" title="liblab - 从 FastAPI 生成 SDK"><img src="https://fastapi.tiangolo.com/img/sponsors/liblab.png"></a>
<a href="https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi" target="_blank" title="在 Render 上部署和扩展任何全栈 Web 应用。专注于构建应用而非基础设施。"><img src="https://fastapi.tiangolo.com/img/sponsors/render.svg"></a>
<a href="https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=badge&utm_campaign=fastapi" target="_blank" title="使用 CodeRabbit 将代码审查时间和 Bug 减半"><img src="https://fastapi.tiangolo.com/img/sponsors/coderabbit.png"></a>
<a href="https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source" target="_blank" title="零售账户关联的黄金标准"><img src="https://fastapi.tiangolo.com/img/sponsors/subtotal.svg"></a>
<a href="https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi" target="_blank" title="以初创公司速度部署企业级应用"><img src="https://fastapi.tiangolo.com/img/sponsors/railway.png"></a>
<a href="https://serpapi.com/?utm_source=fastapi_website" target="_blank" title="SerpApi: 网页搜索 API"><img src="https://fastapi.tiangolo.com/img/sponsors/serpapi.png"></a>
<a href="https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page" target="_blank" title="Greptile: AI 代码审查工具"><img src="https://fastapi.tiangolo.com/img/sponsors/greptile.png"></a>

### Silver 赞助商

<a href="https://databento.com/?utm_source=fastapi&utm_medium=sponsor&utm_content=display" target="_blank" title="按量付费的市场数据"><img src="https://fastapi.tiangolo.com/img/sponsors/databento.svg"></a>
<a href="https://www.svix.com/" target="_blank" title="Svix - Webhooks 即服务"><img src="https://fastapi.tiangolo.com/img/sponsors/svix.svg"></a>
<a href="https://www.stainlessapi.com/?utm_source=fastapi&utm_medium=referral" target="_blank" title="Stainless | 生成最佳 SDK"><img src="https://fastapi.tiangolo.com/img/sponsors/stainless.png"></a>
<a href="https://www.permit.io/blog/implement-authorization-in-fastapi?utm_source=github&utm_medium=referral&utm_campaign=fastapi" target="_blank" title="FastAPI 的细粒度授权"><img src="https://fastapi.tiangolo.com/img/sponsors/permit.png"></a>
<a href="https://www.interviewpal.com/?utm_source=fastapi&utm_medium=open-source&utm_campaign=dev-hiring" target="_blank" title="InterviewPal - 工程师和开发者的 AI 面试教练"><img src="https://fastapi.tiangolo.com/img/sponsors/interviewpal.png"></a>
<a href="https://dribia.com/en/" target="_blank" title="Dribia - 触手可及的数据科学"><img src="https://fastapi.tiangolo.com/img/sponsors/dribia.png"></a>
<a href="https://talordata.com/?campaignid=oh5dVZ3Zc3YGiAI2&utm_source=fastapi&utm_term=fastapi" target="_blank" title="TalorData SERP API - 多引擎搜索结果数据"><img src="https://fastapi.tiangolo.com/img/sponsors/talordata.png"></a>

<!-- /sponsors -->

[其他赞助商](https://fastapi.tiangolo.com/fastapi-people/#sponsors)

## 业界评价

<div class="only-github" markdown="1">

"_[...] 我最近大量使用 **FastAPI**。[...] 我实际上打算把它用在我们 **Microsoft** 所有团队的 **机器学习服务** 上。其中一些正在集成到 **Windows** 核心产品和一些 **Office** 产品中。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_我们采用 **FastAPI** 库来启动一个 **REST** 服务器，用于查询 **预测结果**。[为 Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** 很高兴宣布我们的 **危机管理** 编排框架开源发布：**Dispatch**！[使用 **FastAPI** 构建]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_如果有人想构建生产级 Python API，我强烈推荐 **FastAPI**。它**设计精美**、**简单易用**且**高度可扩展**，已成为我们 API 优先开发策略的**关键组件**，驱动着许多自动化和服务，比如我们的虚拟 TAC 工程师。_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

</div>

## FastAPI Conf

[**FastAPI Conf '26**](https://fastapiconf.com) 将于 **2026 年 10 月 28 日** 在荷兰**阿姆斯特丹**举行。关于 FastAPI 的一切，从源头出发。🎤

<a class="fastapi-feature-banner" href="https://fastapiconf.com"><img src="https://fastapi.tiangolo.com/img/fastapi-conf.jpeg" alt="FastAPI Conf '26 - October 28, 2026 - Amsterdam, NL"></a>

## FastAPI 微纪录片

2025 年底发布的 [FastAPI 微纪录片](https://www.youtube.com/watch?v=mpR8ngthqiE)，可在线观看：

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**，CLI 界的 FastAPI

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你正在构建一个在终端中使用的 <abbr title="命令行界面">CLI</abbr> 应用而非 Web API，请查看 [**Typer**](https://typer.tiangolo.com/)。

**Typer** 是 FastAPI 的小兄弟。它的目标是成为 **CLI 界的 FastAPI**。⌨️ 🚀

## 环境要求

FastAPI 站在巨人的肩膀上：

* [Starlette](https://www.starlette.dev/) 负责 Web 部分。
* [Pydantic](https://docs.pydantic.dev/) 负责数据部分。

## 安装

创建并激活[虚拟环境](https://fastapi.tiangolo.com/virtual-environments/)，然后安装 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注意**：确保将 `"fastapi[standard]"` 放在引号中，以确保在所有终端中都能正常工作。

## 示例

### 创建应用

创建一个 `main.py` 文件，内容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或使用 <code>async def</code>...</summary>

如果你的代码使用 `async` / `await`，请使用 `async def`：

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**注意**：

如果你不确定，请查看文档中[关于 `async` 和 `await` 的快速入门章节](https://fastapi.tiangolo.com/async/#in-a-hurry)。

</details>

### 运行

使用以下命令启动服务器：

<div class="termy">

```console
$ fastapi dev

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>关于 <code>fastapi dev</code> 命令...</summary>

`fastapi dev` 命令会自动读取你的 `main.py` 文件，检测其中的 **FastAPI** 应用，然后使用 [Uvicorn](https://www.uvicorn.dev) 启动服务器。

默认情况下，`fastapi dev` 会启动自动重载以便本地开发。

更多信息请参阅 [FastAPI CLI 文档](https://fastapi.tiangolo.com/fastapi-cli/)。

</details>

### 验证

在浏览器中打开 [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)。

你会看到如下 JSON 响应：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已经创建了一个 API，它：

* 在 _路径_ `/` 和 `/items/{item_id}` 接收 HTTP 请求。
* 两个 _路径_ 都使用 `GET` <em>操作</em>（也称为 HTTP _方法_）。
* _路径_ `/items/{item_id}` 有一个 _路径参数_ `item_id`，应为 `int` 类型。
* _路径_ `/items/{item_id}` 有一个可选的 `str` 类型 _查询参数_ `q`。

### 交互式 API 文档

现在访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你将看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 备选 API 文档

现在访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你将看到备选的自动生成文档（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 进阶示例

现在修改 `main.py` 文件，接收来自 `PUT` 请求的请求体。

使用标准 Python 类型声明请求体，感谢 Pydantic。

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` 服务器应该会自动重载。

### 交互式 API 文档升级

现在访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

* 交互式 API 文档将自动更新，包含新的请求体：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 点击 "Try it out" 按钮，你可以填写参数并直接与 API 交互：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然后点击 "Execute" 按钮，用户界面将与你的 API 通信，发送参数，获取结果并显示在屏幕上：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 备选 API 文档升级

现在访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

* 备选文档也会反映新的查询参数和请求体：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 总结

总的来说，你只需要**一次性**将参数、请求体等的类型声明为函数参数。

你使用的是标准的现代 Python 类型。

你不需要学习新的语法、特定库的方法或类等。

就是标准的 **Python**。

例如，对于 `int`：

```Python
item_id: int
```

或者对于更复杂的 `Item` 模型：

```Python
item: Item
```

...仅通过这个声明，你就获得了：

* 编辑器支持，包括：
    * 代码补全。
    * 类型检查。
* 数据验证：
    * 数据无效时自动给出清晰的错误提示。
    * 即使对深层嵌套的 JSON 对象也能进行验证。
* 输入数据的<dfn title="也称为：序列化、解析、编组">转换</dfn>：从网络数据到 Python 数据类型。读取来源包括：
    * JSON。
    * 路径参数。
    * 查询参数。
    * Cookies。
    * 请求头。
    * 表单。
    * 文件。
* 输出数据的<dfn title="也称为：序列化、解析、编组">转换</dfn>：从 Python 数据类型到网络数据（如 JSON）：
    * 转换 Python 类型（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 对象。
    * `UUID` 对象。
    * 数据库模型。
    * ...等等更多。
* 自动生成交互式 API 文档，包含 2 种备选用户界面：
    * Swagger UI。
    * ReDoc。

---

回到之前的代码示例，**FastAPI** 将：

* 验证 `GET` 和 `PUT` 请求的路径中是否存在 `item_id`。
* 验证 `GET` 和 `PUT` 请求的 `item_id` 是否为 `int` 类型。
    * 如果不是，客户端将看到一个有用的、清晰的错误信息。
* 对于 `GET` 请求，检查是否存在名为 `q` 的可选查询参数（例如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * 因为 `q` 参数声明为 `= None`，所以它是可选的。
    * 如果没有 `None`，它将是必需的（就像 `PUT` 请求中的请求体一样）。
* 对于 `PUT` 请求到 `/items/{item_id}`，将请求体读取为 JSON：
    * 检查它是否有必需的属性 `name`，应为 `str` 类型。
    * 检查它是否有必需的属性 `price`，应为 `float` 类型。
    * 检查它是否有可选属性 `is_offer`，如果存在则应为 `bool` 类型。
    * 所有这些同样适用于深层嵌套的 JSON 对象。
* 自动进行 JSON 的序列化和反序列化。
* 使用 OpenAPI 记录一切，可用于：
    * 交互式文档系统。
    * 多种语言的自动客户端代码生成系统。
* 直接提供 2 个交互式文档 Web 界面。

---

我们只是浅尝辄止，但你已经了解了它的工作方式。

尝试修改这行：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...从：

```Python
        ... "item_name": item.name ...
```

...改为：

```Python
        ... "item_price": item.price ...
```

...然后看看你的编辑器如何自动补全属性并知道它们的类型：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

有关包含更多功能的完整示例，请参阅 <a href="https://fastapi.tiangolo.com/tutorial/">教程 - 用户指南</a>。

**剧透警告**：教程 - 用户指南包括：

* 从其他不同位置声明**参数**，如：**请求头**、**Cookies**、**表单字段**和**文件**。
* 如何设置**验证约束**，如 `maximum_length` 或 `regex`。
* 一个非常强大且易用的 **<dfn title="也称为组件、资源、提供者、服务、可注入对象">依赖注入</dfn>** 系统。
* 安全与认证，包括 **OAuth2** 配合 **JWT tokens** 和 **HTTP Basic** 认证。
* 更高级（但同样简单）的声明**深层嵌套 JSON 模型**的技术（感谢 Pydantic）。
* 与 [Strawberry](https://strawberry.rocks) 和其他库的 **GraphQL** 集成。
* 许多额外特性（感谢 Starlette），如：
    * **WebSockets**
    * 基于 HTTPX 和 `pytest` 的极其简单的测试
    * **CORS**
    * **Cookie Sessions**
    * ...更多。

### 部署你的应用（可选）

你可以选择将 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)，如果还没有的话赶紧加入等待列表。🚀

如果你已经有一个 **FastAPI Cloud** 账号（我们从等待列表中邀请你了 😉），你可以用一条命令部署你的应用。

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 准备好鸡！你的应用已就绪：https://myapp.fastapicloud.dev
```

</div>

就这些！现在你可以通过该 URL 访问你的应用了。✨

#### 关于 FastAPI Cloud

**[FastAPI Cloud](https://fastapicloud.com)** 由 **FastAPI** 的原作者和团队打造。

它简化了以最小工作量**构建**、**部署**和**访问** API 的过程。

它将 FastAPI 构建应用的**开发者体验**同样带到了将它们**部署**到云端的环节。🎉

FastAPI Cloud 是 *FastAPI 及周边* 开源项目的主要赞助商和资金来源。✨

#### 部署到其他云服务商

FastAPI 是开源的，基于标准。你可以将 FastAPI 应用部署到你选择的任何云服务商。

按照你所用云服务商的指南来部署 FastAPI 应用。🤓

## 性能

独立的 TechEmpower 基准测试显示，在 Uvicorn 下运行的 **FastAPI** 应用是[目前最快的 Python 框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)，仅次于 Starlette 和 Uvicorn 本身（FastAPI 内部使用）。(*)

了解更多，请参阅 [Benchmarks](https://fastapi.tiangolo.com/benchmarks/) 章节。

## 依赖

FastAPI 依赖 Pydantic 和 Starlette。

### `standard` 依赖

当你使用 `pip install "fastapi[standard]"` 安装 FastAPI 时，会附带 `standard` 组的可选依赖：

由 Pydantic 使用：

* [`email-validator`](https://github.com/JoshData/python-email-validator) - 用于邮箱验证。

由 Starlette 使用：

* [`httpx`](https://www.python-httpx.org) - 如果你想使用 `TestClient` 则需要。
* [`jinja2`](https://jinja.palletsprojects.com) - 如果你想使用默认模板配置则需要。
* [`python-multipart`](https://github.com/Kludex/python-multipart) - 如果你想支持表单<dfn title="将 HTTP 请求中的字符串转换为 Python 数据">"解析"</dfn>（通过 `request.form()`）则需要。

由 FastAPI 使用：

* [`uvicorn`](https://www.uvicorn.dev) - 用于加载和提供应用的服务器。包括 `uvicorn[standard]`，其中包含高性能服务所需的一些依赖（例如 `uvloop`）。
* `fastapi-cli[standard]` - 提供 `fastapi` 命令。
    * 其中包括 `fastapi-cloud-cli`，允许你将 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。

### 不包含 `standard` 依赖

如果你不想要 `standard` 可选依赖，可以改用 `pip install fastapi` 而不是 `pip install "fastapi[standard]"`。

### 不包含 `fastapi-cloud-cli`

如果你想安装 FastAPI 的标准依赖但不包含 `fastapi-cloud-cli`，可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"`。

### 额外的可选依赖

还有一些你可能想安装的额外依赖。

额外的可选 Pydantic 依赖：

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - 用于设置管理。
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - 用于 Pydantic 的额外类型。

额外的可选 FastAPI 依赖：

* [`orjson`](https://github.com/ijl/orjson) - 如果你想使用 `ORJSONResponse` 则需要。
* [`ujson`](https://github.com/esnme/ultrajson) - 如果你想使用 `UJSONResponse` 则需要。

## 许可证

本项目基于 MIT 许可证条款授权。

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/zh"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 框架，高性能，易于学习，高效编码，生产可用</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**文档**： <a href="https://fastapi.tiangolo.com/zh" target="_blank">https://fastapi.tiangolo.com</a>

**源码**： <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 并基于标准的 Python 类型提示。

关键特性:

* **快速**：可与 **NodeJS** 和 **Go** 并肩的极高性能（归功于 Starlette 和 Pydantic）。[最快的 Python 框架之一](#performance)。
* **高效编码**：提高功能开发速度约 200％ 至 300％。*
* **更少 bug**：减少约 40％ 的人为（开发者）导致错误。*
* **直观**：极佳的编辑器支持。处处皆可<abbr title="也被称为自动完成、自动补全、IntelliSense">自动补全</abbr>，减少调试时间。
* **简单**：设计的易于使用和学习，阅读文档的时间更短。
* **简短**：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少。
* **健壮**：生产可用级别的代码。还有自动生成的交互式文档。
* **标准化**：基于（并完全兼容）API 的相关开放标准：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>（以前被称为 Swagger）和 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>。

<small>* 根据对某个构建线上应用的内部开发团队所进行的测试估算得出。</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold and Silver Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/zh/fastapi-people/#sponsors" class="external-link" target="_blank">其他赞助商</a>

## 评价 { #opinions }

「_[...] 最近我一直在使用 **FastAPI**。[...] 实际上我正在计划将其用于我所在的**微软**团队的所有**机器学习服务**。其中一些服务正被集成进核心 **Windows** 产品和一些 **Office** 产品。_」

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>微软</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

「_我们选择了 **FastAPI** 来创建用于获取**预测结果**的 **REST** 服务。[用于 Ludwig]_」

<div style="text-align: right; margin-right: 10%;">Piero Molino，Yaroslav Dudin 和 Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

「_**Netflix** 非常高兴地宣布，正式开源我们的**危机管理**编排框架：**Dispatch**！[使用 **FastAPI** 构建]_」

<div style="text-align: right; margin-right: 10%;">Kevin Glisson，Marc Vilanova，Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

「_**FastAPI** 让我兴奋的欣喜若狂。它太棒了！_」

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> 播客主持人</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

「_老实说，你的作品看起来非常可靠和优美。在很多方面，这就是我想让 **Hug** 成为的样子 - 看到有人实现了它真的很鼓舞人心。_」

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> 作者</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

「_如果你正打算学习一个**现代框架**用来构建 REST API，来看下 **FastAPI** [...] 它快速、易用且易于学习 [...]_」

「_我们已经将 **API** 服务切换到了 **FastAPI** [...] 我认为你会喜欢它的 [...]_」

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> 创始人 - <a href="https://spacy.io" target="_blank">spaCy</a> 作者</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

「_如果有人想构建生产级的 Python API，我强烈推荐 **FastAPI**。它**设计优美**、**使用简单**且**高度可扩展**，已经成为我们 API-first 开发策略中的**关键组件**，并推动了许多自动化与服务，例如我们的 Virtual TAC Engineer。_」

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI 迷你纪录片 { #fastapi-mini-documentary }

在 2025 年末发布了一部 <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI 迷你纪录片</a>，你可以在线观看：

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**，命令行中的 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你正在开发一个在终端中运行的<abbr title="Command Line Interface">CLI</abbr> 应用而不是 web API，不妨试下 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>。

**Typer** 是 FastAPI 的小同胞。它想要成为**命令行中的 FastAPI**。 ⌨️ 🚀

## 依赖 { #requirements }

FastAPI 站在以下巨人的肩膀之上：

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> 负责 web 部分。
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 负责数据部分。

## 安装 { #installation }

创建并激活一个<a href="https://fastapi.tiangolo.com/zh/virtual-environments/" class="external-link" target="_blank">虚拟环境</a>，然后安装 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注意**：请确保将 `"fastapi[standard]"` 放在引号中，以确保它在所有终端中都能正常工作。

## 示例 { #example }

### 创建 { #create-it }

创建一个 `main.py` 文件并写入以下内容:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或者使用 <code>async def</code>...</summary>

如果你的代码里会出现 `async` / `await`，请使用 `async def`：

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**注意**:

如果你不知道是否会用到，可以查看文档的 _"In a hurry?"_ 章节中 <a href="https://fastapi.tiangolo.com/zh/async/#in-a-hurry" target="_blank">关于 `async` 和 `await` 的部分</a>。

</details>

### 运行 { #run-it }

通过以下命令运行服务器：

<div class="termy">

```console
$ fastapi dev main.py

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
<summary>关于 <code>fastapi dev main.py</code> 命令...</summary>

`fastapi dev` 命令会读取你的 `main.py` 文件，检测其中的 **FastAPI** app，并使用 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> 启动一个服务器。

默认情况下，`fastapi dev` 会启用自动重载，以便于本地开发。

你可以在 <a href="https://fastapi.tiangolo.com/zh/fastapi-cli/" target="_blank">FastAPI CLI 文档</a>中了解更多。

</details>

### 检查 { #check-it }

使用浏览器访问 <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>。

你将会看到如下 JSON 响应：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已经创建了一个具有以下功能的 API：

* 通过 _路径_ `/` 和 `/items/{item_id}` 接受 HTTP 请求。
* 以上 _路径_ 都接受 `GET` <em>操作</em>（也被称为 HTTP _方法_）。
* `/items/{item_id}` _路径_ 有一个 _路径参数_ `item_id` 并且应该为 `int` 类型。
* `/items/{item_id}` _路径_ 有一个可选的 `str` 类型的 _查询参数_ `q`。

### 交互式 API 文档 { #interactive-api-docs }

现在访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 可选的 API 文档 { #alternative-api-docs }

现在访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

你会看到另一个自动生成的文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 示例升级 { #example-upgrade }

现在修改 `main.py` 文件来从 `PUT` 请求中接收请求体。

我们借助 Pydantic 来使用标准的 Python 类型声明请求体。

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` 服务器应当会自动重载。

### 交互式 API 文档升级 { #interactive-api-docs-upgrade }

访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

* 交互式 API 文档将会自动更新，并加入新的请求体：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 点击「Try it out」按钮，之后你可以填写参数并直接与 API 交互：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然后点击「Execute」按钮，用户界面将会和你的 API 进行通信，发送参数，获取结果并在屏幕上展示：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 可选文档升级 { #alternative-api-docs-upgrade }

访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

* 可选文档同样会体现新加入的查询参数和请求体：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 总结 { #recap }

总的来说，你就像声明函数的参数类型一样只声明了**一次**参数、请求体等的类型。

你使用了标准的现代 Python 类型来完成声明。

你不需要去学习新的语法、了解特定库的方法或类，等等。

只需要使用标准的 **Python**。

举个例子，比如声明 `int` 类型：

```Python
item_id: int
```

或者一个更复杂的 `Item` 模型：

```Python
item: Item
```

......在进行一次声明之后，你将获得：

* 编辑器支持，包括：
    * 自动补全。
    * 类型检查。
* 数据校验：
    * 在校验失败时自动生成清晰的错误信息。
    * 对多层嵌套的 JSON 对象依然执行校验。
* <abbr title="also known as: serialization, parsing, marshalling">转换</abbr> 来自网络的输入数据为 Python 数据和类型。读取的数据包括：
    * JSON。
    * 路径参数。
    * 查询参数。
    * Cookies。
    * 请求头。
    * 表单。
    * 文件。
* <abbr title="also known as: serialization, parsing, marshalling">转换</abbr> 输出数据：将 Python 数据和类型转换为网络数据（JSON）：
    * 转换 Python 类型（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 对象。
    * `UUID` 对象。
    * 数据库模型。
    * ......以及更多其他类型。
* 自动生成的交互式 API 文档，包括两种可选的用户界面：
    * Swagger UI。
    * ReDoc。

---

回到前面的代码示例，**FastAPI** 将会：

* 校验 `GET` 和 `PUT` 请求的路径中是否含有 `item_id`。
* 校验 `GET` 和 `PUT` 请求中的 `item_id` 是否为 `int` 类型。
    * 如果不是，客户端将会收到清晰有用的错误信息。
* 检查 `GET` 请求中是否有命名为 `q` 的可选查询参数（比如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * 因为 `q` 被声明为 `= None`，所以它是可选的。
    * 如果没有 `None` 它将会是必需的（如 `PUT` 场景下的请求体）。
* 对于访问 `/items/{item_id}` 的 `PUT` 请求，将请求体读取为 JSON：
    * 检查是否有必需属性 `name` 并且值为 `str` 类型。
    * 检查是否有必需属性 `price` 并且值必须为 `float` 类型。
    * 检查是否有可选属性 `is_offer`，如果有的话值应该为 `bool` 类型。
    * 以上过程对于多层嵌套的 JSON 对象同样也会执行。
* 自动在 JSON 之间进行转换。
* 通过 OpenAPI 文档来记录所有内容，可被用于：
    * 交互式文档系统。
    * 许多编程语言的客户端代码自动生成系统。
* 直接提供 2 种交互式文档 web 界面。

---

虽然我们才刚刚开始，但其实你已经了解了这一切是如何工作的。

尝试更改下面这行代码：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

......从：

```Python
        ... "item_name": item.name ...
```

......改为：

```Python
        ... "item_price": item.price ...
```

......注意观察编辑器是如何自动补全属性并且还知道它们的类型：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

想看一个包含更多特性的更完整示例，请参阅 <a href="https://fastapi.tiangolo.com/zh/tutorial/">教程 - 用户指南</a>。

**剧透警告**：教程 - 用户指南中的内容包括：

* 从其他不同位置声明**参数**，如：**请求头**、**cookies**、**form 表单字段**以及**文件**。
* 如何设置**校验约束**如 `maximum_length` 或者 `regex`。
* 一个强大并易于使用的 **<abbr title="also known as components, resources, providers, services, injectables">依赖注入</abbr>** 系统。
* 安全性和身份验证，包括通过 **JWT tokens** 和 **HTTP Basic** 认证来支持 **OAuth2**。
* 更进阶（但同样简单）的技巧来声明 **多层嵌套 JSON 模型**（借助 Pydantic）。
* 使用 <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> 与其他库的 **GraphQL** 集成。
* 许多额外功能（归功于 Starlette）比如：
    * **WebSockets**
    * 基于 HTTPX 和 `pytest` 的极其简单的测试
    * **CORS**
    * **Cookie Sessions**
    * ......以及更多

### 部署你的应用（可选） { #deploy-your-app-optional }

你也可以选择将你的 FastAPI 应用部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>；如果你还没有加入等待列表，可以去加入。 🚀

如果你已经有 **FastAPI Cloud** 账号（我们从等待列表邀请了你 😉），你可以用一个命令部署你的应用。

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

就这样！现在你可以通过该 URL 访问你的应用。 ✨

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** 由 **FastAPI** 背后的同一位作者与团队构建。

它将 **构建**、**部署** 与 **访问** API 的过程简化到最小的工作量。

它把用 FastAPI 构建应用的同样 **开发者体验** 带到了将它们 **部署** 到云端。 🎉

FastAPI Cloud 是 *FastAPI and friends* 开源项目的主要赞助方与资金提供方。 ✨

#### 部署到其他云服务提供商 { #deploy-to-other-cloud-providers }

FastAPI 是开源的并且基于标准。你可以将 FastAPI 应用部署到你选择的任何云服务提供商。

按照你的云服务提供商的指南，用它们来部署 FastAPI 应用。 🤓

## 性能 { #performance }

独立机构 TechEmpower 所作的基准测试结果显示，基于 Uvicorn 运行的 **FastAPI** 程序是 <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">最快的 Python 框架之一</a>，仅次于 Starlette 和 Uvicorn 本身（FastAPI 内部使用了它们）。(*)

想了解更多，请查阅 <a href="https://fastapi.tiangolo.com/zh/benchmarks/" class="internal-link" target="_blank">基准测试</a> 章节。

## 依赖项 { #dependencies }

FastAPI 依赖 Pydantic 和 Starlette。

### `standard` 依赖项 { #standard-dependencies }

当你使用 `pip install "fastapi[standard]"` 安装 FastAPI 时，会包含 `standard` 这组可选依赖项：

用于 Pydantic：

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - 用于 email 校验。

用于 Starlette：

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - 如果你想使用 `TestClient` 则需要。
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - 如果你想使用默认模板配置则需要。
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - 如果你想使用 `request.form()` 支持表单 <abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据">“解析”</abbr>，则需要。

用于 FastAPI：

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - 用于加载和运行你的应用程序的服务器。这包括 `uvicorn[standard]`，其中包含一些用于高性能服务所需的依赖（例如 `uvloop`）。
* `fastapi-cli[standard]` - 用于提供 `fastapi` 命令。
    * 其中包含 `fastapi-cloud-cli`，它允许你将 FastAPI 应用部署到 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>。

### 不使用 `standard` 依赖项 { #without-standard-dependencies }

如果你不想包含 `standard` 可选依赖项，你可以使用 `pip install fastapi` 来安装，而不是 `pip install "fastapi[standard]"`。

### 不使用 `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

如果你想安装包含标准依赖项的 FastAPI，但不包含 `fastapi-cloud-cli`，你可以使用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"` 安装。

### 额外的可选依赖项 { #additional-optional-dependencies }

还有一些额外的依赖项你可能想安装。

Pydantic 的额外可选依赖项：

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - 用于配置管理。
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - 用于在 Pydantic 中使用额外类型。

FastAPI 的额外可选依赖项：

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - 如果你想使用 `ORJSONResponse` 则需要。
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - 如果你想使用 `UJSONResponse` 则需要。

## 许可协议 { #license }

该项目遵循 MIT 许可协议。

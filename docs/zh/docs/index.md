---
include_yaml:
  sponsors: data/sponsors.yml
---

# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/zh"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 框架，高性能。容易上手。开发更快。开箱即用，能上生产。</em>
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

文档: [https://fastapi.tiangolo.com/zh](https://fastapi.tiangolo.com/zh)

源码: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI 是一个现代、快速（高性能）的 Web 框架。用标准的 Python 类型标注来构建 API。

核心特性：

* 快：性能很高。和 **NodeJS**、**Go** 一个量级（得益于 Starlette 和 Pydantic）。[Python 里最快的框架之一](#performance)。
* 开发快：开发效率提升大约 200% 到 300%。*
* 更少的 bug：减少大约 40% 的人为（开发者）错误。*
* 直观：编辑器支持好。<dfn title="也称为：自动补全、autocompletion、IntelliSense">补全</dfn> 无处不在。更少调试时间。
* 简单：易用、易学。更少查文档时间。
* 精简：最小化重复代码。一次声明，多处生效。更少 bug。
* 稳健：代码上生产。自带交互式文档。
* 基于标准：完全兼容 API 开放标准：[OpenAPI](https://github.com/OAI/OpenAPI-Specification)（以前叫 Swagger）和 [JSON Schema](https://json-schema.org/)。

<small>* 基于内部团队在真实生产项目中的测试估算。</small>

## 赞助商 { #sponsors }

<!-- sponsors -->

### Keystone 赞助商 { #keystone-sponsor }

<div class="fastapi-sponsors fastapi-sponsors--keystone">
{% for sponsor in sponsors.keystone -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--keystone" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}"></a>
{% endfor -%}
</div>

### 黄金赞助商 { #gold-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--gold">
{% for sponsor in sponsors.gold -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--gold" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor -%}
</div>

### 白银赞助商 { #silver-sponsors }

<div class="fastapi-sponsors fastapi-sponsors--silver">
{% for sponsor in sponsors.silver -%}
<a class="fastapi-sponsors__card fastapi-sponsors__card--silver" href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img class="fastapi-sponsors__banner" src="{{ sponsor.img }}" alt="{{ sponsor.title }}" loading="lazy"></a>
{% endfor %}
</div>

<!-- /sponsors -->

[其他赞助商](https://fastapi.tiangolo.com/zh/fastapi-people/#sponsors)

## 评价 { #opinions }

<!-- only-mkdocs -->
<div class="fastapi-opinions" data-fastapi-opinions>
  <div class="fastapi-opinions__tabs" role="tablist" aria-label="Companies using FastAPI">
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-microsoft" aria-controls="fo-panel-microsoft" aria-selected="true" tabindex="0">
      <span class="fastapi-opinions__mark"><img src="/img/logos/microsoft.svg" alt="Microsoft" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-uber" aria-controls="fo-panel-uber" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/uber.svg" alt="Uber" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-netflix" aria-controls="fo-panel-netflix" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/netflix.svg" alt="Netflix" loading="lazy"></span>
    </button>
    <button class="fastapi-opinions__tab" role="tab" type="button" id="fo-tab-cisco" aria-controls="fo-panel-cisco" aria-selected="false" tabindex="-1">
      <span class="fastapi-opinions__mark"><img src="/img/logos/cisco.svg" alt="Cisco" loading="lazy"></span>
    </button>
  </div>

  <div class="fastapi-opinions__panel" id="fo-panel-microsoft" role="tabpanel" aria-labelledby="fo-tab-microsoft" tabindex="0">
    <blockquote class="fastapi-opinions__quote">“我这段时间用 <strong>FastAPI</strong> 用得很多。打算把我们团队在 <strong>Microsoft 的 ML 服务</strong>全都切到它上面。一些已经集成进核心的 <strong>Windows</strong> 产品，还有一些 <strong>Office</strong> 产品。”</blockquote>
    <div class="fastapi-opinions__attr">— Kabir Khan，<strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-uber" role="tabpanel" aria-labelledby="fo-tab-uber" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“我们采用了 <strong>FastAPI</strong> 库来启动一个 <strong>REST</strong> 服务器，通过它查询得到<strong>预测</strong>。” <em>[用于 Ludwig]</em></blockquote>
    <div class="fastapi-opinions__attr">— Piero Molino, Yaroslav Dudin, Sai Sumanth Miryala，<strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-netflix" role="tabpanel" aria-labelledby="fo-tab-netflix" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“<strong>Netflix</strong> 很高兴开源我们的<strong>危机管理</strong>编排框架：<strong>Dispatch</strong>！” <em>[基于 FastAPI 构建]</em></blockquote>
    <div class="fastapi-opinions__attr">— Kevin Glisson, Marc Vilanova, Forest Monsen，<strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072">(ref)</a></div>
  </div>
  <div class="fastapi-opinions__panel" id="fo-panel-cisco" role="tabpanel" aria-labelledby="fo-tab-cisco" tabindex="0" hidden>
    <blockquote class="fastapi-opinions__quote">“如果你在找生产可用的 Python API 框架，我强烈推荐 <strong>FastAPI</strong>。它<strong>设计优雅</strong>、<strong>简单易用</strong>、<strong>可扩展性强</strong>——已经成了我们 API-first 开发战略的<strong>关键组件</strong>。”</blockquote>
    <div class="fastapi-opinions__attr">— Deon Pillsbury，<strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/">(ref)</a></div>
  </div>
</div>
<!-- /only-mkdocs -->

<div class="only-github" markdown="1">

“_[...] 我这段时间用 **FastAPI** 用得很多。[...] 打算把我们团队在 **Microsoft 的 ML 服务**全都切到它上面。一些已经集成进核心的 **Windows** 产品，还有一些 **Office** 产品。_”

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

“_我们采用了 **FastAPI** 库来启动一个 **REST** 服务器，通过它查询得到**预测**。 [用于 Ludwig]_”

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

“_**Netflix** 很高兴开源我们的**危机管理**编排框架：**Dispatch**！[基于 **FastAPI** 构建]_”

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

“_如果你在找生产可用的 Python API 框架，我强烈推荐 **FastAPI**。它**设计优雅**、**简单易用**、**可扩展性强**，已经成了我们 API-first 开发战略的**关键组件**，驱动了很多自动化和服务，比如我们的 Virtual TAC Engineer。_”

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

</div>

## FastAPI 大会 { #fastapi-conf }

[**FastAPI Conf '26**](https://fastapiconf.com) 将在 **2026 年 10 月 28 日** 于 **荷兰阿姆斯特丹** 举办。全是 FastAPI 干货，来自源头。🎤

<a class="fastapi-feature-banner" href="https://fastapiconf.com"><img src="https://fastapi.tiangolo.com/img/fastapi-conf.jpeg" alt="FastAPI Conf '26 - October 28, 2026 - Amsterdam, NL"></a>

## FastAPI 微纪录片 { #fastapi-mini-documentary }

这里有一部 [FastAPI 微纪录片](https://www.youtube.com/watch?v=mpR8ngthqiE)，在 2025 年底发布。可以在线看：

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## Typer：CLI 里的 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果你要做一个终端里用的 <abbr title="Command Line Interface - 命令行界面">CLI</abbr> 应用，不是 Web API，看看 [**Typer**](https://typer.tiangolo.com/)。

**Typer** 是 FastAPI 的小老弟。目标是做 **CLI 里的 FastAPI**。⌨️ 🚀

## 依赖和基座 { #requirements }

FastAPI 站在巨人肩膀上：

* [Starlette](https://www.starlette.dev/) 负责 Web 部分。
* [Pydantic](https://docs.pydantic.dev/) 负责数据部分。

## 安装 { #installation }

先创建并激活一个[虚拟环境](https://fastapi.tiangolo.com/zh/virtual-environments/)，然后安装 FastAPI：

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

注意：把 "fastapi[standard]" 加上引号。所有终端都能正常识别。

## 示例 { #example }

### 创建 { #create-it }

新建文件 `main.py`，写入：

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
<summary>或者用 <code>async def</code>...</summary>

如果你的代码用到了 `async` / `await`，就用 `async def`：

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

注意：

不确定的话，去看「In a hurry?」里关于文档中的 [`async` 和 `await`](https://fastapi.tiangolo.com/zh/async/#in-a-hurry)。

</details>

### 运行 { #run-it }

启动服务：

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

`fastapi dev` 会自动读取你的 `main.py`，检测里面的 **FastAPI** 应用，然后用 [Uvicorn](https://www.uvicorn.dev) 启动服务器。

默认开启自动重载，方便本地开发。

更多见 [FastAPI CLI 文档](https://fastapi.tiangolo.com/zh/fastapi-cli/)。

</details>

### 查看 { #check-it }

打开浏览器访问 [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)。

你会看到 JSON 响应：

```JSON
{"item_id": 5, "q": "somequery"}
```

你已经写好了一个 API，它：

* 接收 `/` 和 `/items/{item_id}` 两个路径的 HTTP 请求。
* 这两个路径都接收 `GET` 操作（也叫 HTTP 方法）。
* `/items/{item_id}` 的路径参数 `item_id` 必须是 `int`。
* `/items/{item_id}` 还有一个可选的 `str` 类型查询参数 `q`。

### 交互式 API 文档 { #interactive-api-docs }

访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到自动生成的交互式 API 文档（由 [Swagger UI](https://github.com/swagger-api/swagger-ui) 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 另一套 API 文档 { #alternative-api-docs }

再访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

你会看到另一套自动文档（由 [ReDoc](https://github.com/Rebilly/ReDoc) 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 升级示例 { #example-upgrade }

现在改一下 `main.py`，让它能接收 `PUT` 请求的 body。

用标准 Python 类型声明 body，多亏了 Pydantic：

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

`fastapi dev` 会自动重载。

### 交互式文档同步升级 { #interactive-api-docs-upgrade }

访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

* 交互式文档会自动更新。包含新的 body：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 点 “Try it out” 按钮。可以填参数，直接和 API 交互：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然后点 “Execute”。界面会调用你的 API，发送参数，拿到结果并展示：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 另一套文档同步升级 { #alternative-api-docs-upgrade }

再访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)。

* 这套文档也会反映新的查询参数和 body：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 小结 { #recap }

总结一下。你只需要在函数参数里声明一次参数类型、body 等。

用的就是现代标准 Python 类型。

不用学一堆新语法、不用背某个库的方法或类。

就是标准的 **Python**。

比如，一个 `int`：

```Python
item_id: int
```

或者更复杂的 `Item` 模型：

```Python
item: Item
```

...只要这一个声明，你就能得到：

* 编辑器支持，包括：
    * 补全。
    * 类型检查。
* 数据校验：
    * 数据不合法时自动抛出清晰的错误。
    * 支持深层嵌套 JSON 的校验。
* 输入数据的<dfn title="也称为：序列化、解析、封送">转换</dfn>：从网络到 Python 数据和类型。读取来源：
    * JSON。
    * 路径参数。
    * 查询参数。
    * Cookies。
    * Headers。
    * 表单。
    * 文件。
* 输出数据的<dfn title="也称为：序列化、解析、封送">转换</dfn>：从 Python 数据和类型到网络数据（JSON）：
    * 转换 Python 基本类型（`str`、`int`、`float`、`bool`、`list` 等）。
    * `datetime` 对象。
    * `UUID` 对象。
    * 数据库模型。
    * ...等等。
* 自动生成的交互式 API 文档，有两套 UI：
    * Swagger UI。
    * ReDoc。

---

回到上面的代码示例，**FastAPI** 会：

* 校验 `GET` 和 `PUT` 请求的路径里有 `item_id`。
* 校验 `GET` 和 `PUT` 请求里的 `item_id` 是 `int`。
    * 如果不是，客户端会看到清晰有用的错误。
* 对 `GET` 到 `/items/{item_id}` 的请求，检查是否有名为 `q` 的可选查询参数（比如 `http://127.0.0.1:8000/items/foo?q=somequery`）。
    * `q` 参数声明了 `= None`，所以它是可选的。
    * 去掉 `None` 就会变成必填（`PUT` 里的 body 也是必填）。
* 对 `/items/{item_id}` 的 `PUT` 请求，把 body 当作 JSON 读取：
    * 检查是否有必填属性 `name`，类型为 `str`。
    * 检查是否有必填属性 `price`，类型为 `float`。
    * 检查是否有可选属性 `is_offer`，如果有则必须是 `bool`。
    * 这些校验也适用于深层嵌套的 JSON。
* 自动在 JSON 和 Python 之间转换。
* 用 OpenAPI 文档化一切，可以被以下工具使用：
    * 交互式文档系统。
    * 多语言的自动客户端代码生成系统。
* 直接提供两套交互式文档 Web 界面。

---

这里只是开了个头，但你已经知道它怎么运作了。

把这一行：

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...从：

```Python
        ... "item_name": item.name ...
```

...改成：

```Python
        ... "item_price": item.price ...
```

...看看你的编辑器如何自动补全属性，并且知道它们的类型：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

更完整的示例和更多特性，见 <a href="https://fastapi.tiangolo.com/zh/tutorial/">教程 - 用户指南</a>。

剧透：教程 - 用户指南包含：

* 从不同位置声明**参数**：**headers**、**cookies**、**表单字段**、**文件**。
* 如何设置**校验约束**，比如 `maximum_length` 或 `regex`。
* 一个强大且好用的**<dfn title="也称为：组件、资源、提供者、服务、可注入">依赖注入</dfn>**系统。
* 安全与认证。包括 **OAuth2**（配合 **JWT tokens**）和 **HTTP Basic**。
* 更高级（但一样简单）的**深度嵌套 JSON 模型**声明技巧（感谢 Pydantic）。
* **GraphQL** 集成，支持 [Strawberry](https://strawberry.rocks) 等库。
* 许多额外特性（感谢 Starlette），比如：
    * **WebSockets**
    * 基于 HTTPX 和 `pytest` 的超简单测试
    * **CORS**
    * **Cookie Sessions**
    * ...等等。

### 部署你的应用（可选） { #deploy-your-app-optional }

你可以把 FastAPI 应用部署到 [FastAPI Cloud](https://fastapicloud.com)。还没有账号就去等候名单报名。🚀

如果你已经有 **FastAPI Cloud** 账号（我们从等候名单邀请了你 😉），只要一条命令就能部署应用。

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

就这些！现在用这个地址就能访问你的应用了。✨

#### 关于 FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** 出自 **FastAPI** 同一位作者和团队。

它让你以最小成本**构建**、**部署**、**访问**一个 API。

把用 FastAPI 开发应用时的**开发者体验**，带到了**部署到云上**这一步。🎉

FastAPI Cloud 是「FastAPI and friends」开源项目的主要赞助方和资金来源。✨

#### 部署到其他云厂商 { #deploy-to-other-cloud-providers }

FastAPI 是开源且基于标准的。你可以部署到任意云厂商。

按照各家云厂商的指南部署 FastAPI 应用就行。🤓

## 性能 { #performance }

独立的 TechEmpower 基准测试显示，Uvicorn 下运行的 **FastAPI** 应用[是 Python 里最快的框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)。仅次于 Starlette 和 Uvicorn 本身（FastAPI 内部就用到它们）。(*)

想了解更多，查看[基准测试](https://fastapi.tiangolo.com/zh/benchmarks/)。

## 依赖 { #dependencies }

FastAPI 依赖 Pydantic 和 Starlette。

### `standard` 依赖组 { #standard-dependencies }

用 `pip install "fastapi[standard]"` 安装时，会包含 `standard` 这组可选依赖：

Pydantic 用到：

* [`email-validator`](https://github.com/JoshData/python-email-validator) —— 用于邮箱校验。

Starlette 用到：

* [`httpx`](https://www.python-httpx.org) —— 想用 `TestClient` 就需要它。
* [`jinja2`](https://jinja.palletsprojects.com) —— 想用默认模板配置就需要它。
* [`python-multipart`](https://github.com/Kludex/python-multipart) —— 想支持表单<dfn title="把来自 HTTP 请求的字符串转换成 Python 数据">"解析"</dfn>，即 `request.form()`，就需要它。

FastAPI 用到：

* [`uvicorn`](https://www.uvicorn.dev) —— 负责加载和服务你的应用。包含 `uvicorn[standard]`，内置一些高性能服务需要的依赖（比如 `uvloop`）。
* `fastapi-cli[standard]` —— 提供 `fastapi` 命令。
    * 其中包含 `fastapi-cloud-cli`，可把应用部署到 [FastAPI Cloud](https://fastapicloud.com)。

### 不包含 `standard` 依赖 { #without-standard-dependencies }

如果不想带上 `standard` 这组可选依赖，就用 `pip install fastapi`，而不是 `pip install "fastapi[standard]"`。

### 不包含 `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

如果你想安装标准依赖，但去掉 `fastapi-cloud-cli`，可以用 `pip install "fastapi[standard-no-fastapi-cloud-cli]"`。

### 额外可选依赖 { #additional-optional-dependencies }

还有一些你可能会用到的额外依赖。

Pydantic 的可选依赖：

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) —— 管理配置。
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) —— 更多可用于 Pydantic 的类型。

FastAPI 的可选依赖：

* [`orjson`](https://github.com/ijl/orjson) —— 想用 `ORJSONResponse` 就需要它。
* [`ujson`](https://github.com/esnme/ultrajson) —— 想用 `UJSONResponse` 就需要它。

## 许可证 { #license }

本项目使用 MIT 许可证。

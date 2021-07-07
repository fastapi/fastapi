<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI 速度快、上手快、开发快，生产环境可用</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>



---

**文档**： <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**源码**： <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI 是**快速**构建高效 API 的现代网络框架，它使用的是 Python 3.6+，并基于 Python 标准类型提示。

核心特性：

* **速度快**：可与 **NodeJS** 和 **Go** 比肩的极高性能（归功于 Starlette 和 Pydantic）。[最快的 Python 网络框架之一](#_11)
* **开发快**：开发速度提高约 200％ 至 300％*
* **Bug 少**：人为错误减少约 40％*
* **智能**：极佳的编辑器支持。处处皆可<abbr title="也被称为自动完成、智能感知">自动补全</abbr>，减少调试时间
* **简单**：易学、易用，阅读文档所需时间更短
* **简短**：代码重复最小化，通过不同的参数声明实现丰富功能，Bug 更少
* **健壮**：生产级别的代码，还有自动交互文档
* **标准**：完全兼容并基于 API 开放标准：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>（曾用名为 Swagger）和 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>

<small>* 根据对某线上应用内部开发团队的测试估算得出。</small>

## 金牌赞助商

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">其他赞助商</a>

## 评价

「_[...] 最近我一直在用 **FastAPI**。[...] 实际上，我打算用 FastAPI 实现我们**微软**团队所有的**机器学习服务**。目前，我们正把一些服务集成至 **Windows** 和 **Office** 等核心产品。_」

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>微软</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

「_我们选择用 **FastAPI** 创建获取**预测结果**的 **REST** 服务。[用于 Ludwig]_」

<div style="text-align: right; margin-right: 10%;">Piero Molino，Yaroslav Dudin 和 Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

「_**Netflix** 很荣幸地宣布，正式开源**危机管理**编排框架：**Dispatch**！[使用 **FastAPI** 构建]_」

<div style="text-align: right; margin-right: 10%;">Kevin Glisson，Marc Vilanova，Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

「_**FastAPI** 让我欣喜若狂。它太棒了！_」

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> 播客主持人</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

「_老实说，您的作品看起来非常可靠和优美。这就是我心目中的 **Hug** - 看到有人实现了，真的很鼓舞人心。_」

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://www.hug.rest/" target="_blank">Hug</a> 作者</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

「_如果你想学习构建 REST API 的**现代网络框架**，看下 **FastAPI** 吧 [...] 它易学、易用、速度快 [...]_」

「_我们已经将 **API** 服务切换到了 **FastAPI** [...] 我觉得你也会喜欢 [...]_」

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> 创始人 - <a href="https://spacy.io" target="_blank">spaCy</a> 作者</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**，命令行中的 FastAPI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

如果您开发的不是网络 API，而是在终端中运行的<abbr title="Command Line Interface">命令行</abbr>应用，不妨试下 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>。

**Typer** 是 FastAPI 的小兄弟，立志要成为**命令行中的 FastAPI**。 ⌨️ 🚀

## 依赖支持

Python 3.6 及更高版本

FastAPI 站在以下巨人的肩膀上：

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> 负责网络
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 负责数据

## 安装

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

FastAPI 还需要 ASGI 服务器，生产环境下可以使用 <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> 或 <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>。

<div class="termy">

```console
$ pip install uvicorn[standard]

---> 100%
```

</div>

## 示例

### 创建

* 创建 `main.py`，写入以下内容：

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>或者使用 <code>async def</code>...</summary>

如果代码中使用了 `async` / `await`，请配套使用 `async def`：

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

**笔记**：

如果不清楚是否应该使用异步，请参阅文档「着急了？」中<a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">关于 `async` 和 `await` 的介绍</a>。

</details>

### 运行

用以下命令运行服务器：

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>关于 <code>uvicorn main:app --reload</code> 命令......</summary>

 `uvicorn main:app` 命令含义如下：

* `main`：`main.py`（ Python 「模块」）
* `app`：`main.py` 中通过 `app = FastAPI()` 创建的对象
* `--reload`：代码更新后，重启服务器。仅在开发时使用

</details>

### 检查

使用浏览器访问 <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>。

可以获得如下 JSON 响应：

```JSON
{"item_id": 5, "q": "somequery"}
```

至此，我们就创建了具有以下功能的 API：

* 通过*路径* `/` 和 `/items/{item_id}` 接收 HTTP 请求
* 这两个*路径*都能接收 `GET` 操作（也叫作 HTTP _方法_）
* `/items/{item_id}` *路径*包含类型为 `int` 的*路径参数* `item_id`
* `/items/{item_id}` *路径*还包含可选的，类型为 `str` 的*查询参数* `q`

### API 交互文档

访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

可以看到（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>）自动生成的 API 交互文档：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 备选 API 文档

访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

可以看到（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>）自动生成的文档：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 更新示例

修改 `main.py`，从 `PUT` 请求中接收请求体。

借助 Pydantic 使用 Python 标准类型声明请求体。

```Python hl_lines="4  9-12  25-27"
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

（因为之前为 `uvicorn` 命令添加了 `--reload` 选项），服务器会自动重载。

### 更新 API 交互文档

访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

* API 交互文档会自动更新，并加入新的请求体：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 点击「Try it out」按钮，填写参数，直接调用 API：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 然后，点击「Execute」按钮，用户界面和 API 通信，发送参数，获取结果，并在屏幕上显示：

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 更新备选文档

访问 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

* 备选文档也会显示新加入的请求参数和请求体：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 小结

总的来说，和声明函数的参数一样，只需声明**一次**参数类型和请求体。

在此，使用了现代 Python 的标准类型进行声明。

开发人员不用学习新语法，也不用了解特定库的方法或类。

只要使用标准的 **Python 3.6 及更高版本**。

举个例子，比如，声明 `int` 类型：

```Python
item_id: int
```

或者使用更复杂的 `Item` 模型：

```Python
item: Item
```

......只需一次声明，就可以获得以下好处：

* 编辑器支持，包括：
    * 自动补全
    * 类型检查
* 数据校验：
    * 在校验失败时自动生成清晰的错误信息
    * 对多层嵌套的 JSON 对象依然执行校验
* <abbr title="也叫：序列化或解析">转换</abbr>输入数据：转换为 Python 数据与类型。可以从以下对象中读取：
    * JSON
    * 路径参数
    * 查询参数
    * Cookies
    * 请求头
    * 表单
    * 文件
* <abbr title="也被称为：序列化或解析">转换</abbr>输出数据：把 Python 数据类型转换为供网络传输的（ JSON ）数据：
    * Python 基础类型 （`str`、 `int`、 `float`、 `bool`、 `list` 等）
    * `datetime` 对象
    * `UUID` 对象
    * 数据库模型
    * ......及更多其他类型
* 自动生成 API 交互文档，包括两种用户界面：
    * Swagger UI
    * ReDoc

---

回顾本章的代码示例，**FastAPI** 可以：

* 校验 `GET` 和 `PUT` 请求的路径中是否含有 `item_id`；
* 校验 `GET` 和 `PUT` 请求中的 `item_id` 是否为 `int` 类型
    * 如果不是 `int` 类型，客户端返回错误信息
* 检查 `GET` 请求中是否包含可选查询参数 `q`（比如 `http://127.0.0.1:8000/items/foo?q=somequery`）
    * `q` 声明为 `= None`，所以是可选的
    * 没有 `None`，`q` 就是必选的（如 `PUT` 例子中的请求体）
* 对于访问 `/items/{item_id}` 的 `PUT` 请求，把请求体读取为 JSON，并且：
    * 检查是否包含必选属性 `name`，并且值的类型为 `str`
    * 检查是否包含必选属性 `price`，并且值的类型为 `float`
    * 检查是否包含可选属性 `is_offer`， 如果包含，值的类型应为 `bool`
    * 以上过程也适用于多层嵌套的 JSON 对象
* 自动转换 JSON
* 通过 OpenAPI 文档存档所有内容，可被用于：
    * 交互文档
    * 其他编程语言的客户端代码自动生成系统
* 直接提供两种交互文档

---

虽然本篇的介绍比较粗浅，但其实已经涵盖了 FastAPI 的所有工作原理。

试着把下面这行代码：

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

......注意，编辑器可以自动补全属性，还知道属性的类型：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

<a href="https://fastapi.tiangolo.com/tutorial/">教程 - 用户指南</a>中介绍了包含更多功能的完整示例。

**剧透警告**： 教程 - 用户指南中的内容有：

* 声明各种来源的参数，如：**请求头**、**cookies**、**form 表单**及**上传文件**
* 设置**校验约束**，如 `maximum_length` 或 `regex`
* 强大、但易用的**<abbr title="也被称为 components, resources, providers, services, injectables">依赖注入</abbr>**系统
* 安全和身份验证，支持 **OAuth2**、**JWT Token **、**HTTP 基本身份验证**等方式
* （借助 Pydantic）使用更高级，但同样简单的技术声明**深度嵌套 JSON 模型**
* （借助 Starlette）实现以下更多功能：
    * **WebSockets**
    * **GraphQL**
    * 基于 `requests` 和 `pytest` 的简单测试
    * **CORS**，跨域资源共享
    * **Cookie Sessions**
    * ......以及更多

## 性能

独立机构 TechEmpower 的基准测试结果显示，基于 Uvicorn 运行的 **FastAPI** 是<a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">最快的 Python 网络框架之一</a>，仅次于（FastAPI 内部使用的） Starlette 和 Uvicorn。(*)

更多详情，请参阅<a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">基准测试</a>一章。

## 可选依赖支持库

用于 Pydantic：

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - 更快的 JSON<abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">「解析」</abbr>
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - 用于 email 校验

用于 Starlette：

* <a href="https://requests.readthedocs.io" target="_blank"><code>requests</code></a> - 使用 `TestClient` 时安装
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - 使用 `FileResponse` 或 `StaticFiles` 时安装
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - 使用默认模板配置时安装
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - 通过 `request.form()` <abbr title="将来自 HTTP 请求中的字符串转换为 Python 数据类型">「解析」</abbr>表单时安装
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - 需要 `SessionMiddleware` 支持时安装
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - 使用 Starlette 的 `SchemaGenerator` 时安装（FastAPI 可能不需要此支持库）
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - 需要 `GraphQLApp` 支持时安装
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - 使用 `UJSONResponse` 时安装

用于 FastAPI / Starlette：

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - 用于加载和运行应用的服务器
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - 使用 `ORJSONResponse` 时安装

使用 `pip install fastapi[all]` 可以安装上述所有依赖支持库。

## 许可协议

本项目遵循 MIT 许可协议。

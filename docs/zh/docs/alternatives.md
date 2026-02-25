# 替代方案、灵感与对比 { #alternatives-inspiration-and-comparisons }

是什么启发了 **FastAPI**，它与替代方案的比较，以及它从中学到的东西。

## 介绍 { #intro }

没有前人的工作，就不会有 **FastAPI**。

在它诞生之前，已经有许多工具为其提供了灵感。

我曾经多年避免创建一个新框架。起初，我尝试用许多不同的框架、插件和工具来解决 **FastAPI** 所覆盖的全部功能。

但在某个时刻，除了创造一个能提供所有这些功能的东西之外，别无选择；它要吸收以往工具的最佳理念，并以尽可能好的方式组合起来，利用之前都不存在的语言特性（Python 3.6+ 类型提示）。

## 先前的工具 { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

它是最流行且被广泛信任的 Python 框架。被用于构建 Instagram 等系统。

它与关系型数据库（如 MySQL、PostgreSQL）耦合相对紧密，因此若要以 NoSQL 数据库（如 Couchbase、MongoDB、Cassandra 等）作为主要存储引擎并不容易。

它最初用于在后端生成 HTML，而不是创建由现代前端（如 React、Vue.js、Angular）或与之通信的其他系统（如 <abbr title="Internet of Things - 物联网">IoT</abbr> 设备）使用的 API。

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Django REST framework 作为一个灵活工具箱而创建，用于在底层使用 Django 构建 Web API，从而增强其 API 能力。

它被包括 Mozilla、Red Hat、Eventbrite 在内的许多公司使用。

它是最早的“自动 API 文档”的范例之一，这正是启发“寻找” **FastAPI** 的最初想法之一。

/// note | 注意

Django REST Framework 由 Tom Christie 创建。他也是 Starlette 和 Uvicorn 的作者，**FastAPI** 就是基于它们构建的。

///

/// check | 启发 **FastAPI**：

提供自动化的 API 文档 Web 界面。

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask 是一个“微框架”，它不包含数据库集成，也没有像 Django 那样的许多默认内建功能。

这种简单与灵活使得可以将 NoSQL 数据库作为主要的数据存储系统。

由于非常简单，它相对直观易学，尽管文档在某些部分略显偏技术。

它也常用于不一定需要数据库、用户管理，或任何 Django 预构建功能的应用；当然，许多这类功能可以通过插件添加。

这种组件解耦、可按需扩展的“微框架”特性，是我想保留的关键点。

鉴于 Flask 的简洁，它似乎非常适合构建 API。接下来要找的，就是 Flask 版的 “Django REST Framework”。

/// check | 启发 **FastAPI**：

- 成为微框架，便于按需组合所需的工具与组件。
- 提供简单易用的路由系统。

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI** 实际上不是 **Requests** 的替代品。它们的作用范围完全不同。

在 FastAPI 应用程序内部使用 Requests 其实非常常见。

尽管如此，FastAPI 依然从 Requests 中获得了不少灵感。

**Requests** 是一个用于与 API 交互（作为客户端）的库，而 **FastAPI** 是一个用于构建 API（作为服务端）的库。

它们处在某种意义上的“对立端”，彼此互补。

Requests 设计非常简单直观，易于使用，且有合理的默认值。同时它也非常强大、可定制。

这就是为什么，正如其官网所说：

> Requests 是有史以来下载量最高的 Python 包之一

它的用法非常简单。例如，进行一次 `GET` 请求，你会这样写：

```Python
response = requests.get("http://example.com/some/url")
```

对应地，FastAPI 的 API 路径操作可能看起来是这样的：

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

可以看到 `requests.get(...)` 与 `@app.get(...)` 的相似之处。

/// check | 启发 **FastAPI**：

- 提供简单直观的 API。
- 直接、自然地使用 HTTP 方法名（操作）。
- 具备合理默认值，同时支持强大定制能力。

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

我想从 Django REST Framework 得到的主要特性之一是自动 API 文档。

随后我发现有一个用于用 JSON（或 YAML，JSON 的扩展）来描述 API 的标准，称为 Swagger。

并且已经有了用于 Swagger API 的 Web 用户界面。因此，只要能为 API 生成 Swagger 文档，就能自动使用这个 Web 界面。

后来，Swagger 交由 Linux 基金会管理，并更名为 OpenAPI。

因此，在谈到 2.0 版本时人们常说 “Swagger”，而 3+ 版本则称为 “OpenAPI”。

/// check | 启发 **FastAPI**：

采用并使用开放的 API 规范标准，而非自定义模式。

并集成基于标准的用户界面工具：

- <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
- <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

选择这两者是因为它们相当流行且稳定；但稍作搜索，你就能找到数十种 OpenAPI 的替代用户界面（都可以与 **FastAPI** 搭配使用）。

///

### Flask REST 框架 { #flask-rest-frameworks }

有若干基于 Flask 的 REST 框架，但在投入时间精力深入调研后，我发现许多已停止维护或被弃用，并存在多处未解决问题，不太适合采用。

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

API 系统所需的主要特性之一是数据“<dfn title="也称为：编组、转换">序列化</dfn>”，即将代码（Python）中的数据转换为可通过网络发送的形式。例如，将包含数据库数据的对象转换为 JSON 对象、将 `datetime` 对象转换为字符串等。

API 的另一个重要特性是数据校验，确保数据在给定约束下是有效的。例如，某个字段必须是 `int` 而不是任意字符串。这对传入数据尤其有用。

没有数据校验系统的话，你就得在代码里手写所有检查。

这些正是 Marshmallow 要提供的功能。它是个很棒的库，我之前大量使用过。

但它诞生于 Python 类型提示出现之前。因此，定义每个<dfn title="数据应如何构造的定义">模式</dfn>都需要使用 Marshmallow 提供的特定工具和类。

/// check | 启发 **FastAPI**：

使用代码定义“模式”，自动提供数据类型与校验。

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

API 的另一个重要需求是从传入请求中<dfn title="读取并转换为 Python 数据">解析</dfn>数据。

Webargs 是一个在多个框架（包括 Flask）之上提供该功能的工具。

它在底层使用 Marshmallow 进行数据校验，并且由相同的开发者创建。

在拥有 **FastAPI** 之前，我也大量使用过它，这是个很棒的工具。

/// info | 信息

Webargs 由与 Marshmallow 相同的开发者创建。

///

/// check | 启发 **FastAPI**：

对传入请求数据进行自动校验。

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow 与 Webargs 通过插件提供了校验、解析与序列化。

但文档仍然缺失，于是出现了 APISpec。

它为许多框架提供插件（Starlette 也有插件）。

它的工作方式是：你在处理路由的每个函数的文档字符串里，用 YAML 格式编写模式定义。

然后它会生成 OpenAPI 模式。

这正是它在 Flask、Starlette、Responder 等框架里的工作方式。

但这样我们又回到了在 Python 字符串中维护一套“微语法”（一大段 YAML）的问题上。

编辑器很难为此提供帮助；而且如果我们修改了参数或 Marshmallow 模式，却忘了同步更新那个 YAML 文档字符串，生成的模式就会过时。

/// info | 信息

APISpec 由与 Marshmallow 相同的开发者创建。

///

/// check | 启发 **FastAPI**：

支持开放的 API 标准 OpenAPI。

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

这是一个 Flask 插件，将 Webargs、Marshmallow 与 APISpec 结合在一起。

它利用 Webargs 与 Marshmallow 的信息，通过 APISpec 自动生成 OpenAPI 模式。

这是个很棒却被低估的工具；它理应比许多 Flask 插件更流行。或许是因为它的文档过于简洁与抽象。

这解决了在 Python 文档字符串里书写 YAML（另一套语法）的问题。

在构建 **FastAPI** 之前，Flask + Flask-apispec + Marshmallow + Webargs 的组合是我最喜欢的后端技术栈。

使用它促成了若干 Flask 全栈脚手架的诞生。以下是我（以及若干外部团队）至今使用的主要技术栈：

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

这些全栈脚手架也成为了[**FastAPI** 项目脚手架](project-generation.md){.internal-link target=_blank}的基础。

/// info | 信息

Flask-apispec 由与 Marshmallow 相同的开发者创建。

///

/// check | 启发 **FastAPI**：

从定义序列化与校验的同一份代码自动生成 OpenAPI 模式。

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a>（以及 <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>） { #nestjs-and-angular }

这甚至不是 Python。NestJS 是一个 JavaScript（TypeScript）的 NodeJS 框架，受 Angular 启发。

它实现了与 Flask-apispec 有些类似的效果。

它集成了受 Angular 2 启发的依赖注入系统。与我所知的其他依赖注入系统一样，需要预先注册“可注入项”，因此会增加冗长与重复。

由于参数用 TypeScript 类型描述（类似 Python 类型提示），编辑器支持相当好。

但由于 TypeScript 的类型在编译为 JavaScript 后不会保留，无法只依赖这些类型同时定义校验、序列化与文档。受此以及一些设计决策影响，为了获得校验、序列化与自动 schema 生成，需要在许多位置添加装饰器，因此代码会相当冗长。

它对嵌套模型的支持并不好。如果请求的 JSON 体是包含嵌套 JSON 对象的 JSON 对象，则无法被正确文档化和校验。

/// check | 启发 **FastAPI**：

使用 Python 类型以获得出色的编辑器支持。

拥有强大的依赖注入系统，并设法尽量减少代码重复。

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

它是最早的一批基于 `asyncio` 的极速 Python 框架之一，且做得与 Flask 很相似。

/// note | 技术细节

它使用了 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> 来替代 Python 默认的 `asyncio` 循环。这正是它如此之快的原因。

它显然启发了 Uvicorn 和 Starlette；在公开的基准测试中，它们目前比 Sanic 更快。

///

/// check | 启发 **FastAPI**：

找到实现疯狂性能的路径。

这就是 **FastAPI** 基于 Starlette 的原因，因为它是目前可用的最快框架（由第三方基准测试验证）。

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon 是另一个高性能 Python 框架，它被设计为精简且可作为 Hug 等其他框架的基础。

它设计为接收两个参数的函数：一个“request”和一个“response”。然后从 request 中“读取”，向 response 中“写入”。由于这种设计，无法用标准的 Python 类型提示将请求参数和请求体声明为函数形参。

因此，数据校验、序列化与文档要么需要手写完成，无法自动化；要么需要在 Falcon 之上实现一个框架，例如 Hug。其他受 Falcon 设计启发、采用“一个 request 对象 + 一个 response 对象作为参数”的框架也有同样的区别。

/// check | 启发 **FastAPI**：

寻找获得卓越性能的方法。

与 Hug（Hug 基于 Falcon）一起，启发 **FastAPI** 在函数中声明一个 `response` 参数。尽管在 FastAPI 中它是可选的，主要用于设置 headers、cookies 和可选的状态码。

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

我在构建 **FastAPI** 的早期阶段发现了 Molten。它有不少相似的想法：

* 基于 Python 类型提示。
* 从这些类型获得校验与文档。
* 依赖注入系统。

它没有使用像 Pydantic 这样的第三方数据校验、序列化与文档库，而是有自己的实现。因此这些数据类型定义不太容易在其他地方复用。

它需要稍微冗长一些的配置。并且由于基于 WSGI（而非 ASGI），它并未设计为充分利用 Uvicorn、Starlette、Sanic 等工具所提供的高性能。

其依赖注入系统需要预先注册依赖，且依赖根据声明的类型来解析。因此无法为同一类型声明多于一个“组件”。

路由在一个地方集中声明，使用在其他地方声明的函数（而不是使用可以直接放在处理端点函数之上的装饰器）。这更接近 Django 的做法，而不是 Flask（和 Starlette）。它在代码中割裂了相对紧耦合的内容。

/// check | 启发 **FastAPI**：

通过模型属性的“默认值”为数据类型定义额外校验。这提升了编辑器支持，而这在当时的 Pydantic 中尚不可用。

这实际上促成了对 Pydantic 的部分更新，以支持这种校验声明风格（这些功能现已在 Pydantic 中可用）。

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug 是最早使用 Python 类型提示来声明 API 参数类型的框架之一。这一绝妙想法也启发了其他工具。

它在声明中使用自定义类型而不是标准的 Python 类型，但这依然是巨大的进步。

它也是最早生成一个自定义 JSON 模式来声明整个 API 的框架之一。

它并不基于 OpenAPI 与 JSON Schema 这类标准。因此与其他工具（如 Swagger UI）的集成并非一帆风顺。但它仍是非常有创新性的想法。

它有一个有趣且少见的特性：使用同一框架，可以同时创建 API 与 CLI。

由于基于同步 Python Web 框架的上一代标准（WSGI），它无法处理 WebSocket 等，尽管它的性能仍然很高。

/// info | 信息

Hug 由 Timothy Crosley 创建，他也是 <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a> 的作者，这是一个能自动排序 Python 文件中导入的优秀工具。

///

/// check | 启发 **FastAPI** 的想法：

Hug 启发了 APIStar 的部分设计，也是我当时最看好的工具之一，与 APIStar 并列。

Hug 促使 **FastAPI** 使用 Python 类型提示来声明参数，并自动生成定义整个 API 的模式。

Hug 启发 **FastAPI** 在函数中声明 `response` 参数，用于设置 headers 与 cookies。

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5) { #apistar-0-5 }

就在决定动手构建 **FastAPI** 之前，我找到了 **APIStar** 服务器。它几乎具备我想要的一切，设计也很出色。

在我见过的框架中，它是最早使用 Python 类型提示来声明参数和请求的实现之一（早于 NestJS 与 Molten）。我与 Hug 几乎同时发现了它。但 APIStar 使用了 OpenAPI 标准。

它基于相同的类型提示，在多处自动进行数据校验、序列化并生成 OpenAPI 模式。

请求体模式定义并未使用与 Pydantic 相同的 Python 类型提示，它更接近 Marshmallow，因此编辑器支持不如 Pydantic 好，但即便如此，APIStar 仍是当时可用的最佳选择。

它在当时拥有最好的性能基准（仅被 Starlette 超越）。

起初它没有自动 API 文档 Web 界面，但我知道我可以把 Swagger UI 加进去。

它有一个依赖注入系统。与上文提到的其他工具一样，需要预先注册组件。但这依然是很棒的特性。

我从未在完整项目中使用过它，因为它没有安全集成，因此我无法用它替代基于 Flask-apispec 的全栈脚手架所具备的全部功能。我曾把“提交一个增加该功能的 PR”放在了待办里。

但随后，项目的重心发生了变化。

它不再是一个 API Web 框架，因为作者需要专注于 Starlette。

现在 APIStar 是一组用于校验 OpenAPI 规范的工具，而不是 Web 框架。

/// info | 信息

APIStar 由 Tom Christie 创建。他还创建了：

* Django REST Framework
* Starlette（**FastAPI** 基于其之上）
* Uvicorn（被 Starlette 与 **FastAPI** 使用）

///

/// check | 启发 **FastAPI**：

诞生。

用同一套 Python 类型同时声明多件事（数据校验、序列化与文档），并且还能提供出色的编辑器支持——我认为这是个极其巧妙的想法。

在长时间寻找与测试多种替代之后，APIStar 是当时最好的选择。

随后 APIStar 不再作为服务器存在，而 Starlette 出现，成为实现该体系的更佳基础。这成为构建 **FastAPI** 的最终灵感来源。

我把 **FastAPI** 视为 APIStar 的“精神续作”，并在此基础上，结合前述工具的经验，改进并增强了功能、类型系统及其他各方面。

///

## **FastAPI** 所使用的组件 { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic 是一个基于 Python 类型提示来定义数据校验、序列化与文档（使用 JSON Schema）的库。

这使得它极其直观。

它可与 Marshmallow 类比。尽管在基准测试中它比 Marshmallow 更快。并且由于同样基于 Python 类型提示，编辑器支持优秀。

/// check | **FastAPI** 用它来：

处理所有数据校验、数据序列化与自动模型文档（基于 JSON Schema）。

随后 **FastAPI** 会把这些 JSON Schema 数据纳入 OpenAPI（以及完成其他所有工作）。

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette 是一个轻量级的 <dfn title="构建异步 Python Web 应用的新标准">ASGI</dfn> 框架/工具集，非常适合构建高性能的 asyncio 服务。

它非常简单直观。被设计为易于扩展，且具有模块化组件。

它具备：

* 性能极其出色。
* 支持 WebSocket。
* 进程内后台任务。
* 启动与停止事件。
* 基于 HTTPX 的测试客户端。
* CORS、GZip、静态文件、流式响应。
* 会话与 Cookie 支持。
* 100% 测试覆盖率。
* 100% 类型注解的代码库。
* 极少的强依赖。

Starlette 目前是测试中最快的 Python 框架。仅次于 Uvicorn，它不是框架，而是服务器。

Starlette 提供了 Web 微框架的全部基础能力。

但它不提供自动的数据校验、序列化或文档。

这正是 **FastAPI** 在其之上增加的主要内容之一，全部基于 Python 类型提示（通过 Pydantic）。此外还有依赖注入系统、安全工具、OpenAPI 模式生成等。

/// note | 技术细节

ASGI 是由 Django 核心团队成员推动的新“标准”。它尚不是正式的“Python 标准”（PEP），尽管正朝此方向推进。

尽管如此，已有多种工具将其作为“标准”使用。这极大提升了互操作性：你可以把 Uvicorn 换成其他 ASGI 服务器（如 Daphne 或 Hypercorn），或添加 ASGI 兼容的工具，如 `python-socketio`。

///

/// check | **FastAPI** 用它来：

处理所有核心 Web 部分，并在其之上扩展功能。

`FastAPI` 类本身直接继承自 `Starlette`。

因此，凡是你能用 Starlette 完成的事，也能直接用 **FastAPI** 完成；可以把它看作“加速版”的 Starlette。

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn 是一个基于 uvloop 与 httptools 构建的极速 ASGI 服务器。

它不是 Web 框架，而是服务器。例如它不提供按路径路由的工具——这是 Starlette（或 **FastAPI**）这类框架在其之上提供的功能。

它是 Starlette 与 **FastAPI** 推荐的服务器。

/// check | **FastAPI** 推荐将其作为：

运行 **FastAPI** 应用的主要 Web 服务器。

你也可以使用 `--workers` 命令行选项以获得异步的多进程服务器。

更多细节见[部署](deployment/index.md){.internal-link target=_blank}一节。

///

## 基准与速度 { #benchmarks-and-speed }

要理解、比较并查看 Uvicorn、Starlette 与 FastAPI 之间的差异，请查看[基准](benchmarks.md){.internal-link target=_blank}一节。

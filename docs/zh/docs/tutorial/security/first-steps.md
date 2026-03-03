# 安全 - 第一步 { #security-first-steps }

假设你的**后端** API 位于某个域名下。

而**前端**在另一个域名，或同一域名的不同路径（或在移动应用中）。

你希望前端能通过**username** 和 **password** 与后端进行身份验证。

我们可以用 **OAuth2** 在 **FastAPI** 中实现它。

但为了节省你的时间，不必为获取少量信息而通读冗长的规范。

我们直接使用 **FastAPI** 提供的安全工具。

## 效果预览 { #how-it-looks }

先直接运行代码看看效果，之后再回过头理解其背后的原理。

## 创建 `main.py` { #create-main-py }

把下面的示例代码复制到 `main.py`：

{* ../../docs_src/security/tutorial001_an_py310.py *}

## 运行 { #run-it }

/// info | 信息

当你使用命令 `pip install "fastapi[standard]"` 安装 **FastAPI** 时，<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> 包会自动安装。

但是，如果你使用 `pip install fastapi`，默认不会包含 `python-multipart` 包。

如需手动安装，请先创建并激活[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，然后执行：

```console
$ pip install python-multipart
```

这是因为 **OAuth2** 使用“表单数据”来发送 `username` 和 `password`。

///

用下面的命令运行示例：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 查看 { #check-it }

打开交互式文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到类似这样的界面：

<img src="/img/tutorial/security/image01.png">

/// check | Authorize 按钮！

页面右上角已经有一个崭新的“Authorize”按钮。

你的*路径操作*右上角还有一个可点击的小锁图标。

///

点击它，会弹出一个授权表单，可输入 `username` 和 `password`（以及其它可选字段）：

<img src="/img/tutorial/security/image02.png">

/// note | 注意

目前无论在表单中输入什么都不会生效，我们稍后就会实现它。

///

这当然不是面向最终用户的前端，但它是一个很棒的自动化工具，可交互式地为整个 API 提供文档。

前端团队（也可能就是你自己）可以使用它。

第三方应用和系统也可以使用它。

你也可以用它来调试、检查和测试同一个应用。

## `password` 流 { #the-password-flow }

现在回过头来理解这些内容。

`password` “流”（flow）是 OAuth2 定义的处理安全与身份验证的一种方式。

OAuth2 的设计目标是让后端或 API 与负责用户认证的服务器解耦。

但在这个例子中，**FastAPI** 应用同时处理 API 和认证。

从这个简化的角度来看看流程：

* 用户在前端输入 `username` 和 `password`，然后按下 `Enter`。
* 前端（运行在用户浏览器中）把 `username` 和 `password` 发送到我们 API 中的特定 URL（使用 `tokenUrl="token"` 声明）。
* API 校验 `username` 和 `password`，并返回一个“令牌”（这些我们尚未实现）。
    * “令牌”只是一个字符串，包含一些内容，之后可用来验证该用户。
    * 通常，令牌会在一段时间后过期。
        * 因此，用户过一段时间需要重新登录。
        * 如果令牌被窃取，风险也更小。它不像一把永久有效的钥匙（在大多数情况下）。
* 前端会把令牌临时存储在某处。
* 用户在前端中点击跳转到前端应用的其他部分。
* 前端需要从 API 获取更多数据。
    * 但该端点需要身份验证。
    * 因此，为了与我们的 API 进行身份验证，它会发送一个 `Authorization` 请求头，值为 `Bearer ` 加上令牌。
    * 如果令牌内容是 `foobar`，`Authorization` 请求头的内容就是：`Bearer foobar`。

## **FastAPI** 的 `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** 在不同抽象层级提供了多种安全工具。

本示例将使用 **OAuth2** 的 **Password** 流程并配合 **Bearer** 令牌，通过 `OAuth2PasswordBearer` 类来实现。

/// info | 信息

“Bearer” 令牌并非唯一选项。

但它非常适合我们的用例。

对于大多数用例，它也可能是最佳选择，除非你是 OAuth2 专家，并明确知道为何其他方案更适合你的需求。

在那种情况下，**FastAPI** 同样提供了相应的构建工具。

///

创建 `OAuth2PasswordBearer` 类实例时，需要传入 `tokenUrl` 参数。该参数包含客户端（运行在用户浏览器中的前端）用来发送 `username` 和 `password` 以获取令牌的 URL。

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | 提示

这里的 `tokenUrl="token"` 指向的是尚未创建的相对 URL `token`，等价于 `./token`。

因为使用的是相对 URL，若你的 API 位于 `https://example.com/`，它将指向 `https://example.com/token`；若你的 API 位于 `https://example.com/api/v1/`，它将指向 `https://example.com/api/v1/token`。

使用相对 URL 很重要，这能确保你的应用在诸如[使用代理](../../advanced/behind-a-proxy.md){.internal-link target=_blank}等高级用例中依然正常工作。

///

这个参数不会创建该端点/*路径操作*，而是声明客户端应使用 `/token` 这个 URL 来获取令牌。这些信息会用于 OpenAPI，进而用于交互式 API 文档系统。

我们很快也会创建对应的实际路径操作。

/// info | 信息

如果你是非常严格的 “Pythonista”，可能不喜欢使用参数名 `tokenUrl` 而不是 `token_url`。

这是因为它使用了与 OpenAPI 规范中相同的名称。这样当你需要深入了解这些安全方案时，可以直接复制粘贴去查找更多信息。

///

`oauth2_scheme` 变量是 `OAuth2PasswordBearer` 的一个实例，同时它也是“可调用”的。

可以像这样调用：

```Python
oauth2_scheme(some, parameters)
```

因此，它可以与 `Depends` 一起使用。

### 使用 { #use-it }

现在你可以通过 `Depends` 将 `oauth2_scheme` 作为依赖传入。

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

该依赖会提供一个 `str`，赋值给*路径操作函数*的参数 `token`。

**FastAPI** 会据此在 OpenAPI 架构（以及自动生成的 API 文档）中定义一个“安全方案”。

/// info | 技术细节

**FastAPI** 之所以知道可以使用（在依赖中声明的）`OAuth2PasswordBearer` 在 OpenAPI 中定义安全方案，是因为它继承自 `fastapi.security.oauth2.OAuth2`，而后者又继承自 `fastapi.security.base.SecurityBase`。

所有与 OpenAPI（以及自动 API 文档）集成的安全工具都继承自 `SecurityBase`，这就是 **FastAPI** 能将它们集成到 OpenAPI 的方式。

///

## 它做了什么 { #what-it-does }

它会在请求中查找 `Authorization` 请求头，检查其值是否为 `Bearer ` 加上一些令牌，并将该令牌作为 `str` 返回。

如果没有 `Authorization` 请求头，或者其值不包含 `Bearer ` 令牌，它会直接返回 401 状态码错误（`UNAUTHORIZED`）。

你甚至无需检查令牌是否存在即可返回错误；只要你的函数被执行，就可以确定会拿到一个 `str` 类型的令牌。

你已经可以在交互式文档中试试了：

<img src="/img/tutorial/security/image03.png">

我们还没有验证令牌是否有效，但这已经是一个良好的开端。

## 小结 { #recap }

只需增加三四行代码，你就已经拥有了一种初步的安全机制。

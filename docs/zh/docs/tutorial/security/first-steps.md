# 安全 - 第一步 { #security-first-steps }

假设你有一个 **backend** API，在某个域名下。

并且你有一个 **frontend**，在另一个域名下，或是在同一域名的不同路径下（或是在移动应用中）。

并且你希望前端能使用 **username** 与 **password** 向后端进行身份验证。

我们可以使用 **OAuth2** 来配合 **FastAPI** 构建它。

但我们先帮你省下阅读那份冗长完整规范的时间，你只是想找到你需要的那一点点信息。

让我们使用 **FastAPI** 提供的工具来处理安全。

## 效果如下 { #how-it-looks }

我们先直接用代码看看它如何工作，然后再回过头来理解发生了什么。

## 创建 `main.py` { #create-main-py }

把示例复制到 `main.py` 文件中：

{* ../../docs_src/security/tutorial001_an_py39.py *}

## 运行 { #run-it }

/// info | 信息

当你运行 `pip install "fastapi[standard]"` 命令时，<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> 包会随 **FastAPI** 自动安装。

不过，如果你使用 `pip install fastapi` 命令，默认不会包含 `python-multipart` 包。

要手动安装它，请确保你创建了一个[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，激活它，然后用下面的命令安装：

```console
$ pip install python-multipart
```

这是因为 **OAuth2** 使用“form data”来发送 `username` 和 `password`。

///

用下面命令运行示例：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 检查 { #check-it }

打开交互式文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到类似这样的内容：

<img src="/img/tutorial/security/image01.png">

/// check | Authorize button!

你已经有了一个闪亮的新“Authorize”按钮。

并且你的 *路径操作* 右上角有一个小锁图标可以点击。

///

如果你点击它，会出现一个小的授权表单，用来输入 `username` 和 `password`（以及其他可选字段）：

<img src="/img/tutorial/security/image02.png">

/// note | 注意

你在表单里输入什么都无所谓，它现在还不会工作。但我们很快会讲到。

///

当然，这不是给最终用户使用的前端，但它是一个很棒的自动化工具，可以用交互方式为你的全部 API 生成文档。

前端团队可以使用它（也可能就是你自己）。

第三方应用和系统也可以使用它。

你自己也可以用它来调试、检查和测试同一个应用。

## `password` 流 { #the-password-flow }

现在我们退一步，来理解这一切是什么。

`password` “流”是 OAuth2 定义的处理安全与身份验证的一种方式（“流”）。

OAuth2 的设计目标是让后端或 API 可以独立于进行用户身份验证的服务器。

但在这个例子中，将由同一个 **FastAPI** 应用来处理 API 和身份验证。

因此，从这个简化视角来回顾一下：

* 用户在前端输入 `username` 和 `password`，然后按下 `Enter`。
* 前端（在用户浏览器中运行）把 `username` 和 `password` 发送到我们 API 中的某个特定 URL（用 `tokenUrl="token"` 声明）。
* API 校验 `username` 与 `password`，并用一个“token”进行响应（我们还没实现任何这些）。
    * “token” 只是一个包含某些内容的字符串，我们之后可以用它来验证该用户。
    * 通常，token 会在一段时间后过期。
        * 因此，用户之后某个时间点需要再次登录。
        * 并且如果 token 被盗，风险更小。它不像永久密钥那样会一直有效（在大多数情况下）。
* 前端会在某处临时存储该 token。
* 用户在前端点击进入前端 Web 应用的另一个部分。
* 前端需要从 API 获取更多数据。
    * 但它需要对那个特定的 endpoint 进行身份验证。
    * 因此，为了向我们的 API 进行身份验证，它发送一个 `Authorization` 请求头，其值为 `Bearer ` 加上该 token。
    * 如果 token 是 `foobar`，那么 `Authorization` 请求头的内容会是：`Bearer foobar`。

## **FastAPI** 的 `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** 在不同抽象级别提供了多种工具来实现这些安全特性。

在这个例子中，我们将使用 **OAuth2** 的 **Password** 流，并使用 **Bearer** token。我们通过 `OAuth2PasswordBearer` 类来实现。

/// info | 信息

“bearer” token 不是唯一选项。

但它是最适合我们这个用例的方案。

并且它可能也是大多数用例的最佳方案，除非你是 OAuth2 专家，且非常清楚为什么另一个选项更适合你的需求。

在那种情况下，**FastAPI** 也为你提供了构建它的工具。

///

当我们创建 `OAuth2PasswordBearer` 类的实例时，会传入 `tokenUrl` 参数。该参数包含客户端（用户浏览器中运行的前端）用来发送 `username` 与 `password` 以获取 token 的 URL。

{* ../../docs_src/security/tutorial001_an_py39.py hl[8] *}

/// tip | 提示

这里的 `tokenUrl="token"` 指的是一个我们还没创建的相对 URL `token`。因为它是相对 URL，它等同于 `./token`。

因为我们使用的是相对 URL，如果你的 API 位于 `https://example.com/`，那么它会指向 `https://example.com/token`。但如果你的 API 位于 `https://example.com/api/v1/`，它就会指向 `https://example.com/api/v1/token`。

使用相对 URL 很重要，以确保你的应用即使在类似[位于代理之后](../../advanced/behind-a-proxy.md){.internal-link target=_blank}这样的高级用例中也能继续正常工作。

///

这个参数不会创建该 endpoint / *路径操作*，但会声明客户端应该使用 URL `/token` 来获取 token。这个信息会被用在 OpenAPI 中，进而用于交互式 API 文档系统中。

我们很快也会创建实际的路径操作。

/// info | 信息

如果你是一个非常严格的 “Pythonista”，你可能不喜欢参数名 `tokenUrl` 而不是 `token_url` 的风格。

这是因为它使用了与 OpenAPI 规范中相同的名字。这样，如果你需要进一步研究任何这些安全方案，只要复制粘贴就能找到更多相关信息。

///

`oauth2_scheme` 变量是 `OAuth2PasswordBearer` 的实例，但它也是一个“可调用项”。

它可以这样调用：

```Python
oauth2_scheme(some, parameters)
```

因此，它可以配合 `Depends` 使用。

### 使用 { #use-it }

现在你可以用 `Depends` 在依赖项中传入 `oauth2_scheme`。

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

这个依赖项会提供一个 `str`，并赋值给 *路径操作函数* 的参数 `token`。

**FastAPI** 将知道它可以使用这个依赖项在 OpenAPI schema（以及自动 API 文档）中定义一个“security scheme”。

/// info | 技术细节

**FastAPI** 会知道它可以使用（在依赖项中声明的）`OAuth2PasswordBearer` 类在 OpenAPI 中定义 security scheme，因为它继承自 `fastapi.security.oauth2.OAuth2`，而该类又继承自 `fastapi.security.base.SecurityBase`。

所有与 OpenAPI（以及自动 API 文档）集成的安全工具都继承自 `SecurityBase`，这就是 **FastAPI** 知道如何将它们集成到 OpenAPI 中的原因。

///

## 它做了什么 { #what-it-does }

它会在请求中查找 `Authorization` 请求头，检查其值是否为 `Bearer ` 加上某个 token，并将该 token 作为 `str` 返回。

如果没有看到 `Authorization` 请求头，或者其值不包含 `Bearer ` token，它会直接响应 401 状态码错误（`UNAUTHORIZED`）。

你甚至不需要检查 token 是否存在来返回错误。你可以确定：如果你的函数被执行了，那么那个 token 参数里就会有一个 `str`。

你现在就可以在交互式文档中试试看：

<img src="/img/tutorial/security/image03.png">

我们还没有验证 token 的有效性，但这已经是个开始了。

## 小结 { #recap }

所以，只多写 3 或 4 行，你就已经拥有了某种原始形式的安全机制。

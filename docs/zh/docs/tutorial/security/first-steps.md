# 安全性 - 第一步

假设您的 **后端** API在某个域名中。

同时你有一个 **前端** 在另一个域名或在同一域名的不同路径(或在一个移动应用程序)。

您需要有一种方式使用 **用户名** 和 **密码** 让前端与后端进行验证。

我们可以使用 **FastAPI** 和 **OAuth2** 来构建。

但是，让我们为您节省时间来阅读完整的详细说明，以便找到您需要的那些小片段信息。

让我们使用 **FastAPI** 提供的工具来处理安全性。

## 它看起来是什么样

让我们先使用代码，看看它是如何工作的，然后我们会回来理解发生了什么。

## 创建 `main.py`

将示例复制到文件 `main.py` 中:

```Python
{!../../../docs_src/security/tutorial001.py!}
```

## 执行

!!! info
    首先安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>。

    如 `pip install python-multipart` 。

    这是因为 **OAuth2** 使用 "表单数据" 发送 "用户名" 和 "密码" 。

运行示例:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 检查一下

转到交互式文档: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

你会看到这样的东西:

<img src="/img/tutorial/security/image01.png">

!!! check "授权按钮!"
    你已经有了一个崭新的 "授权" 按钮。

    你的 *路径操作* 在右上角有一个小锁，你可以点击它。

 如果你点击它，你有一个小授权表格，输入一个 `username` 和 `password` (和其他可选字段):

<img src="/img/tutorial/security/image02.png">

!!! note
    无论您在表单中输入什么，它都无法工作。但我们会做到的。

这当然不是面向最终用户的前端，但它是一个很好的自动工具，生成所有API的交互文档。

它可以被前端团队使用(也可以是你自己)。

它可以被第三方应用程序和系统使用。

您也可以使用它来调试、检查和测试相同的应用程序。

## `password` 流程

现在让我们回顾一下，理解一下这是什么。

"流程" 是 OAuth2 中定义的处理安全性和身份验证的流程中的一种( "流程们" )。

设计 OAuth2 的目的是使后端或 API 能够独立于对用户进行身份验证的服务器。

但是在本例中，相同的 **FastAPI** 应用程序将处理 API 和身份验证。

所以，让我们从简化的角度来回顾一下:

* 用户在前端输入 `username` 和 `password` 并敲击 `Enter`。
* 前端 (在用户的浏览器中运行) 将 `username` 和 `password` 发送到我们的 API 中的特定 URL， (使用 `tokenUrl="token"` 声明)。
* API 检查 `username` 和 `password`, 并响应一个 "token" (我们还没有实现任何这一点)。
    * 一个 "token" 只是一个字符串，其中包含一些内容，我们稍后可以使用这些内容来验证这个用户。
    * 通常，令牌设置为在一段时间后过期。
        * 因此，用户将不得不在稍后的某个时间再次登录。
        * 如果令牌被盗，风险会更小。它不像一个永久的键，将永远工作(在大多数情况下)。
* 前端在某个地方暂时存 token。
* 用户在前端点击进入前端web应用程序的另一部分。
* 前端需要从API获取更多数据。
    * 但需要对特定端点进行身份验证。
    * 所以，为了验证我们的API，它发送了一个消息头`Authorization` 其值为 `Bearer ` 加上 token 。
    * 如果 token 包含 `foobar`, `Authorization` 消息头的内容将会是: `Bearer foobar`。

## **FastAPI** 的 `OAuth2PasswordBearer`

**FastAPI** 提供了数个工具，在不同的抽象级别上，实现这些安全特性。


在本例中，我们将使用 **OAuth2** 的 **Password** 流程，该流程使用一个 **Bearer** token。我们使用 `OAuth2PasswordBearer` 类来实现这一点。

!!! info
    "bearer" token  并不是唯一的选择。

    但对于我们的用例来说，它是最好的。

    对于大多数用例来说，它可能是最好的，除非您是 OAuth2 专家，并且确切知道为什么有另一种选择更适合您的需求。

    在这个用例里，**FastAPI** 还为您提供了构建它的工具。

When we create an instance of the `OAuth2PasswordBearer` class we pass in the `tokenUrl` parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the `username` and `password` in order to get a token. 
当我们创建 `OAuth2PasswordBearer` 类的实例时，我们传入 `tokenUrl` 参数。此参数包含客户端(在用户浏览器中运行的前端)将用于发送 `username` 和 `password` 以获取令牌的URL。

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! tip
    这里 `tokenUrl="token"` 代表了一个相对 URL `token` ，我们尚未实现它。 因为它是一个相对 URL， 所以它相当于 `./token`.

    因为我们使用的是相对 URL，如果您的 API 位于 `https://example.com/`, 那么它将代表 `https://example.com/token`. 但是如果您的API位于 `https://example.com/api/v1/`, 那么它将代表 `https://example.com/api/v1/token`.

    使用相对URL是很重要的，它可以确保你的应用程序即使在高级用例中如 [Behind a Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank} 也能继续工作。

该参数不创建端点 / *路径操作*, 但声明 URL `/token` 将是客户端用于获取令牌的URL。这些信息在 OpenAPI 中使用，然后在交互式 API 文档系统中使用。

我们将很快创建实际的路径操作。

!!! info
    如果您是一个非常严格的 "Pythonista" 您可能不喜欢参数名是 `tokenUrl` 而不是 `token_url`。

    这是因为它使用了与 OpenAPI 规范中相同的名称，因此如果您需要研究更多关于这些安全方案的信息，您可以复制并粘贴它来查找更多信息。

`oauth2_scheme` 变量是 `OAuth2PasswordBearer` 的一个实例，但是他也是一个 "callable"。

他可以这样被调用:

```Python
oauth2_scheme(some, parameters)
```

所以它也可以被用作 `Depends`。

### 使用它

现在您可以在依赖项中通过 `Depends` 传递 `oauth2_scheme`。

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

这个依赖项将提供一个`str`，它被分配给 *路径操作函数* 的参数 `token` 。

**FastAPI** 知道它可以使用这个依赖关系在 OpenAPI 模式(和自动 API 文档)中定义一个 "安全方案" 。

!!! info "技术细节"
    **FastAPI** 知道它可以使用类 `OAuth2PasswordBearer` (在依赖项中声明)来定义 OpenAPI 中的安全方案，因为它继承自 `fastapi.security.oauth2.OAuth2` ，它又继承自 `fastapi.security.base.SecurityBase`。

    所有与 OpenAPI 集成的安全工具(以及自动 API 文档)都继承自 `SecurityBase` ，这就是为什么 **FastAPI** 知道如何将它们集成到 OpenAPI 中。

## 它做什么

它会在请求中寻找 `Authorization` 消息头，检查值是否为 `Bearer ` 加上一些 token ，并将以 `str` 返回该token。

如果它没有看到一个 `Authorization` 消息头，或者值没有一个 `Bearer ` token ，它将直接响应401状态码错误(`UNAUTHORIZED`)。

您甚至不必检查 token 是否存在以返回错误。您可以确保，如果您的函数被执行，它将在那个 token 中有一个 `str` 。

你可以在互动文档中尝试:

<img src="/img/tutorial/security/image03.png">

我们还没有验证 token 的有效性，但这已经是一个开始。

## 总结

因此，仅在额外的3或4行中，您就已经拥有了某种基本形式的安全性。

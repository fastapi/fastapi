# 安全 - 第一步

假设**后端** API 在某个域。

**前端**在另一个域，或（移动应用中）在同一个域的不同路径下。

并且，前端要使用后端的 **username** 与 **password** 验证用户身份。

固然，**FastAPI** 支持 **OAuth2** 身份验证。

但为了节省开发者的时间，不要只为了查找很少的内容，不得不阅读冗长的规范文档。

我们建议使用 **FastAPI** 的安全工具。

## 概览

首先，看看下面的代码是怎么运行的，然后再回过头来了解其背后的原理。

## 创建 `main.py`

把下面的示例代码复制到 `main.py`：

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/security/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python
    {!> ../../../docs_src/security/tutorial001_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        尽可能选择使用 `Annotated` 的版本。

    ```Python
    {!> ../../../docs_src/security/tutorial001.py!}
    ```

## 运行

!!! info "说明"

    先安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>。

    安装命令： `pip install python-multipart`。

    这是因为 **OAuth2** 使用**表单数据**发送 `username` 与 `password`。

用下面的命令运行该示例：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 查看文档

打开 API 文档： <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs。</a>

界面如下图所示：

<img src="/img/tutorial/security/image01.png">

!!! check "Authorize 按钮！"

    页面右上角出现了一个「**Authorize**」按钮。

    *路径操作*的右上角也出现了一个可以点击的小锁图标。

点击 **Authorize** 按钮，弹出授权表单，输入 `username` 与 `password` 及其它可选字段：

<img src="/img/tutorial/security/image02.png">

!!! note "笔记"

    目前，在表单中输入内容不会有任何反应，后文会介绍相关内容。

虽然此文档不是给前端最终用户使用的，但这个自动工具非常实用，可在文档中与所有 API 交互。

前端团队（可能就是开发者本人）可以使用本工具。

第三方应用与系统也可以调用本工具。

开发者也可以用它来调试、检查、测试应用。

## 密码流

现在，我们回过头来介绍这段代码的原理。

`Password` **流**是 OAuth2 定义的，用于处理安全与身份验证的方式（**流**）。

OAuth2 的设计目标是为了让后端或 API 独立于服务器验证用户身份。

但在本例中，**FastAPI** 应用会处理 API 与身份验证。

下面，我们来看一下简化的运行流程：

- 用户在前端输入 `username` 与`password`，并点击**回车**
- （用户浏览器中运行的）前端把 `username` 与`password` 发送至 API 中指定的 URL（使用 `tokenUrl="token"` 声明）
- API 检查 `username` 与`password`，并用令牌（`Token`） 响应（暂未实现此功能）：
  - 令牌只是用于验证用户的字符串
  - 一般来说，令牌会在一段时间后过期
    - 过时后，用户要再次登录
    - 这样一来，就算令牌被人窃取，风险也较低。因为它与永久密钥不同，**在绝大多数情况下**不会长期有效
- 前端临时将令牌存储在某个位置
- 用户点击前端，前往前端应用的其它部件
- 前端需要从 API 中提取更多数据：
    - 为指定的端点（Endpoint）进行身份验证
    - 因此，用 API 验证身份时，要发送值为 `Bearer` + 令牌的请求头 `Authorization`
    - 假如令牌为 `foobar`，`Authorization` 请求头就是： `Bearer foobar`

## **FastAPI** 的 `OAuth2PasswordBearer`

**FastAPI** 提供了不同抽象级别的安全工具。

本例使用 **OAuth2** 的 **Password** 流以及 **Bearer** 令牌（`Token`）。为此要使用 `OAuth2PasswordBearer` 类。

!!! info "说明"

    `Bearer` 令牌不是唯一的选择。

    但它是最适合这个用例的方案。

    甚至可以说，它是适用于绝大多数用例的最佳方案，除非您是 OAuth2 的专家，知道为什么其它方案更合适。

    本例中，**FastAPI** 还提供了构建工具。

创建 `OAuth2PasswordBearer` 的类实例时，要传递 `tokenUrl` 参数。该参数包含客户端（用户浏览器中运行的前端） 的 URL，用于发送 `username` 与 `password`，并获取令牌。

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! tip "提示"

    在此，`tokenUrl="token"` 指向的是暂未创建的相对 URL `token`。这个相对 URL 相当于 `./token`。

    因为使用的是相对 URL，如果 API 位于 `https://example.com/`，则指向 `https://example.com/token`。但如果 API 位于 `https://example.com/api/v1/`，它指向的就是`https://example.com/api/v1/token`。

    使用相对 URL 非常重要，可以确保应用在遇到[使用代理](../../advanced/behind-a-proxy.md){.internal-link target=_blank}这样的高级用例时，也能正常运行。

该参数不会创建端点或*路径操作*，但会声明客户端用来获取令牌的 URL `/token` 。此信息用于 OpenAPI 及 API 文档。

接下来，学习如何创建实际的路径操作。

!!! info "说明"

    严苛的 **Pythonista** 可能不喜欢用 `tokenUrl` 这种命名风格代替 `token_url`。

    这种命名方式是因为要使用与 OpenAPI 规范中相同的名字。以便在深入校验安全方案时，能通过复制粘贴查找更多相关信息。

`oauth2_scheme` 变量是 `OAuth2PasswordBearer` 的实例，也是**可调用项**。

以如下方式调用：

```Python
oauth2_scheme(some, parameters)
```

因此，`Depends` 可以调用 `oauth2_scheme` 变量。

### 使用

接下来，使用 `Depends` 把 `oauth2_scheme` 传入依赖项。

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

该依赖项使用字符串（`str`）接收*路径操作函数*的参数 `token` 。

**FastAPI** 使用依赖项在 OpenAPI 概图（及 API 文档）中定义**安全方案**。

!!! info "技术细节"

    **FastAPI** 使用（在依赖项中声明的）类 `OAuth2PasswordBearer` 在 OpenAPI 中定义安全方案，这是因为它继承自 `fastapi.security.oauth2.OAuth2`，而该类又是继承自`fastapi.security.base.SecurityBase`。

    所有与 OpenAPI（及 API 文档）集成的安全工具都继承自 `SecurityBase`， 这就是为什么 **FastAPI** 能把它们集成至 OpenAPI 的原因。

## 实现的操作

FastAPI 校验请求中的 `Authorization` 请求头，核对请求头的值是不是由 `Bearer ` ＋ 令牌组成， 并返回令牌字符串（`str`）。

如果没有找到 `Authorization` 请求头，或请求头的值不是 `Bearer ` ＋ 令牌。FastAPI 直接返回 401 错误状态码（`UNAUTHORIZED`）。

开发者不需要检查错误信息，查看令牌是否存在，只要该函数能够执行，函数中就会包含令牌字符串。

正如下图所示，API 文档已经包含了这项功能：

<img src="/img/tutorial/security/image03.png">

目前，暂时还没有实现验证令牌是否有效的功能，不过后文很快就会介绍的。

## 小结

看到了吧，只要多写三四行代码，就可以添加基础的安全表单。

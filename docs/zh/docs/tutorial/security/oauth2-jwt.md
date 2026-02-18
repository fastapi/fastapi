# 使用密码（及哈希）的 OAuth2，基于 JWT 的 Bearer 令牌 { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

现在我们已经有了完整的安全流程，接下来用 <abbr title="JSON Web Tokens - JSON Web 令牌">JWT</abbr> 令牌和安全的密码哈希，让应用真正安全起来。

这些代码可以直接用于你的应用，你可以把密码哈希保存到数据库中，等等。

我们将从上一章结束的地方继续，逐步完善。

## 关于 JWT { #about-jwt }

JWT 意为 “JSON Web Tokens”。

它是一种标准，把一个 JSON 对象编码成没有空格、很密集的一长串字符串。看起来像这样：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

它不是加密的，所以任何人都可以从内容中恢复信息。

但它是“签名”的。因此，当你收到一个自己签发的令牌时，你可以验证它确实是你签发的。

这样你就可以创建一个例如有效期为 1 周的令牌。然后当用户第二天带着这个令牌回来时，你能知道该用户仍然处于登录状态。

一周后令牌过期，用户将不再被授权，需要重新登录以获取新令牌。而如果用户（或第三方）尝试修改令牌来更改过期时间，你也能发现，因为签名将不匹配。

如果你想动手体验 JWT 令牌并了解它的工作方式，请访问 <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>。

## 安装 `PyJWT` { #install-pyjwt }

我们需要安装 `PyJWT`，以便在 Python 中生成和校验 JWT 令牌。

请确保创建并激活一个[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，然后安装 `pyjwt`：

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | 信息

如果你计划使用类似 RSA 或 ECDSA 的数字签名算法，你应该安装加密库依赖项 `pyjwt[crypto]`。

可以在 <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT 安装文档</a>中了解更多。

///

## 密码哈希 { #password-hashing }

“哈希”是指把一些内容（这里是密码）转换成看起来像乱码的一串字节（其实就是字符串）。

当你每次传入完全相同的内容（完全相同的密码）时，都会得到完全相同的“乱码”。

但你无法从这个“乱码”反向还原出密码。

### 为什么使用密码哈希 { #why-use-password-hashing }

如果你的数据库被盗，窃贼拿到的不会是用户的明文密码，而只是哈希值。

因此，窃贼无法把该密码拿去尝试登录另一个系统（很多用户在各处都用相同的密码，这将非常危险）。

## 安装 `pwdlib` { #install-pwdlib }

pwdlib 是一个用于处理密码哈希的优秀 Python 包。

它支持多种安全的哈希算法以及相关工具。

推荐的算法是 “Argon2”。

请确保创建并激活一个[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，然后安装带 Argon2 的 pwdlib：

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | 提示

使用 `pwdlib`，你甚至可以把它配置为能够读取由 **Django**、**Flask** 安全插件或其他许多工具创建的密码。

例如，你可以在数据库中让一个 Django 应用和一个 FastAPI 应用共享同一份数据。或者在使用同一个数据库的前提下，逐步迁移一个 Django 应用到 FastAPI。

同时，你的用户既可以从 Django 应用登录，也可以从 **FastAPI** 应用登录。

///

## 哈希并校验密码 { #hash-and-verify-the-passwords }

从 `pwdlib` 导入所需工具。

用推荐设置创建一个 PasswordHash 实例——它将用于哈希与校验密码。

/// tip | 提示

pwdlib 也支持 bcrypt 哈希算法，但不包含遗留算法——如果需要处理过时的哈希，建议使用 passlib 库。

例如，你可以用它读取并校验其他系统（如 Django）生成的密码，但对任何新密码使用不同的算法（如 Argon2 或 Bcrypt）进行哈希。

并且能够同时与它们全部兼容。

///

创建一个工具函数来哈希用户传入的密码。

再创建一个工具函数来校验接收的密码是否匹配已存储的哈希。

再创建一个工具函数来进行身份验证并返回用户。

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

当使用一个在数据库中不存在的用户名调用 `authenticate_user` 时，我们仍然会针对一个虚拟哈希运行 `verify_password`。

这可以确保无论用户名是否有效，端点的响应时间大致相同，从而防止可用于枚举已存在用户名的“时间攻击”（timing attacks）。

/// note | 注意

如果你查看新的（伪）数据库 `fake_users_db`，现在你会看到哈希后的密码类似这样：`"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`。

///

## 处理 JWT 令牌 { #handle-jwt-tokens }

导入已安装的模块。

创建一个用于对 JWT 令牌进行签名的随机密钥。

使用下列命令生成一个安全的随机密钥：

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

把输出复制到变量 `SECRET_KEY`（不要使用示例中的那个）。

创建变量 `ALGORITHM`，设置用于签名 JWT 令牌的算法，这里设为 `"HS256"`。

创建一个变量用于设置令牌的过期时间。

定义一个用于令牌端点响应的 Pydantic 模型。

创建一个生成新访问令牌的工具函数。

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## 更新依赖项 { #update-the-dependencies }

更新 `get_current_user` 以接收与之前相同的令牌，但这次使用的是 JWT 令牌。

解码接收到的令牌，进行校验，并返回当前用户。

如果令牌无效，立即返回一个 HTTP 错误。

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## 更新 `/token` 路径操作 { #update-the-token-path-operation }

用令牌的过期时间创建一个 `timedelta`。

创建一个真正的 JWT 访问令牌并返回它。

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### 关于 JWT “主题” `sub` 的技术细节 { #technical-details-about-the-jwt-subject-sub }

JWT 规范中有一个 `sub` 键，表示令牌的“主题”（subject）。

使用它是可选的，但通常会把用户的标识放在这里，所以本例中我们使用它。

JWT 除了用于识别用户并允许其直接在你的 API 上执行操作之外，还可能用于其他场景。

例如，你可以用它来标识一辆“车”或一篇“博客文章”。

然后你可以为该实体添加权限，比如“drive”（用于车）或“edit”（用于博客）。

接着，你可以把这个 JWT 令牌交给一个用户（或机器人），他们就可以在没有账户的前提下，仅凭你的 API 生成的 JWT 令牌来执行这些操作（开车、编辑文章）。

基于这些想法，JWT 可以用于更复杂的场景。

在这些情况下，多个实体可能会有相同的 ID，比如都叫 `foo`（用户 `foo`、车 `foo`、博客文章 `foo`）。

因此，为了避免 ID 冲突，在为用户创建 JWT 令牌时，你可以给 `sub` 键的值加一个前缀，例如 `username:`。所以在这个例子中，`sub` 的值可以是：`username:johndoe`。

需要牢记的一点是，`sub` 键在整个应用中应该是一个唯一标识符，并且它应该是字符串。

## 检查 { #check-it }

运行服务器并打开文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到这样的用户界面：

<img src="/img/tutorial/security/image07.png">

像之前一样进行授权。

使用以下凭证：

用户名: `johndoe`
密码: `secret`

/// check | 检查

注意，代码中的任何地方都没有明文密码 “`secret`”，我们只有它的哈希版本。

///

<img src="/img/tutorial/security/image08.png">

调用 `/users/me/` 端点，你将得到如下响应：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

如果你打开开发者工具，你会看到发送的数据只包含令牌。密码只会在第一个请求中用于认证用户并获取访问令牌，之后就不会再发送密码了：

<img src="/img/tutorial/security/image10.png">

/// note | 注意

注意 `Authorization` 请求头，其值以 `Bearer ` 开头。

///

## 使用 `scopes` 的高级用法 { #advanced-usage-with-scopes }

OAuth2 支持 “scopes”（作用域）。

你可以用它们为 JWT 令牌添加一组特定的权限。

然后你可以把这个令牌直接交给用户或第三方，在一组限制条件下与 API 交互。

在**高级用户指南**中你将学习如何使用它们，以及它们如何集成进 **FastAPI**。

## 小结 { #recap }

通过目前所学内容，你可以使用 OAuth2 和 JWT 等标准来搭建一个安全的 **FastAPI** 应用。

在几乎任何框架中，处理安全问题都会很快变得相当复杂。

许多把安全流程大幅简化的包，往往要在数据模型、数据库和可用特性上做出大量妥协。而有些过度简化的包实际上在底层存在安全隐患。

---

**FastAPI** 不会在任何数据库、数据模型或工具上做妥协。

它给予你完全的灵活性，选择最适合你项目的方案。

而且你可以直接使用许多维护良好、广泛使用的包，比如 `pwdlib` 和 `PyJWT`，因为 **FastAPI** 不需要复杂机制来集成外部包。

同时它也为你提供尽可能简化流程的工具，而不牺牲灵活性、健壮性或安全性。

你可以以相对简单的方式使用和实现像 OAuth2 这样的安全、标准协议。

在**高级用户指南**中，你可以进一步了解如何使用 OAuth2 的 “scopes”，以遵循相同标准实现更细粒度的权限系统。带作用域的 OAuth2 是许多大型身份认证提供商（如 Facebook、Google、GitHub、Microsoft、X（Twitter）等）用来授权第三方应用代表其用户与其 API 交互的机制。

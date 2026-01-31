# 使用密码（及哈希）的 OAuth2，使用 JWT 令牌的 Bearer { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

现在我们已经完成了所有安全流，让我们使用 <abbr title="JSON Web Tokens">JWT</abbr> 令牌和安全的密码哈希，让应用真正变得安全。

这段代码是你可以在应用中实际使用的代码，把密码哈希保存到数据库中等。

我们将从上一章结束的地方继续，并逐步完善。

## 关于 JWT { #about-jwt }

JWT 的意思是 “JSON Web Tokens”。

它是一种标准，用于将 JSON 对象编码为一个没有空格的、很长且紧凑的字符串。看起来像这样：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

它不是加密的，所以任何人都可以从内容中恢复信息。

但它是签名的。所以，当你收到一个你自己签发的令牌时，你可以验证它确实是由你签发的。

这样，你可以创建一个过期时间为，比如 1 周的令牌。然后当用户第二天带着令牌回来时，你就知道该用户仍然处于登录状态。

一周后，令牌会过期，用户将不会被授权，并且必须再次登录以获得新令牌。而如果用户（或第三方）尝试修改令牌来改变过期时间，你也能发现，因为签名将不匹配。

如果你想体验 JWT 令牌并看看它们如何工作，请查看 <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>。

## 安装 `PyJWT` { #install-pyjwt }

我们需要安装 `PyJWT`，以便在 Python 中生成并校验 JWT 令牌。

确保你创建一个[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，激活它，然后安装 `pyjwt`：

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | 信息

如果你计划使用类似 RSA 或 ECDSA 的数字签名算法，你应该安装 cryptography 库依赖 `pyjwt[crypto]`。

你可以在 <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT Installation docs</a> 中阅读更多内容。

///

## 密码哈希 { #password-hashing }

“哈希（Hashing）”指的是把某些内容（本例中是密码）转换为一串字节（也就是一个字符串），看起来像乱码。

每次传入完全相同的内容（完全相同的密码），你都会得到完全相同的乱码。

但你无法从乱码反推回原始密码。

### 为什么要使用密码哈希 { #why-use-password-hashing }

如果你的数据库被盗，盗贼拿不到用户的明文密码，只能拿到哈希。

因此，盗贼就无法尝试在其他系统中使用该密码（很多用户在所有地方都用同一个密码，这会很危险）。

## 安装 `pwdlib` { #install-pwdlib }

pwdlib 是一个很棒的 Python 包，用于处理密码哈希。

它支持很多安全的哈希算法以及相关的工具。

推荐的算法是 “Argon2”。

确保你创建一个[虚拟环境](../../virtual-environments.md){.internal-link target=_blank}，激活它，然后安装带 Argon2 的 pwdlib：

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | 提示

使用 `pwdlib`，你甚至可以配置它，使其能够读取由 **Django**、某个 **Flask** 安全插件或其他许多工具创建的密码。

所以，例如，你可以让 FastAPI 应用和 Django 应用共享同一个数据库中的数据。或者使用同一个数据库，逐步迁移 Django 应用。

并且你的用户可以同时从 Django 应用或 **FastAPI** 应用登录。

///

## 哈希并校验密码 { #hash-and-verify-the-passwords }

从 `pwdlib` 导入我们需要的工具。

用推荐设置创建一个 PasswordHash 实例——它将用于对密码进行哈希与校验。

/// tip | 提示

pwdlib 也支持 bcrypt 哈希算法，但不包含 legacy 算法——若需要处理过时的哈希，建议使用 passlib 库。

例如，你可以用它读取并校验由其他系统（如 Django）生成的密码，但用 Argon2 或 Bcrypt 之类的不同算法来哈希任何新密码。

并且同时与它们全部兼容。

///

创建一个工具函数，用来对来自用户的密码进行哈希。

再创建一个工具函数，用来校验接收到的密码是否与存储的哈希匹配。

再创建一个函数，用来验证并返回用户。

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,56:57,60:61,70:76] *}

/// note | 注意

如果你查看新的（伪）数据库 `fake_users_db`，你会看到现在哈希后的密码长这样：`"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`。

///

## 处理 JWT 令牌 { #handle-jwt-tokens }

导入已安装的模块。

创建一个随机密钥，用来签名 JWT 令牌。

要生成一个安全的随机密钥，使用命令：

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

然后把输出复制到变量 `SECRET_KEY`（不要使用示例中的这个）。

创建一个变量 `ALGORITHM`，用于指定 JWT 令牌签名算法，并将其设置为 `"HS256"`。

创建一个变量，用于令牌的过期时间。

定义一个 Pydantic Model，用于 token 端点的响应。

创建一个工具函数，用于生成新的访问令牌。

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,79:87] *}

## 更新依赖项 { #update-the-dependencies }

更新 `get_current_user`，让它接收和之前相同的令牌，但这次使用的是 JWT 令牌。

解码接收到的令牌，验证它，然后返回当前用户。

如果令牌无效，立刻返回一个 HTTP 错误。

{* ../../docs_src/security/tutorial004_an_py310.py hl[90:107] *}

## 更新 `/token` *路径操作* { #update-the-token-path-operation }

使用令牌的过期时间创建一个 `timedelta`。

创建一个真正的 JWT 访问令牌并返回。

{* ../../docs_src/security/tutorial004_an_py310.py hl[118:133] *}

### 关于 JWT “subject” `sub` 的技术细节 { #technical-details-about-the-jwt-subject-sub }

JWT 规范说有一个键 `sub`，表示令牌的 subject。

它是可选的，但你会在这里放用户的标识，所以我们在这里使用它。

JWT 除了用于识别用户并允许他们直接对你的 API 执行操作外，还可能用于其他事情。

例如，你可以识别一辆“车”或一篇“博客文章”。

然后你可以为该实体添加权限，比如“驾驶”（车）或“编辑”（博客）。

然后，你可以把 JWT 令牌交给某个用户（或 bot），他们就可以用它来执行那些动作（驾驶车，或编辑博客文章），甚至不需要有账号，只要有你的 API 为此生成的 JWT 令牌即可。

基于这些思路，JWT 可以用于更复杂得多的场景。

在这些情况下，其中多个实体可能拥有相同的 ID，比如 `foo`（用户 `foo`、车 `foo`、博客文章 `foo`）。

因此，为了避免 ID 冲突，在为用户创建 JWT 令牌时，你可以给 `sub` 键的值加上前缀，例如 `username:`。所以在这个例子中，`sub` 的值可以是：`username:johndoe`。

需要记住的重要一点是：`sub` 键应该在整个应用中具有唯一标识符，并且它应该是一个字符串。

## 检查 { #check-it }

运行服务器并访问文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到这样的用户界面：

<img src="/img/tutorial/security/image07.png">

用与之前相同的方式对应用进行授权。

使用如下凭证：

Username: `johndoe`
Password: `secret`

/// check

注意，代码中没有任何地方出现明文密码 "`secret`"，我们只有哈希后的版本。

///

<img src="/img/tutorial/security/image08.png">

调用端点 `/users/me/`，你会得到如下响应：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

如果你打开开发者工具，你会看到发送的数据只包含令牌；密码只会在第一个请求中发送，用于验证用户并获取访问令牌，之后不会再发送：

<img src="/img/tutorial/security/image10.png">

/// note | 注意

注意请求头 `Authorization`，其值以 `Bearer ` 开头。

///

## `scopes` 的高级用法 { #advanced-usage-with-scopes }

OAuth2 有 “scopes” 的概念。

你可以用它们为 JWT 令牌添加一组特定的权限。

然后你可以把这个令牌直接给用户或第三方，让他们在一组限制下与你的 API 交互。

你可以在之后的 **高级用户指南** 中学习如何使用它们，以及它们如何集成到 **FastAPI** 中。

## 小结 { #recap }

通过目前看到的内容，你可以使用 OAuth2 和 JWT 等标准来搭建一个安全的 **FastAPI** 应用。

在几乎任何框架中，处理安全都会很快变成一个相当复杂的话题。

许多大幅简化它的包，不得不在数据模型、数据库以及可用功能上做出大量妥协。而其中一些把事情简化过头的包，实际上底层存在安全缺陷。

---

**FastAPI** 不会在任何数据库、数据模型或工具上做妥协。

它给了你充分的灵活性，让你选择最适合你项目的方案。

并且你可以直接使用很多维护良好且广泛使用的包，比如 `pwdlib` 和 `PyJWT`，因为 **FastAPI** 不需要任何复杂机制就能集成外部包。

但它也提供了工具，尽可能简化这一过程，同时不牺牲灵活性、健壮性或安全性。

并且你可以相对简单地使用并实现安全的标准协议，比如 OAuth2。

你可以在 **高级用户指南** 中了解更多关于如何使用 OAuth2 “scopes” 的内容，以便在遵循相同标准的前提下实现更细粒度的权限系统。带 scopes 的 OAuth2 是许多大型认证服务商使用的机制，例如 Facebook、Google、GitHub、Microsoft、X（Twitter）等，用来授权第三方应用代表用户与其 API 交互。

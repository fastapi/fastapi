# OAuth2 实现密码哈希与 Bearer  JWT 令牌验证

至此，我们已经编写了所有安全流，本章学习如何使用 <abbr title="JSON Web Tokens">JWT</abbr> 令牌（Token）和安全密码哈希（Hash）实现真正的安全机制。

本章的示例代码真正实现了在应用的数据库中保存哈希密码等功能。

接下来，我们紧接上一章，继续完善安全机制。

## JWT 简介

JWT 即**JSON 网络令牌**（JSON Web Tokens）。

JWT 是一种将 JSON 对象编码为没有空格，且难以理解的长字符串的标准。JWT 的内容如下所示：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

JWT 字符串没有加密，任何人都能用它恢复原始信息。

但 JWT 使用了签名机制。接受令牌时，可以用签名校验令牌。

使用 JWT 创建有效期为一周的令牌。第二天，用户持令牌再次访问时，仍为登录状态。

令牌于一周后过期，届时，用户身份验证就会失败。只有再次登录，才能获得新的令牌。如果用户（或第三方）篡改令牌的过期时间，因为签名不匹配会导致身份验证失败。

如需深入了解 JWT 令牌，了解它的工作方式，请参阅 <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>。

## 安装 `PyJWT`

安装 `PyJWT`，在 Python 中生成和校验 JWT 令牌：

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | 说明

如果您打算使用类似 RSA 或 ECDSA 的数字签名算法，您应该安装加密库依赖项 `pyjwt[crypto]`。

您可以在 <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT Installation docs</a> 获得更多信息。

///

## 密码哈希

**哈希**是指把特定内容（本例中为密码）转换为乱码形式的字节序列（其实就是字符串）。

每次传入完全相同的内容时（比如，完全相同的密码），返回的都是完全相同的乱码。

但这个乱码无法转换回传入的密码。

### 为什么使用密码哈希

原因很简单，假如数据库被盗，窃贼无法获取用户的明文密码，得到的只是哈希值。

这样一来，窃贼就无法在其它应用中使用窃取的密码（要知道，很多用户在所有系统中都使用相同的密码，风险超大）。

## 安装 `passlib`

Passlib 是处理密码哈希的 Python 包。

它支持很多安全哈希算法及配套工具。

本教程推荐的算法是 **Bcrypt**。

因此，请先安装附带 Bcrypt 的 PassLib：

<div class="termy">

```console
$ pip install passlib[bcrypt]

---> 100%
```

</div>

/// tip | 提示

`passlib` 甚至可以读取 Django、Flask 的安全插件等工具创建的密码。

例如，把 Django 应用的数据共享给 FastAPI 应用的数据库。或利用同一个数据库，可以逐步把应用从 Django 迁移到 FastAPI。

并且，用户可以同时从 Django 应用或 FastAPI 应用登录。

///

## 密码哈希与校验

从 `passlib` 导入所需工具。

创建用于密码哈希和身份校验的 PassLib **上下文**。

/// tip | 提示

PassLib 上下文还支持使用不同哈希算法的功能，包括只能校验的已弃用旧算法等。

例如，用它读取和校验其它系统（如 Django）生成的密码，但要使用其它算法，如 Bcrypt，生成新的哈希密码。

同时，这些功能都是兼容的。

///

接下来，创建三个工具函数，其中一个函数用于哈希用户的密码。

第一个函数用于校验接收的密码是否匹配存储的哈希值。

第三个函数用于身份验证，并返回用户。

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,56:57,60:61,70:76] *}

/// note | 笔记

查看新的（伪）数据库 `fake_users_db`，就能看到哈希后的密码：`"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"`。

///

## 处理 JWT 令牌

导入已安装的模块。

创建用于 JWT 令牌签名的随机密钥。

使用以下命令，生成安全的随机密钥：

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

然后，把生成的密钥复制到变量**SECRET_KEY**，注意，不要使用本例所示的密钥。

创建指定 JWT 令牌签名算法的变量 **ALGORITHM**，本例中的值为 `"HS256"`。

创建设置令牌过期时间的变量。

定义令牌端点响应的 Pydantic 模型。

创建生成新的访问令牌的工具函数。

{* ../../docs_src/security/tutorial004.py hl[6,12:14,28:30,78:86] *}

## 更新依赖项

更新 `get_current_user` 以接收与之前相同的令牌，但这里用的是 JWT 令牌。

解码并校验接收到的令牌，然后，返回当前用户。

如果令牌无效，则直接返回 HTTP 错误。

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,79:87] *}

## 更新 `/token` *路径操作*

用令牌过期时间创建 `timedelta` 对象。

创建并返回真正的 JWT 访问令牌。

{* ../../docs_src/security/tutorial004_an_py310.py hl[118:133] *}

### JWT `sub` 的技术细节

JWT 规范还包括 `sub` 键，值是令牌的主题。

该键是可选的，但要把用户标识放在这个键里，所以本例使用了该键。

除了识别用户与许可用户在 API 上直接执行操作之外，JWT 还可能用于其它事情。

例如，识别**汽车**或**博客**。

接着，为实体添加权限，比如**驾驶**（汽车）或**编辑**（博客）。

然后，把 JWT 令牌交给用户（或机器人），他们就可以执行驾驶汽车，或编辑博客等操作。无需注册账户，只要有 API 生成的 JWT 令牌就可以。

同理，JWT 可以用于更复杂的场景。

在这些情况下，多个实体的 ID 可能是相同的，以 ID  `foo` 为例，用户的 ID 是 `foo`，车的 ID 是 `foo`，博客的 ID 也是  `foo`。

为了避免 ID 冲突，在给用户创建 JWT 令牌时，可以为 `sub` 键的值加上前缀，例如 `username:`。因此，在本例中，`sub` 的值可以是：`username:johndoe`。

注意，划重点，`sub` 键在整个应用中应该只有一个唯一的标识符，而且应该是字符串。

## 检查

运行服务器并访问文档： <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

可以看到如下用户界面：

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image07.png">

用与上一章同样的方式实现应用授权。

使用如下凭证：

用户名: `johndoe` 密码: `secret`

/// check | 检查

注意，代码中没有明文密码**`secret`**，只保存了它的哈希值。

///

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image08.png">

调用 `/users/me/` 端点，收到下面的响应：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image09.png">

打开浏览器的开发者工具，查看数据是怎么发送的，而且数据里只包含了令牌，只有验证用户的第一个请求才发送密码，并获取访问令牌，但之后不会再发送密码：

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image10.png">

/// note | 笔记

注意，请求中 `Authorization` 响应头的值以 `Bearer` 开头。

///

## `scopes` 高级用法

OAuth2 支持**`scopes`**（作用域）。

**`scopes`**为 JWT 令牌添加指定权限。

让持有令牌的用户或第三方在指定限制条件下与 API 交互。

**高级用户指南**中将介绍如何使用 `scopes`，及如何把 `scopes` 集成至 **FastAPI**。

## 小结

至此，您可以使用 OAuth2 和 JWT 等标准配置安全的 **FastAPI** 应用。

几乎在所有框架中，处理安全问题很快都会变得非常复杂。

有些包为了简化安全流，不得不在数据模型、数据库和功能上做出妥协。而有些过于简化的软件包其实存在了安全隐患。

---

**FastAPI** 不向任何数据库、数据模型或工具做妥协。

开发者可以灵活选择最适合项目的安全机制。

还可以直接使用 `passlib` 和 `PyJWT` 等维护良好、使用广泛的包，这是因为 **FastAPI** 不需要任何复杂机制，就能集成外部的包。

而且，**FastAPI** 还提供了一些工具，在不影响灵活、稳定和安全的前提下，尽可能地简化安全机制。

**FastAPI** 还支持以相对简单的方式，使用 OAuth2 等安全、标准的协议。

**高级用户指南**中详细介绍了 OAuth2**`scopes`**的内容，遵循同样的标准，实现更精密的权限系统。OAuth2 的作用域是脸书、谷歌、GitHub、微软、推特等第三方身份验证应用使用的机制，让用户授权第三方应用与 API 交互。

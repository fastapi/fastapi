# OAuth2 实现简单的 Password 和 Bearer 验证 { #simple-oauth2-with-password-and-bearer }

现在，让我们在上一章的基础上，补全缺失的部分，以获得完整的安全流程。

## 获取 `username` 和 `password` { #get-the-username-and-password }

我们将使用 **FastAPI** 的安全工具获取 `username` 和 `password`。

OAuth2 规定，当使用（我们正在使用的）“password flow”时，客户端/用户必须以表单数据的形式发送 `username` 和 `password` 字段。

并且规范要求字段必须这样命名。所以 `user-name` 或 `email` 都不能用。

不过别担心，你仍然可以在前端按你希望的方式向最终用户展示。

你的数据库模型也可以使用任何你想要的其它名称。

但对于登录*路径操作*，我们需要使用这些名称，才能兼容规范（并能够例如使用集成的 API 文档系统）。

该规范还规定 `username` 和 `password` 必须以表单数据形式发送（因此，这里不能用 JSON）。

### `scope` { #scope }

规范还说，客户端可以发送另一个表单字段 “`scope`”。

表单字段名是 `scope`（单数），但它实际上是一个长字符串，由用空格分隔的多个 “scopes” 组成。

每个 “scope” 只是一个字符串（不包含空格）。

它们通常用于声明特定的安全权限，例如：

* `users:read` 或 `users:write` 是常见示例。
* Facebook / Instagram 使用 `instagram_basic`。
* Google 使用 `https://www.googleapis.com/auth/drive`。

/// info | 信息

在 OAuth2 中，“scope” 只是一个声明所需特定权限的字符串。

它是否包含 `:` 等其它字符，或者它是不是 URL，都无关紧要。

这些细节是具体实现相关的。

对 OAuth2 来说，它们都只是字符串。

///

## 获取 `username` 和 `password` 的代码 { #code-to-get-the-username-and-password }

现在，让我们使用 **FastAPI** 提供的工具来处理这个问题。

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

首先，导入 `OAuth2PasswordRequestForm`，并在 `/token` 的*路径操作*中通过 `Depends` 将其作为依赖项使用：

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` 是一个类依赖项，用来声明包含以下内容的表单请求体：

* `username`。
* `password`。
* 可选的 `scope` 字段，一个由用空格分隔的字符串组成的大字符串。
* 可选的 `grant_type`。

/// tip | 提示

OAuth2 规范实际上*要求*字段 `grant_type` 必须是固定值 `password`，但 `OAuth2PasswordRequestForm` 并不会强制执行。

如果你需要强制执行，请使用 `OAuth2PasswordRequestFormStrict` 替代 `OAuth2PasswordRequestForm`。

///

* 可选的 `client_id`（本例不需要）。
* 可选的 `client_secret`（本例不需要）。

/// info | 信息

`OAuth2PasswordRequestForm` 并不是像 `OAuth2PasswordBearer` 那样的 **FastAPI** 特殊类。

`OAuth2PasswordBearer` 会让 **FastAPI** 知道它是一个安全方案，所以会以这种方式被添加到 OpenAPI 中。

但 `OAuth2PasswordRequestForm` 只是一个类依赖项，你本可以自己编写它，或者也可以直接声明 `Form` 参数。

但由于这是一个常见用例，**FastAPI** 直接提供了它，让事情更简单。

///

### 使用表单数据 { #use-the-form-data }

/// tip | 提示

依赖类 `OAuth2PasswordRequestForm` 的实例不会有包含空格分隔长字符串的 `scope` 属性，相反，它会有一个 `scopes` 属性，其中包含每个已发送 scope 的实际字符串列表。

本例没有使用 `scopes`，但如果你需要，这个功能是存在的。

///

现在，使用表单字段中的 `username`，从（伪）数据库中获取用户数据。

如果没有这个用户，我们就返回一个错误，提示 “Incorrect username or password”。

对于这个错误，我们使用异常 `HTTPException`：

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### 校验密码 { #check-the-password }

此时我们已经从数据库中获取到了用户数据，但还没有校验密码。

先把这些数据放到 Pydantic 的 `UserInDB` 模型中。

你永远不应该保存明文密码，所以我们将使用（伪）密码哈希系统。

如果密码不匹配，我们返回同样的错误。

#### 密码哈希 { #password-hashing }

“Hashing”的意思是：把某些内容（本例中是密码）转换成一段看起来像乱码的字节序列（其实就是字符串）。

每次传入完全相同的内容（完全相同的密码）都会得到完全相同的乱码。

但你无法从乱码反推回原始密码。

##### 为什么使用密码哈希 { #why-use-password-hashing }

如果你的数据库被盗，窃贼拿不到用户的明文密码，只能拿到哈希值。

因此，窃贼就无法尝试在其它系统中使用相同的密码（因为很多用户在所有地方都用同一个密码，这会很危险）。

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### 关于 `**user_dict` { #about-user-dict }

`UserInDB(**user_dict)` 的意思是：

*将 `user_dict` 的键和值直接作为键值参数传递，等价于：*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | 信息

关于 `**user_dict` 更完整的解释，请回看[**更多模型**的文档](../extra-models.md#about-user-in-dict){.internal-link target=_blank}。

///

## 返回 Token { #return-the-token }

`token` 端点的响应必须是 JSON 对象。

它应该包含 `token_type`。在我们的例子中，因为使用的是 “Bearer” token，所以 token 类型应为 “`bearer`”。

并且它应该包含 `access_token`，其值是一个包含访问 token 的字符串。

对于这个简单示例，我们会完全不安全地直接把同一个 `username` 作为 token 返回。

/// tip | 提示

在下一章中，你会看到真正安全的实现，包括密码哈希和 <abbr title="JSON Web Tokens">JWT</abbr> tokens。

但现在，让我们先专注于我们需要的特定细节。

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | 提示

按规范要求，你应该像本例一样返回包含 `access_token` 和 `token_type` 的 JSON。

这是你必须在代码中自己完成的事情，并确保使用这些 JSON 键。

这几乎是唯一一个你需要自己记住并正确完成、以符合规范的事情。

其余的部分，**FastAPI** 会为你处理。

///

## 更新依赖项 { #update-the-dependencies }

现在我们要更新依赖项。

我们希望 *只有* 在该用户处于激活状态时，才能获取 `current_user`。

所以，我们创建一个额外的依赖项 `get_current_active_user`，它又会使用 `get_current_user` 作为依赖项。

如果用户不存在，或者处于未激活状态，这两个依赖项都会直接返回 HTTP 错误。

因此，在端点中，只有当用户存在、成功通过身份验证并且处于激活状态时，我们才会获得该用户：

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | 信息

我们在这里返回的、值为 `Bearer` 的额外响应头 `WWW-Authenticate` 也是规范的一部分。

任何 HTTP（错误）状态码 401 “UNAUTHORIZED” 也应该返回 `WWW-Authenticate` 响应头。

对于 bearer tokens（我们的情况），该响应头的值应为 `Bearer`。

实际上，你可以跳过这个额外响应头，依然可以正常工作。

但这里提供它是为了符合规范要求。

另外，也可能有一些工具（现在或未来）会期望并使用它，这对你或你的用户（现在或未来）可能会有用。

这就是标准的好处...

///

## 实际效果 { #see-it-in-action }

打开交互式文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

### 身份验证 { #authenticate }

点击 “Authorize” 按钮。

使用以下凭证：

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

在系统中完成身份验证后，你将会看到如下内容：

<img src="/img/tutorial/security/image05.png">

### 获取你自己的用户数据 { #get-your-own-user-data }

现在使用路径 `/users/me` 的 `GET` 操作。

你将获取到你的用户数据，例如：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

如果你点击锁图标并退出登录，然后再次尝试相同的操作，你将得到一个 HTTP 401 错误：

```JSON
{
  "detail": "Not authenticated"
}
```

### 未激活用户 { #inactive-user }

现在试试一个未激活的用户，使用以下信息进行身份验证：

User: `alice`

Password: `secret2`

然后尝试使用路径 `/users/me` 的 `GET` 操作。

你将得到一个 “Inactive user” 错误，例如：

```JSON
{
  "detail": "Inactive user"
}
```

## 小结 { #recap }

现在你已经拥有了工具，可以为你的 API 实现一个基于 `username` 和 `password` 的完整安全系统。

使用这些工具，你可以让安全系统与任何数据库以及任何用户或数据模型兼容。

唯一缺少的细节是：它实际上还不够“安全”。

在下一章中，你将看到如何使用安全的密码哈希库和 <abbr title="JSON Web Tokens">JWT</abbr> tokens。

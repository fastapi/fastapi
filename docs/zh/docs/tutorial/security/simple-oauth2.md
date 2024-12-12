# OAuth2 实现简单的 Password 和 Bearer 验证

本章添加上一章示例中欠缺的部分，实现完整的安全流。

## 获取 `username` 和 `password`

首先，使用 **FastAPI** 安全工具获取 `username` 和 `password`。

OAuth2 规范要求使用**密码流**时，客户端或用户必须以表单数据形式发送 `username` 和 `password` 字段。

并且，这两个字段必须命名为 `username` 和 `password` ，不能使用 `user-name` 或 `email` 等其它名称。

不过也不用担心，前端仍可以显示终端用户所需的名称。

数据库模型也可以使用所需的名称。

但对于登录*路径操作*，则要使用兼容规范的 `username` 和 `password`，（例如，实现与 API 文档集成）。

该规范要求必须以表单数据形式发送 `username` 和 `password`，因此，不能使用 JSON 对象。

### `Scope`（作用域）

OAuth2 还支持客户端发送**`scope`**表单字段。

虽然表单字段的名称是 `scope`（单数），但实际上，它是以空格分隔的，由多个**scope**组成的长字符串。

**作用域**只是不带空格的字符串。

常用于声明指定安全权限，例如：

* 常见用例为，`users:read` 或 `users:write`
* 脸书和 Instagram 使用 `instagram_basic`
* 谷歌使用 `https://www.googleapis.com/auth/drive`

/// info | 说明

OAuth2 中，**作用域**只是声明指定权限的字符串。

是否使用冒号 `:` 等符号，或是不是 URL 并不重要。

这些细节只是特定的实现方式。

对 OAuth2 来说，都只是字符串而已。

///

## 获取 `username` 和 `password` 的代码

接下来，使用 **FastAPI** 工具获取用户名与密码。

### `OAuth2PasswordRequestForm`

首先，导入 `OAuth2PasswordRequestForm`，然后，在 `/token` *路径操作* 中，用 `Depends` 把该类作为依赖项。

{* ../../docs_src/security/tutorial003.py hl[4,76] *}

`OAuth2PasswordRequestForm` 是用以下几项内容声明表单请求体的类依赖项：

* `username`
* `password`
* 可选的 `scope` 字段，由多个空格分隔的字符串组成的长字符串
* 可选的 `grant_type`

/// tip | 提示

实际上，OAuth2 规范*要求* `grant_type` 字段使用固定值 `password`，但 `OAuth2PasswordRequestForm` 没有作强制约束。

如需强制使用固定值 `password`，则不要用 `OAuth2PasswordRequestForm`，而是用 `OAuth2PasswordRequestFormStrict`。

///

* 可选的 `client_id`（本例未使用）
* 可选的 `client_secret`（本例未使用）

/// info | 说明

`OAuth2PasswordRequestForm` 与 `OAuth2PasswordBearer` 一样，都不是 FastAPI 的特殊类。

**FastAPI** 把 `OAuth2PasswordBearer` 识别为安全方案。因此，可以通过这种方式把它添加至 OpenAPI。

但 `OAuth2PasswordRequestForm` 只是可以自行编写的类依赖项，也可以直接声明 `Form` 参数。

但由于这种用例很常见，FastAPI 为了简便，就直接提供了对它的支持。

///

### 使用表单数据

/// tip | 提示

`OAuth2PasswordRequestForm` 类依赖项的实例没有以空格分隔的长字符串属性 `scope`，但它支持 `scopes` 属性，由已发送的 scope 字符串列表组成。

本例没有使用 `scopes`，但开发者也可以根据需要使用该属性。

///

现在，即可使用表单字段 `username`，从（伪）数据库中获取用户数据。

如果不存在指定用户，则返回错误消息，提示**用户名或密码错误**。

本例使用 `HTTPException` 异常显示此错误：

{* ../../docs_src/security/tutorial003.py hl[3,77:79] *}

### 校验密码

至此，我们已经从数据库中获取了用户数据，但尚未校验密码。

接下来，首先将数据放入 Pydantic 的 `UserInDB` 模型。

注意：永远不要保存明文密码，本例暂时先使用（伪）哈希密码系统。

如果密码不匹配，则返回与上面相同的错误。

#### 密码哈希

**哈希**是指，将指定内容（本例中为密码）转换为形似乱码的字节序列（其实就是字符串）。

每次传入完全相同的内容（比如，完全相同的密码）时，得到的都是完全相同的乱码。

但这个乱码无法转换回传入的密码。

##### 为什么使用密码哈希

原因很简单，假如数据库被盗，窃贼无法获取用户的明文密码，得到的只是哈希值。

这样一来，窃贼就无法在其它应用中使用窃取的密码，要知道，很多用户在所有系统中都使用相同的密码，风险超大。

{* ../../docs_src/security/tutorial003.py hl[80:83] *}

#### 关于 `**user_dict`

`UserInDB(**user_dict)` 是指：

*直接把 `user_dict` 的键与值当作关键字参数传递，等效于：*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | 说明

`user_dict` 的说明，详见[**更多模型**一章](../extra-models.md#user_indict){.internal-link target=_blank}。

///

## 返回 Token

`token` 端点的响应必须是 JSON 对象。

响应返回的内容应该包含 `token_type`。本例中用的是**Bearer**Token，因此， Token 类型应为**`bearer`**。

返回内容还应包含 `access_token` 字段，它是包含权限 Token 的字符串。

本例只是简单的演示，返回的 Token 就是 `username`，但这种方式极不安全。

/// tip | 提示

下一章介绍使用哈希密码和 <abbr title="JSON Web Tokens">JWT</abbr> Token 的真正安全机制。

但现在，仅关注所需的特定细节。

///

{* ../../docs_src/security/tutorial003.py hl[85] *}

/// tip | 提示

按规范的要求，应像本示例一样，返回带有 `access_token` 和 `token_type` 的 JSON 对象。

这是开发者必须在代码中自行完成的工作，并且要确保使用这些 JSON 的键。

这几乎是唯一需要开发者牢记在心，并按规范要求正确执行的事。

**FastAPI** 则负责处理其它的工作。

///

## 更新依赖项

接下来，更新依赖项。

使之仅在当前用户为激活状态时，才能获取 `current_user`。

为此，要再创建一个依赖项 `get_current_active_user`，此依赖项以 `get_current_user` 依赖项为基础。

如果用户不存在，或状态为未激活，这两个依赖项都会返回 HTTP 错误。

因此，在端点中，只有当用户存在、通过身份验证、且状态为激活时，才能获得该用户：

{* ../../docs_src/security/tutorial003.py hl[58:67,69:72,90] *}

/// info | 说明

此处返回值为 `Bearer` 的响应头 `WWW-Authenticate` 也是规范的一部分。

任何 401**UNAUTHORIZED**HTTP（错误）状态码都应返回 `WWW-Authenticate` 响应头。

本例中，因为使用的是 Bearer Token，该响应头的值应为 `Bearer`。

实际上，忽略这个附加响应头，也不会有什么问题。

之所以在此提供这个附加响应头，是为了符合规范的要求。

说不定什么时候，就有工具用得上它，而且，开发者或用户也可能用得上。

这就是遵循标准的好处……

///

## 实际效果

打开 API 文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

### 身份验证

点击**Authorize**按钮。

使用以下凭证：

用户名：`johndoe`

密码：`secret`

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image04.png">

通过身份验证后，显示下图所示的内容：

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image05.png">

### 获取当前用户数据

使用 `/users/me` 路径的 `GET` 操作。

可以提取如下当前用户数据：

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="https://fastapi.tiangolo.com/img/tutorial/security/image06.png">

点击小锁图标，注销后，再执行同样的操作，则会得到 HTTP 401 错误：

```JSON
{
  "detail": "Not authenticated"
}
```

### 未激活用户

测试未激活用户，输入以下信息，进行身份验证：

用户名：`alice`

密码：`secret2`

然后，执行 `/users/me` 路径的 `GET` 操作。

显示下列**未激活用户**错误信息：

```JSON
{
  "detail": "Inactive user"
}
```

## 小结

使用本章的工具实现基于 `username` 和 `password` 的完整 API 安全系统。

这些工具让安全系统兼容任何数据库、用户及数据模型。

唯一欠缺的是，它仍然不是真的**安全**。

下一章，介绍使用密码哈希支持库与 <abbr title="JSON Web Tokens">JWT</abbr> 令牌实现真正的安全机制。

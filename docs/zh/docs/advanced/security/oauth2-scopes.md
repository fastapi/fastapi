# OAuth2 作用域

**FastAPI** 无缝集成 OAuth2 作用域（`Scopes`），可以直接使用。

作用域是更精密的权限系统，遵循 OAuth2 标准，与 OpenAPI 应用（和 API 自动文档）集成。

OAuth2 也是脸书、谷歌、GitHub、微软、推特等第三方身份验证应用使用的机制。这些身份验证应用在用户登录应用时使用 OAuth2 提供指定权限。

脸书、谷歌、GitHub、微软、推特就是 OAuth2 作用域登录。

本章介绍如何在 **FastAPI** 应用中使用 OAuth2 作用域管理验证与授权。

/// warning | 警告

本章内容较难，刚接触 FastAPI 的新手可以跳过。

OAuth2 作用域不是必需的，没有它，您也可以处理身份验证与授权。

但 OAuth2 作用域与 API（通过 OpenAPI）及 API 文档集成地更好。

不管怎么说，**FastAPI** 支持在代码中使用作用域或其它安全/授权需求项。

很多情况下，OAuth2 作用域就像一把牛刀。

但如果您确定要使用作用域，或对它有兴趣，请继续阅读。

///

## OAuth2 作用域与 OpenAPI

OAuth2 规范的**作用域**是由空格分割的字符串组成的列表。

这些字符串支持任何格式，但不能包含空格。

作用域表示的是**权限**。

OpenAPI 中（例如 API 文档）可以定义**安全方案**。

这些安全方案在使用 OAuth2 时，还可以声明和使用作用域。

**作用域**只是（不带空格的）字符串。

常用于声明特定安全权限，例如：

* 常见用例为，`users:read` 或 `users:write`
* 脸书和 Instagram 使用 `instagram_basic`
* 谷歌使用 `https://www.googleapis.com/auth/drive`

/// info | 说明

OAuth2 中，**作用域**只是声明特定权限的字符串。

是否使用冒号 `:` 等符号，或是不是 URL 并不重要。

这些细节只是特定的实现方式。

对 OAuth2 来说，它们都只是字符串而已。

///

## 全局纵览

首先，快速浏览一下以下代码与**用户指南**中 [OAuth2 实现密码哈希与 Bearer  JWT 令牌验证](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank}一章中代码的区别。以下代码使用 OAuth2 作用域：

{* ../../docs_src/security/tutorial005.py hl[2,4,8,12,46,64,105,107:115,121:124,128:134,139,153] *}

下面，我们逐步说明修改的代码内容。

## OAuth2 安全方案

第一个修改的地方是，使用两个作用域 `me` 和 `items ` 声明 OAuth2 安全方案。

`scopes` 参数接收**字典**，键是作用域、值是作用域的描述：

{* ../../docs_src/security/tutorial005.py hl[62:65] *}

因为声明了作用域，所以登录或授权时会在 API 文档中显示。

此处，选择给予访问权限的作用域： `me` 和 `items`。

这也是使用脸书、谷歌、GitHub 登录时的授权机制。

<img src="/img/tutorial/security/image11.png">

## JWT 令牌作用域

现在，修改令牌*路径操作*，返回请求的作用域。

此处仍然使用 `OAuth2PasswordRequestForm`。它包含类型为**字符串列表**的 `scopes` 属性，且`scopes` 属性中包含要在请求里接收的每个作用域。

这样，返回的 JWT 令牌中就包含了作用域。

/// danger | 危险

为了简明起见，本例把接收的作用域直接添加到了令牌里。

但在您的应用中，为了安全，应该只把作用域添加到确实需要作用域的用户，或预定义的用户。

///

{* ../../docs_src/security/tutorial005.py hl[153] *}

## 在*路径操作*与依赖项中声明作用域

接下来，为*路径操作*  `/users/me/items/` 声明作用域 `items`。

为此，要从 `fastapi` 中导入并使用 `Security` 。

`Security` 声明依赖项的方式和 `Depends` 一样，但 `Security` 还能接收作用域（字符串）列表类型的参数 `scopes`。

此处使用与 `Depends` 相同的方式，把依赖项函数 `get_current_active_user` 传递给 `Security`。

同时，还传递了作用域**列表**，本例中只传递了一个作用域：`items`（此处支持传递更多作用域）。

依赖项函数 `get_current_active_user` 还能声明子依赖项，不仅可以使用 `Depends`，也可以使用 `Security`。声明子依赖项函数（`get_current_user`）及更多作用域。

本例要求使用作用域 `me`（还可以使用更多作用域）。

/// note | 笔记

不必在不同位置添加不同的作用域。

本例使用的这种方式只是为了展示 **FastAPI** 如何处理在不同层级声明的作用域。

///

{* ../../docs_src/security/tutorial005.py hl[4,139,166] *}

/// info | 技术细节

`Security` 实际上是 `Depends` 的子类，而且只比 `Depends` 多一个参数。

但使用 `Security` 代替 `Depends`，**FastAPI** 可以声明安全作用域，并在内部使用这些作用域，同时，使用 OpenAPI 存档 API。

但实际上，从 `fastapi` 导入的 `Query`、`Path`、`Depends`、`Security` 等对象，只是返回特殊类的函数。

///

## 使用 `SecurityScopes`

修改依赖项 `get_current_user`。

这是上面的依赖项使用的依赖项。

这里使用的也是之前创建的 OAuth2 方案，并把它声明为依赖项：`oauth2_scheme`。

该依赖项函数本身不需要作用域，因此，可以使用 `Depends` 和 `oauth2_scheme`。不需要指定安全作用域时，不必使用 `Security`。

此处还声明了从 `fastapi.security` 导入的 `SecurityScopes` 类型的特殊参数。

`SecuriScopes` 类与 `Request` 类似（`Request` 用于直接提取请求对象）。

{* ../../docs_src/security/tutorial005.py hl[8,105] *}

## 使用 `scopes`

参数 `security_scopes` 的类型是 `SecurityScopes`。

它的属性 `scopes`  是作用域列表，所有依赖项都把它作为子依赖项。也就是说所有**依赖**……这听起来有些绕，后文会有解释。

（类 `SecurityScopes` 的）`security_scopes` 对象还提供了单字符串类型的属性 `scope_str`，该属性是（要在本例中使用的）用空格分割的作用域。

此处还创建了后续代码中要复用（`raise`）的 `HTTPException` 。

该异常包含了作用域所需的（如有），以空格分割的字符串（使用 `scope_str`）。该字符串要放到包含作用域的 `WWW-Authenticate` 请求头中（这也是规范的要求）。

{* ../../docs_src/security/tutorial005.py hl[105,107:115] *}

## 校验 `username` 与数据形状

我们可以校验是否获取了 `username`，并抽取作用域。

然后，使用 Pydantic 模型校验数据（捕获 `ValidationError` 异常），如果读取 JWT 令牌或使用 Pydantic 模型验证数据时出错，就会触发之前创建的 `HTTPException` 异常。

对此，要使用新的属性 `scopes` 更新 Pydantic 模型 `TokenData`。

使用 Pydantic 验证数据可以确保数据中含有由作用域组成的**字符串列表**，以及 `username` 字符串等内容。

反之，如果使用**字典**或其它数据结构，就有可能在后面某些位置破坏应用，形成安全隐患。

还可以使用用户名验证用户，如果没有用户，也会触发之前创建的异常。

{* ../../docs_src/security/tutorial005.py hl[46,116:127] *}

## 校验 `scopes`

接下来，校验所有依赖项和依赖要素（包括*路径操作*）所需的作用域。这些作用域包含在令牌的 `scopes` 里，如果不在其中就会触发 `HTTPException` 异常。

为此，要使用包含所有作用域**字符串列表**的 `security_scopes.scopes`， 。

{* ../../docs_src/security/tutorial005.py hl[128:134] *}

## 依赖项树与作用域

再次查看这个依赖项树与作用域。

`get_current_active_user` 依赖项包含子依赖项 `get_current_user`，并在 `get_current_active_user`中声明了作用域 `"me"` 包含所需作用域列表 ，在 `security_scopes.scopes` 中传递给 `get_current_user`。

*路径操作*自身也声明了作用域，`"items"`，这也是 `security_scopes.scopes` 列表传递给 `get_current_user` 的。

依赖项与作用域的层级架构如下：

* *路径操作* `read_own_items` 包含：
    * 依赖项所需的作用域 `["items"]`：
    * `get_current_active_user`:
        *  依赖项函数 `get_current_active_user` 包含：
            * 所需的作用域 `"me"` 包含依赖项：
            * `get_current_user`:
                * 依赖项函数 `get_current_user` 包含：
                    * 没有作用域需求其自身
                    * 依赖项使用 `oauth2_scheme`
                    * `security_scopes` 参数的类型是 `SecurityScopes`：
                        * `security_scopes` 参数的属性 `scopes` 是包含上述声明的所有作用域的**列表**，因此：
                            * `security_scopes.scopes` 包含用于*路径操作*的 `["me", "items"]`
                            * `security_scopes.scopes` 包含*路径操作* `read_users_me` 的 `["me"]`，因为它在依赖项里被声明
                            * `security_scopes.scopes` 包含用于*路径操作* `read_system_status` 的 `[]`（空列表），并且它的依赖项 `get_current_user` 也没有声明任何 `scope`

/// tip | 提示

此处重要且**神奇**的事情是，`get_current_user` 检查每个*路径操作*时可以使用不同的 `scopes` 列表。

所有这些都依赖于在每个*路径操作*和指定*路径操作*的依赖树中的每个依赖项。

///

## `SecurityScopes` 的更多细节

您可以任何位置或多个位置使用 `SecurityScopes`，不一定非得在**根**依赖项中使用。

它总是在当前 `Security` 依赖项中和所有依赖因子对于**特定** *路径操作*和**特定**依赖树中安全作用域

因为 `SecurityScopes` 包含所有由依赖项声明的作用域，可以在核心依赖函数中用它验证所需作用域的令牌，然后再在不同的*路径操作*中声明不同作用域需求。

它们会为每个*路径操作*进行单独检查。

## 查看文档

打开 API 文档，进行身份验证，并指定要授权的作用域。

<img src="/img/tutorial/security/image11.png">

没有选择任何作用域，也可以进行**身份验证**，但访问 `/uses/me` 或 `/users/me/items` 时，会显示没有足够的权限。但仍可以访问 `/status/`。

如果选择了作用域 `me`，但没有选择作用域 `items`，则可以访问 `/users/me/`，但不能访问 `/users/me/items`。

这就是通过用户提供的令牌使用第三方应用访问这些*路径操作*时会发生的情况，具体怎样取决于用户授予第三方应用的权限。

## 关于第三方集成

本例使用 OAuth2 **密码**流。

这种方式适用于登录我们自己的应用，最好使用我们自己的前端。

因为我们能控制自己的前端应用，可以信任它接收 `username` 与 `password`。

但如果构建的是连接其它应用的 OAuth2 应用，比如具有与脸书、谷歌、GitHub 相同功能的第三方身份验证应用。那您就应该使用其它安全流。

最常用的是隐式流。

最安全的是代码流，但实现起来更复杂，而且需要更多步骤。因为它更复杂，很多第三方身份验证应用最终建议使用隐式流。

/// note | 笔记

每个身份验证应用都会采用不同方式会命名流，以便融合入自己的品牌。

但归根结底，它们使用的都是 OAuth2 标准。

///

**FastAPI** 的 `fastapi.security.oauth2` 里包含了所有 OAuth2 身份验证流工具。

## 装饰器 `dependencies` 中的 `Security`

同样，您可以在装饰器的 `dependencies` 参数中定义 `Depends` 列表，（详见[路径操作装饰器依赖项](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank})），也可以把 `scopes` 与 `Security` 一起使用。

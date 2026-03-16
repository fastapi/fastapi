# OAuth2 作用域 { #oauth2-scopes }

你可以在 **FastAPI** 中直接使用 OAuth2 作用域（Scopes），它们已无缝集成。

这样你就可以按照 OAuth2 标准，构建更精细的权限系统，并将其集成进你的 OpenAPI 应用（以及 API 文档）中。

带作用域的 OAuth2 是很多大型身份验证提供商使用的机制，例如 Facebook、Google、GitHub、Microsoft、X (Twitter) 等。它们用它来为用户和应用授予特定权限。

每次你“使用” Facebook、Google、GitHub、Microsoft、X (Twitter) “登录”时，该应用就在使用带作用域的 OAuth2。

本节将介绍如何在你的 **FastAPI** 应用中，使用相同的带作用域的 OAuth2 管理认证与授权。

/// warning | 警告

本节内容相对进阶，如果你刚开始，可以先跳过。

你并不一定需要 OAuth2 作用域，你也可以用你自己的方式处理认证与授权。

但带作用域的 OAuth2 能很好地集成进你的 API（通过 OpenAPI）和 API 文档。

不过，无论如何，你都可以在代码中按需强制这些作用域，或任何其它安全/授权需求。

很多情况下，带作用域的 OAuth2 可能有点“大材小用”。

但如果你确实需要它，或者只是好奇，请继续阅读。

///

## OAuth2 作用域与 OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 规范将“作用域”定义为由空格分隔的字符串列表。

这些字符串的内容可以是任意格式，但不应包含空格。

这些作用域表示“权限”。

在 OpenAPI（例如 API 文档）中，你可以定义“安全方案”（security schemes）。

当这些安全方案使用 OAuth2 时，你还可以声明并使用作用域。

每个“作用域”只是一个（不带空格的）字符串。

它们通常用于声明特定的安全权限，例如：

* 常见示例：`users:read` 或 `users:write`
* Facebook / Instagram 使用 `instagram_basic`
* Google 使用 `https://www.googleapis.com/auth/drive`

/// info | 信息

在 OAuth2 中，“作用域”只是一个声明所需特定权限的字符串。

是否包含像 `:` 这样的字符，或者是不是一个 URL，并不重要。

这些细节取决于具体实现。

对 OAuth2 而言，它们都只是字符串。

///

## 全局纵览 { #global-view }

首先，让我们快速看看与**用户指南**中 [OAuth2 实现密码（含哈希）、Bearer + JWT 令牌](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} 示例相比有哪些变化。现在开始使用 OAuth2 作用域：

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

下面我们逐步回顾这些更改。

## OAuth2 安全方案 { #oauth2-security-scheme }

第一个变化是：我们在声明 OAuth2 安全方案时，添加了两个可用的作用域 `me` 和 `items`。

参数 `scopes` 接收一个 `dict`，以作用域为键、描述为值：

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

因为我们现在声明了这些作用域，所以当你登录/授权时，它们会显示在 API 文档里。

你可以选择要授予访问权限的作用域：`me` 和 `items`。

这与使用 Facebook、Google、GitHub 等登录时授予权限的机制相同：

<img src="/img/tutorial/security/image11.png">

## 带作用域的 JWT 令牌 { #jwt-token-with-scopes }

现在，修改令牌的*路径操作*以返回请求的作用域。

我们仍然使用 `OAuth2PasswordRequestForm`。它包含 `scopes` 属性，其值是 `list[str]`，包含请求中接收到的每个作用域。

我们把这些作用域作为 JWT 令牌的一部分返回。

/// danger | 危险

为简单起见，此处我们只是把接收到的作用域直接添加到了令牌中。

但在你的应用里，为了安全起见，你应该只添加该用户实际能够拥有的作用域，或你预先定义的作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## 在*路径操作*与依赖项中声明作用域 { #declare-scopes-in-path-operations-and-dependencies }

现在我们声明，路径操作 `/users/me/items/` 需要作用域 `items`。

为此，从 `fastapi` 导入并使用 `Security`。

你可以用 `Security` 来声明依赖（就像 `Depends` 一样），但 `Security` 还接收一个 `scopes` 参数，其值是作用域（字符串）列表。

在这里，我们把依赖函数 `get_current_active_user` 传给 `Security`（就像用 `Depends` 一样）。

同时还传入一个作用域 `list`，此处仅包含一个作用域：`items`（也可以包含更多）。

依赖函数 `get_current_active_user` 也可以声明子依赖，不仅可以用 `Depends`，也可以用 `Security`。它声明了自己的子依赖函数（`get_current_user`），并添加了更多的作用域需求。

在这个例子里，它需要作用域 `me`（也可以需要多个作用域）。

/// note | 注意

不必在不同位置添加不同的作用域。

这里这样做，是为了演示 **FastAPI** 如何处理在不同层级声明的作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | 技术细节

`Security` 实际上是 `Depends` 的子类，它只多了一个我们稍后会看到的参数。

但当你使用 `Security` 而不是 `Depends` 时，**FastAPI** 会知道它可以声明安全作用域，在内部使用它们，并用 OpenAPI 文档化 API。

另外，从 `fastapi` 导入的 `Query`、`Path`、`Depends`、`Security` 等，实际上都是返回特殊类的函数。

///

## 使用 `SecurityScopes` { #use-securityscopes }

现在更新依赖项 `get_current_user`。

上面那些依赖会用到它。

这里我们使用之前创建的同一个 OAuth2 方案，并把它声明为依赖：`oauth2_scheme`。

因为这个依赖函数本身没有任何作用域需求，所以我们可以用 `Depends(oauth2_scheme)`，当不需要指定安全作用域时，不必使用 `Security`。

我们还声明了一个从 `fastapi.security` 导入的特殊参数 `SecurityScopes` 类型。

这个 `SecurityScopes` 类类似于 `Request`（`Request` 用来直接获取请求对象）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## 使用 `scopes` { #use-the-scopes }

参数 `security_scopes` 的类型是 `SecurityScopes`。

它会有一个 `scopes` 属性，包含一个列表，里面是它自身以及所有把它作为子依赖的依赖项所需要的所有作用域。也就是说，所有“依赖者”……这可能有点绕，下面会再次解释。

`security_scopes` 对象（类型为 `SecurityScopes`）还提供了一个 `scope_str` 属性，它是一个用空格分隔这些作用域的单个字符串（我们将会用到它）。

我们创建一个 `HTTPException`，后面可以在多个位置复用（`raise`）它。

在这个异常中，我们包含所需的作用域（如果有的话），以空格分隔的字符串（使用 `scope_str`）。我们把这个包含作用域的字符串放在 `WWW-Authenticate` 响应头中（这是规范要求的一部分）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## 校验 `username` 与数据形状 { #verify-the-username-and-data-shape }

我们校验是否获取到了 `username`，并提取作用域。

然后使用 Pydantic 模型验证这些数据（捕获 `ValidationError` 异常），如果读取 JWT 令牌或用 Pydantic 验证数据时出错，就抛出我们之前创建的 `HTTPException`。

为此，我们给 Pydantic 模型 `TokenData` 添加了一个新属性 `scopes`。

通过用 Pydantic 验证数据，我们可以确保确实得到了例如一个由作用域组成的 `list[str]`，以及一个 `str` 类型的 `username`。

而不是，例如得到一个 `dict` 或其它什么，这可能会在后续某个时刻破坏应用，形成安全风险。

我们还验证是否存在该用户名的用户，如果没有，就抛出前面创建的同一个异常。

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## 校验 `scopes` { #verify-the-scopes }

现在我们要验证，这个依赖以及所有依赖者（包括*路径操作*）所需的所有作用域，是否都包含在接收到的令牌里的作用域中，否则就抛出 `HTTPException`。

为此，我们使用 `security_scopes.scopes`，它包含一个由这些作用域组成的 `list[str]`。

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 依赖树与作用域 { #dependency-tree-and-scopes }

再次回顾这个依赖树与作用域。

由于 `get_current_active_user` 依赖把 `get_current_user` 作为子依赖，因此在 `get_current_active_user` 中声明的作用域 `"me"` 会被包含在传给 `get_current_user` 的 `security_scopes.scopes` 所需作用域列表中。

*路径操作*本身也声明了一个作用域 `"items"`，它也会包含在传给 `get_current_user` 的 `security_scopes.scopes` 列表中。

依赖与作用域的层级结构如下：

* *路径操作* `read_own_items` 包含：
    * 带有依赖的必需作用域 `["items"]`：
    * `get_current_active_user`：
        *  依赖函数 `get_current_active_user` 包含：
            * 带有依赖的必需作用域 `["me"]`：
            * `get_current_user`：
                * 依赖函数 `get_current_user` 包含：
                    * 自身不需要任何作用域。
                    * 一个使用 `oauth2_scheme` 的依赖。
                    * 一个类型为 `SecurityScopes` 的 `security_scopes` 参数：
                        * 该 `security_scopes` 参数有一个 `scopes` 属性，它是一个包含上面所有已声明作用域的 `list`，因此：
                            * 对于*路径操作* `read_own_items`，`security_scopes.scopes` 将包含 `["me", "items"]`。
                            * 对于*路径操作* `read_users_me`，`security_scopes.scopes` 将包含 `["me"]`，因为它在依赖 `get_current_active_user` 中被声明。
                            * 对于*路径操作* `read_system_status`，`security_scopes.scopes` 将包含 `[]`（空列表），因为它既没有声明任何带 `scopes` 的 `Security`，其依赖 `get_current_user` 也没有声明任何 `scopes`。

/// tip | 提示

这里重要且“神奇”的地方是，`get_current_user` 在检查每个*路径操作*时会得到不同的 `scopes` 列表。

这一切都取决于为该特定*路径操作*在其自身以及依赖树中的每个依赖里声明的 `scopes`。

///

## 关于 `SecurityScopes` 的更多细节 { #more-details-about-securityscopes }

你可以在任意位置、多个位置使用 `SecurityScopes`，不一定非得在“根”依赖里。

它总会包含当前 `Security` 依赖中以及所有依赖者在“该特定”*路径操作*和“该特定”依赖树里声明的安全作用域。

因为 `SecurityScopes` 会包含依赖者声明的所有作用域，你可以在一个核心依赖函数里用它验证令牌是否具有所需作用域，然后在不同的*路径操作*里声明不同的作用域需求。

它们会针对每个*路径操作*分别检查。

## 查看文档 { #check-it }

打开 API 文档，你可以进行身份验证，并指定要授权的作用域。

<img src="/img/tutorial/security/image11.png">

如果你不选择任何作用域，你依然会“通过认证”，但当你访问 `/users/me/` 或 `/users/me/items/` 时，会收到一个错误，提示你没有足够的权限。你仍然可以访问 `/status/`。

如果你选择了作用域 `me`，但没有选择作用域 `items`，你可以访问 `/users/me/`，但不能访问 `/users/me/items/`。

当第三方应用使用用户提供的令牌访问这些*路径操作*时，也会发生同样的情况，取决于用户授予该应用了多少权限。

## 关于第三方集成 { #about-third-party-integrations }

在这个示例中我们使用的是 OAuth2 的“password”流。

当我们登录自己的应用（很可能还有我们自己的前端）时，这是合适的。

因为我们可以信任它来接收 `username` 和 `password`，毕竟我们掌控它。

但如果你在构建一个 OAuth2 应用，让其它应用来连接（也就是说，你在构建等同于 Facebook、Google、GitHub 等的身份验证提供商），你应该使用其它的流。

最常见的是隐式流（implicit flow）。

最安全的是代码流（authorization code flow），但实现更复杂，需要更多步骤。也因为更复杂，很多提供商最终会建议使用隐式流。

/// note | 注意

每个身份验证提供商常常会用不同的方式给它们的流命名，以融入自己的品牌。

但归根结底，它们实现的都是同一个 OAuth2 标准。

///

**FastAPI** 在 `fastapi.security.oauth2` 中为所有这些 OAuth2 身份验证流提供了工具。

## 装饰器 `dependencies` 中的 `Security` { #security-in-decorator-dependencies }

就像你可以在装饰器的 `dependencies` 参数中定义 `Depends` 的 `list`（详见[路径操作装饰器依赖项](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}），你也可以在那儿配合 `Security` 使用 `scopes`。

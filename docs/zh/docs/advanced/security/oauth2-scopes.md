# OAuth2 作用域 { #oauth2-scopes }

你可以直接在 **FastAPI** 中使用 OAuth2 作用域，它们已集成并能无缝工作。

这将允许你拥有更细粒度的权限系统，遵循 OAuth2 标准，并集成到你的 OpenAPI 应用（以及 API 文档）中。

带作用域的 OAuth2 是许多大型身份验证提供商使用的机制，例如 Facebook、Google、GitHub、Microsoft、X（Twitter）等。他们用它来为用户和应用提供特定权限。

每次你使用 Facebook、Google、GitHub、Microsoft、X（Twitter）进行“使用...登录”时，该应用都在使用带作用域的 OAuth2。

在本节中，你将看到如何在你的 **FastAPI** 应用中，使用同样的带作用域的 OAuth2 来管理身份验证与授权。

/// warning | 警告

本节属于或多或少偏高级的内容。如果你刚开始学习，可以跳过。

你不一定需要 OAuth2 作用域，你也可以用任何你想要的方式来处理身份验证与授权。

但带作用域的 OAuth2 可以很好地集成到你的 API（通过 OpenAPI）及你的 API 文档中。

尽管如此，你仍然可以在你的代码中按需强制执行这些作用域，或任何其他安全/授权需求。

在很多情况下，带作用域的 OAuth2 可能有些“用力过猛”。

但如果你知道你需要它，或者你只是好奇，那就继续阅读。

///

## OAuth2 作用域与 OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 规范将“作用域”定义为空格分隔的字符串列表。

每个字符串的内容可以是任何格式，但不应包含空格。

这些作用域表示“权限”。

在 OpenAPI（例如 API 文档）中，你可以定义“安全方案”。

当其中一个安全方案使用 OAuth2 时，你也可以声明和使用作用域。

每个“作用域”只是一个字符串（不包含空格）。

它们通常用于声明特定的安全权限，例如：

* `users:read` 或 `users:write` 是常见示例。
* Facebook / Instagram 使用 `instagram_basic`。
* Google 使用 `https://www.googleapis.com/auth/drive`。

/// info | 信息

在 OAuth2 中，“作用域”只是一个字符串，用于声明所需的特定权限。

它是否包含 `:` 等其他字符，或者是否为 URL，都不重要。

这些细节是实现相关的。

对 OAuth2 来说，它们都只是字符串。

///

## 全局纵览 { #global-view }

首先，让我们快速看一下与 **教程 - 用户指南** 中 [带密码（和哈希）的 OAuth2，带 JWT 令牌的 Bearer](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} 示例相比发生变化的部分。现在使用 OAuth2 作用域：

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

现在我们逐步回顾这些改动。

## OAuth2 安全方案 { #oauth2-security-scheme }

第一个变化是，现在我们用两个可用作用域 `me` 和 `items` 来声明 OAuth2 安全方案。

`scopes` 参数接收一个 `dict`，每个作用域作为键，描述作为值：

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

因为现在我们声明了这些作用域，当你登录/授权时，它们会显示在 API 文档中。

你将能够选择要授予访问权限的作用域：`me` 和 `items`。

这与使用 Facebook、Google、GitHub 等登录时授予权限的机制相同：

<img src="/img/tutorial/security/image11.png">

## 带作用域的 JWT 令牌 { #jwt-token-with-scopes }

现在，修改令牌*路径操作*以返回请求的作用域。

我们仍然使用同一个 `OAuth2PasswordRequestForm`。它包含一个属性 `scopes`，类型为 `list` 的 `str`，包含它在请求中接收到的每个作用域。

然后我们把这些作用域作为 JWT 令牌的一部分返回。

/// danger | 危险

为简单起见，这里我们只是把接收到的作用域直接添加到令牌中。

但在你的应用中，为了安全，你应该确保只添加用户实际能够拥有的作用域，或者你预先定义的那些作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## 在*路径操作*与依赖项中声明作用域 { #declare-scopes-in-path-operations-and-dependencies }

现在我们声明 `/users/me/items/` 的*路径操作*需要作用域 `items`。

为此，我们从 `fastapi` 导入并使用 `Security`。

你可以使用 `Security` 来声明依赖项（就像 `Depends` 一样），但 `Security` 还会接收一个参数 `scopes`，它是作用域（字符串）的列表。

在这种情况下，我们把依赖函数 `get_current_active_user` 传给 `Security`（方式与使用 `Depends` 时相同）。

但我们还传入了一个作用域 `list`，此处只有一个作用域：`items`（也可以有更多）。

并且依赖函数 `get_current_active_user` 也可以声明子依赖项，不仅可以用 `Depends`，也可以用 `Security`。它声明自己的子依赖函数（`get_current_user`），以及更多作用域需求。

在这种情况下，它需要作用域 `me`（也可以需要多个作用域）。

/// note | 注意

你不一定需要在不同位置添加不同的作用域。

我们在这里这样做是为了演示 **FastAPI** 如何处理在不同层级声明的作用域。

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | Technical Details

`Security` 实际上是 `Depends` 的子类，它只多了一个我们稍后会看到的额外参数。

但通过使用 `Security` 替代 `Depends`，**FastAPI** 将知道它可以声明安全作用域，在内部使用它们，并使用 OpenAPI 记录 API。

但当你从 `fastapi` 导入 `Query`、`Path`、`Depends`、`Security` 等时，它们实际上是返回特殊类的函数。

///

## 使用 `SecurityScopes` { #use-securityscopes }

现在更新依赖项 `get_current_user`。

这是上面依赖项使用的那个依赖项。

这里我们使用之前创建的同一个 OAuth2 方案，并将它声明为依赖项：`oauth2_scheme`。

因为这个依赖函数本身没有任何作用域需求，我们可以用 `Depends` 配合 `oauth2_scheme`；当不需要指定安全作用域时，不必使用 `Security`。

我们还声明了一个特殊参数，类型为 `SecurityScopes`，从 `fastapi.security` 导入。

`SecurityScopes` 类类似于 `Request`（`Request` 用于直接获取请求对象）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## 使用 `scopes` { #use-the-scopes }

参数 `security_scopes` 的类型将是 `SecurityScopes`。

它会有一个属性 `scopes`，其中的列表包含它自身以及所有把它作为子依赖项使用的依赖项所需的全部作用域。也就是说，所有的 “dependants”……这可能听起来有点绕，下面会再次解释。

`security_scopes` 对象（`SecurityScopes` 类）还提供一个 `scope_str` 属性，它是一个单一字符串，包含这些用空格分隔的作用域（我们将使用它）。

我们创建一个 `HTTPException`，以便稍后在多个位置复用（`raise`）。

在这个异常中，我们把所需的作用域（如果有）作为一个空格分隔的字符串（使用 `scope_str`）包含进去。我们把这个包含作用域的字符串放在 `WWW-Authenticate` 头中（这是规范的一部分）。

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## 校验 `username` 与数据形状 { #verify-the-username-and-data-shape }

我们校验能拿到 `username`，并提取作用域。

然后使用 Pydantic 模型验证数据（捕获 `ValidationError` 异常）。如果读取 JWT 令牌或用 Pydantic 验证数据时出错，我们就抛出之前创建的 `HTTPException`。

为此，我们给 Pydantic 模型 `TokenData` 增加一个新属性 `scopes`。

通过使用 Pydantic 验证数据，我们可以确保例如确实拿到的是包含作用域的 `list` 的 `str`，以及一个 `str` 类型的 `username`。

而不是例如一个 `dict` 或其他什么结构，因为它可能在之后的某个点破坏应用，从而形成安全风险。

我们还会验证是否存在该 `username` 对应的用户，如果没有，也会抛出之前创建的同一个异常。

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## 校验 `scopes` { #verify-the-scopes }

现在我们校验：此依赖项及所有依赖它的项（包括*路径操作*）所需的全部作用域，是否都包含在收到的令牌所提供的作用域中，否则抛出 `HTTPException`。

为此，我们使用 `security_scopes.scopes`，它包含一个 `list`，其中所有这些作用域都是 `str`。

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 依赖树与作用域 { #dependency-tree-and-scopes }

让我们再次回顾这个依赖树与作用域。

由于 `get_current_active_user` 依赖项将 `get_current_user` 作为子依赖项，在 `get_current_active_user` 中声明的作用域 `"me"` 会被包含在传递给 `get_current_user` 的 `security_scopes.scopes` 所需作用域列表中。

*路径操作*本身也声明了一个作用域 `"items"`，因此它也会出现在传递给 `get_current_user` 的 `security_scopes.scopes` 列表中。

依赖项与作用域的层级结构如下：

* *路径操作* `read_own_items` 有：
    * 所需作用域 `["items"]`，并带有依赖项：
    * `get_current_active_user`：
        * 依赖函数 `get_current_active_user` 有：
            * 所需作用域 `["me"]`，并带有依赖项：
            * `get_current_user`：
                * 依赖函数 `get_current_user` 有：
                    * 它自身不需要任何作用域。
                    * 一个使用 `oauth2_scheme` 的依赖项。
                    * 一个类型为 `SecurityScopes` 的 `security_scopes` 参数：
                        * 这个 `security_scopes` 参数有一个属性 `scopes`，其中的 `list` 包含上面声明的所有作用域，因此：
                            * 对于*路径操作* `read_own_items`，`security_scopes.scopes` 将包含 `["me", "items"]`。
                            * 对于*路径操作* `read_users_me`，`security_scopes.scopes` 将包含 `["me"]`，因为它在依赖项 `get_current_active_user` 中声明。
                            * 对于*路径操作* `read_system_status`，`security_scopes.scopes` 将包含 `[]`（空），因为它没有声明任何带 `scopes` 的 `Security`，并且它的依赖项 `get_current_user` 也没有声明任何 `scopes`。

/// tip | 提示

这里重要且“神奇”的一点是，对于每个*路径操作*，`get_current_user` 都会有一份不同的 `scopes` 列表需要检查。

这完全取决于每个*路径操作*中声明的 `scopes`，以及该*路径操作*对应的依赖树中每个依赖项声明的 `scopes`。

///

## 关于 `SecurityScopes` 的更多细节 { #more-details-about-securityscopes }

你可以在任何位置使用 `SecurityScopes`，也可以在多个地方使用，它不一定必须在“根”依赖项中。

它总会包含在当前 `Security` 依赖项中声明的安全作用域，以及 **针对该特定** *路径操作* 和 **该特定** 依赖树的所有依赖它的项所声明的安全作用域。

因为 `SecurityScopes` 会包含 dependants 声明的所有作用域，你可以在一个中心依赖函数中用它验证令牌是否具有所需作用域，然后在不同的*路径操作*中声明不同的作用域需求。

它们会针对每个*路径操作*独立检查。

## 检查一下 { #check-it }

如果你打开 API 文档，你可以进行身份验证并指定你想要授权哪些作用域。

<img src="/img/tutorial/security/image11.png">

如果你不选择任何作用域，你会被“身份验证”通过，但当你尝试访问 `/users/me/` 或 `/users/me/items/` 时会得到一个错误，提示你权限不足。你仍然可以访问 `/status/`。

如果你选择了作用域 `me` 但没有选择作用域 `items`，你可以访问 `/users/me/`，但不能访问 `/users/me/items/`。

这就是第三方应用尝试用用户提供的令牌访问这些*路径操作*时会发生的情况，具体取决于用户给该应用授予了多少权限。

## 关于第三方集成 { #about-third-party-integrations }

在这个示例中，我们使用 OAuth2 “password” 流。

当我们登录自己的应用时，这种方式很合适，通常会配合我们自己的前端。

因为我们控制它，所以可以信任它接收 `username` 和 `password`。

但如果你正在构建一个其他人会连接的 OAuth2 应用（也就是说，如果你在构建一个等同于 Facebook、Google、GitHub 等的身份验证提供商），你应该使用其他流之一。

最常见的是 implicit flow。

最安全的是 code flow，但它实现更复杂，因为需要更多步骤。由于它更复杂，许多提供商最终会建议使用 implicit flow。

/// note | 注意

每个身份验证提供商用不同方式命名它们的 flow 是很常见的，以便将其作为品牌的一部分。

但最终，它们实现的都是同一个 OAuth2 标准。

///

**FastAPI** 在 `fastapi.security.oauth2` 中为所有这些 OAuth2 身份验证 flow 都包含了工具。

## 装饰器 `dependencies` 中的 `Security` { #security-in-decorator-dependencies }

与在装饰器的 `dependencies` 参数中定义 `Depends` 的 `list` 的方式相同（如 [路径操作装饰器中的依赖项](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 所述），你也可以在那里使用带 `scopes` 的 `Security`。

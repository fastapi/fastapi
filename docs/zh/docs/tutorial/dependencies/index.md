# 依赖 - 第一步

FastAPI 有一个非常强大但直观的 **<abbr title="也称为组件、资源、提供者、服务、可注入项">依赖注入</abbr>** 系统。

它的设计非常易于使用，任何开发人员都可以很容易地将 **FastAPI** 与其他组件集成。

## 什么是 "依赖注入"

**"依赖注入"** 意味着，在编程中，有一种方法可以让你的代码(在本例中，是你的 *路径操作函数* )声明它需要工作和使用的东西: "依赖项"。

然后，该系统(在本例中是 **FastAPI** )将负责为你的代码提供所有的所需依赖项( "注入" 依赖项)的任何操作。

这是非常有用的，当你需要:

* 共享逻辑(一次又一次地使用相同的代码逻辑)。
* 共享数据库连接。
* 实施安全性、身份验证、角色需求等。
* 还有许多其他事情……

所有这些，同时最小化代码重复。

## 第一步

让我们看一个非常简单的例子。它将是如此简单，以至于它现在不是很有用。

但通过这种方式，我们可以关注"依赖注入"系统是如何工作的。

### 创建一个依赖关系，或 "可依赖的"

让我们首先关注依赖。

它只是一个函数，它可以取 *路径操作函数* 可以取的所有参数:

```Python hl_lines="8-9"
{!../../../docs_src/dependencies/tutorial001.py!}
```

就是这样。

**2 行**.

它的形状和结构和所有 *路径操作函数* 一样。

您可以将它看作是一个没有 "装饰器" (没有 `@app.get("/some-path")` )的路径操作函数。

它可以返回任何你想要的东西。

在这个例子中，这个依赖项期望获得:

* 一个可选的查询参数 `q` 是一个 `str`.
* 一个可选的查询参数 `skip` 是一个 `int`, 默认是 `0`.
* 一个可选的查询参数 `limit` 是一个 `int`, 默认是 `100`.

然后它返回一个包含这些值的 `dict`。

### 导入 `Depends`

```Python hl_lines="3"
{!../../../docs_src/dependencies/tutorial001.py!}
```

### 使用 "dependant" 声明依赖

与您在 *path操作函数* 参数中使用 `Body`, `Query` 等相同的方式，使用 `Depends` 和一个新参数:

```Python hl_lines="13  18"
{!../../../docs_src/dependencies/tutorial001.py!}
```

尽管您在函数的参数中使用 `Depends` 的方法与使用`Body`, `Query`等相同，但 `Depends` 的工作方式略有不同。

你只给 `Depends` 一个参数

这个参数必须类似于一个函数。

这个函数获取和 *路径操作函数* 一样的参数。

!!! tip
    在下一章中，你会看到除了函数之外，还有哪些 "东西" 可以用作依赖项。

当一个新的请求到达时，**FastAPI** 将处理:

* 用正确的参数调用依赖项("可依赖的")函数。
* *从函数中获取结果。
* 将结果赋给你的 *路径操作函数* 中的参数。

```mermaid
graph TB

common_parameters(["common_parameters"])
read_items["/items/"]
read_users["/users/"]

common_parameters --> read_items
common_parameters --> read_users
```

这样，只需编写一次共享代码，**FastAPI** 就会为您的* 路径操作* 调用它。

!!! check
    注意，您不必创建一个特殊的类并将其传递到 **FastAPI** 以 "注册" 它或任何类似的东西。

    你只需要把它传递给 `Depends`然后 **FastAPI** 知道如何处理其余的工作。

## 用 `async` 或不用 `async`

由于依赖关系也将由**FastAPI**(与 *路径操作函数* 相同)调用，所以在定义函数时应用相同的规则。

你可以使用 `async def` 或常规的 `def`.

你可以在常规 `def` *路径操作函数* 中声明 `async def` 依赖，也可以在 `async def` *路径操作函数* 中声明 `def` 依赖。等等。

没关系 **FastAPI** 将知道该做什么。

!!! note
    如果你不知道相关内容，请看 [Async: *"In a hurry?"*](../../async.md){.internal-link target=_blank} 文档中关于 `async` 和 `await` 的章节.

## 与 OpenAPI 结合

依赖项(以及子依赖项)的所有请求声明、验证和需求都将集成到同一个OpenAPI模式中。

所以，交互文档也会有来自这些依赖项的所有信息:

<img src="/img/tutorial/dependencies/image01.png">

## 简单的使用

如果您仔细看一下，就会发现 *路径操作函数* 被声明为在 *路径* 和 *操作* 匹配时使用，然后 **FastAPI** 负责使用正确的参数调用函数，从请求中提取数据。

实际上，所有(或大多数) web 框架都以同样的方式工作。

你从不直接调用这些函数。它们由您的框架调用(在本例中为 **FastAPI** )。

在依赖注入系统中，您还可以告诉 **FastAPI** ，您的 *路径操作函数* 也 "依赖" 于其他应该在*路径操作函数*之前执行的东西，而 **FastAPI** 将负责执行它并 "注入" 结果。

"依赖注入" 这个概念的其他常见术语是:

* 资源
* 供应商
* 服务
* 可注入的
* 组件

## **FastAPI** 插件

集成和 "插件" 可以使用 **依赖注入系统** 来构建。但实际上，实际上 **不需要创建 "插件"** ，因为通过使用依赖项，可以声明无限数量的集成和交互，这些集成和交互可用于您的 *路径操作函数*。

依赖项可以以一种非常简单和直观的方式创建，允许您导入所需的Python包，*不夸张地*说 可以通过几行代码将它们与API函数集成在一起。

在下一章中，你将看到关于关系型数据库、NoSQL数据库、安全性等的例子。

## **FastAPI** 兼容性

简单的依赖注入系统使得 **FastAPI** 兼容:

* 所有关系数据库
* NoSQL数据库
* 外部 packages
* 外部 APIs
* 认证和授权系统
* API使用监控系统
* 响应数据注入系统
* 等。

## 简单而强大

尽管分层依赖注入系统的定义和使用非常简单，但它仍然非常强大。

您可以定义依赖，而依赖又可以定义依赖本身。

最后，构建了依赖关系的层次树，**依赖注入** 系统会为您解决所有这些依赖关系(及其子依赖关系)，并在每一步提供(注入)结果。

例如，假设你有4个API端点(*路径操作*):

* `/items/public/`
* `/items/private/`
* `/users/{user_id}/activate`
* `/items/pro/`

然后你可以通过使用依赖项和子依赖项为它们添加不同的权限要求:

```mermaid
graph TB

current_user(["current_user"])
active_user(["active_user"])
admin_user(["admin_user"])
paying_user(["paying_user"])

public["/items/public/"]
private["/items/private/"]
activate_user["/users/{user_id}/activate"]
pro_items["/items/pro/"]

current_user --> active_user
active_user --> admin_user
active_user --> paying_user

current_user --> public
active_user --> private
admin_user --> activate_user
paying_user --> pro_items
```

## 与 **OpenAPI** 集成

所有这些依赖项，在声明它们的需求时，也会在 *路径操作* 中添加参数、验证等。

**FastAPI** 将负责将其全部添加到 OpenAPI 模式，以便在交互式文档系统中显示。

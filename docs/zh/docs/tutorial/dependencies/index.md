# 依赖项 { #dependencies }

FastAPI 提供了简单易用，但功能强大的**<abbr title="也称为组件、资源、提供者、服务、可注入项">依赖注入</abbr>**系统。

这个依赖系统设计的简单易用，可以让开发人员轻松地把组件集成至 **FastAPI**。

## 什么是「依赖注入」 { #what-is-dependency-injection }

编程中的**「依赖注入」**是声明代码（本文中为*路径操作函数*）运行所需的，或要使用的「依赖」的一种方式。

然后，由系统（本文中为 **FastAPI**）负责执行任意需要的逻辑，为代码提供这些依赖（「注入」依赖项）。

依赖注入常用于以下场景：

* 共享业务逻辑（复用相同的代码逻辑）
* 共享数据库连接
* 实现安全、验证、角色权限等
* 以及许多其他事情...

上述场景均可以使用**依赖注入**，将代码重复最小化。

## 第一步 { #first-steps }

接下来，我们学习一个非常简单的例子。它会非常简单，以至于现在并不是很有用。

但通过这个例子，我们可以专注于 **依赖注入** 系统是如何工作的。

### 创建依赖项（或「可依赖项」） { #create-a-dependency-or-dependable }

首先，要关注的是依赖项。

依赖项就是一个函数，且可以使用与*路径操作函数*相同的参数：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8:9] *}

大功告成。

只用了**2 行**代码。

依赖项函数的形式和结构与*路径操作函数*一样。

因此，可以把依赖项当作没有「装饰器」（即，没有 `@app.get("/some-path")`）的路径操作函数。

依赖项可以返回各种内容。

本例中的依赖项预期接收如下参数：

* 类型为 `str` 的可选查询参数 `q`
* 类型为 `int` 的可选查询参数 `skip`，默认值是 `0`
* 类型为 `int` 的可选查询参数 `limit`，默认值是 `100`

然后，依赖项函数返回包含这些值的 `dict`。

/// info | 信息

FastAPI 在 0.95.0 版本中添加了对 `Annotated` 的支持（并开始推荐使用）。

如果你使用的是更旧的版本，尝试使用 `Annotated` 时会报错。

在使用 `Annotated` 之前，请确保[升级 FastAPI 版本](../../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}至少到 0.95.1。

///

### 导入 `Depends` { #import-depends }

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[3] *}

### 在「依赖项使用方」中声明依赖项 { #declare-the-dependency-in-the-dependant }

与在*路径操作函数*参数中使用 `Body`、`Query` 等的方式相同，声明依赖项需要使用 `Depends` 和一个新的参数：

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[13,18] *}

虽然，在函数参数中使用 `Depends` 的方式与 `Body`、`Query` 等相同，但 `Depends` 的工作方式略有不同。

你只给 `Depends` 传一个参数。

该参数必须是类似函数这样的东西。

你**不要直接调用它**（不要在末尾加上括号），你只是把它作为参数传给 `Depends()`。

该函数接收的参数和*路径操作函数*的参数一样。

/// tip | 提示

下一章你将看到，除了函数以外，还有哪些「东西」可以用作依赖项。

///

接收到新的请求时，**FastAPI** 执行如下操作：

* 用正确的参数调用依赖项（「可依赖项」）函数
* 获取函数返回的结果
* 把函数返回的结果赋值给*路径操作函数*的参数

```mermaid
graph TB

common_parameters(["common_parameters"])
read_items["/items/"]
read_users["/users/"]

common_parameters --> read_items
common_parameters --> read_users
```

这样，只编写一次共享代码，**FastAPI** 就会负责在你的多个*路径操作*中调用它。

/// check | 检查

注意，你无需创建专门的类，并将之传递给 **FastAPI** 以进行「注册」或类似的操作。

只要把它传递给 `Depends`，**FastAPI** 就知道该如何执行后续操作。

///

## 共享 `Annotated` 依赖项 { #share-annotated-dependencies }

在上面的示例中，你可以看到有一点点**代码重复**。

当你需要使用 `common_parameters()` 依赖项时，你必须写出带类型注解和 `Depends()` 的整个参数：

```Python
commons: Annotated[dict, Depends(common_parameters)]
```

但因为我们在使用 `Annotated`，我们可以把这个 `Annotated` 值存到一个变量中，并在多个地方使用它：

{* ../../docs_src/dependencies/tutorial001_02_an_py310.py hl[12,16,21] *}

/// tip | 提示

这只是标准的 Python，它被称为「类型别名」，其实并不是 **FastAPI** 特有的。

但因为 **FastAPI** 基于 Python 标准（包括 `Annotated`），你可以在代码中使用这个技巧。 😎

///

这些依赖项仍会按预期工作，而**最棒的部分**是：**类型信息会被保留**。这意味着你的编辑器仍然可以为你提供**自动补全**、**行内错误**等功能。对 `mypy` 等其他工具也是一样。

当你在一个**大型代码库**中，需要在**许多*路径操作***里反复使用**相同的依赖项**时，这会特别有用。

## 要不要使用 `async`？ { #to-async-or-not-to-async }

依赖项也会由 **FastAPI** 调用（与*路径操作函数*相同），因此定义函数时也遵循同样的规则。

即，既可以使用异步的 `async def`，也可以使用普通的 `def`。

你可以在普通的 `def` *路径操作函数*中声明异步的 `async def` 依赖项；也可以在异步的 `async def` *路径操作函数*中声明普通的 `def` 依赖项等。

这都没关系。**FastAPI** 知道该怎么处理。

/// note | 注意

如果你不了解，请查看文档中关于 `async` 和 `await` 的[异步：*“着急了？”*](../../async.md#in-a-hurry){.internal-link target=_blank}部分。

///

## 与 OpenAPI 集成 { #integrated-with-openapi }

依赖项（及子依赖项）的所有请求声明、验证和需求都可以集成至同一个 OpenAPI schema。

所以，交互文档里也会显示这些依赖项的所有信息：

<img src="/img/tutorial/dependencies/image01.png">

## 简单用法 { #simple-usage }

观察一下就会发现，*路径操作函数*会在*路径*和*操作*匹配时被使用，然后 **FastAPI** 会用正确的参数调用函数，并从请求中提取数据。

实际上，所有（或大多数）Web framework 都是这样工作的。

你永远都不需要直接调用这些函数。它们是由你的框架（在此为 **FastAPI**）调用的。

通过依赖注入系统，你还可以告诉 **FastAPI**：你的*路径操作函数*也「依赖」于其他应该在*路径操作函数*之前执行的东西，而 **FastAPI** 会负责执行它，并「注入」其结果。

与「依赖注入」这一概念相同的其他常见术语有：

* resources
* providers
* services
* injectables
* components

## **FastAPI** 插件 { #fastapi-plug-ins }

可以使用**依赖注入**系统构建集成和「插件」。但实际上，根本**不需要创建「插件」**，因为使用依赖项可以声明无限数量的集成与交互，让它们对你的*路径操作函数*可用。

创建依赖项非常简单、直观：你只需导入所需的 Python package，并用几行代码就能把它们与 API 函数集成，*字面意义上的*。

下一章你将看到这方面的示例，涵盖关系型与 NoSQL 数据库、安全等内容。

## **FastAPI** 兼容性 { #fastapi-compatibility }

依赖注入系统的简洁性让 **FastAPI** 兼容：

* 所有关系型数据库
* NoSQL 数据库
* 外部 packages
* 外部 APIs
* 认证和授权系统
* API 使用监控系统
* 响应数据注入系统
* 等等...

## 简单而强大 { #simple-and-powerful }

虽然层级式依赖注入系统的定义与使用十分简单，但它却非常强大。

你可以定义依赖项，而这些依赖项本身也可以再定义依赖项。

最终会构建一个层级依赖树，而**依赖注入**系统会负责为你解析（以及它们的子依赖项）所有这些依赖，并在每一步提供（注入）结果。

例如，假设你有 4 个 API 端点（*路径操作*）：

* `/items/public/`
* `/items/private/`
* `/users/{user_id}/activate`
* `/items/pro/`

那么你就可以仅通过依赖项和子依赖项，为它们中的每一个添加不同的权限要求：

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

## 与 **OpenAPI** 集成 { #integrated-with-openapi_1 }

所有这些依赖项在声明需求的同时，也会把参数、验证等添加到你的*路径操作*中。

**FastAPI** 会负责把这些内容全部添加到 OpenAPI schema 中，以便它显示在交互式文档系统里。

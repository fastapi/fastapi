# 更大的应用 - 多个文件 { #bigger-applications-multiple-files }

如果你正在构建一个应用或 Web API，很少能把所有东西都放在一个文件中。

**FastAPI** 提供了一个便捷工具，可以在保持所有灵活性的同时组织你的应用。

/// info | 信息

如果你来自 Flask，这相当于 Flask 的 Blueprints。

///

## 一个文件结构示例 { #an-example-file-structure }

假设你的文件结构如下：

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | 提示

这里有多个 `__init__.py` 文件：每个目录或子目录中都有一个。

这使得可以将代码从一个文件导入到另一个文件中。

例如，在 `app/main.py` 中你可以有这样一行：

```
from app.routers import items
```

///

* `app` 目录包含所有内容。并且它有一个空文件 `app/__init__.py`，所以它是一个「Python package」（「Python module」的集合）：`app`。
* 它包含一个 `app/main.py` 文件。由于它在一个 Python package（一个包含 `__init__.py` 文件的目录）中，它是该 package 的一个「module」：`app.main`。
* 还有一个 `app/dependencies.py` 文件，就像 `app/main.py` 一样，它是一个「module」：`app.dependencies`。
* 有一个子目录 `app/routers/`，里面有另一个 `__init__.py` 文件，所以它是一个「Python subpackage」：`app.routers`。
* 文件 `app/routers/items.py` 位于一个 package `app/routers/` 中，所以它是一个子模块：`app.routers.items`。
* `app/routers/users.py` 也是一样，它是另一个子模块：`app.routers.users`。
* 还有一个子目录 `app/internal/`，里面有另一个 `__init__.py` 文件，所以它是另一个「Python subpackage」：`app.internal`。
* 而文件 `app/internal/admin.py` 是另一个子模块：`app.internal.admin`。

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

带注释的同一文件结构：

```bash
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

## `APIRouter` { #apirouter }

假设专门用于处理用户的文件是 `/app/routers/users.py` 这个子模块。

你希望将与你的用户相关的*路径操作*与其余代码分开，以保持组织性。

但它仍然是同一个 **FastAPI** 应用/web API 的一部分（它是同一个「Python Package」的一部分）。

你可以使用 `APIRouter` 为该模块创建*路径操作*。

### 导入 `APIRouter` { #import-apirouter }

你导入它并创建一个「实例」，方式与你使用 `FastAPI` 类相同：

{* ../../docs_src/bigger_applications/app_an_py39/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### 使用 `APIRouter` 的*路径操作* { #path-operations-with-apirouter }

然后你用它来声明你的*路径操作*。

用法与你使用 `FastAPI` 类相同：

{* ../../docs_src/bigger_applications/app_an_py39/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

你可以把 `APIRouter` 看作一个「迷你 `FastAPI`」类。

支持所有相同的选项。

同样的 `parameters`、`responses`、`dependencies`、`tags` 等。

/// tip | 提示

在这个例子中，变量名叫 `router`，但你可以按你喜欢的方式命名。

///

我们将把这个 `APIRouter` 包含到主 `FastAPI` 应用中，但首先，让我们看看依赖项以及另一个 `APIRouter`。

## 依赖项 { #dependencies }

我们会用到一些在应用多个地方都会用到的依赖项。

所以我们把它们放在自己的 `dependencies` 模块中（`app/dependencies.py`）。

现在我们将用一个简单的依赖项来读取一个自定义的 `X-Token` header：

{* ../../docs_src/bigger_applications/app_an_py39/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | 提示

我们使用了一个虚构的 header 来简化这个示例。

但在实际场景中，使用集成的[安全性工具](security/index.md){.internal-link target=_blank}会得到更好的结果。

///

## 另一个使用 `APIRouter` 的模块 { #another-module-with-apirouter }

假设你也在 `app/routers/items.py` 模块中有专门处理应用「items」的端点。

你有以下*路径操作*：

* `/items/`
* `/items/{item_id}`

结构与 `app/routers/users.py` 完全相同。

但我们想更聪明一些，让代码更简洁。

我们知道该模块中所有*路径操作*都有相同的：

* 路径 `prefix`：`/items`。
* `tags`：（只有一个 tag：`items`）。
* 额外的 `responses`。
* `dependencies`：它们都需要我们创建的 `X-Token` 依赖项。

因此，与其把这些加到每个*路径操作*上，我们可以把它们加到 `APIRouter` 上。

{* ../../docs_src/bigger_applications/app_an_py39/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

由于每个*路径操作*的路径都必须以 `/` 开头，例如：

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...所以前缀末尾不能包含 `/`。

因此，本例中的前缀是 `/items`。

我们还可以添加一个 `tags` 列表和额外的 `responses`，它们会应用到此路由器中包含的所有*路径操作*。

并且我们可以添加一个 `dependencies` 列表，这些依赖项会添加到路由器中的所有*路径操作*中，并会对发往它们的每个请求执行/解析。

/// tip | 提示

注意，这与[*路径操作装饰器*中的依赖项](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}非常类似，不会有值传递给你的*路径操作函数*。

///

最终结果是 items 的路径现在是：

* `/items/`
* `/items/{item_id}`

...正如我们所期望的那样。

* 它们会被标记为包含单个字符串 `"items"` 的 tags 列表。
    * 这些「tags」对于自动交互式文档系统（使用 OpenAPI）特别有用。
* 它们都会包含预定义的 `responses`。
* 所有这些*路径操作*都会在执行之前先计算/执行 `dependencies` 列表。
    * 如果你也在某个具体的*路径操作*中声明了依赖项，**它们也会被执行**。
    * 路由器的依赖项会先执行，然后是[装饰器中的 `dependencies`](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}，然后是普通参数依赖项。
    * 你还可以添加[带 `scopes` 的 `Security` 依赖项](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}。

/// tip | 提示

在 `APIRouter` 中使用 `dependencies` 可以用于，例如，为一整组*路径操作*要求认证，即使这些依赖项没有分别添加到每个路径操作中。

///

/// check

`prefix`、`tags`、`responses`、以及 `dependencies` 参数（和很多其他情况一样）只是 **FastAPI** 的一个特性，用来帮助你避免代码重复。

///

### 导入依赖项 { #import-the-dependencies }

这段代码位于模块 `app.routers.items`，也就是文件 `app/routers/items.py`。

而我们需要从模块 `app.dependencies`（文件 `app/dependencies.py`）中获取依赖函数。

所以我们对依赖项使用了带 `..` 的相对导入：

{* ../../docs_src/bigger_applications/app_an_py39/routers/items.py hl[3] title["app/routers/items.py"] *}

#### 相对导入如何工作 { #how-relative-imports-work }

/// tip | 提示

如果你完全了解导入是如何工作的，请继续阅读下面的下一节。

///

一个点 `.`，例如：

```Python
from .dependencies import get_token_header
```

表示：

* 从该模块（文件 `app/routers/items.py`）所在的同一个 package（目录 `app/routers/`）开始...
* 找到模块 `dependencies`（一个假想的文件 `app/routers/dependencies.py`）...
* 然后从中导入函数 `get_token_header`。

但那个文件不存在，我们的依赖项在 `app/dependencies.py` 中。

请记住我们的应用/文件结构是怎样的：

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

两个点 `..`，例如：

```Python
from ..dependencies import get_token_header
```

表示：

* 从该模块（文件 `app/routers/items.py`）所在的同一个 package（目录 `app/routers/`）开始...
* 进入父 package（目录 `app/`）...
* 在那里找到模块 `dependencies`（文件 `app/dependencies.py`）...
* 然后从中导入函数 `get_token_header`。

这样就能正常工作！🎉

---

同样，如果我们用了三个点 `...`，例如：

```Python
from ...dependencies import get_token_header
```

那将表示：

* 从该模块（文件 `app/routers/items.py`）所在的同一个 package（目录 `app/routers/`）开始...
* 进入父 package（目录 `app/`）...
* 再进入那个 package 的父级（没有父 package，`app` 是顶层 😱）...
* 在那里找到模块 `dependencies`（文件 `app/dependencies.py`）...
* 然后从中导入函数 `get_token_header`。

这会引用 `app/` 之上的某个 package，它有自己的 `__init__.py` 等文件。但我们没有这个 package。因此，这会在示例中抛出错误。🚨

不过现在你知道它是如何工作的了，所以无论你的应用多复杂，你都可以使用相对导入。🤓

### 添加一些自定义的 `tags`、`responses` 和 `dependencies` { #add-some-custom-tags-responses-and-dependencies }

我们不需要在每个*路径操作*上添加前缀 `/items` 或 `tags=["items"]`，因为我们已经把它们加到了 `APIRouter`。

但我们仍然可以添加 _更多_ 会应用到某个特定*路径操作*的 `tags`，以及一些该*路径操作*特有的额外 `responses`：

{* ../../docs_src/bigger_applications/app_an_py39/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | 提示

最后这个路径操作会有 tags 组合：`["items", "custom"]`。

并且它在文档中也会同时有两个响应，一个用于 `404`，一个用于 `403`。

///

## 主 `FastAPI` { #the-main-fastapi }

现在，让我们看看 `app/main.py` 模块。

这里是你导入并使用 `FastAPI` 类的地方。

这将是你的应用中把所有东西串起来的主文件。

并且因为你的大部分逻辑现在都在各自特定的模块中，所以主文件会非常简单。

### 导入 `FastAPI` { #import-fastapi }

你像平常一样导入并创建一个 `FastAPI` 类。

我们甚至可以声明[全局依赖项](dependencies/global-dependencies.md){.internal-link target=_blank}，它们会与每个 `APIRouter` 的依赖项合并：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[1,3,7] title["app/main.py"] *}

### 导入 `APIRouter` { #import-the-apirouter }

现在我们导入其他包含 `APIRouter` 的子模块：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[4:5] title["app/main.py"] *}

由于文件 `app/routers/users.py` 和 `app/routers/items.py` 是同一个 Python package `app` 的子模块，我们可以使用一个点 `.` 通过「相对导入」导入它们。

### 导入是如何工作的 { #how-the-importing-works }

下面这段代码：

```Python
from .routers import items, users
```

表示：

* 从该模块（文件 `app/main.py`）所在的同一个 package（目录 `app/`）开始...
* 查找子 package `routers`（目录 `app/routers/`）...
* 并从中导入子模块 `items`（文件 `app/routers/items.py`）和 `users`（文件 `app/routers/users.py`）...

模块 `items` 将有一个变量 `router`（`items.router`）。这就是我们在 `app/routers/items.py` 中创建的那个，它是一个 `APIRouter` 对象。

然后我们对模块 `users` 做同样的事。

我们也可以这样导入它们：

```Python
from app.routers import items, users
```

/// info | 信息

第一个版本是「相对导入」：

```Python
from .routers import items, users
```

第二个版本是「绝对导入」：

```Python
from app.routers import items, users
```

要了解更多关于 Python Packages 和 Modules 的信息，请阅读 <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">Python 官方关于 Modules 的文档</a>。

///

### 避免名称冲突 { #avoid-name-collisions }

我们直接导入子模块 `items`，而不是只导入它的变量 `router`。

这是因为在子模块 `users` 中也有另一个名为 `router` 的变量。

如果我们像下面这样一个接一个地导入：

```Python
from .routers.items import router
from .routers.users import router
```

来自 `users` 的 `router` 会覆盖来自 `items` 的 `router`，我们就无法同时使用它们。

因此，为了能在同一个文件中同时使用它们，我们直接导入子模块：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[5] title["app/main.py"] *}

### 包含 `users` 和 `items` 的 `APIRouter` { #include-the-apirouters-for-users-and-items }

现在，让我们包含来自子模块 `users` 和 `items` 的 `router`：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[10:11] title["app/main.py"] *}

/// info | 信息

`users.router` 包含文件 `app/routers/users.py` 中的 `APIRouter`。

而 `items.router` 包含文件 `app/routers/items.py` 中的 `APIRouter`。

///

使用 `app.include_router()`，我们可以把每个 `APIRouter` 添加到主 `FastAPI` 应用中。

它会把该路由器中的所有路由都作为应用的一部分包含进来。

/// note | 注意

实际上，它会在内部为 `APIRouter` 中声明的每个*路径操作*创建一个*路径操作*。

因此，在幕后，它会像所有东西都属于同一个单一应用一样工作。

///

/// check

包含路由器时你不必担心性能问题。

这只会花费几微秒，并且只会在启动时发生。

所以它不会影响性能。⚡

///

### 包含一个带自定义 `prefix`、`tags`、`responses` 和 `dependencies` 的 `APIRouter` { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

现在，假设你的组织给了你 `app/internal/admin.py` 文件。

它包含一个 `APIRouter`，里面有一些管理员*路径操作*，你的组织会在多个项目之间共享。

在这个示例中它会非常简单。但假设因为它会与组织中其他项目共享，我们无法修改它，也无法直接在 `APIRouter` 上添加 `prefix`、`dependencies`、`tags` 等：

{* ../../docs_src/bigger_applications/app_an_py39/internal/admin.py hl[3] title["app/internal/admin.py"] *}

但我们仍然想在包含 `APIRouter` 时设置一个自定义 `prefix`，使它的所有*路径操作*都以 `/admin` 开头；我们还想用本项目已有的 `dependencies` 来保护它，并且想包含 `tags` 和 `responses`。

我们可以在不修改原始 `APIRouter` 的情况下，通过把这些参数传给 `app.include_router()` 来声明所有这些内容：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[14:17] title["app/main.py"] *}

这样，原始的 `APIRouter` 会保持不变，因此我们仍然可以与组织中的其他项目共享同一个 `app/internal/admin.py` 文件。

结果是，在我们的应用中，来自 `admin` 模块的每个*路径操作*都会有：

* 前缀 `/admin`。
* tag `admin`。
* 依赖项 `get_token_header`。
* 响应 `418`。 🍵

但这只会影响我们应用中的那个 `APIRouter`，不会影响任何使用它的其他代码。

因此，例如其他项目可以用不同的认证方式使用同一个 `APIRouter`。

### 包含一个*路径操作* { #include-a-path-operation }

我们也可以直接把*路径操作*添加到 `FastAPI` 应用中。

这里我们这么做了……只是为了展示我们可以 🤷：

{* ../../docs_src/bigger_applications/app_an_py39/main.py hl[21:23] title["app/main.py"] *}

它会与所有其他通过 `app.include_router()` 添加的*路径操作*一起正常工作。

/// info | 信息

**注意**：这是一个非常技术性的细节，你可能可以**直接跳过**。

---

这些 `APIRouter` 并没有被「挂载」（mounted），它们并没有与应用的其余部分隔离。

这是因为我们希望在 OpenAPI schema 和用户界面中包含它们的*路径操作*。

由于我们不能把它们隔离出来并独立于其余部分「挂载」，这些*路径操作*会被「克隆」（重新创建），而不是直接包含。

///

## 查看自动 API 文档 { #check-the-automatic-api-docs }

现在，运行你的应用：

<div class="termy">

```console
$ fastapi dev app/main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后打开文档：<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到自动 API 文档，它包含了所有子模块的路径，并且使用了正确的路径（以及前缀）和正确的 tags：

<img src="/img/tutorial/bigger-applications/image01.png">

## 使用不同的 `prefix` 多次包含同一个路由器 { #include-the-same-router-multiple-times-with-different-prefix }

你也可以对*同一个*路由器使用不同的前缀多次调用 `.include_router()`。

例如，这可能很有用：用不同前缀暴露同一个 API，比如 `/api/v1` 和 `/api/latest`。

这是一个你可能并不需要的高级用法，但如果你需要，它就在那里。

## 在另一个中包含一个 `APIRouter` { #include-an-apirouter-in-another }

就像你可以在 `FastAPI` 应用中包含一个 `APIRouter` 一样，你也可以在另一个 `APIRouter` 中包含一个 `APIRouter`，通过：

```Python
router.include_router(other_router)
```

确保你在把 `router` 包含到 `FastAPI` 应用之前就这么做，这样 `other_router` 的*路径操作*也会被包含进去。

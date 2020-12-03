# 更大的应用程序 - 多个文件

如果您正在构建一个应用程序或web API，很少会将所有的内容都放在单个文件中。

**FastAPI** 提供了一种方便的工具来构造应用程序，同时保持所有的灵活性。

!!! info
    如果你使用过 Flask, 这将相当于 Flask 的蓝图(Blueprints)。

## 文件结构示例

假设你有一个这样的文件结构:

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

!!! tip
    有几个 `__init__.py` 文件: 每个目录或子目录中都有一个。

    这允许将代码从一个文件导入到另一个文件中。

    例如，在 `app/main.py` 你可以有这样一行:

    ```
    from app.routers import items
    ```

* `app` 目录包含所有的内容。它包含一个空文件 `app/__init__.py`, 因此它是一个 "Python 包" (一个 "Python 模块" 模块的集合): `app` 。
* 它包含一个 `app/main.py` 文件。它在一个 Python 包的内部 (一个包含 `__init__.py` 文件的目录)， 他是那个包的的一个 "模块": `app.main` 。
* 也有一个 `app/dependencies.py` 文件, 就像 `app/main.py`, 它是一个 "模块": `app.dependencies` 。
* 有一个子目录 `app/routers/` 具有另外一个 `__init__.py`, 因此它是一个 "Python 子包": `app.routers` 。
* 文件 `app/routers/items.py` 在包 `app/routers/` 内部, 因此它是一个子模块: `app.routers.items` 。
* `app/routers/users.py` 文件类似, 是另外一个子模块: `app.routers.users`.
* 还有另外一个子目录 `app/internal/` 和另外一个 `__init__.py` 目录, 因此它是另外一个 "Python 子包": `app.internal` 。
* 文件 `app/internal/admin.py` 是另外一个子模块: `app.internal.admin` 。

<img src="/img/tutorial/bigger-applications/package.svg">

相同的文件结构的注释:

```
.
├── app                  # "app" 是一个 Python 包
│   ├── __init__.py      # 这个文件将 "app" 变成 "Python 包"
│   ├── main.py          # "main" 模块, 如： 导入 app.main
│   ├── dependencies.py  # "dependencies" 模块, 如： 导入 app.dependencies
│   └── routers          # "routers" 是一个 "Python 子包"
│   │   ├── __init__.py  # 将 "routers" 变成 "Python 子包"
│   │   ├── items.py     # "items" 子模块, 如： 导入 app.routers.items
│   │   └── users.py     # "users" 子模块, 如： 导入 app.routers.users
│   └── internal         # "internal" 是一个 "Python 子包"
│       ├── __init__.py  # 将 "internal" 变成 "Python 子包"
│       └── admin.py     # "admin" 子模块, 如： 导入 app.internal.admin
```

## `APIRouter`

让我们假设专门处理用户的文件是`/app/routers/users.py` 子模块。

您希望将与用户相关的 *路径操作* 与代码的其余部分分开，以保持条理性。

但它仍然是相同的**FastAPI** 应用程序/web API 的一部分(它是相同的 "Python 包" 的一部分)。

您可以使用 `APIRouter` 创建该模块的 *路径操作* 。

### 导入 `APIRouter`

导入它并创建一个 "实例"，就像你导入类 `FastAPI` 一样:

```Python hl_lines="1  3"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

### 使用 `APIRouter` 定义 *路径操作*

然后你用它来声明你的 *路径操作* 。

使用它的方式与 `FastAPI` 类相同:

```Python hl_lines="6  11  16"
{!../../../docs_src/bigger_applications/app/routers/users.py!}
```

You can think of `APIRouter` as a "mini `FastAPI`" class. 你可以把 `APIRouter` 看作一个 "迷你的 `FastAPI`" 类

支持所有相同的选项。

所有相同的 `parameters`, `responses`, `dependencies`, `tags` 等等。

!!! tip
    在这个例子中，变量被称为 `router` ，但是您可以随意命名它。

我们将把这个 `APIRouter` 应用在 `FastAPI` 主应用程序中，但首先，让我们检查依赖关系和另一个 `APIRouter` 。

## 依赖项

我们看到，我们将需要在应用程序的几个地方使用一些依赖项。

所以我们把它们放在它们自己的 `依赖` 模块(`app/dependencies.py`)中。

我们现在将使用一个简单的依赖来读取一个自定义的 `X-Token` 消息头:

```Python hl_lines="1  4-6"
{!../../../docs_src/bigger_applications/app/dependencies.py!}
```

!!! tip
    We are using an invented header to simplify this example. 我们使用了一个虚构的消息头来简化这个例子。

    但在实际情况下，使用集成的 [Security utilities](./security/index.md){.internal-link target=_blank} 会得到更好的结果。

## 另一个 `APIRouter` 模块

假设还有专门用于处理应用程序中的 "项目" 的端点在模块 `app/routers/items.py` 中。

你有处理如下路径的 *路径操作*:

* `/items/`
* `/items/{item_id}`

结构与 `app/routers/users.py` 相同。

但是我们想要更聪明一点，稍微简化一下代码。

We know all the *path operations* in this module have the same: 我们知道这个模块中所有的 *路径操作* 都具有相同的:

* 路径 `前缀`: `/items`。
* `标签`: (只有一个标签: `items`)。
* 额外的 `响应`。
* `依赖项`: 他们都需要我们创建的 `X-Token` 依赖项。

 因此，我们可以将它添加到 `APIRouter` ，而不是将所有这些添加到每个 *路径操作* 中。

```Python hl_lines="5-10  16  21"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

因为每个*路径操作* 的路径必须以 `/` 开头，例如:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...前缀不能在结尾包含 `/` 。

所以，这个例子中的前缀是 `/items` 。

我们也可以增加一个 `tags` 的列表，以及将被应用于这个路由中所有的 *路径操作* 的额外 `responses` 。

我们增加了一个 `依赖项` 的列表，这些依赖项将被添加到路由的所有 *路径操作* 中，并将被执行/解析每个向它们发出的请求。

!!! tip
    注意，很像 [*路径操作装饰器* 中的依赖项](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, 不会向 *路径操作函数* 传递任何值。

最终，项目的路径是:

* `/items/`
* `/items/{item_id}`

...正如我们设想的那样。

* 他们被包含单个字符串 `"items"` 的标签列表标记。
    * 这些 "标签" 对于自动交互式文档系统(使用OpenAPI)特别有用。
* 它们都包含预先设定的 `responses` 。
* 所有 *路径操作* 将有一个在它们运行之前评估/执行的 `依赖项` 列表。
    * 如果你也在一个特定的 *路径操作* 中声明依赖项, **它们也会被执行**。
    * 首先执行路由的依赖项，然后执行装饰器中的[*路径操作装饰器* 中的 `依赖项`](dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, 然后执行常规的参数依赖项。
    * 你也可以添加 [`Security` dependencies with `scopes`](../advanced/security/oauth2-scopes.md){.internal-link target=_blank}。

!!! tip
    在 `APIRouter` 可以中拥有 `依赖项` ，例如用于要求整个 *路径操作* 组进行身份验证。即使依赖项没有单独添加到每个依赖项中。

!!! check
    `前缀`, `标签`, `响应`, 和 `依赖项` 参数(在许多其他情况下)只是 **FastAPI** 的一个特性，可以帮助您避免代码重复。

### 导入依赖项

这段代码存在于模块 `app.routers.items` 中, 位于 `app/routers/items.py` 文件。

我们需要从模块 `app.dependencies` 中获取依赖函数，也就是文件 `app/dependencies.py` 。

所以我们对于依赖关系使用一个相对导入 `..` :

```Python hl_lines="3"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

#### 相对导入如何工作

!!! tip
    如果您完全了解导入是如何工作的，请继续阅读下面的下一节。

一个点 `.`, 比如:

```Python
from .dependencies import get_token_header
```

意味着:

* 从这个模块 (`app/routers/items.py` 文件) 所在的包开始 (目录 `app/routers/`)...
* 找到模块 `dependencies` (一个假象的文件，在 `app/routers/dependencies.py`)...
* 并从中导入函数 `get_token_header`.

但是这个文件并不存在，我们的依赖项在文件 `app/dependencies.py` 中.

还记得我们的应用程序/文件结构是什么样的吗:

<img src="/img/tutorial/bigger-applications/package.svg">

---

两个点 `..`, 比如:

```Python
from ..dependencies import get_token_header
```

意味着:

* 从这个模块 (`app/routers/items.py` 文件) 所在的包开始 (目录 `app/routers/`) ...
* 转到父包 (目录 `app/`) ...
* 在那里，找到模块的 `dependencies` (文件在 `app/routers/dependencies.py`) ...
* 并从中导入函数 `get_token_header` 。

工作正常! 🎉

---

同理，如果我们用三个点 `...`, 比如:

```Python
from ...dependencies import get_token_header
```

这意味着:

* 从这个模块 ( `app/routers/items.py`文件) 所在的包开始 (目录 `app/routers/`)...
* 转到父包 (目录 `app/`)...
* 然后转到该包的父包 (然而并没有父包, `app` 已经是顶级 😱)...
* 在那里，找到模块的 `dependencies` (文件在 `app/routers/dependencies.py`) ...
* 并从中导入函数 `get_token_header` 。

它指向的是 `app/` 上层的某个包，以及它自己的 `__init__.py` 文件，等。但我们没有。这会在我们的例子中抛出一个错误。🚨

但现在你知道了它是如何工作的，所以你可以在你自己的应用中使用相对导入，不管它们有多复杂。🤓

### Add some custom `tags`, `responses`, and `dependencies`

We are not adding the prefix `/items` nor the `tags=["items"]` to each *path operation* because we added them to the `APIRouter`.

But we can still add _more_ `tags` that will be applied to a specific *path operation*, and also some extra `responses` specific to that *path operation*:

```Python hl_lines="30-31"
{!../../../docs_src/bigger_applications/app/routers/items.py!}
```

!!! tip
    最后这个路径操作将有标签的组合: `["items", "custom"]`。

    文档中也会有两个响应，一个用于 `404` ，另一个用于  `403` 。

## `FastAPI` 主程序

现在，让我们看看 `app/main.py` 上的模块。

这里是导入和使用 `FastAPI` 类的地方。

这将是应用程序中的主文件，它将所有内容绑定在一起。

由于您的大多数逻辑现在都保存在自己的特定模块中，所以主文件将非常简单。

### 导入 `FastAPI`

像往常一样导入 `FastAPI` 类并创建一个实例。

你也可以声明 [全局依赖项](dependencies/global-dependencies.md){.internal-link target=_blank} 这将与每个 `APIRouter` 的依赖项结合在一起:

```Python hl_lines="1  3  7"
{!../../../docs_src/bigger_applications/app/main.py!}
```

### 导入 `APIRouter`

现在我们导入拥有 `APIRouter` 的子模块：

```Python hl_lines="5"
{!../../../docs_src/bigger_applications/app/main.py!}
```

由于文件 `app/routers/users.py` 和 `app/routers/items.py` 是同一个 Python 包 `app` 的子模块，我们可以使用单个点  `.` ，使用 "相对导入" 导入它们。 

### 导入如何工作

The section:

```Python
from .routers import items, users
```

意思是:

* 从这个模块 (  `app/main.py`文件) 所在的包开始 (目录`app/`)...
* 转到子包 `routers` (目录 `app/routers/`)...
* 从中导入子模块 `items` (文件 `app/routers/items.py`) 和 `users` (文件 `app/routers/users.py`)...

模块 `items` 具有一个变量 `router` (`items.router`). 这就是我们在 `app/routers/items.py` 文件中创建的那个 `APIRouter` 对象。

然后我们对模块 `users` 做同样的事情。

我们也可以像这样导入它们:

```Python
from app.routers import items, users
```

!!! info
    第一个版本是 "relative import":

    ```Python
    from .routers import items, users
    ```
    
    第二个版本是 "absolute import":

    ```Python
    from app.routers import items, users
    ```

    要了解更多关于Python包和模块的信息，请阅读 <a href="https://docs.python.org/3/tutorial/modules.html" class="external-link" target="_blank">关于模块的Python官方文档</a>.

### 避免名称冲突

我们直接导入子模块 `items` ，而不是只导入它的变量 `router` 。

这是因为在子模块 `users` 中还有一个名为 `router` 的变量。



如果我们一个接一个地导入，比如:
```Python
from .routers.items import router
from .routers.users import router
```

来自 `users` 的 `router` 将覆盖来自 `items` 的 `router` ，我们将不能够同时拥有两者。

所以，为了能够在同一个文件中使用它们，我们直接导入子模块:

```Python hl_lines="4"
{!../../../docs_src/bigger_applications/app/main.py!}
```

### 引入 `users` 和 `items` 的 `APIRouter`

Now, let's include the `router`s from the submodules `users` and `items`: 现在，让我们引入来自子模块 `users` 和 `items` 的 `router`:

```Python hl_lines="10-11"
{!../../../docs_src/bigger_applications/app/main.py!}
```

!!! info
    `users.router` 包含来自文件 `app/routers/users.py` 的 `APIRouter` 。

    `items.router` 包含来自文件 `app/routers/items.py` 的 `APIRouter` 。

通过 `app.include_router()` 我们可以将每个 `APIRouter` 添加到 `FastAPI` 主程序。

It will include all the routes from that router as part of it.它将引入来自该路由模块的所有路由作为它的一部分。

!!! note "技术细节"
    它实际上会在内部为在 `APIRouter` 中声明的每个 *路径操作* 创建一个 *路径操作* 。

    所以，在后台，它实际上会像所有东西都是同一个应用一样工作。

!!! check
    您不必担心在包含路由时的性能问题。

    这将花费几微秒的时间，并且只会在启动时发生。

    所以它不会影响性能。⚡

### 引入具有自定义 `前缀`, `标签`, `响应`, 和 `依赖项` 的 `APIRouter`

现在，让我们想象一下你的组织给你一个 `app/internal/admin.py` 文件。

它包含带有一些管理(admin) *路径操作* 的 `APIRouter` ，您的组织可以在几个项目之间共享它。

对于这个例子来说，它非常简单。但我们假设，因为它是与组织中的其他项目共享的，我们不能修改它，并直接在`APIRouter` 上添加 `前缀`, `依赖项`, `标签` 等:

```Python hl_lines="3"
{!../../../docs_src/bigger_applications/app/internal/admin.py!}
```

但是我们仍然想在引入 `APIRouter` 时设置一个自定义的 `前缀` ，这样它的所有 *路径操作* 都以 `/admin` 开始，我们想用已拥有的 `依赖` 来保护它，并且我们想包含 `标签` 和 `响应` 。

我们可以通过传递这些参数到 `app.include_router()` 来声明，而不需要修改原始的 `APIRouter` :

```Python hl_lines="14-17"
{!../../../docs_src/bigger_applications/app/main.py!}
```

这样，原始的 `APIRouter` 将保持不变，这样我们仍然可以共享相同的 `app/internal/admin.py` 的文件和组织中的其他项目。

The result is that in our app, each of the *path operations* from the `admin` module will have: 结果是，在我们的应用程序，每个从 `admin` 模块引入的 *路径操作* 将有:

* 前缀 `/admin`.
* 标签 `admin`.
* 依赖项 `get_token_header`.
* 响应 `418`. 🍵

但这只会影响app中的 `APIRouter` 而不会影响其他使用它的代码。

例如，其他项目可以使用相同的 `APIRouter` ，但使用不同的身份验证方法。

### 引入一个 *path operation*

我们也可以直接在 `FastAPI` 应用中添加 *路径操作*。

我们在这里做的…只是为了表明我们可以🤷:

```Python hl_lines="21-23"
{!../../../docs_src/bigger_applications/app/main.py!}
```

它将与所有其他由 `app.include_router()` 添加的 *路径操作* 一起正常工作。

!!! info "非常技术细节"
    **注**: 这是一个你可能可以 **直接跳过** 的非常技术性的细节，

    ---

    `APIRouter` 并没有被 "挂载" ，它们没有与应用程序的其余部分隔离。

    这是因为我们希望在OpenAPI模式和用户界面中包含它们的 *路径操作* 。

    由于我们不能仅隔离它们并独立于其他操作 "挂载" 它们，所以 *路径操作* 被 "克隆" (重新创建)了，而不是直接包含在其中。

## 检查自动API文档

现在执行 `uvicorn`, 使用模块 `app.main` 和变量 `app` :

<div class="termy">

```console
$ uvicorn app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后在浏览器访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> 打开文档。

你会看到自动API文档，包括所有子模块的路径，使用正确的路径(和前缀)和正确的标签:

<img src="/img/tutorial/bigger-applications/image01.png">

## 使用不同的 `前缀` 多次包含相同的路由

你也可以多次使用 `.include_router()` 和不同的前缀，引入 *相同的* 路由。

这可能是有用的，例如，以不同的前缀公开相同的API，例如 `/api/v1` 和 `/api/latest`.

这是一种高级用法，您可能并不真正需要它，但它确实存在，以防您需要。

## 在一个 `APIRouter` 中包含另外一个 `APIRouter`

与在 `FastAPI` 应用程序中包含一个 `APIRouter` 的方式相同，您可以使用以下方法在一个 `APIRouter` 中包含另外一个 `APIRouter` :

```Python
router.include_router(other_router)
```

该操作需要确保在 `FastAPI` 应用程序中包含 `router` 之前完成，这样来自 `other_router` 的 *路径操作* 也会包含在内。

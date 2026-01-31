# SQL（关系型）数据库 { #sql-relational-databases }

**FastAPI** 并不要求你使用 SQL（关系型）数据库。但你可以使用你想要的**任何数据库**。

这里我们来看一个使用 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> 的示例。

**SQLModel** 是构建在 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> 和 Pydantic 之上的。它由 **FastAPI** 的同一作者制作，旨在完美匹配需要使用 **SQL 数据库**的 FastAPI 应用程序。

/// tip | 提示

你可以使用任何其他你想要的 SQL 或 NoSQL 数据库库（在某些情况下称为 <abbr title="Object Relational Mapper - 对象关系映射器: 一个花哨的术语，用来指代一种库，其中某些类表示 SQL 表，而这些类的实例表示这些表中的行">"ORMs"</abbr>），FastAPI 不会强迫你使用任何东西。 😎

///

由于 SQLModel 基于 SQLAlchemy，因此你可以轻松使用任何由 SQLAlchemy **支持的数据库**（这也让它们被 SQLModel 支持），例如：

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 等。

在这个例子中，我们将使用 **SQLite**，因为它使用单个文件，并且 Python 对其有集成支持。因此，你可以直接复制这个例子并原样运行。

之后，对于你的生产应用程序，你可能会想要使用像 **PostgreSQL** 这样的数据库服务器。

/// tip | 提示

有一个使用 **FastAPI** 和 **PostgreSQL** 的官方项目生成器，其中包括了前端和更多工具： <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

这是一个非常简单且简短的教程，如果你想了解一般的数据库、SQL 或更高级的功能，请查看 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel 文档</a>。

## 安装 `SQLModel` { #install-sqlmodel }

首先，确保你创建你的[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后安装 `sqlmodel`：

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 使用单一模型创建应用程序 { #create-the-app-with-a-single-model }

我们首先创建应用程序最简单的第一个版本，只有一个 **SQLModel** 模型。

稍后我们将通过下面的**多个模型**提高其安全性和多功能性。🤓

### 创建模型 { #create-models }

导入 `SQLModel` 并创建一个数据库模型：

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 类与 Pydantic 模型非常相似（实际上，从底层来看，它确实*就是一个 Pydantic 模型*）。

有一些区别：

* `table=True` 会告诉 SQLModel 这是一个*表模型*，它应该表示 SQL 数据库中的一张**表**，而不仅仅是一个*数据模型*（就像其他常规的 Pydantic 类一样）。

* `Field(primary_key=True)` 会告诉 SQLModel `id` 是 SQL 数据库中的**主键**（你可以在 SQLModel 文档中了解更多关于 SQL 主键的信息）。

    **注意：** 我们对主键字段使用 `int | None`，这样在 Python 代码里我们就可以*创建一个没有 `id` 的对象*（`id=None`），并假设数据库会在*保存时生成它*。SQLModel 会理解数据库将提供 `id`，并在数据库 schema 中*将该列定义为非空的 `INTEGER`*。详见 <a href="https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id" class="external-link" target="_blank">SQLModel 关于主键的文档</a>。

* `Field(index=True)` 会告诉 SQLModel 应该为此列创建一个 **SQL 索引**，这样在读取按此列过滤的数据时，程序能在数据库中进行更快的查找。

    SQLModel 会知道声明为 `str` 的内容将是类型为 `TEXT`（或 `VARCHAR`，具体取决于数据库）的 SQL 列。

### 创建引擎（Engine） { #create-an-engine }

SQLModel 的 `engine`（实际上它是一个 SQLAlchemy `engine`）是用来**保持与数据库的连接**的。

你只需构建**一个 `engine` 对象**，来让你的所有代码连接到同一个数据库。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

使用 `check_same_thread=False` 可以让 FastAPI 在不同线程中使用同一个 SQLite 数据库。这很有必要，因为**单个请求**可能会使用**多个线程**（例如在依赖项中）。

不用担心，按照代码的结构，我们稍后会确保**每个请求使用一个单独的 SQLModel *session***，这实际上就是 `check_same_thread` 想要实现的。

### 创建表 { #create-the-tables }

然后，我们来添加一个函数，使用 `SQLModel.metadata.create_all(engine)` 为所有*表模型***创建表**。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 创建会话（Session）依赖项 { #create-a-session-dependency }

**`Session`** 会存储**内存中的对象**并跟踪数据中所需更改的内容，然后它**使用 `engine`** 与数据库进行通信。

我们会使用 `yield` 创建一个 FastAPI **依赖项**，为每个请求提供一个新的 `Session`。这确保我们每个请求使用一个单独的 session。🤓

然后我们创建一个 `Annotated` 的依赖项 `SessionDep` 来简化其余将使用此依赖项的代码。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 在启动时创建数据库表 { #create-database-tables-on-startup }

我们会在应用程序启动时创建数据库表。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

此处，我们在应用程序启动事件中创建表。

而对于生产环境，你可能会用一个能够在启动应用程序之前运行的迁移脚本。🤓

/// tip | 提示

SQLModel 将会拥有封装 Alembic 的迁移工具，但目前你可以直接使用 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>。

///

### 创建 Hero { #create-a-hero }

因为每个 SQLModel 模型同时也是一个 Pydantic 模型，所以你可以在与 Pydantic 模型相同的**类型注释**中使用它。

例如，如果你声明一个类型为 `Hero` 的参数，它将从 **JSON 主体**中读取数据。

同样，你可以将其声明为函数的**返回类型**，然后数据的结构就会显示在自动生成的 API 文档 UI 中。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

这里，我们使用 `SessionDep` 依赖项（一个 `Session`）将新的 `Hero` 添加到 `Session` 实例中，提交更改到数据库，刷新 `hero` 中的数据，然后返回它。

### 读取 Heroes { #read-heroes }

我们可以使用 `select()` 从数据库中**读取** `Hero`。我们可以包含 `limit` 和 `offset` 来对结果进行分页。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 读取单个 Hero { #read-one-hero }

我们可以**读取**单个 `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### 删除 Hero { #delete-a-hero }

我们也可以**删除** `Hero`。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 运行应用程序 { #run-the-app }

你可以运行这个应用程序：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后访问 `/docs` UI，你会看到 **FastAPI** 正在使用这些**模型**来**记录** API，并且还会用它们来**序列化**和**验证**数据。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 使用多个模型更新应用程序 { #update-the-app-with-multiple-models }

现在让我们稍微**重构**一下这个应用，以提高**安全性**和**多功能性**。

如果你查看之前的应用程序，你可以在 UI 中看到，到目前为止，它让客户端决定要创建的 `Hero` 的 `id`。😱

我们不应该允许这样做，因为他们可能会覆盖我们在 DB 中已经分配的 `id`。决定 `id` 的行为应该由**后端**或**数据库**来完成，**而非客户端**。

此外，我们为 hero 创建了一个 `secret_name`，但到目前为止，我们在各处都返回了它，这就不太**秘密**了... 😅

我们将通过添加一些**额外的模型**来解决这些问题，而 SQLModel 将在这里大放异彩。✨

### 创建多个模型 { #create-multiple-models }

在 **SQLModel** 中，任何含有 `table=True` 的模型类都是一个**表模型**。

而任何不含有 `table=True` 的模型类都是**数据模型**，这些实际上只是 Pydantic 模型（附带一些小的额外功能）。🤓

有了 SQLModel，我们就可以利用**继承**来在所有情况下**避免重复**所有字段。

#### `HeroBase` - 基类 { #herobase-the-base-class }

我们从一个 `HeroBase` 模型开始，该模型具有所有模型**共享的字段**：

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *表模型* { #hero-the-table-model }

接下来，我们创建 `Hero`，实际的*表模型*，并添加那些不总是在其他模型中的**额外字段**：

* `id`
* `secret_name`

因为 `Hero` 继承自 `HeroBase`，所以它**也**包含了在 `HeroBase` 中声明过的**字段**。因此 `Hero` 的所有字段为：

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公共*数据模型* { #heropublic-the-public-data-model }

接下来，我们创建一个 `HeroPublic` 模型，这是将**返回**给 API 客户端的模型。

它包含与 `HeroBase` 相同的字段，因此不会包括 `secret_name`。

终于，我们英雄的身份得到了保护！ 🥷

它还重新声明了 `id: int`。这样我们便与 API 客户端建立了一种**约定**，使他们始终可以期待 `id` 存在并且是一个 `int`（永远不会是 `None`）。

/// tip | 提示

确保返回模型始终提供一个值并且始终是 `int`（而不是 `None`）对 API 客户端非常有用，他们可以在这种确定性下编写更简单的代码。

此外，**自动生成的客户端**将拥有更简洁的接口，这样与您的 API 交互的开发者就能更轻松地使用你的 API。😎

///

`HeroPublic` 中的所有字段都与 `HeroBase` 中的相同，其中 `id` 声明为 `int`（不是 `None`）：

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - 用于创建 hero 的*数据模型* { #herocreate-the-data-model-to-create-a-hero }

现在我们创建一个 `HeroCreate` 模型，这是用于**验证**客户数据的模型。

它不仅拥有与 `HeroBase` 相同的字段，还有 `secret_name`。

现在，当客户端**创建一个新的 hero** 时，他们会发送 `secret_name`，它会被存储到数据库中，但这些 secret names 不会通过 API 返回给客户端。

/// tip | 提示

这应当是**密码**被处理的方式：接收它们，但不要通过 API 返回它们。

在存储密码之前，你还应该对密码的值进行**哈希**处理，**绝不要以明文形式存储它们**。

///

`HeroCreate` 的字段包括：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - 用于更新 hero 的*数据模型* { #heroupdate-the-data-model-to-update-a-hero }

在之前的应用程序中，我们没有办法**更新 hero**，但现在有了**多个模型**，我们便能做到这一点了。🎉

`HeroUpdate` *数据模型*有些特殊，它包含创建新 hero 所需的**所有相同字段**，但所有字段都是**可选的**（它们都有默认值）。这样，当你更新一个 hero 时，你可以只发送你想要更新的字段。

因为所有**字段实际上都发生了变化**（类型现在包括 `None`，并且它们现在有一个默认值 `None`），我们需要**重新声明**它们。

我们并不真的需要从 `HeroBase` 继承，因为我们正在重新声明所有字段。我会让它继承只是为了保持一致，但这并不必要。这更多是个人喜好的问题。🤷

`HeroUpdate` 的字段包括：

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### 使用 `HeroCreate` 创建并返回 `HeroPublic` { #create-with-herocreate-and-return-a-heropublic }

既然我们有了**多个模型**，我们就可以对使用它们的应用程序部分进行更新。

我们在请求中接收到一个 `HeroCreate` *数据模型*，然后从中创建一个 `Hero` *表模型*。

这个新的*表模型* `Hero` 会包含客户端发送的字段，以及一个由数据库生成的 `id`。

然后我们将函数中相同的*表模型* `Hero` 原样返回。但是由于我们使用 `HeroPublic` *数据模型*声明了 `response_model`，**FastAPI** 会使用 `HeroPublic` 来验证和序列化数据。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | 提示

现在我们使用 `response_model=HeroPublic` 来代替**返回类型注释** `-> HeroPublic`，因为我们返回的值实际上*并不是* `HeroPublic`。

如果我们声明了 `-> HeroPublic`，你的编辑器和 linter 会抱怨（但也确实理所应当）你返回了一个 `Hero` 而不是一个 `HeroPublic`。

通过在 `response_model` 中声明它，我们是在告诉 **FastAPI** 按照它自己的方式处理，而不会干扰类型注解以及你的编辑器和其他工具提供的帮助。

///

### 使用 `HeroPublic` 读取 Heroes { #read-heroes-with-heropublic }

我们可以像之前一样**读取** `Hero`，同样，我们使用 `response_model=list[HeroPublic]` 来确保正确地验证和序列化数据。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### 使用 `HeroPublic` 读取单个 Hero { #read-one-hero-with-heropublic }

我们可以**读取**单个 hero：

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### 使用 `HeroUpdate` 更新 Hero { #update-a-hero-with-heroupdate }

我们可以**更新一个 hero**。为此，我们会使用 HTTP 的 `PATCH` 操作。

在代码中，我们会得到一个 `dict`，其中包含客户端发送的所有数据，**只有客户端发送的数据**，并排除了任何一个仅仅作为默认值存在的值。为此，我们使用 `exclude_unset=True`。这是最主要的技巧。🪄

然后我们会使用 `hero_db.sqlmodel_update(hero_data)`，来利用 `hero_data` 的数据更新 `hero_db`。

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### 再次删除 Hero { #delete-a-hero-again }

**删除**一个 hero 基本保持不变。

我们不会满足在这一部分中重构一切的愿望。😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### 再次运行应用程序 { #run-the-app-again }

你可以再运行一次应用程序：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果你访问 `/docs` API UI，你会看到它现在已经更新，并且在进行创建 hero 等操作时，它不会再期望从客户端接收 `id`。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## 总结 { #recap }

你可以使用 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a> 与 SQL 数据库进行交互，并通过*数据模型*和*表模型*简化代码。

你可以在 **SQLModel** 文档中学习到更多内容，其中有一个更长的迷你 <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">关于将 SQLModel 与 **FastAPI** 一起使用的教程</a>。🚀

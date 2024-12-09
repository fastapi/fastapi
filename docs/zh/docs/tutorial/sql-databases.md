# SQL（关系型）数据库

**FastAPI** 并不要求您使用 SQL（关系型）数据库。您可以使用**任何**想用的数据库。

这里，我们来看一个使用 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> 的示例。

**SQLModel** 建立在 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> 和 Pydantic 之上。它由 **FastAPI** 的同一作者制作，旨在完美匹配需要使用 **SQL 数据库**的 FastAPI 应用程序。

/// tip

您可以使用任何其他您想要的 SQL 或 NoSQL 数据库库（在某些情况下称为 <abbr title="对象关系映射器（Object Relational Mapper，ORM），一个比较花哨的说法，用来指代一种库，其中某些类对应于 SQL 数据表，这些类的实例则对应于表中的行。">“ORM”</abbr>），FastAPI 不会强迫您使用任何东西。😎

///

由于 SQLModel 基于 SQLAlchemy，因此您可以轻松使用任何由 SQLAlchemy **支持的数据库**（这也让它们被 SQLModel 支持），例如：

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server 等.

在这个例子中，我们将使用 **SQLite**，因为它使用单个文件，并且 Python 对其有集成支持。因此，您可以直接复制这个例子并运行。

之后，对于您的生产应用程序，您可能会想要使用像 PostgreSQL 这样的数据库服务器。

/// tip

有一个使用 **FastAPI** 和 **PostgreSQL** 的官方的项目生成器，其中包括了前端和更多工具： <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

这是一个非常简单和简短的教程。如果你想了解一般的数据库、SQL 或更高级的功能，请查看 <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel 文档</a>。

## 安装 `SQLModel`

首先，确保您创建、激活了[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，然后安装 `sqlmodel` :

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## 创建含有单一模型的应用程序

我们首先创建应用程序的最简单的第一个版本，只有一个 **SQLModel** 模型。

稍后我们将通过下面的**多个模型**提高其安全性和多功能性。🤓

### 创建模型

导入 `SQLModel` 并创建一个数据库模型：

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` 类与 Pydantic 模型非常相似（实际上，从底层来看，它确实*就是一个 Pydantic 模型*）。

有一些区别：

* `table=True` 会告诉 SQLModel 这是一个*表模型*，它应该表示 SQL 数据库中的一个*表*，而不仅仅是一个*数据模型*（就像其他常规的 Pydantic 类一样）。

* `Field(primary_key=True)` 会告诉 SQLModel `id` 是 SQL 数据库中的**主键**（您可以在 SQLModel 文档中了解更多关于 SQL 主键的信息）。

    把类型设置为 `int | None` ，SQLModel 就能知道该列在 SQL 数据库中应该是 `INTEGER` ，并且应该是 `NULLABLE` 。

* `Field(index=True)` 会告诉 SQLModel 应该为此列创建一个 **SQL 索引**，这样在读取按此列过滤的数据时，程序能在数据库中进行更快的查找。

    SQLModel 会知道声明为 `str` 的内容将是类型为 `TEXT` （或 `VARCHAR` ，具体取决于数据库）的 SQL 列。

### 创建引擎（Engine）对象

SQLModel 的 `engine` 对象（实际上它是一个 SQLAlchemy `engine` ）是用来与数据库**保持连接**的。

您只需构建**一个 `engine` 对象**，来让您的所有代码连接到同一个数据库。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

使用 `check_same_thread=False` 可以让 FastAPI 在不同线程中使用同一个 SQLite 数据库。这很有必要，因为**单个请求**可能会使用**多个线程**（例如在依赖项中）。

不用担心，我们会按照代码结构确保**每个请求使用一个单独的 SQLModel *会话***，这实际上就是 `check_same_thread` 想要实现的。

### 创建表

然后，我们来添加一个函数，使用 `SQLModel.metadata.create_all(engine)` 为所有*表模型***创建表**。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### 创建会话（Session）依赖项

**`Session`** 会存储**内存中的对象**并跟踪数据中所需更改的内容，然后它**使用 `engine`** 与数据库进行通信。

我们会使用 `yield` 创建一个 FastAPI **依赖项**，为每个请求提供一个新的 `Session` 。这确保我们每个请求使用一个单独的会话。🤓

然后我们创建一个 `Annotated` 的依赖项 `SessionDep` 来简化其他也会用到此依赖的代码。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### 在启动时创建数据库表

我们会在应用程序启动时创建数据库表。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

此处，在应用程序启动事件中，我们创建了表。

而对于生产环境，您可能会用一个能够在启动应用程序之前运行的迁移脚本。🤓

/// tip

SQLModel 将会拥有封装 Alembic 的迁移工具，但目前您可以直接使用 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>。

///

### 创建 Hero 类

因为每个 SQLModel 模型同时也是一个 Pydantic 模型，所以您可以在与 Pydantic 模型相同的**类型注释**中使用它。

例如，如果您声明一个类型为 `Hero` 的参数，它将从 **JSON 主体**中读取数据。

同样，您可以将其声明为函数的**返回类型**，然后数据的结构就会显示在自动生成的 API 文档界面中。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

</details>

这里，我们使用 `SessionDep` 依赖项（一个 `Session` ）将新的 `Hero` 添加到 `Session` 实例中，提交更改到数据库，刷新 hero 中的数据，并返回它。

### 读取 Hero 类

我们可以使用 `select()` 从数据库中**读取** `Hero` 类。我们可以利用 `limit` 和 `offset` 来对结果进行分页。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### 读取 Hero

我们可以**读取**一个单独的 `Hero` 。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### 删除 Hero

我们也可以**删除**一个 `Hero` 。

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### 运行应用程序

您可以运行这个应用程序：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后在 `/docs` UI 中，你会看到 **FastAPI** 会用这些**模型**来**记录** API，并且还会用它们来**序列化**和**验证**数据。

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## 更新应用程序以支持多个模型

现在让我们稍微**重构**一下这个应用，以提高**安全性**和**多功能性**。

如果你查看之前的应用程序，你可以在 UI 界面中看到，到目前为止，由客户端决定要创建的 `Hero` 的 `id` 值。😱

我们不应该允许这样做，因为他们可能会覆盖我们在数据库中已经分配的 `id` 。决定 `id` 的行为应该由**后端**或**数据库**来完成，**而非客户端**。

此外，我们为 hero 创建了一个 `secret_name` ，但到目前为止，我们在各处都返回了它，这就不太**秘密**了……😅

我们将通过添加一些**额外的模型**来解决这些问题，而 SQLModel 将在这里大放异彩。✨

### Create Multiple Models

在 **SQLModel** 中，任何含有 `table=True` 属性的模型类都是一个**表模型**。

任何不含有 `table=True` 属性的模型类都是**数据模型**，这些实际上只是 Pydantic 模型（附带一些小的额外功能）。🤓

有了 SQLModel，我们就可以利用**继承**来在所有情况下**避免重复**所有字段。

#### `HeroBase` - 基类

我们从一个 `HeroBase` 模型开始，该模型具有所有模型`共享的字段`：

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *表模型*

接下来，我们创建 `Hero` ，实际的*表模型*，并添加那些不总是在其他模型中的**额外字段**：

* `id`
* `secret_name`

因为 `Hero` 继承自 HeroBase ，所以它**也**包含了在 `HeroBase` 中声明过的**字段**。因此 `Hero` 的所有字段为：

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - 公共*数据模型*

接下来，我们创建一个 `HeroPublic` 模型，这是将**返回**给 API 客户端的模型。

它包含与 `HeroBase` 相同的字段，因此不会包括 `secret_name` 。

最后，我们英雄（hero）的身份得到了保护！ 🥷

它还重新声明了 `id: int` 。这样我们便与 API 客户端建立了一种**约定**，使他们始终可以期待 `id` 存在并且是一个整数 `int`（永远不会是 `None` ）。

/// tip

确保返回模型始终提供一个值并且始终是 `int` （而不是 `None` ）对 API 客户端非常有用，他们可以在这种确定性下编写更简单的代码。

此外，**自动生成的客户端**将拥有更简洁的接口，这样与您的 API 交互的开发者就能更轻松地使用您的 API。😎

///

`HeroPublic` 中的所有字段都与 `HeroBase` 中的相同，其中 `id` 声明为 `int` （不是 `None` ）：

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - the *data model* to create a hero

Now we create a `HeroCreate` model, this is the one that will **validate** the data from the clients.

It has the same fields as `HeroBase`, and it also has `secret_name`.

Now, when the clients **create a new hero**, they will send the `secret_name`, it will be stored in the database, but those secret names won't be returned in the API to the clients.

/// tip

This is how you would handle **passwords**. Receive them, but don't return them in the API.

You would also **hash** the values of the passwords before storing them, **never store them in plain text**.

///

The fields of `HeroCreate` are:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - the *data model* to update a hero

We didn't have a way to **update a hero** in the previous version of the app, but now with **multiple models**, we can do it. 🎉

The `HeroUpdate` *data model* is somewhat special, it has **all the same fields** that would be needed to create a new hero, but all the fields are **optional** (they all have a default value). This way, when you update a hero, you can send just the fields that you want to update.

Because all the **fields actually change** (the type now includes `None` and they now have a default value of `None`), we need to **re-declare** them.

We don't really need to inherit from `HeroBase` because we are re-declaring all the fields. I'll leave it inheriting just for consistency, but this is not necessary. It's more a matter of personal taste. 🤷

The fields of `HeroUpdate` are:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Create with `HeroCreate` and return a `HeroPublic`

Now that we have **multiple models**, we can update the parts of the app that use them.

We receive in the request a `HeroCreate` *data model*, and from it, we create a `Hero` *table model*.

This new *table model* `Hero` will have the fields sent by the client, and will also have an `id` generated by the database.

Then we return the same *table model* `Hero` as is from the function. But as we declare the `response_model` with the `HeroPublic` *data model*, **FastAPI** will use `HeroPublic` to validate and serialize the data.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip

Now we use `response_model=HeroPublic` instead of the **return type annotation** `-> HeroPublic` because the value that we are returning is actually *not* a `HeroPublic`.

If we had declared `-> HeroPublic`, your editor and linter would complain (rightfully so) that you are returning a `Hero` instead of a `HeroPublic`.

By declaring it in `response_model` we are telling **FastAPI** to do its thing, without interfering with the type annotations and the help from your editor and other tools.

///

### Read Heroes with `HeroPublic`

We can do the same as before to **read** `Hero`s, again, we use `response_model=list[HeroPublic]` to ensure that the data is validated and serialized correctly.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### Read One Hero with `HeroPublic`

We can **read** a single hero:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Update a Hero with `HeroUpdate`

We can **update a hero**. For this we use an HTTP `PATCH` operation.

And in the code, we get a `dict` with all the data sent by the client, **only the data sent by the client**, excluding any values that would be there just for being the default values. To do it we use `exclude_unset=True`. This is the main trick. 🪄

Then we use `hero_db.sqlmodel_update(hero_data)` to update the `hero_db` with the data from `hero_data`.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Delete a Hero Again

**Deleting** a hero stays pretty much the same.

We won't satisfy the desire to refactor everything in this one. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Run the App Again

You can run the app again:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

If you go to the `/docs` API UI, you will see that it is now updated, and it won't expect to receive the `id` from the client when creating a hero, etc.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Recap

You can use <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a> to interact with a SQL database and simplify the code with *data models*  and *table models*.

You can learn a lot more at the **SQLModel** docs, there's a longer mini <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">tutorial on using SQLModel with **FastAPI**</a>. 🚀

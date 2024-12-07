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

## 创建含有一个模型的应用程序

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

    SQLModel will know that something declared as `str` will be a SQL column of type `TEXT` (or `VARCHAR`, depending on the database).

    SQLModel 会知道声明为 `str` 的内容将是类型为 `TEXT` （或 `VARCHAR` ，具体取决于数据库）的 SQL 列。

### Create an Engine

A SQLModel `engine` (underneath it's actually a SQLAlchemy `engine`) is what **holds the connections** to the database.

You would have **one single `engine` object** for all your code to connect to the same database.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

Using `check_same_thread=False` allows FastAPI to use the same SQLite database in different threads. This is necessary as **one single request** could use **more than one thread** (for example in dependencies).

Don't worry, with the way the code is structured, we'll make sure we use **a single SQLModel *session* per request** later, this is actually what the `check_same_thread` is trying to achieve.

### Create the Tables

We then add a function that uses `SQLModel.metadata.create_all(engine)` to **create the tables** for all the *table models*.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Create a Session Dependency

A **`Session`** is what stores the **objects in memory** and keeps track of any changes needed in the data, then it **uses the `engine`** to communicate with the database.

We will create a FastAPI **dependency** with `yield` that will provide a new `Session` for each request. This is what ensures that we use a single session per request. 🤓

Then we create an `Annotated` dependency `SessionDep` to simplify the rest of the code that will use this dependency.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Create Database Tables on Startup

We will create the database tables when the application starts.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Here we create the tables on an application startup event.

For production you would probably use a migration script that runs before you start your app. 🤓

/// tip

SQLModel will have migration utilities wrapping Alembic, but for now, you can use <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> directly.

///

### Create a Hero

Because each SQLModel model is also a Pydantic model, you can use it in the same **type annotations** that you could use Pydantic models.

For example, if you declare a parameter of type `Hero`, it will be read from the **JSON body**.

The same way, you can declare it as the function's **return type**, and then the shape of the data will show up in the automatic API docs UI.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

</details>

Here we use the `SessionDep` dependency (a `Session`) to add the new `Hero` to the `Session` instance, commit the changes to the database, refresh the data in the `hero`, and then return it.

### Read Heroes

We can **read** `Hero`s from the database using a `select()`. We can include a `limit` and `offset` to paginate the results.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Read One Hero

We can **read** a single `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Delete a Hero

We can also **delete** a `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Run the App

You can run the app:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Then go to the `/docs` UI, you will see that **FastAPI** is using these **models** to **document** the API, and it will use them to **serialize** and **validate** the data too.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Update the App with Multiple Models

Now let's **refactor** this app a bit to increase **security** and **versatility**.

If you check the previous app, in the UI you can see that, up to now, it lets the client decide the `id` of the `Hero` to create. 😱

We shouldn't let that happen, they could overwrite an `id` we already have assigned in the DB. Deciding the `id` should be done by the **backend** or the **database**, **not by the client**.

Additionally, we create a `secret_name` for the hero, but so far, we are returning it everywhere, that's not very **secret**... 😅

We'll fix these things by adding a few **extra models**. Here's where SQLModel will shine. ✨

### Create Multiple Models

In **SQLModel**, any model class that has `table=True` is a **table model**.

And any model class that doesn't have `table=True` is a **data model**, these ones are actually just Pydantic models (with a couple of small extra features). 🤓

With SQLModel, we can use **inheritance** to **avoid duplicating** all the fields in all the cases.

#### `HeroBase` - the base class

Let's start with a `HeroBase` model that has all the **fields that are shared** by all the models:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - the *table model*

Then let's create `Hero`, the actual *table model*, with the **extra fields** that are not always in the other models:

* `id`
* `secret_name`

Because `Hero` inherits form `HeroBase`, it **also** has the **fields** declared in `HeroBase`, so all the fields for `Hero` are:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - the public *data model*

Next, we create a `HeroPublic` model, this is the one that will be **returned** to the clients of the API.

It has the same fields as `HeroBase`, so it won't include `secret_name`.

Finally, the identity of our heroes is protected! 🥷

It also re-declares `id: int`. By doing this, we are making a **contract** with the API clients, so that they can always expect the `id` to be there and to be an `int` (it will never be `None`).

/// tip

Having the return model ensure that a value is always available and always `int` (not `None`) is very useful for the API clients, they can write much simpler code having this certainty.

Also, **automatically generated clients** will have simpler interfaces, so that the developers communicating with your API can have a much better time working with your API. 😎

///

All the fields in `HeroPublic` are the same as in `HeroBase`, with `id` declared as `int` (not `None`):

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

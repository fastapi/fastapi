# SQL (关系型) 数据库

FastAPI**不需要你使用一个SQL(关系型)数据库。

但是你可以使用任何你想要的关系数据库。

这里我们将看到一个使用 <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>的示例。
 
您可以轻松地通过SQLAlchemy适配到它支持的任何数据库，如:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

在本例中，我们将使用**SQLite**，因为它使用单个文件，而Python已经集成了支持。因此，您可以复制这个示例并按原样运行它。

稍后，对于您的生产应用程序，您可能需要使用像**PostgreSQL**这样的数据库服务器。

!!! tip
    有一个正式的项目生成 **FastAPI** 和 **PostgreSQL** ,全部基于 **Docker** ,包括前端和更多的工具: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! note
    注意，大多数代码是标准的 `SQLAlchemy` 代码，您可以在任何框架中使用。

    特定于 **FastAPI** 的代码一如既往地小。

## ORMs

**FastAPI** 可以使用任何数据库和任何样式的库与数据库进行对话。

一种常见的模式是使用 "ORM" : "object-relational mapping"（对象-关系映射）库。

ORM拥有将代码中的 *objects* 和数据库表("*relations*")之间进行转换的工具。

使用ORM，您通常创建一个表示SQL数据库中的表的类，类的每个属性表示一个列，具有名称和类型。

例如，一个类 `Pet` 可以表示一个SQL表 `pets`。

该类的每个 *instance* 对象表示数据库中的一行。

例如，一个对象 `orion_cat` ( `Pet` 的一个实例)可以有一个属性 `orion_cat.type` ，用于列`type`。该属性的值可以是，例如 `"cat"`。

这些orm还具有在表或实体之间建立连接或关系的工具。

这样，您还可以拥有一个属性 `orion_cat.owner` ，owner将包含此宠物的所有者的数据，取自表 *owners*。

因此，`orion_cat.owner.name` 可以是这个宠物的主人的名字(来自 `owners` 表中的 `name` 列)。

它可以有一个像 `"Arquilian"` 这样的值。

当您试图从宠物对象访问相应的表 *owners* 时，ORM将完成所有获取信息的工作。

常见的ORM有:Django-ORM (Django框架的一部分)、SQLAlchemy ORM (SQLAlchemy的一部分，独立于框架)和Peewee(独立于框架)等等。

在这里，我们将看到如何使用 **SQLAlchemy ORM** 。

您可以以类似的方式使用任何其他ORM。

!!! tip
    在文档中有一篇同样使用Peewee的文章。

## 文件结构

对于这些例子，我们假设你有一个名为 `my_super_project` 的目录，它包含一个名为 `sql_app` 的子目录，其结构如下:

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

The file `__init__.py` is just an empty file, but it tells Python that `sql_app` with all its modules (Python files) is a package.
`__init__.py` 只是一个空文件，但它告诉Python `sql_app` 及其所有模块(Python文件)是一个包。

现在让我们看看每个文件/模块做什么。

## 创建SQLAlchemy部件

让我们看看这个文件 `sql_app/database.py`.

### 导入SQLAlchemy部件

```Python hl_lines="1-3"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### 为SQLAlchemy创建一个数据库URL

```Python hl_lines="5-6"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

在本例中，我们 "连接" 到一个SQLite数据库(用SQLite数据库打开一个文件)。

该文件将位同一目录中名为`sql_app.db`。

这就是为什么最后一部分是 `./sql_app.db`.

如果你使用的是 **PostgreSQL** 数据库，你只需要取消注释行:

```Python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
```

…并将其根据您的数据库数据和凭证进行调整(对MySQL、MariaDB或任何其他数据库来说都是一样的)。

!!! tip

    This is the main line that you would have to modify if you wanted to use a different database.
    如果您想使用不同的数据库，这是您必须修改的主要的代码行。

### 创建SQLAlchemy `引擎`

第一步是创建一个SQLAlchemy "engine"。

我们稍后将在其他地方使用这个 `engine`.

```Python hl_lines="8-10"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

#### 请注意

参数:

```Python
connect_args={"check_same_thread": False}
```

...只有SQLite需要。其他数据库不需要它。


!!! info "技术细节"

    默认情况下，SQLite只允许一个线程与它通信，假设每个线程处理一个独立的请求。

    这是为了防止意外地为不同的事情(针对不同的请求)共享相同的连接。

    但是在FastAPI中，使用普通函数 (`def`) 可以有多个线程为了相同请求与数据库交互，所以我们需要通过`connect_args={"check_same_thread": False}`让SQLite知道它应该允许。

    此外，我们将确保每个请求在依赖项中获得自己的数据库连接会话，因此不需要使用默认机制。

### 创建一个 `SessionLocal` 类

`SessionLocal` 类的每个实例将是一个数据库会话。类本身还不是数据库会话。

但是一旦我们创建了 `SessionLocal` 类的实例，这个实例将是实际的数据库会话。

我们将其命名为 `SessionLocal` ，以区别于从SQLAlchemy导入的 `Session`。

稍后我们将使用 `Session` (从SQLAlchemy导入的那个)。

要创建 `SessionLocal` 类，使用函数 `sessionmaker`:

```Python hl_lines="11"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### 创建一个 `Base` 类

现在我们将使用返回类的函数 `declarative_base()` 。

稍后我们将继承这个类来创建每个数据库模型或类(ORM模型):

```Python hl_lines="13"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

## 创建数据库模型

现在让我们看看文件 `sql_app/models.py`.

### 从 `Base` 类创建SQLAlchemy模型

我们将使用之前创建的这个 `Base` 类来创建SQLAlchemy模型。

!!! tip
    SQLAlchemy使用术语 "**model**" 来指这些与数据库交互的类和实例。

    但是Pydantic也使用术语 "**model**" 来指代不同的东西，即数据验证、转换以及文档类和实例。

从 `database` 导入 `Base`  (上面的 `database.py` 文件)。

创建从它继承的类。

这些类就是SQLAlchemy模型。

```Python hl_lines="4  7-8  18-19"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

属性 `__tablename__` 告诉SQLAlchemy在数据库中为每个模型使用的表的名称。

### 创建模型属性/列

现在创建所有的模型(类)属性。

每一个属性都表示对应数据库表中的一列。

我们使用SQLAlchemy中的 `Column` 作为默认值。

并且我们传递一个SQLAlchemy类 "type" ，比如“Integer”、“String”和“Boolean”作为一个参数，它们定义了数据库中数据的类型。

```Python hl_lines="1  10-13  21-24"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

### 创建关系

现在创建关系。

为此，我们使用SQLAlchemy ORM提供的 `relationship` 。

这将或多或少成为一个 "magic" 属性，它将包含与此相关的其他表的值。

```Python hl_lines="2  15  26"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

在访问 `User` 中的 `items` 属性时，如 `my_user.items` ，它将有一个SQLAlchemy模型 `Item` 的列表(来自 `items` 表)，这些模型有一个外键指向 `users` 表中的这个记录。

当你访问 `my_user.items`， SQLAlchemy实际上会从数据库 `items` 表中获取项目，并将它们填充到这里。

当访问 `Item` 中的 `owner` 属性时，它将包含 `users` 表中的SQLAlchemy模型 `User` 。它将使用 `owner_id` 属性/列作为其外键来知道从  `users`  表中获取哪条记录。

## 创建Pydantic模型

现在让我们看看文件 `sql_app/schemas.py`.

!!! tip
    为了避免SQLAlchemy *models* 和Pydantic *models* 之间的混淆，我们将使用文件 `models.py` 表示SQLAlchemy模型，使用文件 `schemas.py` 表示Pydantic模型。

    这些Pydantic模型或多或少地定义了一个"模式"(有效的数据形状)。

    这将帮助我们在使用这两种方法时避免混淆。

### 创建初始的Pydantic *models* / 模式

创建一个 `ItemBase` 和 `UserBase` Pydantic *模型* (或者我们说"模式")，在创建或读取数据时具有共同的属性。

然后创建一个 `ItemCreate` 和 `UserCreate` ，从它们那里继承(这样它们将拥有相同的属性)，再加上创建所需的任何其他数据(属性)。

因此，用户在创建它时也会有一个“密码”。

但为了安全起见，`password` 不会在其他Pydantic *模式*中，例如，它不会在读取用户时从API中发送。

```Python hl_lines="3  6-8  11-12  23-24  27-28"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

#### SQLAlchemy样式和Pydantic样式

注意SQLAlchemy *models* 使用 `=` 定义属性，并将类型作为参数传递给 `Column` ，如:

```Python
name = Column(String)
```

而Pydantic *models* 使用 `:` 声明类型，即使用新的类型注释语法/类型提示:

```Python
name: str
```

记住这一点，这样当你把 `=` 与 `:` 和它们一起使用时就不会混淆了。

### 为读取 / 返回创建Pydantic *models* / 模式

现在创建Pydantic *models*(模式)，它将在读取数据和从API返回数据时使用。

例如，在创建一个item之前，我们不知道分配给它的ID是什么，但是当读取它时(当从API返回它时)我们已经知道了它的ID。

同样，在读取用户时，我们现在可以断言 `items` 将包含属于该用户的items。

不仅是这些items的ID，还有我们在Pydantic *模式* 中定义的用于读取items的所有数据:`Item`。

```Python hl_lines="15-17  31-34"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

!!! tip
    请注意 `User`，在读取用户(从API返回用户)时使用的Pydantic *模式* 不包含密码。


### 使用Pydantic的 `orm_mode` 

现在，在用于读取的Pydantic *模式* ，`Item` 和 `User` 中，添加一个内部的“Config”类。

这个 <a href="https://pydantic-docs.helpmanual.io/#config" class="external-link" target="_blank">`Config`</a> 类用于为Pydantic提供配置。

在这个 `Config` 类中, 设置属性 `orm_mode = True`.

```Python hl_lines="15  19-20  31  36-37"
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

!!! tip
    注意它用 `=` 赋值，比如:

    `orm_mode = True`

    它并不和之前的类型声明一样使用 `:` 。

    这是设置配置值，而不是声明类型。

Pydantic的 `orm_mode` 将告诉Pydantic *模式* 读取数据，即使它不是 `dict` ，而是ORM模型(或任何其他具有属性的任意对象)。

这样，就不再试图从一个 `dict` 中获取 `id` 值，如下所示:

```Python
id = data["id"]
```

它还会尝试从属性中获取它，如:

```Python
id = data.id
```

通过这个，Pydantic *model*与ORMs兼容，你可以在*path operations* 中的`response_model`参数中声明它。

您将能够返回一个数据库模型，它将从中读取数据。

#### 关于ORM模式的技术细节

SQLAlchemy和许多其他工具默认情况下是“延迟加载”。

例如，这意味着它们不会从数据库中获取关系数据，除非您试图访问将包含该数据的属性。

例如，访问属性 `items`:

```Python
current_user.items
```

将使SQLAlchemy访问 `items` 表并为这个用户获取items，但不是在此之前。

如果没有 `orm_mode` ，如果您从 *path operation* 返回SQLAlchemy模型，它将不会包含关系数据。

即使你在Pydantic模型中声明了这些关系。

但是在ORM模式下，由于Pydantic本身将尝试从属性访问它需要的数据(而不是假设一个 `dict` )，您可以声明您想要返回的特定数据，它将能够去获取它，甚至从ORMs。

## CRUD 工具

现在让我们看看文件 `sql_app/crud.py`.

在这个文件中，我们将使用可重用的函数来与数据库中的数据交互。

**CRUD** 来自: **C**reate, **R**ead, **U**pdate, 和 **D**elete.

...虽然在本例中我们只创建和读取。

### 读取数据

从 `sqlalchemy.orm` 中导入 `Session` ，这将允许你声明 `db` 参数的类型，并在你的函数中有更好的类型检查和补全。

导入 `模型` (SQLAlchemy模型)和 `模式` (Pydantic *models* / 模式)。

创建实用函数可以:

* 通过ID和电子邮件读取单个用户。
* 读取多个用户。
* 阅读单个条目。

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip
    通过创建只致力于与数据库交互(获取用户或项目)的函数,独立于您的 *路径操作函数* ,您可以更容易地在多个部分重用它们,并给他们添加<abbr title="用代码编写的自动化测试，检查另一段代码是否工作正常。">单元测试</abbr>。

### 创建数据

现在创建工具函数来创建数据。

步骤是::

* 用您的数据创建一个SQLAlchemy模型 *实例* 。
* `add` 实例对象到数据库会话。
* `commit` 更改到数据库(以便它们被保存)。
* `refresh` 您的实例(以便它包含来自数据库的任何新数据，比如生成的ID)。

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip
    SQLAlchemy的模型 `User` 包含一个 `hashed_password` ，它应该包含密码的安全散列版本。

    但是由于API客户端提供的是原始密码，所以需要提取它并在应用程序中生成hash后的密码。

    And then pass the `hashed_password` argument with the value to save.
    然后传递保存的值给 `hashed_password` 参数。

!!! warning
    此示例不安全，密码并没有hash。

    在实际应用程序中，您需要对密码进行hash，并且不要以明文形式保存密码。

    要了解更多细节，请返回本教程中的安全性一节。

    这里我们只关注数据库的工具和机制。

!!! tip
    我们不需要从Pydantic *model* 中读取每个关键字参数，然后将它们传递给 `Item` ，而是使用以下方法生成一个带有Pydantic *model* 的数据的“dict”:

    `item.dict()`

    and then we are passing the `dict`'s key-value pairs as the keyword arguments to the SQLAlchemy `Item`, with:
    然后我们将' dict '的键-值对作为关键字参数传递给SQLAlchemy ' Item ':

    `Item(**item.dict())`

    然后传递Pydantic *model* 不提供的额外关键字参数 `owner_id` :

    `Item(**item.dict(), owner_id=user_id)`

## **FastAPI** app 主函数

现在在文件 `sql_app/main.py` 中。让我们集成和使用之前创建的所有其他部分。

### 创建数据库表

以非常简单的方式创建数据库表:

```Python hl_lines="9"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

#### Alembic 注意事项

通常你可能会用<a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>初始化你的数据库(创建表，等等)。

您还可以使用Alembic进行 "迁移" (这是它的主要工作)。

"迁移" 是在更改SQLAlchemy模型的结构、添加新属性等之后，需要在数据库中复制这些更改、添加新列、新表等时所需要的一组步骤。

您可以在FastAPI项目中的模板中找到Alembic的示例。[Project Generation - Template](../project-generation.md){.internal-link target=_blank}. 特别是在 <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/" class="external-link" target="_blank">源代码的 `alembic` 目录中</a>。

### 创建一个依赖

!!! info
    为了做到这一点，您需要使用 **Python 3.7** 或以上版本, 或者使用 **Python 3.6** 并安装 "backports":

    ```console
    $ pip install async-exit-stack async-generator
    ```

    这将安装 <a href="https://github.com/sorcio/async_exit_stack" class="external-link" target="_blank">async-exit-stack</a> 和 <a href="https://github.com/python-trio/async_generator" class="external-link" target="_blank">async-generator</a>.

    您还可以使用在最后解释的 "middleware" 的替代方法。

现在使用我们在 `sql_app/databases.py` 文件中创建的 `SessionLocal` 类来创建一个依赖项。

我们需要为每个请求提供独立的数据库会话/连接 (`SessionLocal`) ，在所有请求中使用相同的会话，然后在请求完成后关闭它。

然后下一个请求将会创建一个新的会话。

为此，我们将创建一个新的yield依赖，如前面关于yield依赖的部分所解释的那样 [Dependencies with `yield`](dependencies/dependencies-with-yield.md){.internal-link target=_blank}。

我们的依赖项将创建一个新的SQLAlchemy `SessionLocal` ，它将在单个请求中使用，然后在请求完成后关闭它。

```Python hl_lines="15-20"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

!!! info
    我们将创建 `SessionLocal()` 和处理请求放在 `try` 块中。

    然后我们在 `finally` 块中关闭它。

    这样，我们可以确保数据库会话在请求之后始终关闭。即使在处理请求时出现异常。

    **但是您不能从退出代码中引发另一个异常**。了解更多 [Dependencies with `yield` and `HTTPException`](./dependencies/dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank}

然后，当在 *path操作函数* 中使用依赖项时，我们使用直接从SQLAlchemy导入的类型 `Session` 来声明它。

这将在 *path操作函数* 中为我们提供更好的编辑器支持，因为编辑器将知道 `db` 参数的类型是 `Session` :

```Python hl_lines="24  32  38  47  53"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

!!! info "技术细节"
    参数 `db` 实际上是类型 `SessionLocal`, 但是这个类 (使用 `sessionmaker()`创建) 是SQLAlchemy `Session` 的一个 "代理"，因此, 因此编辑器实际上并不知道提供了什么方法。

    但是通过将类型声明为 `Session`, 编辑器现在可以知道可用的方法 (`.add()`, `.query()`, `.commit()`, 等) 并且可以提供更好的支持(比如补全)。类型声明不会影响实际对象。

### 创建你的 **FastAPI** *路径操作*

现在，最后，这里是标准的 **FastAPI** *路径操作* 代码.

```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

我们在每个请求之前通过 `yield` 依赖项创建数据库会话，在之后关闭它。

然后，我们可以在*路径操作函数*中创建所需的依赖项，以直接获得该会话。

With that, we can just call `crud.get_user` directly from inside of the *path operation function* and use that session.
这样，我们就可以在 *路径操作函数* 内部直接调用 `crud.get_user` 并使用该会话。

!!! tip
    注意，返回的值是SQLAlchemy模型或SQLAlchemy模型列表。

    但是，由于所有 *路径操作* 都有一个带有使用 `orm_mode` 的Pydantic*模型*/模式的 `response_model` , Pydantic模型中声明的数据将从它们中提取出来，并返回给客户端，同时进行所有正常的过滤和验证。

!!! tip
    还要注意，有些 `response_models` 具有标准的Python类型，如 `List[schemas.Item]`。

    但是由于该 `List` 的内容/参数是一个带有orm_mode的 Pydantic*模型*，数据将像往常一样被检索并返回给客户端，没有问题。

### 关于 `def` 和 `async def`

在这里，我们在 *路径操作函数* 内部和依赖项中使用SQLAlchemy代码，反过来，它将与外部数据库通信。

这可能需要一些 "等待"。

But as SQLAlchemy doesn't have compatibility for using `await` directly, as would be with something like:
但由于SQLAlchemy不兼容直接使用 `await`，类似以下的代码:

```Python
user = await db.query(User).first()
```

...相反，我们使用:

```Python
user = db.query(User).first()
```

然后我们应该声明 *路径操作函数* 和依赖没有 `async def`，只是用一个普通的 `def`，如:

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info
    如果需要异步连接到关系数据库，请参阅 [Async SQL (Relational) Databases](../advanced/async-sql-databases.md){.internal-link target=_blank}.

!!! note "非常技术细节"
    如果你很好奇并且有深入的技术知识，你可以检查这个`async def` 和 `def`是如何处理的技术细节[Async](../async.md#very-technical-details){.internal-link target=_blank} docs.

## 迁移

因为我们直接使用SQLAlchemy，并且不需要任何类型的插件来使它与**FastAPI**一起工作，所以我们可以集成数据库<abbr title="自动更新数据库以拥有我们在模型中定义的任何新列。"> 迁移 </abbr> 直接通过 <a href="https://alembic.sqlalchemy.org" class="external-link" target="_blank">Alembic</a>。

由于与SQLAlchemy和SQLAlchemy模型相关的代码存在于独立的文件中，您甚至可以使用Alembic执行迁移，而无需安装FastAPI、Pydantic或其他任何东西。

同样，您也可以在与**FastAPI**无关的代码的其他部分中使用相同的SQLAlchemy模型和实用程序。


例如，在后台的task worker <a href="https://docs.celeryproject.org" class="external-link" target="_blank">Celery</a>, <a href="https://python-rq.org/" class="external-link" target="_blank">RQ</a>, or <a href="https://arq-docs.helpmanual.io/" class="external-link" target="_blank">ARQ</a>.

## 回顾所有的文件

 请记住，您应该有一个名为 `my_super_project` 的目录，该目录包含一个名为 `sql_app` 的子目录。

`sql_app` 应该拥有以下文件:

* `sql_app/__init__.py`: 是一个空文件.

* `sql_app/database.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

* `sql_app/schemas.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/schemas.py!}
```

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

* `sql_app/main.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/main.py!}
```

## 检查它

您可以复制此代码并按原样使用它。

!!! info

    实际上，这里显示的代码是测试的一部分。和这些文档中的大部分代码一样

然后你可以用uvicorn运行它::


<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

然后，你可以打开你的浏览器访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

您将能够与您的 **FastAPI** 应用程序交互，从一个真实的数据库读取数据:

<img src="/img/tutorial/sql-databases/image01.png">

## 与数据库直接交互

如果您想直接检索SQLite数据库(文件)，独立于FastAPI，调试其内容，添加表，列，记录，修改数据，等等，您可以使用<a href="https://sqlitebrowser.org/" class="external-link" target="_blank">DB Browser for SQLite</a>.

它会是这样的:

<img src="/img/tutorial/sql-databases/image02.png">

你也可以使用一个在线的SQLite 浏览器 <a href="https://inloop.github.io/sqlite-viewer/" class="external-link" target="_blank">SQLite Viewer</a> 或 <a href="https://extendsclass.com/sqlite-browser.html" class="external-link" target="_blank">ExtendsClass</a>.

## 使用中间件的替代性的数据库会话

如果你不能使用 `yield` 依赖 -- 例如，如果你没有使用 **Python 3.7** 也不能安装上面提到的 **Python 3.6** "backports" -- 你可以用类似的方式在 "中间件" 中设置会话。

"middleware" 基本上是一个总是为每个请求执行的函数，有些代码在端点函数之前执行，有些代码在端点函数之后执行。

### 创建一个中间件

我们将添加的中间件(只是一个函数)将为每个请求创建一个新的SQLAlchemy  `SessionLocal` ，将其添加到请求中，然后在请求完成后关闭它。

```Python hl_lines="14-22"
{!../../../docs_src/sql_databases/sql_app/alt_main.py!}
```

!!! info
    我们将创建 `SessionLocal()` 和处理请求放在 `try` 块中。

    然后我们在 `finally` 块中关闭它。

    这样，我们可以确保数据库会话在请求之后始终关闭。即使在处理请求时出现异常。

### 关于 `request.state`

`request.state` 是每个 `Request` 对象的属性。它用于存储附加到请求本身的任意对象，如本例中的数据库会话。你可以在 <a href="https://www.starlette.io/requests/#other-state" class="external-link" target="_blank">Starlette's `Request` state</a>文档中了解更多。

在这种情况下，它帮助我们确保在所有请求中使用单个数据库会话，然后(在中间件中)关闭。

### `yield`依赖项或中间件

在这里添加一个**中间件**所做的事与`yield` 依赖项类似，但有一些区别:

* 它需要更多的代码，有点复杂
* 中间件必须是一个 `异步` 函数。
    * 如果有代码在它必须 "等待"网络，它可能将你的应用程序 "阻塞"在那里降低一点性能。
    * 尽管在这里 `SQLAlchemy` 的工作方式可能不是很成问题。
    * 但如果你添加更多的代码到中间件有大量的 <abbr title="input and output">I/O</abbr> 等待，它可能会有问题。
* 中间件为*每个*请求运行。
    * 因此，将为每个请求创建一个连接。
    * 即使处理该请求的*路径操作*不需要数据库。

!!! tip
   当 `yield` 依赖项对于用例来说已经足够时，使用`yield`可能会更好。

!!! info
    最近在**FastAPI**中添加了对`yield`依赖项。

    本教程的前一个版本只有带有中间件的示例，可能有几个应用程序使用中间件进行数据库会话管理。

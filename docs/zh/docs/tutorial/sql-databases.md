# SQL (关系型) 数据库

**FastAPI**不需要你使用SQL(关系型)数据库。

但是您可以使用任何您想要的关系型数据库。

在这里，让我们看一个使用着[SQLAlchemy](https://www.sqlalchemy.org/)的示例。

您可以很容易地将SQLAlchemy支持任何数据库，像：

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server，等等其它数据库

在此示例中，我们将使用**SQLite**，因为它使用单个文件并且 在Python中具有集成支持。因此，您可以复制此示例并按原样来运行它。

稍后，对于您的产品级别的应用程序，您可能会要使用像**PostgreSQL**这样的数据库服务器。

!!! tip
    这儿有一个**FastAPI**和**PostgreSQL**的官方项目生成器，全部基于**Docker**，包括前端和更多工具：<a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

!!! note
    请注意，大部分代码是`SQLAlchemy`的标准代码，您可以用于任何框架。FastAPI特定的代码和往常一样少。

## ORMs（对象关系映射）

**FastAPI**可与任何数据库在任何样式的库中一起与 数据库进行通信。

一种常见的模式是使用“ORM”：对象关系映射。

ORM 具有在代码和数据库表（“*关系型”）中的**对象**之间转换（“*映射*”）的工具。

使用 ORM，您通常会在 SQL 数据库中创建一个代表映射的类，该类的每个属性代表一个列，具有名称和类型。

例如，一个类`Pet`可以表示一个 SQL 表`pets`。

该类的每个*实例对象都代表数据库中的一行数据。*

又例如，一个对象`orion_cat`（`Pet`的一个实例）可以有一个属性`orion_cat.type`, 对标数据库中的`type`列。并且该属性的值可以是其它，例如`"cat"`。

这些 ORM 还具有在表或实体之间建立关系的工具（比如创建多表关系）。

这样，您还可以拥有一个属性`orion_cat.owner`，它包含该宠物所有者的数据，这些数据取自另外一个表。

因此，`orion_cat.owner.name`可能是该宠物主人的姓名（来自表`owners`中的列`name`）。

它可能有一个像`"Arquilian"`(一种业务逻辑)。

当您尝试从您的宠物对象访问它时，ORM 将完成所有工作以从相应的表*所有者那里再获取信息。*

常见的 ORM 例如：Django-ORM（Django 框架的一部分）、SQLAlchemy ORM（SQLAlchemy 的一部分，独立于框架）和 Peewee（独立于框架）等。

在这里，我们将看到如何使用**SQLAlchemy ORM**。

以类似的方式，您也可以使用任何其他 ORM。

!!! tip
    在文档中也有一篇使用 Peewee 的等效的文章。

## 文件结构

对于这些示例，假设您有一个名为的目录`my_super_project`，其中包含一个名为的子目录`sql_app`，其结构如下：

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

该文件`__init__.py`只是一个空文件，但它告诉 Python 其中`sql_app`的所有模块（Python 文件）都是一个包。

现在让我们看看每个文件/模块的作用。

## 创建 SQLAlchemy 部件

让我们涉及到文件`sql_app/database.py`。

### 导入 SQLAlchemy 部件

```Python hl_lines="1-3"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### 为 SQLAlchemy 定义数据库 URL地址

```Python hl_lines="5-6"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

在这个例子中，我们正在“连接”到一个 SQLite 数据库（用 SQLite 数据库打开一个文件）。

该文件将位于文件中的同一目录中`sql_app.db`。

这就是为什么最后一部分是`./sql_app.db`.

如果您使用的是**PostgreSQL**数据库，则只需取消注释该行：

```Python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
```

...并根据您的数据库数据和相关凭据（也适用于 MySQL、MariaDB 或任何其他）对其进行调整。

!!! tip

    如果您想使用不同的数据库，这是就是您必须修改的地方。

### 创建 SQLAlchemy 引擎

第一步，创建一个 SQLAlchemy的“引擎”。

我们稍后会将这个`engine`在其他地方使用。

```Python hl_lines="8-10"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

#### 注意

参数:

```Python
connect_args={"check_same_thread": False}
```

...仅用于`SQLite`，在其他数据库不需要它。

!!! info "技术细节"

    默认情况下，SQLite 只允许一个线程与其通信，假设有多个线程的话，也只将处理一个独立的请求。

    这是为了防止意外地为不同的事物（不同的请求）共享相同的连接。

    但是在 FastAPI 中，普遍使用def函数，多个线程可以为同一个请求与数据库交互，所以我们需要使用`connect_args={"check_same_thread": False}`来让SQLite允许这样。

    此外，我们将确保每个请求都在依赖项中获得自己的数据库连接会话，因此不需要该默认机制。

### 创建一个`SessionLocal`类

每个实例`SessionLocal`都会是一个数据库会话。当然该类本身还不是数据库会话。

但是一旦我们创建了一个`SessionLocal`类的实例，这个实例将是实际的数据库会话。

我们命名它是`SessionLocal`为了将它与我们从 SQLAlchemy 导入的`Session`区别开来。

稍后我们将使用`Session`（从 SQLAlchemy 导入的那个）。

要创建`SessionLocal`类，请使用函数`sessionmaker`：

```Python hl_lines="11"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

### 创建一个`Base`类

现在我们将使用`declarative_base()`返回一个类。

稍后我们将用这个类继承，来创建每个数据库模型或类（ORM 模型）：

```Python hl_lines="13"
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

## 创建数据库模型

现在让我们看看文件`sql_app/models.py`。

### 用`Base`类来创建 SQLAlchemy 模型

我们将使用我们之前创建的`Base`类来创建 SQLAlchemy 模型。

!!! tip
    SQLAlchemy 使用的“**模型**”这个术语 来指代与数据库交互的这些类和实例。

    而 Pydantic 也使用“模型”这个术语 来指代不同的东西，即数据验证、转换以及文档类和实例。

从`database`（来自上面的`database.py`文件）导入`Base`。

创建从它继承的类。

这些类就是 SQLAlchemy 模型。

```Python hl_lines="4  7-8  18-19"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

这个`__tablename__`属性是用来告诉 SQLAlchemy 要在数据库中为每个模型使用的数据库表的名称。

### 创建模型属性/列

现在创建所有模型（类）属性。

这些属性中的每一个都代表其相应数据库表中的一列。

我们使用`Column`来表示 SQLAlchemy 中的默认值。

我们传递一个 SQLAlchemy “类型”，如`Integer`、`String`和`Boolean`，它定义了数据库中的类型，作为参数。

```Python hl_lines="1  10-13  21-24"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

### 创建关系

现在创建关系。

为此，我们使用SQLAlchemy  ORM提供的`relationship`。

这将或多或少会成为一种“神奇”属性，其中表示该表与其他相关的表中的值。

```Python hl_lines="2  15  26"
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

当访问 user 中的属性`items`时，如 中`my_user.items`，它将有一个`Item`SQLAlchemy 模型列表（来自`items`表），这些模型具有指向`users`表中此记录的外键。

当您访问`my_user.items`时，SQLAlchemy 实际上会从`items`表中的获取一批记录并在此处填充进去。

同样，当访问 Item中的属性`owner`时，它将包含表中的`User`SQLAlchemy 模型`users`。使用`owner_id`属性/列及其外键来了解要从`users`表中获取哪条记录。

## 创建 Pydantic 模型

现在让我们查看一下文件`sql_app/schemas.py`。

!!! tip
    为了避免 SQLAlchemy*模型*和 Pydantic*模型*之间的混淆，我们将有`models.py`（SQLAlchemy 模型的文件）和`schemas.py`（ Pydantic 模型的文件）。

    这些 Pydantic 模型或多或少地定义了一个“schema”（一个有效的数据形状）。

    因此，这将帮助我们在使用两者时避免混淆。

### 创建初始 Pydantic*模型*/模式

创建一个`ItemBase`和`UserBase`Pydantic*模型*（或者我们说“schema”）以及在创建或读取数据时具有共同的属性。

`ItemCreate`为 创建一个`UserCreate`继承自它们的所有属性（因此它们将具有相同的属性），以及创建所需的任何其他数据（属性）。

因此在创建时也应当有一个`password`属性。

但是为了安全起见，`password`不会出现在其他同类 Pydantic*模型*中，例如用户请求时不应该从 API 返回响应中包含它。

=== "Python 3.6 及以上版本"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="3  6-8  11-12  23-24  27-28"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 及以上版本"

    ```Python hl_lines="1  4-6  9-10  21-22  25-26"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

#### SQLAlchemy 风格和 Pydantic 风格

请注意，SQLAlchemy*模型*使用 `=`来定义属性，并将类型作为参数传递给`Column`，例如：

```Python
name = Column(String)
```

虽然 Pydantic*模型*使用`:` 声明类型，但新的类型注释语法/类型提示是：

```Python
name: str
```

请牢记这一点，这样您在使用`:`还是`=`时就不会感到困惑。

### 创建用于读取/返回的Pydantic*模型/模式*

现在创建当从 API 返回数据时、将在读取数据时使用的Pydantic*模型（schemas）。*

例如，在创建一个项目之前，我们不知道分配给它的 ID 是什么，但是在读取它时（从 API 返回时）我们已经知道它的 ID。

同样，当读取用户时，我们现在可以声明`items`，将包含属于该用户的项目。

不仅是这些项目的 ID，还有我们在 Pydantic*模型*中定义的用于读取项目的所有数据：`Item`.

=== "Python 3.6  及以上版本"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9  及以上版本"

    ```Python hl_lines="15-17  31-34"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10  及以上版本"

    ```Python hl_lines="13-15  29-32"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

!!! tip
    请注意，读取用户（从 API 返回）时将使用不包括`password`的`User` Pydantic*模型*。

### 使用 Pydantic 的`orm_mode`

现在，在用于查询的 Pydantic*模型*`Item`中`User`，添加一个内部`Config`类。

此类[`Config`](https://pydantic-docs.helpmanual.io/usage/model_config/)用于为 Pydantic 提供配置。

在`Config`类中，设置属性`orm_mode = True`。

=== "Python 3.6 及以上版本"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="15  19-20  31  36-37"
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 及以上版本"

    ```Python hl_lines="13  17-18  29  34-35"
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

!!! tip
    请注意，它使用`=`分配一个值，例如：

    `orm_mode = True`

    它不使用之前的`:`来类型声明。

    这是设置配置值，而不是声明类型。

Pydantic`orm_mode`将告诉 Pydantic*模型*读取数据，即它不是一个`dict`，而是一个 ORM 模型（或任何其他具有属性的任意对象）。

这样，而不是仅仅试图从`dict`上 `id` 中获取值，如下所示：

```Python
id = data["id"]
```

尝试从属性中获取它，如：

```Python
id = data.id
```

有了这个，Pydantic*模型*与 ORM 兼容，您只需在*路径操作*`response_model`的参数中声明它即可。

您将能够返回一个数据库模型，它将从中读取数据。

#### ORM 模式的技术细节

SQLAlchemy 和许多其他默认情况下是“延迟加载”。

这意味着，例如，除非您尝试访问包含该数据的属性，否则它们不会从数据库中获取关系数据。

例如，访问属性`items`：

```Python
current_user.items
```

将使 SQLAlchemy 转到`items`表并获取该用户的项目，在调用`.items`之前不会去查询数据库。

没有`orm_mode`，如果您从*路径操作*返回一个 SQLAlchemy 模型，它不会包含关系数据。

即使您在 Pydantic 模型中声明了这些关系，也没有用处。

但是在 ORM 模式下，由于 Pydantic 本身会尝试从属性访问它需要的数据（而不是假设为 `dict`），你可以声明你想要返回的特定数据，它甚至可以从 ORM 中获取它。

## CRUD工具

现在让我们看看文件`sql_app/crud.py`。

在这个文件中，我们将编写可重用的函数用来与数据库中的数据进行交互。

**CRUD**分别为：**增加**、**查询**、**更改**和**删除**，即增删改查。

...虽然在这个例子中我们只是新增和查询。

### 读取数据

从 `sqlalchemy.orm`中导入`Session`，这将允许您声明`db`参数的类型，并在您的函数中进行更好的类型检查和完成。

导入之前的`models`（SQLAlchemy 模型）和`schemas`（Pydantic*模型*/模式）。

创建一些实用函数来完成：

* 通过 ID 和电子邮件查询单个用户。
* 查询多个用户。
* 查询多个项目。

```Python hl_lines="1  3  6-7  10-11  14-15  27-28"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip
    通过创建仅专用于与数据库交互（获取用户或项目）的函数，独立于*路径操作函数*，您可以更轻松地在多个部分中重用它们，并为它们添加单元测试。

### 创建数据

现在创建实用程序函数来创建数据。

它的步骤是：

* 使用您的数据创建一个 SQLAlchemy 模型*实例。*
* 使用`add`来将该实例对象添加到您的数据库。
* 使用`commit`来对数据库的事务提交（以便保存它们）。
* 使用`refresh`来刷新您的数据库实例（以便它包含来自数据库的任何新数据，例如生成的 ID）。

```Python hl_lines="18-24  31-36"
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

!!! tip
    SQLAlchemy 模型`User`包含一个`hashed_password`，它应该是一个包含散列的安全密码。

    但由于 API 客户端提供的是原始密码，因此您需要将其提取并在应用程序中生成散列密码。

    然后将hashed_password参数与要保存的值一起传递。

!!! warning
    此示例不安全，密码未经过哈希处理。

    在现实生活中的应用程序中，您需要对密码进行哈希处理，并且永远不要以明文形式保存它们。

    有关更多详细信息，请返回教程中的安全部分。

    在这里，我们只关注数据库的工具和机制。

!!! tip
    这里不是将每个关键字参数传递给Item并从Pydantic模型中读取每个参数，而是先生成一个字典，其中包含Pydantic模型的数据：

    `item.dict()`

    然后我们将dict的键值对 作为关键字参数传递给 SQLAlchemy `Item`：

    `Item(**item.dict())`

    然后我们传递 Pydantic模型未提供的额外关键字参数`owner_id`：

    `Item(**item.dict(), owner_id=user_id)`

## 主**FastAPI**应用程序

现在在`sql_app/main.py`文件中 让我们集成和使用我们之前创建的所有其他部分。

### 创建数据库表

以非常简单的方式创建数据库表：

=== "Python 3.6 及以上版本"

    ```Python hl_lines="9"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="7"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

#### Alembic 注意

通常你可能会使用 <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>，来进行格式化数据库（创建表等）。

而且您还可以将 Alembic 用于“迁移”（这是它的主要工作）。

“迁移”是每当您更改 SQLAlchemy 模型的结构、添加新属性等以在数据库中复制这些更改、添加新列、新表等时所需的一组步骤。

您可以在[Project Generation - Template](https://fastapi.tiangolo.com/zh/project-generation/)的模板中找到一个 FastAPI 项目中的 Alembic 示例。具体在[`alembic`代码目录中](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/)。

### 创建依赖项

现在使用我们在`sql_app/database.py`文件中创建的`SessionLocal`来创建依赖项。

我们需要每个请求有一个独立的数据库会话/连接（`SessionLocal`），在所有请求中使用相同的会话，然后在请求完成后关闭它。

然后将为下一个请求创建一个新会话。

为此，我们将创建一个新的依赖项`yield`，正如前面关于[Dependencies with`yield`](https://fastapi.tiangolo.com/zh/tutorial/dependencies/dependencies-with-yield/)的部分中所解释的那样。

我们的依赖项将创建一个新的 SQLAlchemy `SessionLocal`，它将在单个请求中使用，然后在请求完成后关闭它。

=== "Python 3.6 及以上版本"

    ```Python hl_lines="15-20"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="13-18"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info
    我们将`SessionLocal()`请求的创建和处理放在一个`try`块中。

    然后我们在finally块中关闭它。

    通过这种方式，我们确保数据库会话在请求后始终关闭。即使在处理请求时出现异常。

    但是您不能从退出代码中引发另一个异常（在yield之后）。可以查阅 [Dependencies with yield and HTTPException](https://fastapi.tiangolo.com/zh/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception)

*然后，当在路径操作函数*中使用依赖项时，我们使用`Session`，直接从 SQLAlchemy 导入的类型声明它。

*这将为我们在路径操作函数*中提供更好的编辑器支持，因为编辑器将知道`db`参数的类型`Session`：

=== "Python 3.6 及以上版本"

    ```Python hl_lines="24  32  38  47  53"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="22  30  36  45  51"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

!!! info "技术细节"
    参数`db`实际上是 type `SessionLocal`，但是这个类（用 创建`sessionmaker()`）是 SQLAlchemy 的“代理” `Session`，所以，编辑器并不真正知道提供了哪些方法。

    但是通过将类型声明为Session，编辑器现在可以知道可用的方法（.add()、.query()、.commit()等）并且可以提供更好的支持（比如完成）。类型声明不影响实际对象。

### 创建您的**FastAPI** *路径操作*

现在，到了最后，编写标准的**FastAPI** *路径操作*代码。

=== "Python 3.6 及以上版本"

    ```Python hl_lines="23-28  31-34  37-42  45-49  52-55"
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="21-26  29-32  35-40  43-47  50-53"
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

我们在依赖项中的每个请求之前利用`yield`创建数据库会话，然后关闭它。

所以我们就可以在*路径操作函数*中创建需要的依赖，就能直接获取会话。

这样，我们就可以直接从*路径操作函数*内部调用`crud.get_user`并使用该会话，来进行对数据库操作。

!!! tip
    请注意，您返回的值是 SQLAlchemy 模型或 SQLAlchemy 模型列表。

    但是由于所有路径操作的response_model都使用 Pydantic模型/使用orm_mode模式，因此您的 Pydantic 模型中声明的数据将从它们中提取并返回给客户端，并进行所有正常的过滤和验证。

!!! tip
    另请注意，`response_models`应当是标准 Python 类型，例如`List[schemas.Item]`.

    但是由于它的内容/参数List是一个 使用orm_mode模式的Pydantic模型，所以数据将被正常检索并返回给客户端，所以没有问题。

### 关于 `def` 对比 `async def`

*在这里，我们在路径操作函数*和依赖项中都使用着 SQLAlchemy 模型，它将与外部数据库进行通信。

这会需要一些“等待时间”。

但是由于 SQLAlchemy 不具有`await`直接使用的兼容性，因此类似于：

```Python
user = await db.query(User).first()
```

...相反，我们可以使用：

```Python
user = db.query(User).first()
```

然后我们应该声明*路径操作函数*和不带 的依赖关系`async def`，只需使用普通的`def`，如下：

```Python hl_lines="2"
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    ...
```

!!! info
    如果您需要异步连接到关系数据库，请参阅[Async SQL (Relational) Databases](https://fastapi.tiangolo.com/zh/advanced/async-sql-databases/)

!!! note "Very Technical Details"
    如果您很好奇并且拥有深厚的技术知识，您可以在[Async](https://fastapi.tiangolo.com/zh/async/#very-technical-details)文档中查看有关如何处理 `async def`于`def`差别的技术细节。

## 迁移

因为我们直接使用 SQLAlchemy，并且我们不需要任何类型的插件来使用**FastAPI**，所以我们可以直接将数据库迁移至[Alembic](https://alembic.sqlalchemy.org/)进行集成。

由于与 SQLAlchemy 和 SQLAlchemy 模型相关的代码位于单独的独立文件中，您甚至可以使用 Alembic 执行迁移，而无需安装 FastAPI、Pydantic 或其他任何东西。

同样，您将能够在与**FastAPI**无关的代码的其他部分中使用相同的 SQLAlchemy 模型和实用程序。

例如，在具有[Celery](https://docs.celeryq.dev/)、[RQ](https://python-rq.org/)或[ARQ](https://arq-docs.helpmanual.io/)的后台任务工作者中。

## 审查所有文件

最后回顾整个案例，您应该有一个名为的目录`my_super_project`，其中包含一个名为`sql_app`。

`sql_app`中应该有以下文件：

* `sql_app/__init__.py`：这是一个空文件。

* `sql_app/database.py`：

```Python
{!../../../docs_src/sql_databases/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/models.py!}
```

* `sql_app/schemas.py`:

=== "Python 3.6 及以上版本"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/schemas.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/schemas.py!}
    ```

=== "Python 3.10 及以上版本"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py310/schemas.py!}
    ```

* `sql_app/crud.py`:

```Python
{!../../../docs_src/sql_databases/sql_app/crud.py!}
```

* `sql_app/main.py`:

=== "Python 3.6 及以上版本"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app/main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python
    {!> ../../../docs_src/sql_databases/sql_app_py39/main.py!}
    ```

## 执行项目

您可以复制这些代码并按原样使用它。

!!! info

    事实上，这里的代码只是大多数测试代码的一部分。

你可以用 Uvicorn 运行它：


<div class="termy">

```console
$ uvicorn sql_app.main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

打开浏览器进入 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs。</a>

您将能够与您的**FastAPI**应用程序交互，从真实数据库中读取数据：

<img src="/img/tutorial/sql-databases/image01.png">

## 直接与数据库交互

如果您想独立于 FastAPI 直接浏览 SQLite 数据库（文件）以调试其内容、添加表、列、记录、修改数据等，您可以使用[SQLite 的 DB Browser](https://sqlitebrowser.org/)

它看起来像这样：

<img src="/img/tutorial/sql-databases/image02.png">

您还可以使用[SQLite Viewer](https://inloop.github.io/sqlite-viewer/)或[ExtendsClass](https://extendsclass.com/sqlite-browser.html)等在线 SQLite 浏览器。

## 中间件替代数据库会话

如果你不能使用依赖项`yield`——例如，如果你没有使用**Python 3.7**并且不能安装上面提到的**Python 3.6**的“backports” ——你可以在类似的“中间件”中设置会话方法。

“中间件”基本功能是一个为每个请求执行的函数在请求之前进行执行相应的代码，以及在请求执行之后执行相应的代码。

### 创建中间件

我们将添加中间件（只是一个函数）将为每个请求创建一个新的 SQLAlchemy`SessionLocal`，将其添加到请求中，然后在请求完成后关闭它。

=== "Python 3.6 及以上版本"

    ```Python hl_lines="14-22"
    {!> ../../../docs_src/sql_databases/sql_app/alt_main.py!}
    ```

=== "Python 3.9 及以上版本"

    ```Python hl_lines="12-20"
    {!> ../../../docs_src/sql_databases/sql_app_py39/alt_main.py!}
    ```

!!! info
    我们将`SessionLocal()`请求的创建和处理放在一个`try`块中。

    然后我们在finally块中关闭它。

    通过这种方式，我们确保数据库会话在请求后始终关闭，即使在处理请求时出现异常也会关闭。

### 关于`request.state`

`request.state`是每个`Request`对象的属性。它用于存储附加到请求本身的任意对象，例如本例中的数据库会话。您可以在[Starlette 的关于`Request`state](https://www.starlette.io/requests/#other-state)的文档中了解更多信息。

对于这种情况下，它帮助我们确保在所有请求中使用单个数据库会话，然后关闭（在中间件中）。

### 使用`yield`依赖项与使用中间件的区别

在此处添加**中间件**与`yield`的依赖项的作用效果类似，但也有一些区别：

* 中间件需要更多的代码并且更复杂一些。
* 中间件必须是一个`async`函数。
    * 如果其中有代码必须“等待”网络，它可能会在那里“阻止”您的应用程序并稍微降低性能。
    * 尽管这里的`SQLAlchemy`工作方式可能不是很成问题。
    * 但是，如果您向等待大量I/O的中间件添加更多代码，则可能会出现问题。
* *每个*请求都会运行一个中间件。
    * 将为每个请求创建一个连接。
    * 即使处理该请求的*路径操作*不需要数据库。

!!! tip
    `tyield`当依赖项 足以满足用例时，使用`tyield`依赖项方法会更好。

!!! info
    `yield`的依赖项是最近刚加入**FastAPI**中的。

    所以本教程的先前版本只有带有中间件的示例，并且可能有多个应用程序使用中间件进行数据库会话管理。

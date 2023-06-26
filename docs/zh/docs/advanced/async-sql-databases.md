# 异步 SQL 关系型数据库

**FastAPI** 使用 <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases`</a> 为连接数据库提供异步支持（`async` 与 `await`）。

`databases` 兼容以下数据库：

* PostgreSQL
* MySQL
* SQLite

本章示例使用 **SQLite**，它使用的是单文件，且 Python 内置集成了 SQLite，因此，可以直接复制并运行本章示例。

生产环境下，则要使用 **PostgreSQL** 等数据库服务器。

!!! tip "提示"

    您可以使用 SQLAlchemy ORM（[SQL 关系型数据库一章](../tutorial/sql-databases.md){.internal-link target=_blank}）中的思路，比如，使用工具函数在数据库中执行操作，独立于 **FastAPI** 代码。

    本章不应用这些思路，等效于 <a href="https://www.starlette.io/database/" class="external-link" target="_blank">Starlette</a> 的对应内容。

## 导入与设置 `SQLAlchemy`

* 导入 `SQLAlchemy`
* 创建 `metadata` 对象
* 使用 `metadata` 对象创建 `notes` 表

```Python hl_lines="4  14  16-22"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip "提示"

    注意，上例是都是纯 SQLAlchemy Core 代码。

    `databases` 还没有进行任何操作。

## 导入并设置 `databases`

* 导入 `databases`
* 创建 `DATABASE_URL`
* 创建 `database`

```Python hl_lines="3  9  12"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip "提示"

    连接 PostgreSQL 等数据库时，需要修改 `DATABASE_URL`。

## 创建表

本例中，使用 Python 文件创建表，但在生产环境中，应使用集成迁移等功能的 Alembic 创建表。

本例在启动 **FastAPI** 应用前，直接执行这些操作。

* 创建 `engine`
* 使用 `metadata` 对象创建所有表

```Python hl_lines="25-28"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## 创建模型

创建以下 Pydantic 模型：

* 创建笔记的模型（`NoteIn`）
* 返回笔记的模型（`Note`）

```Python hl_lines="31-33  36-39"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

这两个 Pydantic 模型都可以辅助验证、序列化（转换）并注释（存档）输入的数据。

因此，API 文档会显示这些数据。

## 连接与断开

* 创建 `FastAPI` 应用
* 创建事件处理器，执行数据库连接与断开操作

```Python hl_lines="42  45-47  50-52"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## 读取笔记

创建读取笔记的*路径操作函数*：

```Python hl_lines="55-58"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note "笔记"

    注意，本例与数据库通信时使用 `await`，因此*路径操作函数*要声明为异步函数（`asnyc`）。

### 注意 `response_model=List[Note]`

`response_model=List[Note]` 使用的是 `typing.List`。

它以笔记（`Note`）列表的形式存档（及验证、序列化、筛选）输出的数据。

## 创建笔记

创建新建笔记的*路径操作函数*：

```Python hl_lines="61-65"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note "笔记"

    注意，本例与数据库通信时使用 `await`，因此要把*路径操作函数*声明为异步函数（`asnyc`）。

### 关于 `{**note.dict(), "id": last_record_id}`

`note` 是 Pydantic `Note` 对象：

`note.dict()` 返回包含如下数据的**字典**：

```Python
{
    "text": "Some note",
    "completed": False,
}
```

但它不包含 `id` 字段。

因此要新建一个包含 `note.dict()` 键值对的**字典**：

```Python
{**note.dict()}
```

`**note.dict()` 直接**解包**键值对， 因此，`{**note.dict()}` 是 `note.dict()` 的副本。

然后，扩展`dict` 副本，添加键值对`"id": last_record_id`：

```Python
{**note.dict(), "id": last_record_id}
```

最终返回的结果如下：

```Python
{
    "id": 1,
    "text": "Some note",
    "completed": False,
}
```

## 查看文档

复制这些代码，查看文档 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs。</a>

API 文档显示如下内容：

<img src="/img/tutorial/async-sql-databases/image01.png">

## 更多说明

更多内容详见 <a href="https://github.com/encode/databases" class="external-link" target="_blank">Github 上的`encode/databases` 的说明</a>。

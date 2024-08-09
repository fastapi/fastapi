# 测试数据库

您还可以使用[测试依赖项](testing-dependencies.md){.internal-link target=_blank}中的覆盖依赖项方法变更测试的数据库。

实现设置其它测试数据库、在测试后回滚数据、或预填测试数据等操作。

本章的主要思路与上一章完全相同。

## 为 SQL 应用添加测试

为了使用测试数据库，我们要升级 [SQL 关系型数据库](../tutorial/sql-databases.md){.internal-link target=_blank} 一章中的示例。

应用的所有代码都一样，直接查看那一章的示例代码即可。

本章只是新添加了测试文件。

正常的依赖项 `get_db()` 返回数据库会话。

测试时使用覆盖依赖项返回自定义数据库会话代替正常的依赖项。

本例中，要创建仅用于测试的临时数据库。

## 文件架构

创建新文件 `sql_app/tests/test_sql_app.py`。

因此，新的文件架构如下：

``` hl_lines="9-11"
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── tests
        ├── __init__.py
        └── test_sql_app.py
```

## 创建新的数据库会话

首先，为新建数据库创建新的数据库会话。

测试时，使用 `test.db` 替代 `sql_app.db`。

但其余的会话代码基本上都是一样的，只要复制就可以了。

```Python hl_lines="8-13"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

/// tip | "提示"

为减少代码重复，最好把这段代码写成函数，在 `database.py` 与 `tests/test_sql_app.py`中使用。

为了把注意力集中在测试代码上，本例只是复制了这段代码。

///

## 创建数据库

因为现在是想在新文件中使用新数据库，所以要使用以下代码创建数据库：

```Python
Base.metadata.create_all(bind=engine)
```

一般是在 `main.py` 中调用这行代码，但在 `main.py` 里，这行代码用于创建 `sql_app.db`，但是现在要为测试创建 `test.db`。

因此，要在测试代码中添加这行代码创建新的数据库文件。

```Python hl_lines="16"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

## 覆盖依赖项

接下来，创建覆盖依赖项，并为应用添加覆盖内容。

```Python hl_lines="19-24  27"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

/// tip | "提示"

`overrider_get_db()` 与 `get_db` 的代码几乎完全一样，只是 `overrider_get_db` 中使用测试数据库的 `TestingSessionLocal`。

///

## 测试应用

然后，就可以正常测试了。

```Python hl_lines="32-47"
{!../../../docs_src/sql_databases/sql_app/tests/test_sql_app.py!}
```

测试期间，所有在数据库中所做的修改都在 `test.db` 里，不会影响主应用的 `sql_app.db`。

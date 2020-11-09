# Async Databases with SQLAlchemy

This tutorial will cover the usage of SQLAlchemy async parts as an ORM.

!!! tip
    We strongly suggest going through the non async tutorial first ([SQL (Relational) Databases](../tutorial/sql-databases.md){.internal-link target=_blank}), since this tutorial will only cover the async parts of SQLAlchemy.

!!! warning
    This tutorial expects SQLAlchemy >= 1.4.

## File structure

For this example, let's say you have a directory named `my_super_project` that contains a sub-directory called `sql_app` with a structure like this:

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

Now let's see what each file/module does.
    
## Create the `SQLAlchemy` parts

To use the async parts you will need to import `create_async_engine` instead of the base engine.

```Python hl_lines="1  4  7"
{!../../../docs_src/async_sql_databases/sql_app/database.py!}
```

!!! tip
    If your using PostgreSQL you need to append `asyncpg` to the database string, as shown above.
    
    You will also need to `pip install asyncpg`

## Create models and schemas

This step in unchanged from the non-async way, so we'll just copy the code in, if you want more detail on how it works ([SQL (Relational) Databases](../tutorial/sql-databases.md){.internal-link target=_blank}).

```Python
{!../../../docs_src/async_sql_databases/sql_app/models.py!}
```

```Python
{!../../../docs_src/async_sql_databases/sql_app/schemas.py!}
```

## CRUD utils

```Python
{!../../../docs_src/async_sql_databases/sql_app/crud.py!}
```

!!! Note
    Notice that as we communicate with the database using `await`, the *function* is declared with `async`.

## Main FastAPI app

On startup we run the engine to create all the declarative_base models, you can also drop all of them on each start.

Notice how we are creating an instance of `AsyncSession` instead of the usual `Session`, this is also what we pass as the db type.

```Python
{!../../../docs_src/async_sql_databases/sql_app/main.py!}
```

## Check it

You can copy this code as is, and see the docs at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

There you can see all your API documented and interact with it:

<img src="/img/tutorial/sql-databases/image01.png">


## More info

You can read more about <a href="https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html" class="external-link" target="_blank">`SQLAlchemy` at its Docs page</a>.

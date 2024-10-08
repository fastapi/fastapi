# SQL (Relational) Databases

**FastAPI** doesn't require you to use a SQL (relational) database. But you can use any database that you want.

Here we'll see an example using <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a>.

**SQLModel** is built on top of <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> and Pydantic. It was made by the same author of **FastAPI** to be the perfect match for FastAPI applications that need to use SQL databases.

/// tip

You could use any other SQL or NoSQL database library you want (in some cases called <abbr title="Object Relational Mapper, a fancy term for a library where some classes represent SQL tables and instances represent rows in those tables">"ORMs"</abbr>), FastAPI doesn't force you to use anything. 😎

///

As SQLModel is based on SQLAlchemy, you can easily use any database supported by SQLAlchemy (which makes them also supported by SQLModel), like:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

In this example, we'll use **SQLite**, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.

Later, for your production application, you might want to use a database server like **PostgreSQL**.

/// tip

There is an official project generator with **FastAPI** and **PostgreSQL**, all based on **Docker**, including a frontend and more tools: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

This is a very simple and short tutorial, if you want to learn about databases in general, about SQL, or more advanced features, go to the <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel docs</a>.

## Install `SQLModel`

First, make sure you create your [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install `sqlmodel`:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Create Models

Import `SQLModel` and create a database model:

{* ../../docs_src/sql_databases/tutorial001.py ln[1:11] *}

The `Hero` class is very similar to a Pydantic model (in fact, underneath, it actually *is* a Pydantic model).

There are a few differences:

* `table=True` tells SQLModel that this is a *table model*, it should represent a **table** in the SQL database, it's not just a *data model* (as would be any other regular Pydantic class).

* `Field(primary_key=True)` tells SQLModel that the `id` is the **primary key** in the SQL database (you can learn more about SQL primary keys in the SQLModel docs).

    By having the type as `int | None`, SQLModel will know that this column should be an `INTEGER` in the SQL database and that it should be `NULLABLE`.

* `Field(index=True)` tells SQLModel that it should create a **SQL index** for this column, that would allow faster lookups in the database when reading data filtered by this column.

    SQLModel will know that something declared as `str` will be a SQL column of type `TEXT` (or `VARCHAR`, depending on the database).

## Create an Engine and Create the Tables

A SQLModel (actually SQLAlchemy) `engine` is what holds the connections to the database.

You would have one single `engine` object for all your code to connect to the same database.

{* ../../docs_src/sql_databases/tutorial001.py ln[1:22] *}

Using `check_same_thread=False` allows FastAPI to use the same SQLite database in different threads, as **one single request** could use **more than one thread** (for example in dependencies).

Don't worry, with the way the code is structured, we'll make sure we use **a single SQLModel *session* per request** later, this is actually what the `check_same_thread` is trying to achieve.

We then add a function that uses `SQLModel.metadata.create_all(engine)` to create the tables for all the *table models*.

## Create a Session Dependency

A `Session` is what stores the objects in memory and keeps track of any changes needed in the data, then it uses the `engine` to communicate with the database.

We will create a FastAPI dependency with `yield` that will provide a new `Session` for each request.

{* ../../docs_src/sql_databases/tutorial001.py ln[1:27] *}

## Create Database Tables on Startup

We will create the database tables when the application starts.

{* ../../docs_src/sql_databases/tutorial001.py ln[1:35] *}

Here we create the tables on an application startup event.

For production you would probably use a migration script that runs before you start your app. 🤓

/// tip

SQLModel will have migration utilities wrapping Alembic, but for now, you can use <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a> directly.

///

## Create a Hero

Because each SQLModel model is also a Pydantic model, you can use it in the same type annotations that you could use Pydantic models.

For example, if you declare a parameter of type `Hero`, it will be read from the JSON body.

The same way, you can declare it as the function's return type, and then the shape of the data will show up in the automatic API docs UI.

{* ../../docs_src/sql_databases/tutorial001.py ln[38:43] *}

</details>

Here we use the `Session` dependency to add the new `Hero` to the `Session`, commit the changes to the database, refresh the data in the `hero`, and then return it.

## Read Heroes

We can use the same `Session` dependency to read the `Hero` from the database using a `select()`. We can include a `limit` and `offset` to paginate the results.

{* ../../docs_src/sql_databases/tutorial001.py ln[46:54] *}

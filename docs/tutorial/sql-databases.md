**FastAPI** doesn't require you to use a SQL (relational) database.

But you can use any relational database that you want.

Here we'll see an example using <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy</a>.

You can easily adapt it to any database supported by SQLAlchemy, like:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

In this example, we'll use **PostgreSQL**.

!!! note
    Notice that most of the code is the standard `SQLAlchemy` code you would use with any framework.

    The **FastAPI** specific code is as small as always.

## Import SQLAlchemy components

For now, don't pay attention to the rest, only the imports:

```Python hl_lines="3 4 5"
{!./src/sql_databases/tutorial001.py!}
```

## Define the database

Define the database that SQLAlchemy should connect to:

```Python hl_lines="8"
{!./src/sql_databases/tutorial001.py!}
```

!!! tip
    This is the main line that you would have to modify if you wanted to use a different database than **PostgreSQL**.

## Create the SQLAlchemy `engine`

```Python hl_lines="10"
{!./src/sql_databases/tutorial001.py!}
```

## Create a `scoped_session`

```Python hl_lines="11 12 13"
{!./src/sql_databases/tutorial001.py!}
```

!!! note "Very Technical Details"
    Don't worry too much if you don't understand this. You can still use the code.

    This `scoped_session` is a feature of SQLAlchemy.

    The resulting object, the `db_session` can then be used anywhere a a normal SQLAlchemy session.
    
    It can be used as a global because it is implemented to work independently on each "<abbr title="A sequence of code being executed by the program, while at the same time, or at intervals, there can be others being executed too.">thread</abbr>", so the actions you perform with it in one path operation function won't affect the actions performed (possibly concurrently) by other path operation functions.

## Create a `CustomBase` model

This is more of a trick to facilitate your life than something required.

But by creating this `CustomBase` class and inheriting from it, your models will have automatic `__tablename__` attributes (that are required by SQLAlchemy).

That way you don't have to declare them explicitly.

So, your models will behave very similarly to, for example, Flask-SQLAlchemy.

```Python hl_lines="16 17 18 19 20"
{!./src/sql_databases/tutorial001.py!}
```

## Create the SQLAlchemy `Base` model

```Python hl_lines="23"
{!./src/sql_databases/tutorial001.py!}
```

## Create your application data model

Now this is finally code specific to your app.

Here's a user model that will be a table in the database:

```Python hl_lines="26 27 28 29 30"
{!./src/sql_databases/tutorial001.py!}
```

## Get a user

By creating a function that is only dedicated to getting your user from a `username` (or any other parameter) independent of your path operation function, you can more easily re-use it in multiple parts and also add <abbr title="Automated test, written in code, that checks if another piece of code is working correctly.">unit tests</abbr> for it:

```Python hl_lines="33 34"
{!./src/sql_databases/tutorial001.py!}
```

## Create your **FastAPI** code

Now, finally, here's the standard **FastAPI** code.

Create your app and path operation function:

```Python hl_lines="38 41 42 43 44"
{!./src/sql_databases/tutorial001.py!}
```

As we are using SQLAlchemy's `scoped_session`, we don't even have to create a dependency with `Depends`.

We can just call `get_user` directly from inside of the path operation function and use the global `db_session`.

## Create the path operation function

Here we are using SQLAlchemy code inside of the path operation function, and it in turn will go and communicate with an external database. 

That could potentially require some "waiting".

But as SQLAlchemy doesn't have compatibility for using `await`, as would be with something like:

```Python
user = await get_user(username, db_session)
```

...and instead we are using:

```Python
user = get_user(username, db_session)
```

Then we should declare the path operation without `async def`, just with a normal `def`:

```Python hl_lines="42"
{!./src/sql_databases/tutorial001.py!}
```

## Migrations

Because we are using SQLAlchemy directly and we don't require any kind of plug-in for it to work with **FastAPI**, we could integrate database <abbr title="Automatically updating the database to have any new column we define in our models.">migrations</abbr> with <a href="https://alembic.sqlalchemy.org" target="_blank">Alembic</a> directly.

You would probably want to declare your database and models in a different file or set of files, this would allow Alembic to import it and use it without even needing to have **FastAPI** installed for the migrations.

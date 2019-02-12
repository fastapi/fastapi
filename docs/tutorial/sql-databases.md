**FastAPI** doesn't require you to use a SQL (relational) database.

But you can use any relational database that you want.

Here we'll see an example using <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy</a>.

You can easily adapt it to any database supported by SQLAlchemy, like:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

In this example, we'll use **SQLite**, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.

Later, for your production application, you might want to use a database server like **PostgreSQL**.

!!! note
    Notice that most of the code is the standard `SQLAlchemy` code you would use with any framework.

    The **FastAPI** specific code is as small as always.

## Import SQLAlchemy components

For now, don't pay attention to the rest, only the imports:

```Python hl_lines="2 3 4"
{!./src/sql_databases/tutorial001.py!}
```

## Define the database

Define the database that SQLAlchemy should "connect" to:

```Python hl_lines="7"
{!./src/sql_databases/tutorial001.py!}
```

In this example, we are "connecting" to a SQLite database (opening a file with the SQLite database).

The file will be located at the same directory in the file `test.db`. That's why the last part is `./test.db`.

If you were using a **PostgreSQL** database instead, you would just have to uncomment the line:

```Python
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"
```

...and adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other).

!!! tip
    
    This is the main line that you would have to modify if you wanted to use a different database.

## Create the SQLAlchemy `engine`

```Python hl_lines="10 11 12"
{!./src/sql_databases/tutorial001.py!}
```

### Note

The argument:

```Python
connect_args={"check_same_thread": False}
```

...is needed only for `SQLite`. It's not needed for other databases.

!!! info "Technical Details"

    That argument `check_same_thread` is there mainly to be able to run the tests that cover this example.
    

## Create a `scoped_session`

```Python hl_lines="13 14 15"
{!./src/sql_databases/tutorial001.py!}
```

!!! note "Very Technical Details"
    Don't worry too much if you don't understand this. You can still use the code.

    This `scoped_session` is a feature of SQLAlchemy.

    The resulting object, the `db_session` can then be used anywhere as a normal SQLAlchemy session.
    
    It can be used as a "global" variable because it is implemented to work independently on each "<abbr title="A sequence of code being executed by the program, while at the same time, or at intervals, there can be others being executed too.">thread</abbr>", so the actions you perform with it in one path operation function won't affect the actions performed (possibly concurrently) by other path operation functions.

## Create a `CustomBase` model

This is more of a trick to facilitate your life than something required.

But by creating this `CustomBase` class and inheriting from it, your models will have automatic `__tablename__` attributes (that are required by SQLAlchemy).

That way you don't have to declare them explicitly in every model.

So, your models will behave very similarly to, for example, Flask-SQLAlchemy.

```Python hl_lines="18 19 20 21 22"
{!./src/sql_databases/tutorial001.py!}
```

## Create the SQLAlchemy `Base` model

```Python hl_lines="25"
{!./src/sql_databases/tutorial001.py!}
```

## Create your application data model

Now this is finally code specific to your app.

Here's a user model that will be a table in the database:

```Python hl_lines="28 29 30 31 32"
{!./src/sql_databases/tutorial001.py!}
```

## Initialize your application

In a very simplistic way, initialize your database (create the tables, etc) and make sure you have a first user:

```Python hl_lines="35 37 38 39 40 41"
{!./src/sql_databases/tutorial001.py!}
```

### Note

Normally you would probably initialize your database (create tables, etc) with <a href="https://alembic.sqlalchemy.org/en/latest/" target="_blank">Alembic</a>.

And you would also use Alembic for migrations (that's its main job). For whenever you change the structure of your database, add a new column, a new table, etc.

The same way, you would probably make sure there's a first user in an external script that runs before your application, or as part of the application startup.

In this example we are doing those two operations in a very simple way, directly in the code, to focus on the main points.

Also, as all the functionality is self-contained in the same code, you can copy it and run it directly, and it will work as is.


## Get a user

By creating a function that is only dedicated to getting your user from a `user_id` (or any other parameter) independent of your path operation function, you can more easily re-use it in multiple parts and also add <abbr title="Automated tests, written in code, that check if another piece of code is working correctly.">unit tests</abbr> for it:

```Python hl_lines="45 46"
{!./src/sql_databases/tutorial001.py!}
```

## Create your **FastAPI** code

Now, finally, here's the standard **FastAPI** code.

Create your app and path operation function:

```Python hl_lines="50 53 54 55 56"
{!./src/sql_databases/tutorial001.py!}
```

As we are using SQLAlchemy's `scoped_session`, we don't even have to create a dependency with `Depends`.

We can just call `get_user` directly from inside of the path operation function and use the global `db_session`.

## Create the path operation function

Here we are using SQLAlchemy code inside of the path operation function, and in turn it will go and communicate with an external database. 

That could potentially require some "waiting".

But as SQLAlchemy doesn't have compatibility for using `await` directly, as would be with something like:

```Python
user = await get_user(db_session, user_id=user_id)
```

...and instead we are using:

```Python
user = get_user(db_session, user_id=user_id)
```

Then we should declare the path operation without `async def`, just with a normal `def`:

```Python hl_lines="54"
{!./src/sql_databases/tutorial001.py!}
```

## Migrations

Because we are using SQLAlchemy directly and we don't require any kind of plug-in for it to work with **FastAPI**, we could integrate database <abbr title="Automatically updating the database to have any new column we define in our models.">migrations</abbr> with <a href="https://alembic.sqlalchemy.org" target="_blank">Alembic</a> directly.

You would probably want to declare your database and models in a different file or set of files, this would allow Alembic to import it and use it without even needing to have **FastAPI** installed for the migrations.

## Check it

You can copy this code and use it as is.

!!! info

    In fact, the code shown here is part of the tests. As most of the code in these docs.


You can copy it, let's say, to a file `main.py`.

Then you can run it with Uvicorn:

```bash
uvicorn main:app --debug
```

And then, you can open your browser at <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

And you will be able to interact with your **FastAPI** application, reading data from a real database:

<img src="/img/tutorial/sql-databases/image01.png">

## Response schema and security

This section has the minimum code to show how it works and how you can integrate SQLAlchemy with FastAPI.

But it is recommended that you also create a response model with Pydantic, as described in the section about <a href="/tutorial/extra-models/" target="_blank">Extra Models</a>.

That way you will document the schema of the responses of your API, and you will be able to limit/filter the returned data.

Limiting the returned data is important for security, as for example, you shouldn't be returning the `hashed_password` to the clients.

That's something that you can improve in this example application, here's the current response data:

```JSON
{
  "is_active": true,
  "hashed_password": "notreallyhashed",
  "email": "johndoe@example.com",
  "id": 1
}
```

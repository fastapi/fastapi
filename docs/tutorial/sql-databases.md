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

!!! tip
    There is an official project generator with **FastAPI** and **PostgreSQL**, all based on **Docker**, including a frontend and more tools: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>


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

```Python hl_lines="9"
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

```Python hl_lines="12 13 14"
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
    

## Create a `SessionLocal` class

Each instance of the `SessionLocal` class will have a connection to the database.

This object (class) is not a connection to the database yet, but once we create an instance of this class, that instance will have the actual connection to the database.

We name it `SessionLocal` to distinguish it form the `Session` we are importing from SQLAlchemy.

We will use `Session` to declare types later and to get better editor support and completion.

For now, create the `SessionLocal`:

```Python hl_lines="15"
{!./src/sql_databases/tutorial001.py!}
```

## Create a middleware to handle sessions

Now let's temporarily jump to the end of the file, to use the `SessionLocal` class we created above.

We need to have an independent database session/connection (`SessionLocal`) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new middleware.

A "middleware" is a function that is always executed for each request, and have code before and after the request.

This middleware (just a function) will create a new SQLAlchemy `SessionLocal` for each request, add it to the request and then close it once the request is finished.

```Python hl_lines="68 69 70 71 72 73 74 75 76"
{!./src/sql_databases/tutorial001.py!}
```

!!! info
    We put the creation of the `SessionLocal()` and handling of the requests in a `try` block.

    And then we close it in the `finally` block.
    
    This way we make sure the database session is always closed after the request. Even if there was an exception in the middle.

### About `request.state`

<a href="https://www.starlette.io/requests/#other-state" target="_blank">`request.state` is a property of each Starlette `Request` object</a>, it is there to store arbitrary objects attached to the request itself, like the database session in this case.

For us in this case, it helps us ensuring a single session/database-connection is used through all the request, and then closed afterwards (in the middleware).

## Create a dependency

To simplify the code, reduce repetition and get better editor support, we will create a dependency that returns this same database session from the request.

And when using the dependency in a path operation function, we declare it with the type `Session` we imported directly from SQLAlchemy.

This will then give us better editor support inside the path operation function, because the editor will know that the `db` parameter is of type `Session`.

```Python hl_lines="54 55 69"
{!./src/sql_databases/tutorial001.py!}
```

!!! info "Technical Details"
    The parameter `db` is actually of type `SessionLocal`, but this class (created with `sessionmaker()`) is a "proxy" of a SQLAlchemy `Session`, so, the editor doesn't really know what methods are provided.
    
    But by declaring the type as `Session`, the editor now can know the available methods (`.add()`, `.query()`, `.commit()`, etc) and can provide better support (like completion). The type declaration doesn't affect the actual object.

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

```Python hl_lines="35 37 39 40 41 42 43 45"
{!./src/sql_databases/tutorial001.py!}
```

!!! info
    Notice that we close the session with `db_session.close()`.

    We close this session because we only used it to create this first user.

    Every new request will get its own new session.

### Note

Normally you would probably initialize your database (create tables, etc) with <a href="https://alembic.sqlalchemy.org/en/latest/" target="_blank">Alembic</a>.

And you would also use Alembic for migrations (that's its main job). For whenever you change the structure of your database, add a new column, a new table, etc.

The same way, you would probably make sure there's a first user in an external script that runs before your application, or as part of the application startup.

In this example we are doing those two operations in a very simple way, directly in the code, to focus on the main points.

Also, as all the functionality is self-contained in the same code, you can copy it and run it directly, and it will work as is.


## Get a user

By creating a function that is only dedicated to getting your user from a `user_id` (or any other parameter) independent of your path operation function, you can more easily re-use it in multiple parts and also add <abbr title="Automated tests, written in code, that check if another piece of code is working correctly.">unit tests</abbr> for it:

```Python hl_lines="49 50"
{!./src/sql_databases/tutorial001.py!}
```

## Create your **FastAPI** code

Now, finally, here's the standard **FastAPI** code.

Create your app and path operation function:

```Python hl_lines="59 62 63 64 65"
{!./src/sql_databases/tutorial001.py!}
```

We are creating the database session before each request, attaching it to the request, and then closing it afterwards.

All of this is done in the middleware explained above.

Then, in the dependency `get_db()` we are extracting the database session from the request.

And then we can create the dependency in the path operation function, to get that session directly.

With that, we can just call `get_user` directly from inside of the path operation function and use that session.

Having this 3-step process (middleware, dependency, path operation) in this simple example might seem like an overkill. But imagine if you had 20 or 100 path operations, doing this, you would be reducing a lot of code repetition, and getting better support/checks/completion in all those path operation functions.

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

```Python hl_lines="63"
{!./src/sql_databases/tutorial001.py!}
```

!!! note "Very Technical Details"
    If you are curious and have a deep technical knowledge, you can check <a href="https://fastapi.tiangolo.com/async/#very-technical-details" target="_blank">the very technical details of how this `async def` vs `def` is handled</a>.

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
uvicorn main:app --reload
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

## Interact with the database directly

If you want to explore the SQLite database (file) directly, independently of FastAPI, to debug its contents, add tables, columns, records, modify data, etc. you can use <a href="https://sqlitebrowser.org/" target="_blank">DB Browser for SQLite</a>.

It will look like this:

<img src="/img/tutorial/sql-databases/image02.png">

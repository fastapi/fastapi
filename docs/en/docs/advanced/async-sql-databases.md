# Async SQL (Relational) Databases

You can also use <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases`</a> with **FastAPI** to connect to databases using `async` and `await`.

It is compatible with:

* PostgreSQL
* MySQL
* SQLite

In this example, we'll use **SQLite**, because it uses a single file and Python has integrated support. So, you can copy this example and run it as is.

Later, for your production application, you might want to use a database server like **PostgreSQL**.

!!! tip
    You could adopt ideas from the section about SQLAlchemy ORM ([SQL (Relational) Databases](../tutorial/sql-databases.md){.internal-link target=_blank}), like using utility functions to perform operations in the database, independent of your **FastAPI** code.

    This section doesn't apply those ideas, to be equivalent to the counterpart in <a href="https://www.starlette.io/database/" class="external-link" target="_blank">Starlette</a>.

## Create a configuration for our database

We start by creating [Pydantic Settings](../../advanced/settings.md#pydantic-settings){.internal-link target=_blank} for our app:

```Python hl_lines="6  9-10  13-14"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip
    You'll see that in our demo and tests we use **SQLite**, because it uses a single file and Python has integrated support.
    For your production application, you might want to use a database server like **PostgreSQL**.

!!! tip
    Since we are loading our config using dependency injection, we can use [Dependency overrides](testing-dependencies.md){.internal-link target=_blank} in our tests to set the database URL, without touching enviroment variables!

## Import and set up `SQLAlchemy`

* Import `SQLAlchemy`.
* Create a `metadata` object.
* Create a table `notes` using the `metadata` object.

```Python hl_lines="4  17  19-25"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## Create the tables

In this case, we are creating the tables in the same Python file, but in production, you would probably want to create them with Alembic, integrated with migrations, etc.

Here, this section will run directly, right before starting your **FastAPI** application.

* Create a **FastAPI** dependency that depends on our app's settings.
* Create an `engine`.
* Create all the tables from the `metadata` object.

```Python hl_lines="28 29-31 32"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! tip
    Notice that all this code is pure SQLAlchemy Core.

    `databases` is not doing anything here yet.

## Import and set up `databases`

* Import `databases`.
* Create a `database` dependency called `get_db` that depends on our `setup_schema` dependency.

```Python hl_lines="3  35-39"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## Create models

Create Pydantic models for:

* Notes to be created (`NoteIn`).
* Notes to be returned (`Note`).

```Python hl_lines="42-44  47-50"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

By creating these Pydantic models, the input data will be validated, serialized (converted), and annotated (documented).

So, you will be able to see it all in the interactive API docs.

## Create a startup handler

* Create a startup event handler that connects to the database, applies the migrations and checks the connection.
* Create your `FastAPI` application and bind the startup event handler.

```Python hl_lines="53-54  57"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

## Read notes

Create the *path operation function* to read notes:

```Python hl_lines="60-63"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note
    Notice that as we communicate with the database using `await`, the *path operation function* is declared with `async`.

### Notice the `response_model=List[Note]`

It uses `typing.List`.

That documents (and validates, serializes, filters) the output data, as a `list` of `Note`s.

## Create notes

Create the *path operation function* to create notes:

```Python hl_lines="66-70"
{!../../../docs_src/async_sql_databases/tutorial001.py!}
```

!!! Note
    Notice that as we communicate with the database using `await`, the *path operation function* is declared with `async`.

### About `{**note.dict(), "id": last_record_id}`

`note` is a Pydantic `Note` object.

`note.dict()` returns a `dict` with its data, something like:

```Python
{
    "text": "Some note",
    "completed": False,
}
```

but it doesn't have the `id` field.

So we create a new `dict`, that contains the key-value pairs from `note.dict()` with:

```Python
{**note.dict()}
```

`**note.dict()` "unpacks" the key value pairs directly, so, `{**note.dict()}` would be, more or less, a copy of `note.dict()`.

And then, we extend that copy `dict`, adding another key-value pair: `"id": last_record_id`:

```Python
{**note.dict(), "id": last_record_id}
```

So, the final result returned would be something like:

```Python
{
    "id": 1,
    "text": "Some note",
    "completed": False,
}
```

## Check it

To run this code, set an enviroment variable named `DB_URL` to point to your database.
If you are running PostgreSQL locally, you might do: `export DB_URL=postgresql://user:password@postgresserver/db`.
To test with SQLite, you can set `export DB_URL=sqlite:///./test.db`.

For more information on enviroment variables, see [Environment Variables](settings.md#environment-variables){.internal-link target=_blank}.

Then you can copy this code as is, run it using Uvicorn and see the docs at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

There you can see all your API documented and interact with it:

<img src="/img/tutorial/async-sql-databases/image01.png">

## Testing

To test this app, we'll first import the app and it's dependencies into a test file:

```Python hl_lines="6"
{!../../../docs_src/async_sql_databases/test_tutorial_001.py!}
```

Then create a dependency override for our config that points to a local SQLite database:

```Python hl_lines="2 9-10"
{!../../../docs_src/async_sql_databases/test_tutorial_001.py!}
```

!!! tip
    We create a new database for every test run by using `uuid4()` instead of a fixed name for our test database.
    This saves us from worrying about side effects between tests.

Finally, in our tests we use `app.dependency_overrides` to inject our test config:

```Python hl_lines="1 14"
{!../../../docs_src/async_sql_databases/test_tutorial_001.py!}
```

!!! tip
    We use `unittest.mock.patch` to *patch* the dictionary instead of assigning to it directly.
    This saves us the trouble of having to clean up our dependency override, even if our test fails, which otherwise might have created a confusing cascade of failing tests.

## More info

You can read more about <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases` at its GitHub page</a>.

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

## Import and set up `SQLAlchemy`

* Import `SQLAlchemy`.
* Create a `metadata` object.
* Create a table `notes` using the `metadata` object.

```Python hl_lines="4 14 16 17 18 19 20 21 22"
{!./src/async_sql_databases/tutorial001.py!}
```

!!! tip
    Notice that all this code is pure SQLAlchemy Core.

    `databases` is not doing anything here yet.

## Import and set up `databases`

* Import `databases`.
* Create a `DATABASE_URL`.
* Create a `database` object.

```Python hl_lines="3 9 12"
{!./src/async_sql_databases/tutorial001.py!}
```

!!! tip
    If you were connecting to a different database (e.g. PostgreSQL), you would need to change the `DATABASE_URL`.

## Create the tables

In this case, we are creating the tables in the same Python file, but in production, you would probably want to create them with Alembic, integrated with migrations, etc.

Here, this section would run directly, right before starting your **FastAPI** application.

* Create an `engine`.
* Create all the tables from the `metadata` object.

```Python hl_lines="25 26 27 28"
{!./src/async_sql_databases/tutorial001.py!}
```

## Create models

Create Pydantic models for:

* Notes to be created (`NoteIn`).
* Notes to be returned (`Note`).

```Python hl_lines="31 32 33 36 37 38 39"
{!./src/async_sql_databases/tutorial001.py!}
```

By creating these Pydantic models, the input data will be validated, serialized (converted), and annotated (documented).

So, you will be able to see it all in the interactive API docs.

## Connect and disconnect

* Create your `FastAPI` application.
* Create event handlers to connect and disconnect from the database.

```Python hl_lines="42 45 46 47 50 51 52"
{!./src/async_sql_databases/tutorial001.py!}
```

## Read notes

Create the *path operation function* to read notes:

```Python hl_lines="55 56 57 58"
{!./src/async_sql_databases/tutorial001.py!}
```

!!! Note
    Notice that as we communicate with the database using `await`, the *path operation function* is declared with `async`.

### Notice the `response_model=List[Note]`

It uses `typing.List`.

That documents (and validates, serializes, filters) the output data, as a `list` of `Note`s.

## Create notes

Create the *path operation function* to create notes:

```Python hl_lines="61 62 63 64 65"
{!./src/async_sql_databases/tutorial001.py!}
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

You can copy this code as is, and see the docs at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

There you can see all your API documented and interact with it:

<img src="/img/tutorial/async-sql-databases/image01.png">

## More info

You can read more about <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases` at its GitHub page</a>.

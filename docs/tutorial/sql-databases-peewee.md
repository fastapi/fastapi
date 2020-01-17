!!! warning
    If you are just starting, the <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">SQLAlchemy tutorial</a> should be enough.

    Feel free to skip this.

If you are starting a project from scratch, you are probably better off with <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">SQLAlchemy ORM</a>, or any other async ORM.

If you already have a code base that uses <a href="http://docs.peewee-orm.com/en/latest/" target="_blank">Peewee ORM</a>, you can check here how to use it with **FastAPI**.

!!! warning "Python 3.7+ required"
    You will need Python 3.7 or above to safely use Peewee with FastAPI.

## Peewee for async

Peewee was not designed for async frameworks, or with them in mind.

Peewee has some heavy assumptions about its defaults and about how it should be used.

If you are developing an application with an older non-async framework, and can work with all its defaults, **it can be a great tool**.

But if you need to change some of the defaults, support more than one predefined database, work with an async framework (like FastAPI), etc, you will need to add quite some complex extra code to override those defaults.

Nevertheless, it's possible to do it, and here you'll see exactly what code you have to add to be able to use Peewee with FastAPI.

!!! note "Technical Details"
    You can read more about Peewee's stand about async in Python <a href="http://docs.peewee-orm.com/en/latest/peewee/database.html#async-with-gevent" target="_blank">in the docs</a>, <a href="https://github.com/coleifer/peewee/issues/263#issuecomment-517347032" target="_blank">an issue</a>, <a href="https://github.com/coleifer/peewee/pull/2072#issuecomment-563215132" target="_blank">a PR</a>.

## The same app

We are going to create the same application as in the <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/" target="_blank">SQLAlchemy tutorial</a>.

Most of the code is actually the same.

So, we are going to focus only on the differences.

## File structure

Let's say you have a directory named `my_super_project` that contains a sub-directory called `sql_app` with a structure like this:

```
.
└── sql_app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    └── schemas.py
```

This is almost the same structure as we had for the SQLAlchemy tutorial.

Now let's see what each file/module does.

## Create the Peewee parts

Let's refer to the file `sql_app/database.py`.

### The standard Peewee code

Let's first check all the normal Peewee code, create a Peewee database:

```Python hl_lines="3  5  22"
{!./src/sql_databases_peewee/sql_app/database.py!}
```

!!! tip
    Have in mind that if you wanted to use a different database, like PostgreSQL, you couldn't just change the string. You would need to use a different Peewee database class.

#### Note

The argument:

```Python
check_same_thread=False
```

is equivalent to the one in the SQLAlchemy tutorial:

```Python
connect_args={"check_same_thread": False}
```

...it is needed only for `SQLite`.

!!! info "Technical Details"

    Exactly the same technical details as in the <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/#note" target="_blank">SQLAlchemy tutorial</a> apply.

### Make Peewee async-compatible `PeeweeConnectionState`

The main issue with Peewee and FastAPI is that Peewee relies heavily on <a href="https://docs.python.org/3/library/threading.html#thread-local-data" target="_blank">Python's `threading.local`</a>, and it doesn't have a direct way to override it or let you handle connections/sessions directly (as is done in the SQLAlchemy tutorial).

And `threading.local` is not compatible with the new async features of modern Python.

!!! note "Technical Details"
    `threading.local` is used to have a "magic" variable that has a different value for each thread.

    This was useful in older frameworks designed to have one single thread per request, no more, no less.

    Using this, each request would have its own database connection/session, which is the actual final goal.

    But FastAPI, using the new async features, could handle more than one request on the same thread. And at the same time, for a single request, it could run multiple things in different threads (in a threadpool), depending on if you use `async def` or normal `def`. This is what gives all the performance improvements to FastAPI.

But Python 3.7 and above provide a more advanced alternative to `threading.local`, that can also be used in the places where `threading.local` would be used, but is compatible with the new async features.

We are going to use that. It's called <a href="https://docs.python.org/3/library/contextvars.html" target="_blank">`contextvars`</a>.

We are going to override the internal parts of Peewee that use `threading.local` and replace them with `contextvars`, with the corresponding updates.

This might seem a bit complex (and it actually is), you don't really need to completely understand how it works to use it.

We will create a `PeeweeConnectionState`:

```Python hl_lines="10 11 12 13 14 15 16 17 18 19"
{!./src/sql_databases_peewee/sql_app/database.py!}
```

This class inherits from a special internal class used by Peewee.

It has all the logic to make Peewee use `contextvars` instead of `threading.local`.

`contextvars` works a bit differently than `threading.local`. But the rest of Peewee's internal code assumes that this class works with `threading.local`.

So, we need to do some extra tricks to make it work as if it was just using `threading.local`. The `__init__`, `__setattr__`, and `__getattr__` implement all the required tricks for this to be used by Peewee without knowing that it is now compatible with FastAPI.

!!! tip
    This will just make Peewee behave correctly when used with FastAPI. Not randomly opening or closing connections that are being used, creating errors, etc.

    But it doesn't give Peewee async super-powers. You should still use normal `def` functions and not `async def`.

### Use the custom `PeeweeConnectionState` class

Now, overwrite the `._state` internal attribute in the Peewee database `db` object using the new `PeeweeConnectionState`:

```Python hl_lines="24"
{!./src/sql_databases_peewee/sql_app/database.py!}
```

!!! tip
    Make sure you overwrite `db._state` *after* creating `db`.

!!! tip
    You would do the same for any other Peewee database, including `PostgresqlDatabase`, `MySQLDatabase`, etc.

## Create the database models

Let's now see the file `sql_app/models.py`.

### Create Peewee models for our data

Now create the Peewee models (classes) for `User` and `Item`.

This is the same you would do if you followed the Peewee tutorial and updated the models to have the same data as in the SQLAlchemy tutorial.

!!! tip
    Peewee also uses the term "**model**" to refer to these classes and instances that interact with the database.

    But Pydantic also uses the term "**model**" to refer to something different, the data validation, conversion, and documentation classes and instances.

Import `db` from `database` (the file `database.py` from above) and use it here.

```Python hl_lines="3  6 7 8 9 10 11 12  15 16 17 18 19 20 21"
{!./src/sql_databases_peewee/sql_app/models.py!}
```

!!! tip
    Peewee creates several magic attributes.

    It will automatically add an `id` attribute as an integer to be the primary key.

    It will chose the name of the tables based on the class names.

    For the `Item`, it will create an attribute `owner_id` with the integer ID of the `User`. But we don't declare it anywhere.

## Create the Pydantic models

Now let's check the file `sql_app/schemas.py`.

!!! tip
    To avoid confusion between the Peewee *models* and the Pydantic *models*, we will have the file `models.py` with the Peewee models, and the file `schemas.py` with the Pydantic models.

    These Pydantic models define more or less a "schema" (a valid data shape).
    
    So this will help us avoiding confusion while using both.

### Create the Pydantic *models* / schemas

Create all the same Pydantic models as in the SQLAlchemy tutorial:

```Python hl_lines="16 17 18  21 22  25 26 27 28 29 30  34 35  38 39  42 43 44 45 46 47 48"
{!./src/sql_databases_peewee/sql_app/schemas.py!}
```

!!! tip
    Here we are creating the models with an `id`.

    We didn't explicitly specify an `id` attribute in the Peewee models, but Peewee adds one automatically.

    We are also adding the magic `owner_id` attribute to `Item`.

### Create a `PeeweeGetterDict` for the Pydantic *models* / schemas

When you access a relationship in a Peewee object, like in `some_user.items`, Peewee doesn't provide a `list` of `Item`.

It provides a special custom object of class `ModelSelect`.

It's possible to create a `list` of its items with `list(some_user.items)`.

But the object itself is not a `list`. And it's also not an actual Python <a href="https://docs.python.org/3/glossary.html#term-generator" target="_blank">generator</a>. Because of this, Pydantic doesn't know by default how to convert it to a `list` of Pydantic *models* / schemas.

But recent versions of Pydantic allow providing a custom class that inherits from `pydantic.utils.GetterDict`, to provide the functionality used when using the `orm_mode = True` to retrieve the values for ORM model attributes.

We are going to create a custom `PeeweeGetterDict` class and use it in all the same Pydantic *models* / schemas that use `orm_mode`:

```Python hl_lines="3 8 9 10 11 12 13  31  49"
{!./src/sql_databases_peewee/sql_app/schemas.py!}
```

Here we are checking if the attribute that is being accessed (e.g. `.items` in `some_user.items`) is an instance of `peewee.ModelSelect`.

And if that's the case, just return a `list` with it.

And then we use it in the Pydantic *models* / schemas that use `orm_mode = True`, with the configuration variable `getter_dict = PeeweeGetterDict`.

!!! tip
    We only need to create one `PeeweeGetterDict` class, and we can use it in all the Pydantic *models* / schemas.

## CRUD utils

Now let's see the file `sql_app/crud.py`.

### Create all the CRUD utils

Create all the same CRUD utils as in the SQLAlchemy tutorial, all the code is very similar:

```Python hl_lines="1  4 5  8 9  12 13  16 17 18 19 20  23 24  27 28 29 30"
{!./src/sql_databases_peewee/sql_app/crud.py!}
```

There are some differences with the code for the SQLAlchemy tutorial.

We don't pass a `db` attribute around. Instead we use the models directly. This is because the `db` object is a global object, that includes all the connection logic. That's why we had to do all the `contextvars` updates above.

Aso, when returning several objects, like in `get_users`, we directly call `list`, like in:

```Python
list(models.User.select())
```

This is for the same reason that we had to create a custom `PeeweeGetterDict`. But by returning something that is already a `list` instead of the `peewee.ModelSelect` the `response_model` in the path operation with `List[models.User]` (that we'll see later) will work correctly.

## Main **FastAPI** app

And now in the file `sql_app/main.py` let's integrate and use all the other parts we created before.

### Create the database tables

In a very simplistic way create the database tables:

```Python hl_lines="10 11 12"
{!./src/sql_databases_peewee/sql_app/main.py!}
```

### Create a dependency

Create a dependency that will connect the database right at the beginning of a request and disconnect it at the end:

```Python hl_lines="19 20 21 22 23 24 25"
{!./src/sql_databases_peewee/sql_app/main.py!}
```

Here we have an empty `yield` because we are actually not using the database object directly.

It is connecting to the database and storing the connection data in an internal variable that is independent for each request (using the `contextvars` tricks from above).

And then, in each *path operation function* that needs to access the database we add it as a dependency.

But we are not using the value given by this dependency (it actually doesn't give any value, as it has an empty `yield`). So, we don't add it to the *path operation function* but to the *path operation decorator* in the `dependencies` parameter:

```Python hl_lines="36  44  51  63  69  76"
{!./src/sql_databases_peewee/sql_app/main.py!}
```

### Context Variable Middleware

For all the `contextvars` parts to work, we need to make sure there's a new "context" each time there's a new request, so that we have a specific context variable Peewee can use to save its state (database connection, transactions, etc).

For that, we need to create a middleware.

Right before the request, we are going to reset the database state. We will "set" a value to the context variable and then we will ask the Peewee database state to "reset" (this will create the default values it uses).

And then the rest of the request is processed with that new context variable we just set, all automatically and more or less "magically".

For the **next request**, as we will reset that context variable again in the middleware, that new request will have its own database state (connection, transactions, etc).

```Python hl_lines="28 29 30 31 32 33"
{!./src/sql_databases_peewee/sql_app/main.py!}
```

!!! tip
    As FastAPI is an async framework, one request could start being processed, and before finishing, another request could be received and start processing as well, and it all could be processed in the same thread.

    But context variables are aware of these async features, so, a Peewee database state set in the middleware will keep its own data throughout the entire request.

    And at the same time, the other concurrent request will have its own database state that will be independent for the whole request.

#### Peewee Proxy


If you are using a [Peewee Proxy](http://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database){.external-link target=_blank}, the actual database is at `db.obj`.

So, you would reset it with:

```Python hl_lines="3 4"
@app.middleware("http")
async def reset_db_middleware(request: Request, call_next):
    database.db.obj._state._state.set(db_state_default.copy())
    database.db.obj._state.reset()
    response = await call_next(request)
    return response
```

### Create your **FastAPI** *path operations*

Now, finally, here's the standard **FastAPI** *path operations* code.

```Python hl_lines="36 37 38 39 40 41  44 45 46 47  50 51 52 53 54 55 56 57  60 61 62 63 64 65 66  69 70 71 72  75 76 77 78 79 80 81 82 83"
{!./src/sql_databases_peewee/sql_app/main.py!}
```

### About `def` vs `async def`

The same as with SQLAlchemy, we are not doing something like:

```Python
user = await models.User.select().first()
```

...but instead we are using:

```Python
user = models.User.select().first()
```

So, again, we should declare the *path operation functions* and the dependency without `async def`, just with a normal `def`, as:

```Python hl_lines="2"
# Something goes here
def read_users(skip: int = 0, limit: int = 100):
    # Something goes here
```

## Testing Peewee with async

This example includes an extra *path operation* that simulates a long processing request with `time.sleep(sleep_time)`.

It will have the database connection open at the beginning and will just wait some seconds before replying back. And each new request will wait one second less.

This will easily let you test that your app with Peewee and FastAPI is behaving correctly with all the stuff about threads.

If you want to check how Peewee would break your app if used without modification, go the the `sql_app/database.py` file and comment the line:

```Python
# db._state = PeeweeConnectionState()
```

And in the file `sql_app/main.py` file, comment the middleware:

```Python
# @app.middleware("http")
# async def reset_db_middleware(request: Request, call_next):
#     database.db._state._state.set(db_state_default.copy())
#     database.db._state.reset()
#     response = await call_next(request)
#     return response
```

Then run your app with Uvicorn:

```bash
uvicorn sql_app.main:app --reload
```

Open your browser at <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>  and create a couple of users.

Then open 10 tabs at <a href="http://127.0.0.1:8000/docs#/default/read_slow_users_slowusers__get" target="_blank">http://127.0.0.1:8000/docs#/default/read_slow_users_slowusers__get</a> at the same time.

Go to the *path operation* "Get `/slowusers/`" in all of the tabs. Use the "Try it out" button and execute the request in each tab, one right after the other.

The tabs will wait for a bit and then some of them will show `Internal Server Error`.

### What happens

The first tab will make your app create a connection to the database and wait for some seconds before replying back and closing the connection.

Then, for the request in the next tab, your app will wait for one second less, and so on.

This means that it will end up finishing some of the last tabs' requests than some of the previous ones.

Then one the last requests that wait less seconds will try to open a database connection, but as one of those previous requests for the other tabs will probably be handled in the same thread as the first one, it will have the same database connection that is already open, and Peewee will throw an error and you will see it in the terminal, and the response will have an `Internal Server Error`.

This will probably happen for more than one of those tabs.

If you had multiple clients talking to your app exactly at the same time, this is what could happen.

And as your app starts to handle more and more clients at the same time, the waiting time in a single request needs to be shorter and shorter to trigger the error.

### Fix Peewee with FastAPI

Now go back to the file `sql_app/database.py`, and uncomment the line:

```Python
db._state = PeeweeConnectionState()
```

And in the file `sql_app/main.py` file, uncomment the middleware:

```Python
@app.middleware("http")
async def reset_db_middleware(request: Request, call_next):
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()
    response = await call_next(request)
    return response
```

Terminate your running app and start it again.

Repeat the same process with the 10 tabs. This time all of them will wait and you will get all the results without errors.

...You fixed it!

## Review all the files

 Remember you should have a directory named `my_super_project` (or however you want) that contains a sub-directory called `sql_app`.

`sql_app` should have the following files:

* `sql_app/__init__.py`: is an empty file.

* `sql_app/database.py`:

```Python hl_lines=""
{!./src/sql_databases_peewee/sql_app/database.py!}
```

* `sql_app/models.py`:

```Python hl_lines=""
{!./src/sql_databases_peewee/sql_app/models.py!}
```

* `sql_app/schemas.py`:

```Python hl_lines=""
{!./src/sql_databases_peewee/sql_app/schemas.py!}
```

* `sql_app/crud.py`:

```Python hl_lines=""
{!./src/sql_databases_peewee/sql_app/crud.py!}
```

* `sql_app/main.py`:

```Python hl_lines=""
{!./src/sql_databases_peewee/sql_app/main.py!}
```

## Technical Details

!!! warning
    These are very technical details that you probably don't need.

### The problem

Peewee uses [`threading.local`](https://docs.python.org/3/library/threading.html#thread-local-data){.external-link target=_blank} by default to store it's database "state" data (connection, transactions, etc).

`threading.local` creates a value exclusive to the current thread, but an async framework would run all the "tasks" (e.g. requests) in the same thread, and possibly not in order.

On top of that, an async framework could run some sync code in a threadpool (using `asyncio.run_in_executor`), but belonging to the same "task" (e.g. to the same request).

This means that, with Peewee's current implementation, multiple tasks could be using the same `threading.local` variable and end up sharing the same connection and data, and at the same time, if they execute sync IO-blocking code in a threadpool (as with normal `def` functions in FastAPI, in *path operations*  and dependencies), that code won't have access to the database state variables, even while it's part of the same "task" (request) and it should be able to get access to that.

### Context variables

Python 3.7 has [`contextvars`](https://docs.python.org/3/library/contextvars.html){.external-link target=_blank} that can create a local variable very similar to `threading.local`, but also supporting these async features.

There are several things to have in mind.

The `ContextVar` has to be created at the top of the module, like `some_var = ContextVar("some_var", default="default value")`.

To set a value used in the current "context" (e.g. for the current request) use `some_var.set("new value")`.

To get a value anywhere inside of the context (e.g. in any part handling the current request) use `some_var.get()`.

### Set context variables in middleware

If some part of the async code sets the value with `some_var.set("updated in function")` (e.g. the middleware), the rest of the code in it will see that new value.

And if it calls any other function with `await some_function()` (e.g. `response = await call_next(request)` in our middleware) that internal `some_function()` (or `response = await call_next(request)` in our example) and everything it calls inside, will see that same new value `"updated in function"`.

So, in our case, if we set the Peewee state variable in the middleware and then call `response = await call_next(request)` all the rest of the internal code in our app (that is called by `call_next()`) will see this value we set in the middleware and will be able to reuse it.

But if the value is set in an internal function (e.g. in `get_db()`) that value will be seen only by that internal function and any code it calls, not by the parent function nor by any sibling function. So, we can't set the Peewee database state in `get_db()`, or the *path operation functions* wouldn't see the new Peewee database state for that "context".

### But `get_db` is an async context manager

You might be thinking that `get_db()` is actually not used as a function, it's converted to a context manager.

So the *path operation function* is part of it.

But the code after the `yield`, in the `finally` is not executed in the same "context".

So, if you reset the state in `get_db()`, the *path operation function* would see the database connection set there. But the `finally` block would not see the same context variable value, and so, as the database object would not have the same context variable for its state, it would not have the same connection, so you couldn't close it in the `finally` in `get_db()` after the request is done.

In the middleware we are setting the Peewee state to a context variable that holds a `dict`. So, it's set for every new request.

And as the database state variables are stored inside of that `dict` instead of new context variables, when Peewee sets the new database state (connection, transactions, etc) in any part of the internal code, underneath, all that will be set as keys in that `dict`. But the `dict` would still be the same we set in the middleware. That's what allows the `get_db()` dependency to make Peewee create a new connection (that is stored in that `dict`) and allows the `finally` block to still have access to the same connection.

Because the context variable is set outside all that, in the middleware.

### Connect and disconnect in dependency

Then the next question would be, why not just connect and disconnect the database in the middleware itself, instead of `get_db()`?

First, the middleware has to be `async`, and creating and closing the database connection is potentially blocking, so it could degrade performance.

But more importantly, the middleware returns a `response`, and this `response` is actually an awaitable function that will do all the work in your code, including background tasks.

If you closed the connection in the middleware right before returning the `response`, some of your code would not have the chance to use the database connection set in the context variable.

Because some other code will call that `response` with `await response(...)`. And inside of that `await response(...)` is that, for example, background tasks are run. But if the connection was already closed before `response` is awaited, then it won't be able to access it.

If you are building an application or a web API, it's rarely the case that you can put everything on a single file.

**FastAPI** provides a convenience tool to structure your application while keeping all the flexibility.


## An example file structure

Let's say you have a file structure like this:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── routers
│       ├── __init__.py
│       ├── items.py
│       └── users.py
```

!!! tip
    There are two `__init__.py` files: one in each directory or subdirectory.
    
    This is what allows importing code from one file into another.

    For example, in `app/main.py` you could have a line like:
    
    ```
    from app.routers import items
    ```


* The `app` directory contains everything.
* This `app` directory has an empty file `app/__init__.py`.
    * So, the `app` directory is a "Python package" (a collection of "Python modules").
* The `app` directory also has a `app/main.py` file.
    * As it is inside a Python package directory (because there's a file `__init__.py`), it is a "module" of that package: `app.main`.
* There's a subdirectory `app/routers/`.
* The subdirectory `app/routers` also has an empty file `__init__.py`.
    * So, it is a "Python subpackage".
* The file `app/routers/items.py` is beside the `app/routers/__init__.py`.
    * So, it's a submodule: `app.routers.items`.
* The file `app/routers/users.py` is beside the `app/routers/__init__.py`.
    * So, it's a submodule: `app.routers.users`.


## `APIRouter`

Let's say the file dedicated to handling just users is the submodule at `/app/routers/users.py`.

You want to have the *path operations* related to your users separated from the rest of the code, to keep it organized.

But it's still part of the same **FastAPI** application/web API (it's part of the same "Python Package").

You can create the *path operations* for that module using `APIRouter`.


### Import `APIRouter`

You import it and create an "instance" the same way you would with the class `FastAPI`:

```Python hl_lines="1 3"
{!./src/bigger_applications/app/routers/users.py!}
```


### Path operations with `APIRouter`

And then you use it to declare your *path operations*.

Use it the same way you would use the `FastAPI` class:

```Python hl_lines="6 11 16"
{!./src/bigger_applications/app/routers/users.py!}
```

You can think of `APIRouter` as a "mini `FastAPI`" class.

All the same options are supported.

All the same parameters, responses, dependencies, tags, etc.

!!! tip
    In this example, the variable is called `router`, but you can name it however you want.

We are going to include this `APIrouter` in the main `FastAPI` app, but first, let's add another `APIRouter`.


## Another module with `APIRouter`

Let's say you also have the endpoints dedicated to handling "Items" from your application in the module at `app/routers/items.py`.

You have path operations for:

* `/items/`
* `/items/{item_id}`

It's all the same structure as with `app/routers/users.py`.

But let's say that this time we are more lazy.

And we don't want to have to explicitly type `/items/` in every path operation, we can do it later:

```Python hl_lines="6 11 16"
{!./src/bigger_applications/app/routers/items.py!}
```


## The main `FastAPI`

Now, let's see the module at `app/main.py`.

Here's where you import and use the class `FastAPI`.

This will be the main file in your application that ties everything together.

### Import `FastAPI`

You import and create a `FastAPI` class as normally:

```Python hl_lines="1 6"
{!./src/bigger_applications/app/main.py!}
```

### Import the `APIRouter`

But this time we are not adding path operations directly with the `FastAPI` `app`.

We import the `APIRouter`s from the other files:

```Python hl_lines="3 4"
{!./src/bigger_applications/app/main.py!}
```

As the file `app/routers/items.py` is part of the same Python package, we can import it using "dot notation".


### How the importing works

The section:

```Python
from .routers.items import router
```

Means:

* Starting in the same package that this module (the file `app/main.py`) lives in (the directory `app/`)...
* look for the subpackage `routers` (the directory at `app/routers/`)...
* and from it, the submodule `items` (the file at `app/routers/items.py`)...
* and from that submodule, import the variable `router`.

The variable `router` is the same one we created in the file `app/routers/items.py`. It's an `APIRouter`.

We could also import it like:

```Python
from app.routers.items import router
```

!!! info
    The first version is a "relative import".

    The second version is an "absolute import".

    To learn more about Python Packages and Modules, read <a href="https://docs.python.org/3/tutorial/modules.html" target="_blank">the official Python documentation about Modules</a>.


### Avoid name collisions

We are importing a variable named `router` from the submodule `items`.

But we also have another variable named `router` in the submodule `users`.

If we import one after the other, like:

```Python
from .routers.items import router
from .routers.users import router
```

The `router` from `users` will overwrite the one form `items` and we won't be able to use them at the same time.

So, to be able to use both of them in the same file, we rename them while importing them using `as`:

```Python hl_lines="3 4"
{!./src/bigger_applications/app/main.py!}
```


### Include an `APIRouter`

Now, let's include the router from the submodule `users`, now in the variable `users_router`:

```Python hl_lines="8"
{!./src/bigger_applications/app/main.py!}
```

With `app.include_router()` we can add an `APIRouter` to the main `FastAPI` application.

It will include all the routes from that router as part of it.

!!! note "Technical Details"
    It will actually internally create a path operation for each path operation that was declared in the `APIRouter`.

    So, behind the scenes, it will actually work as if everything was the same single app.


!!! check
    You don't have to worry about performance when including routers.
    
    This will take microseconds and will only happen at startup.
    
    So it won't affect performance.


### Include an `APIRouter` with a prefix

Now, let's include the router form the `items` submodule, now in the variable `items_router`.

But, remember that we were lazy and didn't add `/items/` to all the path operations?

We can add a prefix to all the path operations using the parameter `prefix` of `app.include_router()`.

As the path of each path operation has to start with `/`, like in:

```Python hl_lines="1"
@router.get("/{item_id}", tags=["items"])
async def read_item(item_id: str):
    ...
```

...the prefix must not include a final `/`.

So, the prefix in this case would be `/items`:

```Python hl_lines="9"
{!./src/bigger_applications/app/main.py!}
```

The end result is that the item paths are now:

* `/items/`
* `/items/{item_id}`

...as we intended.

!!! check
    The `prefix` parameter is (as in many other cases) just a feature from **FastAPI** to help you avoid code duplication.


!!! tip
    You could also add path operations directly, for example with: `@app.get(...)`.
    
    Apart from `app.include_router()`, in the same **FastAPI** app.
    
    It would still work the same.


!!! info "Very Technical Details"
    **Note**: this is a very technical detail that you probably can **just skip**.

    ---

    The `APIRouter`s are not "mounted", they are not isolated from the rest of the application.

    This is because we want to include their path operations in the OpenAPI schema and the user interfaces.

    As we cannot just isolate them and "mount" them independently of the rest, the path operations are "cloned" (re-created), not included directly.


## Check the automatic API docs

Now, run `uvicorn`, using the module `app.main` and the variable `app`:

```bash
uvicorn app.main:app --reload
```

And open the docs at <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic API docs, including the paths from all the submodules:

<img src="/img/tutorial/bigger-applications/image01.png">

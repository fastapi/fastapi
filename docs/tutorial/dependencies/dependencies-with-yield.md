# Dependencies with `yield`

FastAPI supports dependencies that do some <abbr title='sometimes also called "exit", "cleanup", "teardown", "close", "context managers", ...'>extra steps after finishing</abbr>.

To do this, use `yield` instead of `return`, and write the extra steps after.

!!! tip
    Make sure to use `yield` one single time.

!!! info
    For this to work, you need to use **Python 3.7** or above, or in **Python 3.6**, install the "backports":

    ```bash
    pip install async-exit-stack async-generator
    ```

    This installs <a href="https://github.com/sorcio/async_exit_stack" target="_blank">async-exit-stack</a> and <a href="https://github.com/python-trio/async_generator" target="_blank">async-generator</a>.

!!! note "Technical Details"
    Any function that is valid to use with:

    * <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" target="_blank">`@contextlib.contextmanager`</a> or 
    * <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" target="_blank">`@contextlib.asynccontextmanager`</a>

    would be valid to use as a **FastAPI** dependency.

    In fact, FastAPI uses those two decorators internally.

## A database dependency with `yield`

For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the `yield` statement is executed before sending a response:

```Python hl_lines="2 3 4"
{!./src/dependencies/tutorial007.py!}
```

The yielded value is what is injected into *path operations* and other dependencies:

```Python hl_lines="4"
{!./src/dependencies/tutorial007.py!}
```

The code following the `yield` statement is executed after the response has been delivered:

```Python hl_lines="5 6"
{!./src/dependencies/tutorial007.py!}
```

!!! tip
    You can use `async` or normal functions.

    **FastAPI** will do the right thing with each, the same as with normal dependencies.

## A dependency with `yield` and `try`

If you use a `try` block in a dependency with `yield`, you'll receive any exception that was thrown when using the dependency.

For example, if some code at some point in the middle, in another dependency or in a *path operation*, made a database transaction "rollback" or create any other error, you will receive the exception in your dependency.

So, you can look for that specific exception inside the dependency with `except SomeException`.

In the same way, you can use `finally` to make sure the exit steps are executed, no matter if there was an exception or not.

```Python hl_lines="3 5"
{!./src/dependencies/tutorial007.py!}
```

## Sub-dependencies with `yield`

You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use `yield`.

**FastAPI** will make sure that the "exit code" in each dependency with `yield` is run in the correct order.

For example, `dependency_c` can have a dependency on `dependency_b`, and `dependency_b` on `dependency_a`:

```Python hl_lines="4 12 20"
{!./src/dependencies/tutorial008.py!}
```

And all of them can use `yield`.

In this case `dependency_c`, to execute its exit code, needs the value from `dependency_b` (here named `dep_b`) to still be available.

And, in turn, `dependency_b` needs the value from `dependency_a` (here named `dep_a`) to be available for its exit code.

```Python hl_lines="16 17 24 25"
{!./src/dependencies/tutorial008.py!}
```

The same way, you could have dependencies with `yield` and `return` mixed.

And you could have a single dependency that requires several other dependencies with `yield`, etc.

You can have any combinations of dependencies that you want.

**FastAPI** will make sure everything is run in the correct order.

!!! note "Technical Details"
    This works thanks to Python's <a href="https://docs.python.org/3/library/contextlib.html" target="_blank">Context Managers</a>.

    **FastAPI** uses them internally to achieve this.

## Context Managers

### What are "Context Managers"

"Context Managers" are any of those Python objects that you can use in a `with` statement.

For example, <a href="https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files" target="_blank">you can use `with` to read a file</a>:

```Python
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
```

Underneath, the `open("./somefile.txt")` returns an object that is a called a "Context Manager".

When the `with` block finishes, it makes sure to close the file, even if there were exceptions.

When you create a dependency with `yield`, **FastAPI** will internally convert it to a context manager, and combine it with some other related tools.

### Using context managers in dependencies with `yield`

!!! warning
    This is, more or less, an "advanced" idea.

    If you are just starting with **FastAPI** you might want to skip it for now.

In Python, you can create context managers by <a href="https://docs.python.org/3/reference/datamodel.html#context-managers" target="_blank">creating a class with two methods: `__enter__()` and `__exit__()`</a>.

You can also use them with **FastAPI** dependencies with `yield` by using
`with` or `async with` statements inside of the dependency function:

```Python hl_lines="1 2 3 4 5 6 7 8 9 13"
{!./src/dependencies/tutorial010.py!}
```

!!! tip
    Another way to create a context manager is with:

    * <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" target="_blank">`@contextlib.contextmanager`</a> or 
    * <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" target="_blank">`@contextlib.asynccontextmanager`</a>

    using them to decorate a function with a single `yield`.

    That's what **FastAPI** uses internally for dependencies with `yield`.

    But you don't have to use the decorators for FastAPI dependencies (and you shouldn't).

    FastAPI will do it for you internally.

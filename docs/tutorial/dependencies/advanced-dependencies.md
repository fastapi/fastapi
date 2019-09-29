!!! danger
    This is, more or less, an "advanced" chapter.
    
    If you are just starting with **FastAPI** you might want to skip this chapter and come back to it later.

## Parameterized dependencies

All the dependencies we have seen are a fixed function or class.

But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.

Let's imagine that we want to have a dependency that checks if the query parameter `q` contains some fixed content.

But we want to be able to parameterize that fixed content.

## A "callable" instance

In Python there's a way to make an instance of a class a "callable".

Not the class itself (which is already a callable), but an instance of that class.

To do that, we declare a method `__call__`:

```Python hl_lines="10"
{!./src/dependencies/tutorial007.py!}
```

In this case, this `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your *path operation function* later.

## Parameterize the instance

And now, we can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency:

```Python hl_lines="7"
{!./src/dependencies/tutorial007.py!}
```

In this case, **FastAPI** won't ever touch or care about `__init__`, we will use it directly in our code.

## Create an instance

We could create an instance of this class with:

```Python hl_lines="16"
{!./src/dependencies/tutorial007.py!}
```

And that way we are able to "parameterize" our dependency, that now has `"bar"` inside of it, as the attribute `checker.fixed_content`.

## Use the instance as a dependency

Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like:

```Python
checker(q="somequery")
```

...and pass whatever that returns as the value of the dependency in our path operation function as the parameter `fixed_content_included`:

```Python hl_lines="20"
{!./src/dependencies/tutorial007.py!}
```

!!! tip
    All this might seem contrived. And it might not be very clear how is it useful yet.

    These examples are intentionally simple, but show how it all works.

    In the chapters about security, you will be using utility functions that are implemented in this same way.

    If you understood all this, you already know how those utility tools for security work underneath.

## Context Manager Dependencies

FastAPI supports dependencies that require both setup and teardown through the use of appropriate generator or
async generator functions.

For example, this would enable you to eliminate the use of middleware while implementing
the `get_db` dependency from the
[SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) section of the tutorial:

```Python hl_lines="4"
{!./src/dependencies/tutorial008.py!}
```

Only the code prior to and including the `yield` statement is executed before sending a response:
```Python hl_lines="5 6 7"
{!./src/dependencies/tutorial008.py!}
```

The yielded value is what is injected into endpoint calls and other dependencies:
```Python hl_lines="7"
{!./src/dependencies/tutorial008.py!}
```

The code following the `yield` statement is executed as a `BackgroundTask` after the response has been delivered:
```Python hl_lines="8 9"
{!./src/dependencies/tutorial008.py!}
```

!!! info
    Any function that is valid for use with the
    [`@contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)
    or [`@contextlib.asynccontextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)
    decorators should be valid for use as a fastapi dependency, and will be handled as described above.

This approach can be made compatible with traditional context managers and async context managers by using
`with` or `async with` statements inside the dependency function: 
```Python hl_lines="16"
{!./src/dependencies/tutorial009.py!}
```

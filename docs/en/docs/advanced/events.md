# Events: startup - shutdown

You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.

These functions can be declared with `async def` or normal `def`.

!!! warning
    Only event handlers for the main application will be executed, not for [Sub Applications - Mounts](./sub-applications.md){.internal-link target=_blank}.

## `startup` event

To add a function that should be run before the application starts, declare it with the event `"startup"`:

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

In this case, the `startup` event handler function will initialize the items "database" (just a `dict`) with some values.

You can add more than one event handler function.

And your application won't start receiving requests until all the `startup` event handlers have completed.

## `shutdown` event

To add a function that should be run when the application is shutting down, declare it with the event `"shutdown"`:

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

Here, the `shutdown` event handler function will write a text line `"Application shutdown"` to a file `log.txt`.

!!! info
    In the `open()` function, the `mode="a"` means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.

!!! tip
    Notice that in this case we are using a standard Python `open()` function that interacts with a file.

    So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.

    But `open()` doesn't use `async` and `await`.

    So, we declare the event handler function with standard `def` instead of `async def`.

!!! info
    You can read more about these event handlers in <a href="https://www.starlette.io/events/" class="external-link" target="_blank">Starlette's  Events' docs</a>.

# Lifespan

You can also define a lifespan context as an asynchronous context manager, instead of using separate startup and shutdown functions.

This `async` function must be declared with the `@asynccontextmanager` decorator.  This was added to `contextlib` in Python 3.7.  For earlier versions of Python,
you can install the `contextlib2` library to get `@asynccontextmanager`.

```Python hl_lines="4"
{!../../../docs_src/events/tutorial003.py!}
```

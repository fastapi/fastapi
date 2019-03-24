
You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.

These functions can be declared with `async def` or normal `def`.

## `startup` event

To add a function that should be run before the application starts, declare it with the event `"startup"`:

```Python hl_lines="8"
{!./src/events/tutorial001.py!}
```

In this case, the `startup` event handler function will initialize the items "database" (just a `dict`) with some values.

You can add more than one event handler function.

And your application won't start receiving requests until all the `startup` event handlers have completed.

## `shutdown` event

To add a function that should be run when the application is shutting down, declare it with the event `"shutdown"`:

```Python hl_lines="6"
{!./src/events/tutorial002.py!}
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
    You can read more about these event handlers in <a href="https://www.starlette.io/events/" target="_blank">Starlette's  Events' docs</a>.
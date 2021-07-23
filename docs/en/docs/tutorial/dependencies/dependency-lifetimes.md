# Dependency Lifetimes

Dependencies in FastAPI are lazily initialized: they are called when they are first needed.

As you saw in [Dependencies with yield](dependencies-with-yield.md){.internal-link target=_blank}, you can use `yield` to give your dependency the ability to execute some teardown after it yields its value.
By default, this teardown happens in the background after the response has been sent (see [Dependencies with `yield` and `HTTPException`](dependencies-with-yield.md#dependencies-with-yield-and-httpexception){.internal-link target=_blank}) for more details on this behaviour).

This section deals with controlling *when* and *how* that teardown is run.

## Available lifetimes

FastAPI offers **3** lifetimes for dependencies:

- `"app"`: the dependencies teardown is run when the app shuts down. This is useful for things like database connections which you want to persist between requests.
- `"request"`: this is the default. Teardown is run *in the background after a response is sent*. You can't raise any HTTPExceptions from your teardown.
- `"endpoint"`: this is similar to `"request"`, except that teardown is run in the foreground *before* [Exception Handlers](../handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} and so you *can* raise an `HTTPException`.

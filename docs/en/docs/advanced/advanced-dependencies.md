# Advanced Dependencies { #advanced-dependencies }

## Parameterized dependencies { #parameterized-dependencies }

All the dependencies we have seen are a fixed function or class.

But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.

Let's imagine that we want to have a dependency that checks if the query parameter `q` contains some fixed content.

But we want to be able to parameterize that fixed content.

## A "callable" instance { #a-callable-instance }

In Python there's a way to make an instance of a class a "callable".

Not the class itself (which is already a callable), but an instance of that class.

To do that, we declare a method `__call__`:

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

In this case, this `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your *path operation function* later.

## Parameterize the instance { #parameterize-the-instance }

And now, we can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency:

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

In this case, **FastAPI** won't ever touch or care about `__init__`, we will use it directly in our code.

## Create an instance { #create-an-instance }

We could create an instance of this class with:

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

And that way we are able to "parameterize" our dependency, that now has `"bar"` inside of it, as the attribute `checker.fixed_content`.

## Use the instance as a dependency { #use-the-instance-as-a-dependency }

Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like:

```Python
checker(q="somequery")
```

...and pass whatever that returns as the value of the dependency in our *path operation function* as the parameter `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip

All this might seem contrived. And it might not be very clear how it is useful yet.

These examples are intentionally simple, but show how it all works.

In the chapters about security, there are utility functions that are implemented in this same way.

If you understood all this, you already know how those utility tools for security work underneath.

///

## Limit dependency concurrency { #limit-dependency-concurrency }

In some cases, you might want to limit how many requests can use a dependency at the same time.

For example, your database might have a limited number of connections available. You could make new requests wait before creating a session, until another request finishes using its session.

You can do this with `max_concurrency` in `Depends()`.

Let's update the `SessionDep` alias from the [SQL databases tutorial](../tutorial/sql-databases.md):

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

Now, up to **five requests** can have a database session open through this dependency at the same time.

If another request needs a session, it waits until one of those sessions is closed.

While waiting, it **doesn't occupy a worker thread**, so those threads are available to run other code.

The value must be a positive integer. The default is `None`, which means that FastAPI doesn't limit how many times the dependency can run at the same time.

### Share the limit between routes { #share-the-limit-between-routes }

All the routes in that example use the same `SessionDep` alias, so they share the limit of five sessions.

To share a limit, reuse the **same `Depends()` object**, for example in an `Annotated` alias like this one.

If you write a new `Depends(get_session, max_concurrency=5)` for each route, each one will have its own limit of five. This is true even though they all use the same `get_session` function.

Reusing the same `SessionDep` in another application also shares the limit, as long as both applications run in the same event loop. This includes mounted applications.

For example, if two applications use this `SessionDep` for the same database pool, together they can have up to five sessions open through this dependency.

If the applications use separate pools and need independent limits, create a separate `Depends()` object for each application.

### Close the session before allowing another one { #close-the-session-before-allowing-another-one }

In this example, `get_session` uses `yield`. The session counts toward the limit until the exit code finishes closing it.

The dependency's `scope` determines when that exit code runs:

* With `scope="request"`, the default, it runs after the response is sent.
* With `scope="function"`, it runs after the *path operation function* finishes, before sending the response.

You can read more about [early exit and scope](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

For a dependency without `yield`, the call counts toward the limit only until the function finishes.

If you use a dependency with `yield` in a WebSocket handler, it counts toward the limit until the handler exits and the dependency's exit code finishes.

/// note

Reusing a [cached dependency value](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times) doesn't count again toward the limit. If different declarations share that value, only the declaration that calls the dependency counts toward its limit.

///

### Choose a limit for your application { #choose-a-limit-for-your-application }

Choose a limit that fits the number of database connections available to these sessions.

If other parts of your application also use those connections, leave room for them too. FastAPI doesn't know the size of your database connection pool.

Each worker process has its own limit. For example, two worker processes with this dependency could have up to ten sessions open between them.

/// note | Technical Details

The limits are also separate for each event loop. Applications running in different event loops don't share a limit, even if they reuse the same `Depends()` object.

///

### Dependencies that need more than one resource { #dependencies-that-need-more-than-one-resource }

FastAPI runs a dependency's sub-dependencies before applying that dependency's limit.

So, to limit database sessions, put `max_concurrency` on `Depends(get_session, ...)`, where the session is created.

A request can get stuck if it needs another session while still holding one that will only be closed at the end of the request.

For example, imagine a shared `Depends(get_session, max_concurrency=1, use_cache=False)` used twice in the same request.

The first call creates a session. The second call waits for it to close. But the first session can't close until the request finishes, and the request is waiting for the second call.

Two requests can also get stuck if one holds a session while waiting for another resource, and the other holds that resource while waiting for a session.

If your requests need several resources, acquire them in the same order. FastAPI applies each limit separately, it doesn't reserve all the resources a request will need in advance.

## Dependencies with `yield`, `HTTPException`, `except` and Background Tasks { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning

You most probably don't need these technical details.

These details are useful mainly if you had a FastAPI application older than 0.121.0 and you are facing issues with dependencies with `yield`.

///

Dependencies with `yield` have evolved over time to account for the different use cases and to fix some issues, here's a summary of what has changed.

### Dependencies with `yield` and `scope` { #dependencies-with-yield-and-scope }

In version 0.121.0, FastAPI added support for `Depends(scope="function")` for dependencies with `yield`.

Using `Depends(scope="function")`, the exit code after `yield` is executed right after the *path operation function* is finished, before the response is sent back to the client.

And when using `Depends(scope="request")` (the default), the exit code after `yield` is executed after the response is sent.

You can read more about it in the docs for [Dependencies with `yield` - Early exit and `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Dependencies with `yield` and `StreamingResponse`, Technical Details { #dependencies-with-yield-and-streamingresponse-technical-details }

Before FastAPI 0.118.0, if you used a dependency with `yield`, it would run the exit code after the *path operation function* returned but right before sending the response.

The intention was to avoid holding resources for longer than necessary, waiting for the response to travel through the network.

This change also meant that if you returned a `StreamingResponse`, the exit code of the dependency with `yield` would have been already run.

For example, if you had a database session in a dependency with `yield`, the `StreamingResponse` would not be able to use that session while streaming data because the session would have already been closed in the exit code after `yield`.

This behavior was reverted in 0.118.0, to make the exit code after `yield` be executed after the response is sent.

/// note

As you will see below, this is very similar to the behavior before version 0.106.0, but with several improvements and bug fixes for corner cases.

///

#### Use Cases with Early Exit Code { #use-cases-with-early-exit-code }

There are some use cases with specific conditions that could benefit from the old behavior of running the exit code of dependencies with `yield` before sending the response.

For example, imagine you have code that uses a database session in a dependency with `yield` only to verify a user, but the database session is never used again in the *path operation function*, only in the dependency, **and** the response takes a long time to be sent, like a `StreamingResponse` that sends data slowly, but for some reason doesn't use the database.

In this case, the database session would be held until the response is finished being sent, but if you don't use it, then it wouldn't be necessary to hold it.

Here's how it could look:

{* ../../docs_src/dependencies/tutorial013.py *}

The exit code, the automatic closing of the `Session` in:

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

...would be run after the response finishes sending the slow data:

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

But as `generate_stream()` doesn't use the database session, it is not really necessary to keep the session open while sending the response.

If you have this specific use case using SQLModel (or SQLAlchemy), you could explicitly close the session after you don't need it anymore:

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

That way the session would release the database connection, so other requests could use it.

If you have a different use case that needs to exit early from a dependency with `yield`, please create a [GitHub Discussion Question](https://github.com/fastapi/fastapi/discussions/new?category=questions) with your specific use case and why you would benefit from having early closing for dependencies with `yield`.

If there are compelling use cases for early closing in dependencies with `yield`, I would consider adding a new way to opt in to early closing.

### Dependencies with `yield` and `except`, Technical Details { #dependencies-with-yield-and-except-technical-details }

Before FastAPI 0.110.0, if you used a dependency with `yield`, and then you captured an exception with `except` in that dependency, and you didn't raise the exception again, the exception would be automatically raised/forwarded to any exception handlers or the internal server error handler.

This was changed in version 0.110.0 to fix unhandled memory consumption from forwarded exceptions without a handler (internal server errors), and to make it consistent with the behavior of regular Python code.

### Background Tasks and Dependencies with `yield`, Technical Details { #background-tasks-and-dependencies-with-yield-technical-details }

Before FastAPI 0.106.0, raising exceptions after `yield` was not possible, the exit code in dependencies with `yield` was executed *after* the response was sent, so [Exception Handlers](../tutorial/handling-errors.md#install-custom-exception-handlers) would have already run.

This was designed this way mainly to allow using the same objects "yielded" by dependencies inside of background tasks, because the exit code would be executed after the background tasks were finished.

This was changed in FastAPI 0.106.0 with the intention to not hold resources while waiting for the response to travel through the network.

/// tip

Additionally, a background task is normally an independent set of logic that should be handled separately, with its own resources (e.g. its own database connection).

So, this way you will probably have cleaner code.

///

If you used to rely on this behavior, now you should create the resources for background tasks inside the background task itself, and use internally only data that doesn't depend on the resources of dependencies with `yield`.

For example, instead of using the same database session, you would create a new database session inside of the background task, and you would obtain the objects from the database using this new session. And then instead of passing the object from the database as a parameter to the background task function, you would pass the ID of that object and then obtain the object again inside the background task function.

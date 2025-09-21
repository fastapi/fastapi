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

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

In this case, this `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your *path operation function* later.

## Parameterize the instance { #parameterize-the-instance }

And now, we can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

In this case, **FastAPI** won't ever touch or care about `__init__`, we will use it directly in our code.

## Create an instance { #create-an-instance }

We could create an instance of this class with:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

And that way we are able to "parameterize" our dependency, that now has `"bar"` inside of it, as the attribute `checker.fixed_content`.

## Use the instance as a dependency { #use-the-instance-as-a-dependency }

Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like:

```Python
checker(q="somequery")
```

...and pass whatever that returns as the value of the dependency in our *path operation function* as the parameter `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip

All this might seem contrived. And it might not be very clear how is it useful yet.

These examples are intentionally simple, but show how it all works.

In the chapters about security, there are utility functions that are implemented in this same way.

If you understood all this, you already know how those utility tools for security work underneath.

///

## Dependencies with `yield`, `HTTPException`, `except` and Background Tasks { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning

You most probably don't need these technical details.

These details are useful mainly if you had a FastAPI application older than 0.118.0 and you are facing issues with dependencies with `yield`.

///

Dependencies with `yield` have evolved over time to account for the different use cases and to fix some issues, here's a summary of what has changed.

### Dependencies with `yield` and `StreamingResponse`, Technical Details { #dependencies-with-yield-and-streamingresponse-technical-details }

Before FastAPI 0.118.0, if you used a dependency with `yield`, it would run the exit code after the *path operation function* returned but right before sending the response.

The intention was not to hold resources for longer than necessary, waiting for the response to travel through the network.

/// tip

Later I realized that SQLAlchemy (and hence SQLModel), one of the main tools I was considering when thinking about not holding resources, would not hold the raw database connections indefinitely, but acquire and release them automatically when necessary. For example, releasing the database connection after a `session.commit()`.

So this optimization was not really necessary.

///

This change also meant that if you returned a `StreamingResponse`, the exit code of the dependency with `yield` would have been already run.

For example, if you had a database session in a dependency with `yield`, the `StreamingResponse` would not be able to use that session while streaming data because the session would have already been closed in the exit code after `yield`.

So, the change was not really optimizing much, but it was breaking use cases.

This behavior was reverted in 0.118.0, to make the exit code after `yield` be executed after the response is sent.

/// info

As you will see below, this is very similar to the behavior before version 0.106.0, but with several improvements and bug fixes for corner cases.

///

### Dependencies with `yield` and `except`, Technical Details { #dependencies-with-yield-and-except-technical-details }

Before FastAPI 0.110.0, if you used a dependency with `yield`, and then you captured an exception with `except` in that dependency, and you didn't raise the exception again, the exception would be automatically raised/forwarded to any exception handlers or the internal server error handler.

This was changed in version 0.110.0 to fix unhandled memory consumption from forwarded exceptions without a handler (internal server errors), and to make it consistent with the behavior of regular Python code.

### Background Tasks and Dependencies with `yield`, Technical Details { #background-tasks-and-dependencies-with-yield-technical-details }

Before FastAPI 0.106.0, raising exceptions after `yield` was not possible, the exit code in dependencies with `yield` was executed *after* the response was sent, so [Exception Handlers](../handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} would have already run.

This was designed this way mainly to allow using the same objects "yielded" by dependencies inside of background tasks, because the exit code would be executed after the background tasks were finished.

This was changed in FastAPI 0.106.0 with the intention to not hold resources while waiting for the response to travel through the network.

/// tip

Additionally, a background task is normally an independent set of logic that should be handled separately, with its own resources (e.g. its own database connection).

So, this way you will probably have cleaner code.

///

If you used to rely on this behavior, now you should create the resources for background tasks inside the background task itself, and use internally only data that doesn't depend on the resources of dependencies with `yield`.

For example, instead of using the same database session, you would create a new database session inside of the background task, and you would obtain the objects from the database using this new session. And then instead of passing the object from the database as a parameter to the background task function, you would pass the ID of that object and then obtain the object again inside the background task function.

Let's see a very simple example of the **Dependency Injection** system.

It will be so simple that it is not very useful, for now.

But this way we can focus on how the **Dependency Injection** system works.

In the next chapters we'll extend it to see how can it be so useful.

## Create a dependency, or "dependable"

Let's first focus on the dependency.

It is just a function that can take all the same parameters that a path operation function can take:

```Python hl_lines="6 7"
{!./tutorial/src/dependencies/tutorial001.py!}
```

That's it.

**2 lines**.

And it has the same shape and structure that all your path operation functions.

You can think of it as a path operation function without the "decorator" (the `@app.get("/some-path")`).

And it can return anything you want.

In this case, this dependency expects:

* An optional query parameter `q` that is a `str`.
* An optional query parameter `skip` that is an `int`, and by default is `0`.
* An optional query parameter `limit` that is an `int`, and by default is `100`.

And then it just returns a `dict` containing those values.

## Import `Depends`

```Python hl_lines="1"
{!./tutorial/src/dependencies/tutorial001.py!}
```

## Declare the dependency, in the "dependant"

The same way you use `Body`, `Query`, etc. with your path operation function parameters, use `Depends` with a new parameter:

```Python hl_lines="11"
{!./tutorial/src/dependencies/tutorial001.py!}
```

Although you use it in the parameters of your function too, `Depends` works a bit differently.

You only give `Depends` a single parameter.

This parameter must be a function with the same parameters that can be taken by a path operation function.

Whenever a new request arrives, **FastAPI** will take care of:

* Calling your dependency ("dependable") function with the correct parameters.
* Get the result from your function.
* Assign that result to the parameter in your path operation function.

!!! note
    Notice that you don't have to create a special class and pass it somewhere to **FastAPI** or anything similar.

    You just pass it to `Depends` and **FastAPI** knows how to do the rest.

## To `async` or not to `async`

As dependencies will also be called by **FastAPI** (the same as your path operation functions), the same rules apply while defining your functions.

You can use `async def` or normal `def`.

And you can declare dependencies with `async def` inside of normal `def` path operation functions, or `def` dependencies inside of `async def` path operation functions.

It doesn't matter. **FastAPI** will know what to do.

!!! note
    If you don't know, check the _"In a hurry?"_ section about <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` and `await` in the docs</a>.

## Integrated wiht OpenAPI

All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be integrated in the same OpenAPI schema.

So, the interactive docs will have all the information they need, while you keep all the flexibility of the dependencies:

<img src="/img/tutorial/dependencies/image01.png">

## Recap

Create Dependencies with **2 lines** of code.
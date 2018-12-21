Before diving deeper into the **Dependency Injection** system, let's upgrade the previous example.

## A `dict` from the previous example

In the previous example, we where returning a `dict` from our dependency ("dependable"):

```Python hl_lines="7"
{!./src/dependencies/tutorial001.py!}
```

But then we get a `dict` in the parameter `commons` of the path operation function.

And we know that `dict`s can't provide a lot of editor support because they can't know their keys and value types.

## Create a Pydantic model

But we are already using Pydantic models in other places and we have already seen all the benefits.

Let's use them here too.

Create a model for the common parameters (and don't pay attention to the rest, for now):

```Python hl_lines="11 12 13 14"
{!./src/dependencies/tutorial002.py!}
```

## Return a Pydantic model

Now we can return a Pydantic model from the dependency ("dependable") with the same data as the dict before:

```Python hl_lines="17"
{!./src/dependencies/tutorial002.py!}
```

## Declare the Pydantic model

We can now come back to the path operation function and declare the type of the `commons` parameter to be that Pydantic model:

```Python
commons: CommonQueryParams = Depends(common_parameters)
```

It won't be interpreted as a JSON request `Body` because we are using `Depends`:

```Python hl_lines="21"
{!./src/dependencies/tutorial002.py!}
```

!!! info
    In the case of dependencies with `Depends`, the type of the parameter is only to get editor support.

    Your dependencies won't be enforced to return a specific type of data.

## Use the Pydantic model

And now we can use that model in our code, with all the lovable editor support:

```Python hl_lines="23 24 25"
{!./src/dependencies/tutorial002.py!}
```

<img src="/img/tutorial/dependencies/image02.png">

## Trees of hierarchical dependencies

With the **Dependency Injection** system you can build arbitrarily deep trees of hierarchical dependencies (also known as dependency graphs) by having dependencies that also have dependencies themselves.

You will see examples of these dependency trees in the next chapters about security.

## Recap

By using Pydantic models in your dependencies too you can keep all the editor support that **FastAPI** is designed to support.
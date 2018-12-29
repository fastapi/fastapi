Before diving deeper into the **Dependency Injection** system, let's upgrade the previous example.

## A `dict` from the previous example

In the previous example, we where returning a `dict` from our dependency ("dependable"):

```Python hl_lines="7"
{!./src/dependencies/tutorial001.py!}
```

But then we get a `dict` in the parameter `commons` of the path operation function.

And we know that `dict`s can't provide a lot of editor support because they can't know their keys and value types.

We can do better...

## What makes a dependency

Up to now you have seen dependencies declared as functions.

But that's not the only way to declare dependencies (although it would probably be the more common).

The key factor is that a dependency should be a "callable".

A "**callable**" in Python is anything that Python can "call" like a function.

So, if you have an object `something` (that might _not_ be a function) and you can do:

```Python
something()
```

or

```Python
something(some_argument, some_keyword_argument="foo")
```

then it is a "callable".

## Classes as dependencies

You might notice that to create an instance of a Python class, you use that same syntax.

So, a Python class is also a **callable**.

Then, in **FastAPI**, you could use a Python class as a dependency.

What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.

If you pass a "callable" as a dependency in **FastAPI**, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a path operation function. Including sub-dependencies.

That also applies to callables with no parameters at all. The same as would be for path operation functions with no parameters.

Then, we can change the dependency "dependable" `common_parameters` from above to the class `CommonQueryParameters`:

```Python hl_lines="9 10 11 12 13"
{!./src/dependencies/tutorial002.py!}
```

Pay attention to the `__init__` method used to create the instance of the class:

```Python hl_lines="10"
{!./src/dependencies/tutorial002.py!}
```

...it has the same parameters as our previous `common_parameters`:

```Python hl_lines="6"
{!./src/dependencies/tutorial001.py!}
```

Those parameters are what **FastAPI** will use to "solve" the dependency.

In both cases, it will have:

* an optional `q` query parameter.
* a `skip` query parameter, with a default of `0`.
* a `limit` query parameter, with a default of `100`.

In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.

## Use it

Now you can declare your dependency using this class.

And as when **FastAPI** calls that class the value that will be passed as `commons` to your function will be an "instance" of the class, you can declare that parameter `commons` to be of type of the class, `CommonQueryParams`.

```Python hl_lines="17"
{!./src/dependencies/tutorial002.py!}
```

## Type annotation vs `Depends`

In the code above, you are declaring `commons` as:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

The last `CommonQueryParams`, in:

```Python
... = Depends(CommonQueryParams)
```

...is what **FastAPI** will actually use to know what is the dependency.

From it is that FastAPI will extract the declared parameters and that is what FastAPI will actually call.

---

In this case, the first `CommonQueryParams`, in:

```Python
commons: CommonQueryParams ...
```

...doesn't have any special meaning for **FastAPI**. FastAPI won't use it for data conversion, validation, etc. (as it is using the `= Depends(CommonQueryParams)` for that).

You could actually write just:

```Python
commons = Depends(CommonQueryParams)
```

..as in:

```Python hl_lines="17"
{!./src/dependencies/tutorial003.py!}
```

But declaring the type is encouraged as that way your editor will know what will be passed as the parameter `commons`, and then it can help you with code completion, type checks, etc:

<img src="/img/tutorial/dependencies/image02.png">

## Shortcut

But you see that we are having some code repetition here, writing `CommonQueryParams` twice:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI** provides a shortcut for these cases, in where the dependency is *specifically* a class that **FastAPI** will "call" to create an instance of the class itself.

For those specific cases, you can do the following:

Instead of writing:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...you write:

```Python
commons: CommonQueryParams = Depends()
```

So, you can declare the dependency as the type of the variable, and use `Depends()` as the "default" value, without any parameter, instead of having to write the full class *again* inside of `Depends(CommonQueryParams)`.

So, the same example would look like:

```Python hl_lines="17"
{!./src/dependencies/tutorial004.py!}
```

...and **FastAPI** will know what to do.

!!! tip
    If all that seems more confusing than helpful, disregard it, you don't *need* it.
    
    It is just a shortcut. Because **FastAPI** cares about helping you minimize code repetition.

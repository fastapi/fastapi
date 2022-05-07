# Other annotations
Python 3.9 introduced the `Annotated` syntax for type annotations. This may also be used in older versions of Python by using the `Annotated` from the `typing_extensions` package.

In FastAPI, this allows us to specify annotations without using default values, and allows us to avoid repeating the type annotation for a dependency.

Let's look at the example from the dependecies tutorial:
=== "Python 3.6 and above"
    Before Python 3.9, we have to import `Annotated` from `typing_extensions` rather than `typing`.

    ``` Python hl_lines="13 17"
    {!> ../../../docs_src/annotated/tutorial001.py!}
    ```
=== "Python 3.9 and above"

    ``` Python hl_lines="12 16"
    {!> ../../../docs_src/annotated/tutorial001_py39.py!}
    ```

We first define a _type alias_ for our dependency, called `CommonParamsDepends`. This will allow us to re-use the combined type annotatation (the `dict` part), and the FastAPI annotation (the `Depends` part).

We then use this as the annotation for the `commons` parameter. This will tell FastAPI that the `commons` parameter is a dependency, just like if we had written 

```Python
async def read_items(commons = Depends(common_parameters)):
```

At the same time, it also tells your IDE and type-checker that `commons` is a `dict`. 

This saves you from having to write `param: dict = Depends(common_parameters)` everytime you use the `common_parameters` dependency. Instead we just defined an alias once, and can write `param: CommonParamsDepends` every time we use it.

## Class dependencies
`Annotated` also works with class dependencies.
=== "Python 3.6 and above"

    ``` Python hl_lines="9-16"
    {!> ../../../docs_src/annotated/tutorial002.py!}
    ```
=== "Python 3.9 and above"

    ``` Python hl_lines="8-15"
    {!> ../../../docs_src/annotated/tutorial002_py39.py!}
    ```

## Other Parameters
You may also use `Annotated` with other parameters, like `Path` and `Query`.
=== "Python 3.6 and above"

    ``` Python hl_lines="9"
    {!> ../../../docs_src/annotated/tutorial003.py!}
    ```
=== "Python 3.9 and above"

    ``` Python hl_lines="10"
    {!> ../../../docs_src/annotated/tutorial003_py39.py!}
    ```

When using `Annotated`, you specify the default value as you would normally in Python, because the default value is no longer taken up by the annotation.

=== "Python 3.6 and above"

    ``` Python hl_lines="14"
    {!> ../../../docs_src/annotated/tutorial003.py!}
    ```
=== "Python 3.9 and above"

    ``` Python hl_lines="15"
    {!> ../../../docs_src/annotated/tutorial003_py39.py!}
    ```

Note how we write `= "me"` and not `Query("me", min_length=1)`.

## `Annotated` is optional
Using `Annotated` is optional. You can use it where you want, and continue to use default values in other places.

You can mix both kinds of annotations, as long as you don't use them together for the same parameter.

## Version

This is available since FastAPI version `0.X.0`. 🔖

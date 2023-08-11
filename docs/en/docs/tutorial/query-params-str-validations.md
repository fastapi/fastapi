# Query Parameters and String Validations

**FastAPI** allows you to declare additional information and validation for your parameters.

Let's take this application as example:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

The query parameter `q` is of type `Union[str, None]` (or `str | None` in Python 3.10), that means that it's of type `str` but could also be `None`, and indeed, the default value is `None`, so FastAPI will know it's not required.

!!! note
    FastAPI will know that the value of `q` is not required because of the default value `= None`.

    The `Union` in `Union[str, None]` will allow your editor to give you better support and detect errors.

## Additional validation

We are going to enforce that even though `q` is optional, whenever it is provided, **its length doesn't exceed 50 characters**.

### Import `Query` and `Annotated`

To achieve that, first import:

* `Query` from `fastapi`
* `Annotated` from `typing` (or from `typing_extensions` in Python below 3.9)

=== "Python 3.10+"

    In Python 3.9 or above, `Annotated` is part of the standard library, so you can import it from `typing`.

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.6+"

    In versions of Python below Python 3.9 you import `Annotated` from `typing_extensions`.

    It will already be installed with FastAPI.

    ```Python hl_lines="3-4"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

!!! info
    FastAPI added support for `Annotated` (and started recommending it) in version 0.95.0.

    If you have an older version, you would get errors when trying to use `Annotated`.

    Make sure you [Upgrade the FastAPI version](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} to at least 0.95.1 before using `Annotated`.

## Use `Annotated` in the type for the `q` parameter

Remember I told you before that `Annotated` can be used to add metadata to your parameters in the [Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}?

Now it's the time to use it with FastAPI. 🚀

We had this type annotation:

=== "Python 3.10+"

    ```Python
    q: str | None = None
    ```

=== "Python 3.6+"

    ```Python
    q: Union[str, None] = None
    ```

What we will do is wrap that with `Annotated`, so it becomes:

=== "Python 3.10+"

    ```Python
    q: Annotated[str | None] = None
    ```

=== "Python 3.6+"

    ```Python
    q: Annotated[Union[str, None]] = None
    ```

Both of those versions mean the same thing, `q` is a parameter that can be a `str` or `None`, and by default, it is `None`.

Now let's jump to the fun stuff. 🎉

## Add `Query` to `Annotated` in the `q` parameter

Now that we have this `Annotated` where we can put more metadata, add `Query` to it, and set the parameter `max_length` to 50:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

Notice that the default value is still `None`, so the parameter is still optional.

But now, having `Query(max_length=50)` inside of `Annotated`, we are telling FastAPI that we want it to extract this value from the query parameters (this would have been the default anyway 🤷) and that we want to have **additional validation** for this value (that's why we do this, to get the additional validation). 😎

FastAPI will now:

* **Validate** the data making sure that the max length is 50 characters
* Show a **clear error** for the client when the data is not valid
* **Document** the parameter in the OpenAPI schema *path operation* (so it will show up in the **automatic docs UI**)

## Alternative (old) `Query` as the default value

Previous versions of FastAPI (before <abbr title="before 2023-03">0.95.0</abbr>) required you to use `Query` as the default value of your parameter, instead of putting it in `Annotated`, there's a high chance that you will see code using it around, so I'll explain it to you.

!!! tip
    For new code and whenever possible, use `Annotated` as explained above. There are multiple advantages (explained below) and no disadvantages. 🍰

This is how you would use `Query()` as the default value of your function parameter, setting the parameter `max_length` to 50:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

As in this case (without using `Annotated`) we have to replace the default value `None` in the function with `Query()`, we now need to set the default value with the parameter `Query(default=None)`, it serves the same purpose of defining that default value (at least for FastAPI).

So:

```Python
q: Union[str, None] = Query(default=None)
```

...makes the parameter optional, with a default value of `None`, the same as:

```Python
q: Union[str, None] = None
```

And in Python 3.10 and above:

```Python
q: str | None = Query(default=None)
```

...makes the parameter optional, with a default value of `None`, the same as:

```Python
q: str | None = None
```

But it declares it explicitly as being a query parameter.

!!! info
    Have in mind that the most important part to make a parameter optional is the part:

    ```Python
    = None
    ```

    or the:

    ```Python
    = Query(default=None)
    ```

    as it will use that `None` as the default value, and that way make the parameter **not required**.

    The `Union[str, None]` part allows your editor to provide better support, but it is not what tells FastAPI that this parameter is not required.

Then, we can pass more parameters to `Query`. In this case, the `max_length` parameter that applies to strings:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

This will validate the data, show a clear error when the data is not valid, and document the parameter in the OpenAPI schema *path operation*.

### `Query` as the default value or in `Annotated`

Have in mind that when using `Query` inside of `Annotated` you cannot use the `default` parameter for `Query`.

Instead use the actual default value of the function parameter. Otherwise, it would be inconsistent.

For example, this is not allowed:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...because it's not clear if the default value should be `"rick"` or `"morty"`.

So, you would use (preferably):

```Python
q: Annotated[str, Query()] = "rick"
```

...or in older code bases you will find:

```Python
q: str = Query(default="rick")
```

### Advantages of `Annotated`

**Using `Annotated` is recommended** instead of the default value in function parameters, it is **better** for multiple reasons. 🤓

The **default** value of the **function parameter** is the **actual default** value, that's more intuitive with Python in general. 😌

You could **call** that same function in **other places** without FastAPI, and it would **work as expected**. If there's a **required** parameter (without a default value), your **editor** will let you know with an error, **Python** will also complain if you run it without passing the required parameter.

When you don't use `Annotated` and instead use the **(old) default value style**, if you call that function without FastAPI in **other place**, you have to **remember** to pass the arguments to the function for it to work correctly, otherwise the values will be different from what you expect (e.g. `QueryInfo` or something similar instead of `str`). And your editor won't complain, and Python won't complain running that function, only when the operations inside error out.

Because `Annotated` can have more than one metadata annotation, you could now even use the same function with other tools, like <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Add more validations

You can also add a parameter `min_length`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

## Add regular expressions

You can define a <abbr title="A regular expression, regex or regexp is a sequence of characters that define a search pattern for strings.">regular expression</abbr> `pattern` that the parameter should match:

=== "Python 3.10+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

This specific regular expression pattern checks that the received parameter value:

* `^`: starts with the following characters, doesn't have characters before.
* `fixedquery`: has the exact value `fixedquery`.
* `$`: ends there, doesn't have any more characters after `fixedquery`.

If you feel lost with all these **"regular expression"** ideas, don't worry. They are a hard topic for many people. You can still do a lot of stuff without needing regular expressions yet.

But whenever you need them and go and learn them, know that you can already use them directly in **FastAPI**.

### Pydantic v1 `regex` instead of `pattern`

Before Pydantic version 2 and before FastAPI 0.100.0, the parameter was called `regex` instead of `pattern`, but it's now deprecated.

You could still see some code using it:

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310_regex.py!}
    ```

But know that this is deprecated and it should be updated to use the new parameter `pattern`. 🤓

## Default values

You can, of course, use default values other than `None`.

Let's say that you want to declare the `q` query parameter to have a `min_length` of `3`, and to have a default value of `"fixedquery"`:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial005.py!}
    ```

!!! note
    Having a default value of any type, including `None`, makes the parameter optional (not required).

## Make it required

When we don't need to declare more validations or metadata, we can make the `q` query parameter required just by not declaring a default value, like:

```Python
q: str
```

instead of:

```Python
q: Union[str, None] = None
```

But we are now declaring it with `Query`, for example like:

=== "Annotated"

    ```Python
    q: Annotated[Union[str, None], Query(min_length=3)] = None
    ```

=== "non-Annotated"

    ```Python
    q: Union[str, None] = Query(default=None, min_length=3)
    ```

So, when you need to declare a value as required while using `Query`, you can simply not declare a default value:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006.py!}
    ```

    !!! tip
        Notice that, even though in this case the `Query()` is used as the function parameter default value, we don't pass the `default=None` to `Query()`.

        Still, probably better to use the `Annotated` version. 😉

### Required with Ellipsis (`...`)

There's an alternative way to explicitly declare that a value is required. You can set the default to the literal value `...`:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b.py!}
    ```

!!! info
    If you hadn't seen that `...` before: it is a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">part of Python and is called "Ellipsis"</a>.

    It is used by Pydantic and FastAPI to explicitly declare that a value is required.

This will let **FastAPI** know that this parameter is required.

### Required with `None`

You can declare that a parameter can accept `None`, but that it's still required. This would force clients to send a value, even if the value is `None`.

To do that, you can declare that `None` is a valid type but still use `...` as the default:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

!!! tip
    Pydantic, which is what powers all the data validation and serialization in FastAPI, has a special behavior when you use `Optional` or `Union[Something, None]` without a default value, you can read more about it in the Pydantic docs about <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">Required Optional fields</a>.

### Use Pydantic's `Required` instead of Ellipsis (`...`)

If you feel uncomfortable using `...`, you can also import and use `Required` from Pydantic:

=== "Python 3.9+"

    ```Python hl_lines="4  10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="2  9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="2  8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d.py!}
    ```

!!! tip
    Remember that in most of the cases, when something is required, you can simply omit the default, so you normally don't have to use `...` nor `Required`.

## Query parameter list / multiple values

When you define a query parameter explicitly with `Query` you can also declare it to receive a list of values, or said in other way, to receive multiple values.

For example, to declare a query parameter `q` that can appear multiple times in the URL, you can write:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
    ```

=== "Python 3.9+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

Then, with a URL like:

```
http://localhost:8000/items/?q=foo&q=bar
```

you would receive the multiple `q` *query parameters'* values (`foo` and `bar`) in a Python `list` inside your *path operation function*, in the *function parameter* `q`.

So, the response to that URL would be:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip
    To declare a query parameter with a type of `list`, like in the example above, you need to explicitly use `Query`, otherwise it would be interpreted as a request body.

The interactive API docs will update accordingly, to allow multiple values:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Query parameter list / multiple values with defaults

And you can also define a default `list` of values if none are provided:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an.py!}
    ```

=== "Python 3.9+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

If you go to:

```
http://localhost:8000/items/
```

the default of `q` will be: `["foo", "bar"]` and your response will be:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Using `list`

You can also use `list` directly instead of `List[str]` (or `list[str]` in Python 3.9+):

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial013.py!}
    ```

!!! note
    Have in mind that in this case, FastAPI won't check the contents of the list.

    For example, `List[int]` would check (and document) that the contents of the list are integers. But `list` alone wouldn't.

## Declare more metadata

You can add more information about the parameter.

That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools.

!!! note
    Have in mind that different tools might have different levels of OpenAPI support.

    Some of them might not show all the extra information declared yet, although in most of the cases, the missing feature is already planned for development.

You can add a `title`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

And a `description`:

=== "Python 3.10+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="15"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

## Alias parameters

Imagine that you want the parameter to be `item-query`.

Like in:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

But `item-query` is not a valid Python variable name.

The closest would be `item_query`.

But you still need it to be exactly `item-query`...

Then you can declare an `alias`, and that alias is what will be used to find the parameter value:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

## Deprecating parameters

Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as <abbr title="obsolete, recommended not to use it">deprecated</abbr>.

Then pass the parameter `deprecated=True` to `Query`:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="17"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

The docs will show it like this:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Exclude from OpenAPI

To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter `include_in_schema` of `Query` to `False`:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

## Recap

You can declare additional validations and metadata for your parameters.

Generic validations and metadata:

* `alias`
* `title`
* `description`
* `deprecated`

Validations specific for strings:

* `min_length`
* `max_length`
* `regex`

In these examples you saw how to declare validations for `str` values.

See the next chapters to see how to declare validations for other types, like numbers.

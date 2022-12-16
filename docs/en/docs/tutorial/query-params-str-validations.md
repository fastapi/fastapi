# Query Parameters and String Validations

**FastAPI** allows you to declare additional information and validation for your parameters.

Let's take this application as example:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

The query parameter `q` is of type `Union[str, None]` (or `str | None` in Python 3.10), that means that it's of type `str` but could also be `None`, and indeed, the default value is `None`, so FastAPI will know it's not required.

!!! note
    FastAPI will know that the value of `q` is not required because of the default value `= None`.

    The `Union` in `Union[str, None]` will allow your editor to give you better support and detect errors.

## Additional validation

We are going to enforce that even though `q` is optional, whenever it is provided, **its length doesn't exceed 50 characters**.

### Import `Query`

To achieve that, first import `Query` from `fastapi`:

=== "Python 3.6 and above"

    ```Python hl_lines="3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="1"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

## Use `Query` as the default value

And now use it as the default value of your parameter, setting the parameter `max_length` to 50:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

As we have to replace the default value `None` in the function with `Query()`, we can now set the default value with the parameter `Query(default=None)`, it serves the same purpose of defining that default value.

So:

```Python
q: Union[str, None] = Query(default=None)
```

...makes the parameter optional, the same as:

```Python
q: Union[str, None] = None
```

And in Python 3.10 and above:

```Python
q: str | None = Query(default=None)
```

...makes the parameter optional, the same as:

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

## Add more validations

You can also add a parameter `min_length`:

=== "Python 3.6 and above"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

## Add regular expressions

You can define a <abbr title="A regular expression, regex or regexp is a sequence of characters that define a search pattern for strings.">regular expression</abbr> that the parameter should match:

=== "Python 3.6 and above"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

This specific regular expression checks that the received parameter value:

* `^`: starts with the following characters, doesn't have characters before.
* `fixedquery`: has the exact value `fixedquery`.
* `$`: ends there, doesn't have any more characters after `fixedquery`.

If you feel lost with all these **"regular expression"** ideas, don't worry. They are a hard topic for many people. You can still do a lot of stuff without needing regular expressions yet.

But whenever you need them and go and learn them, know that you can already use them directly in **FastAPI**.

## Default values

The same way that you can pass `None` as the value for the `default` parameter, you can pass other values.

Let's say that you want to declare the `q` query parameter to have a `min_length` of `3`, and to have a default value of `"fixedquery"`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial005.py!}
```

!!! note
    Having a default value also makes the parameter optional.

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

```Python
q: Union[str, None] = Query(default=None, min_length=3)
```

So, when you need to declare a value as required while using `Query`, you can simply not declare a default value:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006.py!}
```

### Required with Ellipsis (`...`)

There's an alternative way to explicitly declare that a value is required. You can set the `default` parameter to the literal value `...`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006b.py!}
```

!!! info
    If you hadn't seen that `...` before: it is a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">part of Python and is called "Ellipsis"</a>.

    It is used by Pydantic and FastAPI to explicitly declare that a value is required.

This will let **FastAPI** know that this parameter is required.

### Required with `None`

You can declare that a parameter can accept `None`, but that it's still required. This would force clients to send a value, even if the value is `None`.

To do that, you can declare that `None` is a valid type but still use `default=...`:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

!!! tip
    Pydantic, which is what powers all the data validation and serialization in FastAPI, has a special behavior when you use `Optional` or `Union[Something, None]` without a default value, you can read more about it in the Pydantic docs about <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">Required Optional fields</a>.

### Use Pydantic's `Required` instead of Ellipsis (`...`)

If you feel uncomfortable using `...`, you can also import and use `Required` from Pydantic:

```Python hl_lines="2  8"
{!../../../docs_src/query_params_str_validations/tutorial006d.py!}
```

!!! tip
    Remember that in most of the cases, when something is required, you can simply omit the `default` parameter, so you normally don't have to use `...` nor `Required`.

## Query parameter list / multiple values

When you define a query parameter explicitly with `Query` you can also declare it to receive a list of values, or said in other way, to receive multiple values.

For example, to declare a query parameter `q` that can appear multiple times in the URL, you can write:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
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

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

=== "Python 3.9 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
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

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial013.py!}
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

=== "Python 3.6 and above"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

And a `description`:

=== "Python 3.6 and above"

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
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

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

## Deprecating parameters

Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as <abbr title="obsolete, recommended not to use it">deprecated</abbr>.

Then pass the parameter `deprecated=True` to `Query`:

=== "Python 3.6 and above"

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="17"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

The docs will show it like this:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Exclude from OpenAPI

To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter `include_in_schema` of `Query` to `False`:

=== "Python 3.6 and above"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
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

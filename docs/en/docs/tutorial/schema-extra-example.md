# Declare Request Example Data

You can declare examples of the data your app can receive.

Here are several ways to do it.

## Extra JSON Schema data in Pydantic models

You can declare `examples` for a Pydantic model that will be added to the generated JSON Schema.

=== "Python 3.10+ Pydantic v2"

    ```Python hl_lines="13-24"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310.py!}
    ```

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="13-23"
    {!> ../../../docs_src/schema_extra_example/tutorial001_py310_pv1.py!}
    ```

=== "Python 3.6+ Pydantic v2"

    ```Python hl_lines="15-26"
    {!> ../../../docs_src/schema_extra_example/tutorial001.py!}
    ```

=== "Python 3.6+ Pydantic v1"

    ```Python hl_lines="15-25"
    {!> ../../../docs_src/schema_extra_example/tutorial001_pv1.py!}
    ```

That extra info will be added as-is to the output **JSON Schema** for that model, and it will be used in the API docs.

=== "Pydantic v2"

    In Pydantic version 2, you would use the attribute `model_config`, that takes a `dict` as described in <a href="https://docs.pydantic.dev/latest/usage/model_config/" class="external-link" target="_blank">Pydantic's docs: Model Config</a>.

    You can set `"json_schema_extra"` with a `dict` containing any additonal data you would like to show up in the generated JSON Schema, including `examples`.

=== "Pydantic v1"

    In Pydantic version 1, you would use an internal class `Config` and `schema_extra`, as described in <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic's docs: Schema customization</a>.

    You can set `schema_extra` with a `dict` containing any additonal data you would like to show up in the generated JSON Schema, including `examples`.

!!! tip
    You could use the same technique to extend the JSON Schema and add your own custom extra info.

    For example you could use it to add metadata for a frontend user interface, etc.

!!! info
    OpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for `examples`, which is part of the **JSON Schema** standard.

    Before that, it only supported the keyword `example` with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate `example` to `examples`. 🤓

    You can read more at the end of this page.

## `Field` additional arguments

When using `Field()` with Pydantic models, you can also declare additional `examples`:

=== "Python 3.10+"

    ```Python hl_lines="2  8-11"
    {!> ../../../docs_src/schema_extra_example/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4  10-13"
    {!> ../../../docs_src/schema_extra_example/tutorial002.py!}
    ```

## `examples` in OpenAPI

When using any of:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

you can also declare a group of `examples` with additional information that will be added to **OpenAPI**.

### `Body` with `examples`

Here we pass `examples` containing one example of the data expected in `Body()`:

=== "Python 3.10+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="22-29"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="23-30"
    {!> ../../../docs_src/schema_extra_example/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="18-25"
    {!> ../../../docs_src/schema_extra_example/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="20-27"
    {!> ../../../docs_src/schema_extra_example/tutorial003.py!}
    ```

### Example in the docs UI

With any of the methods above it would look like this in the `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` with multiple `examples`

You can of course also pass multiple `examples`:

=== "Python 3.10+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23-38"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24-39"
    {!> ../../../docs_src/schema_extra_example/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="19-34"
    {!> ../../../docs_src/schema_extra_example/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="21-36"
    {!> ../../../docs_src/schema_extra_example/tutorial004.py!}
    ```

### Examples in the docs UI

With `examples` added to `Body()` the `/docs` would look like:

<img src="/img/tutorial/body-fields/image02.png">

## Technical Details

!!! tip
    If you are already using **FastAPI** version **0.99.0 or above**, you can probably **skip** these details.

    They are more relevant for older versions, before OpenAPI 3.1.0 was available.

    You can consider this a brief OpenAPI and JSON Schema **history lesson**. 🤓

!!! warning
    These are very technical details about the standards **JSON Schema** and **OpenAPI**.

    If the ideas above already work for you, that might be enough, and you probably don't need these details, feel free to skip them.

Before OpenAPI 3.1.0, OpenAPI used an older and modified version of **JSON Schema**.

JSON Schema didn't have `examples`, so OpenAPI added it's own `example` field to its own modified version.

OpenAPI also added `example` and `examples` fields to other parts of the specification:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object` (in the specification)</a> that was used by FastAPI's:
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object`, in the field `content`, on the `Media Type Object` (in the specification)</a> that was used by FastAPI's:
    * `Body()`
    * `File()`
    * `Form()`

### OpenAPI's `examples` field

The shape of this field `examples` from OpenAPI is a `dict` with **multiple examples**, each with extra information that will be added to **OpenAPI** too.

The keys of the `dict` identify each example, and each value is another `dict`.

Each specific example `dict` in the `examples` can contain:

* `summary`: Short description for the example.
* `description`: A long description that can contain Markdown text.
* `value`: This is the actual example shown, e.g. a `dict`.
* `externalValue`: alternative to `value`, a URL pointing to the example. Although this might not be supported by as many tools as `value`.

This applies to those other parts of the OpenAPI specification apart from JSON Schema.

### JSON Schema's `examples` field

But then JSON Schema added an <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> field to a new version of the specification.

And then the new OpenAPI 3.1.0 was based on the latest version (JSON Schema 2020-12) that included this new field `examples`.

And now this new `examples` field takes precedence over the old single (and custom) `example` field, that is now deprecated.

This new `examples` field in JSON Schema is **just a `list`** of examples, not a dict with extra metadata as in the other places in OpenAPI (described above).

!!! info
    Even after OpenAPI 3.1.0 was released with this new simpler integration with JSON Schema, for a while, Swagger UI, the tool that provides the automatic docs, didn't support OpenAPI 3.1.0 (it does since version 5.0.0 🎉).

    Because of that, versions of FastAPI previous to 0.99.0 still used versions of OpenAPI lower than 3.1.0.

### Pydantic and FastAPI `examples`

When you add `examples` inside of a Pydantic model, using `schema_extra` or `Field(examples=["something"])` that example is added to the **JSON Schema** for that Pydantic model.

And that **JSON Schema** of the Pydantic model is included in the **OpenAPI** of your API, and then it's used in the docs UI.

In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used `example` or `examples` with any of the other utilities (`Query()`, `Body()`, etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the *path operation* declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).

But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.

### Summary

I used to say I didn't like history that much... and look at me now giving "tech history" lessons. 😅

In short, **upgrade to FastAPI 0.99.0 or above**, and things are much **simpler, consistent, and intuitive**, and you don't have to know all these historic details. 😎

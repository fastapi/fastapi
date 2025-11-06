# Declare Request Example Data { #declare-request-example-data }

You can declare examples of the data your app can receive.

Here are several ways to do it.

## Extra JSON Schema data in Pydantic models { #extra-json-schema-data-in-pydantic-models }

You can declare `examples` for a Pydantic model that will be added to the generated JSON Schema.

//// tab | Pydantic v2

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/schema_extra_example/tutorial001_pv1_py310.py hl[13:23] *}

////

That extra info will be added as-is to the output **JSON Schema** for that model, and it will be used in the API docs.

//// tab | Pydantic v2

In Pydantic version 2, you would use the attribute `model_config`, that takes a `dict` as described in <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Pydantic's docs: Configuration</a>.

You can set `"json_schema_extra"` with a `dict` containing any additional data you would like to show up in the generated JSON Schema, including `examples`.

////

//// tab | Pydantic v1

In Pydantic version 1, you would use an internal class `Config` and `schema_extra`, as described in <a href="https://docs.pydantic.dev/1.10/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic's docs: Schema customization</a>.

You can set `schema_extra` with a `dict` containing any additional data you would like to show up in the generated JSON Schema, including `examples`.

////

/// tip

You could use the same technique to extend the JSON Schema and add your own custom extra info.

For example you could use it to add metadata for a frontend user interface, etc.

///

/// info

OpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for `examples`, which is part of the **JSON Schema** standard.

Before that, it only supported the keyword `example` with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate `example` to `examples`. 🤓

You can read more at the end of this page.

///

## `Field` additional arguments { #field-additional-arguments }

When using `Field()` with Pydantic models, you can also declare additional `examples`:

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## `examples` in JSON Schema - OpenAPI { #examples-in-json-schema-openapi }

When using any of:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

you can also declare a group of `examples` with additional information that will be added to their **JSON Schemas** inside of **OpenAPI**.

### `Body` with `examples` { #body-with-examples }

Here we pass `examples` containing one example of the data expected in `Body()`:

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Example in the docs UI { #example-in-the-docs-ui }

With any of the methods above it would look like this in the `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

### `Body` with multiple `examples` { #body-with-multiple-examples }

You can of course also pass multiple `examples`:

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

When you do this, the examples will be part of the internal **JSON Schema** for that body data.

Nevertheless, at the <abbr title="2023-08-26">time of writing this</abbr>, Swagger UI, the tool in charge of showing the docs UI, doesn't support showing multiple examples for the data in **JSON Schema**. But read below for a workaround.

### OpenAPI-specific `examples` { #openapi-specific-examples }

Since before **JSON Schema** supported `examples` OpenAPI had support for a different field also called `examples`.

This **OpenAPI-specific** `examples` goes in another section in the OpenAPI specification. It goes in the **details for each *path operation***, not inside each JSON Schema.

And Swagger UI has supported this particular `examples` field for a while. So, you can use it to **show** different **examples in the docs UI**.

The shape of this OpenAPI-specific field `examples` is a `dict` with **multiple examples** (instead of a `list`), each with extra information that will be added to **OpenAPI** too.

This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the *path operation* directly.

### Using the `openapi_examples` Parameter { #using-the-openapi-examples-parameter }

You can declare the OpenAPI-specific `examples` in FastAPI with the parameter `openapi_examples` for:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

The keys of the `dict` identify each example, and each value is another `dict`.

Each specific example `dict` in the `examples` can contain:

* `summary`: Short description for the example.
* `description`: A long description that can contain Markdown text.
* `value`: This is the actual example shown, e.g. a `dict`.
* `externalValue`: alternative to `value`, a URL pointing to the example. Although this might not be supported by as many tools as `value`.

You can use it like this:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### OpenAPI Examples in the Docs UI { #openapi-examples-in-the-docs-ui }

With `openapi_examples` added to `Body()` the `/docs` would look like:

<img src="/img/tutorial/body-fields/image02.png">

## Technical Details { #technical-details }

/// tip

If you are already using **FastAPI** version **0.99.0 or above**, you can probably **skip** these details.

They are more relevant for older versions, before OpenAPI 3.1.0 was available.

You can consider this a brief OpenAPI and JSON Schema **history lesson**. 🤓

///

/// warning

These are very technical details about the standards **JSON Schema** and **OpenAPI**.

If the ideas above already work for you, that might be enough, and you probably don't need these details, feel free to skip them.

///

Before OpenAPI 3.1.0, OpenAPI used an older and modified version of **JSON Schema**.

JSON Schema didn't have `examples`, so OpenAPI added its own `example` field to its own modified version.

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

/// info

This old OpenAPI-specific `examples` parameter is now `openapi_examples` since FastAPI `0.103.0`.

///

### JSON Schema's `examples` field { #json-schemas-examples-field }

But then JSON Schema added an <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> field to a new version of the specification.

And then the new OpenAPI 3.1.0 was based on the latest version (JSON Schema 2020-12) that included this new field `examples`.

And now this new `examples` field takes precedence over the old single (and custom) `example` field, that is now deprecated.

This new `examples` field in JSON Schema is **just a `list`** of examples, not a dict with extra metadata as in the other places in OpenAPI (described above).

/// info

Even after OpenAPI 3.1.0 was released with this new simpler integration with JSON Schema, for a while, Swagger UI, the tool that provides the automatic docs, didn't support OpenAPI 3.1.0 (it does since version 5.0.0 🎉).

Because of that, versions of FastAPI previous to 0.99.0 still used versions of OpenAPI lower than 3.1.0.

///

### Pydantic and FastAPI `examples` { #pydantic-and-fastapi-examples }

When you add `examples` inside a Pydantic model, using `schema_extra` or `Field(examples=["something"])` that example is added to the **JSON Schema** for that Pydantic model.

And that **JSON Schema** of the Pydantic model is included in the **OpenAPI** of your API, and then it's used in the docs UI.

In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used `example` or `examples` with any of the other utilities (`Query()`, `Body()`, etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the *path operation* declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).

But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.

### Swagger UI and OpenAPI-specific `examples` { #swagger-ui-and-openapi-specific-examples }

Now, as Swagger UI didn't support multiple JSON Schema examples (as of 2023-08-26), users didn't have a way to show multiple examples in the docs.

To solve that, FastAPI `0.103.0` **added support** for declaring the same old **OpenAPI-specific** `examples` field with the new parameter `openapi_examples`. 🤓

### Summary { #summary }

I used to say I didn't like history that much... and look at me now giving "tech history" lessons. 😅

In short, **upgrade to FastAPI 0.99.0 or above**, and things are much **simpler, consistent, and intuitive**, and you don't have to know all these historic details. 😎

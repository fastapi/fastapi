# Schema Extra - Example

You can define extra information to go in JSON Schema.

A common use case is to add an `example` that will be shown in the docs.

There are several ways you can declare extra JSON Schema information.

## Pydantic `schema_extra`

You can declare an example for a Pydantic model using `Config` and `schema_extra`, as described in <a href="https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic's docs: Schema customization</a>:

```Python hl_lines="15 16 17 18 19 20 21 22 23"
{!../../../docs_src/schema_extra_example/tutorial001.py!}
```

That extra info will be added as-is to the output JSON Schema.

## `Field` additional arguments

In `Field`, `Path`, `Query`, `Body` and others you'll see later, you can also declare extra info for the JSON Schema by passing any other arbitrary arguments to the function, for example, to add an `example`:

```Python hl_lines="4 10 11 12 13"
{!../../../docs_src/schema_extra_example/tutorial002.py!}
```

!!! warning
    Have in mind that those extra arguments passed won't add any validation, only annotation, for documentation purposes.

## `Body` additional arguments

The same way you can pass extra info to `Field`, you can do the same with `Path`, `Query`, `Body`, etc.

For example, you can pass an `example` for a body request to `Body`:

```Python hl_lines="21 22 23 24 25 26"
{!../../../docs_src/schema_extra_example/tutorial003.py!}
```

## Example in the docs UI

With any of the methods above it would look like this in the `/docs`:

<img src="/img/tutorial/body-fields/image01.png">

## Technical Details

About `example` vs `examples`...

JSON Schema defines a field <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> in the most recent versions, but OpenAPI is based on an older version of JSON Schema that didn't have `examples`.

So, OpenAPI defined its own <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a> for the same purpose (as `example`, not `examples`), and that's what is used by the docs UI (using Swagger UI).

So, although `example` is not part of JSON Schema, it is part of OpenAPI, and that's what will be used by the docs UI.

## Other info

The same way, you could add your own custom extra info that would be added to the JSON Schema for each model, for example to customize a frontend user interface, etc.

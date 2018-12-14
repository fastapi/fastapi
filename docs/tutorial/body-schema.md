The same way you can declare additional validation and metadata in endpoint function parameters with `Query`, `Path` and `Body`, you can declare validation and metadata inside of Pydantic models using `Schema`.

## Import Schema

First, you have to import it:

```Python hl_lines="2"
{!./tutorial/src/body-schema/tutorial001.py!}
```

!!! warning
    Notice that `Schema` is imported directly from `pydantic`, not form `fastapi` as are all the rest (`Query`, `Path`, `Body`, etc).


## Declare model attributes

You can then use `Schema` with model attributes:

```Python hl_lines="9 10"
{!./tutorial/src/body-schema/tutorial001.py!}
```

`Schema` works the same way as `Query`, `Path` and `Body`, it has all the same parameters, etc.


!!! info
    Actually, `Query`, `Path` and others you'll see next are subclasses of a common `Param` which is itself a subclass of Pydantic's `Schema`.

    `Body` is also a subclass of `Schema` directly. And there are others you will see later that are subclasses of `Body`.

!!! tip
    Notice how each model's attribute with a type, default value and `Schema` has the same structure as an endpoint's function's parameter, with `Schema` instead of `Path`, `Query` and `Body`.

## Schema extras

In `Schema`, `Path`, `Query`, `Body` and others you'll see later, you can declare extra parameters apart from those described before.

Those parameters will be added as-is to the output JSON Schema.

If you know JSON Schema and want to add extra information appart from what we have discussed here, you can pass that as extra keyword arguments.

!!! warning
    Have in mind that extra parameters passed won't add any validation, only annotation, for documentation purposes.

For example, you can use that functionality to pass a <a href="http://json-schema.org/latest/json-schema-validation.html#rfc.section.8.5" target="_blank">JSON Schema example</a> field to a body request JSON Schema:

```Python hl_lines="20 21 22 23 24 25"
{!./tutorial/src/body-schema/tutorial002.py!}
```

## Recap

You can use Pydantic's `Schema` to declare extra validations and metadata for model attributes.

You can also use the extra keyword arguments to pass additional JSON Schema metadata.
The same way you can declare additional validation and metadata in *path operation function* parameters with `Query`, `Path` and `Body`, you can declare validation and metadata inside of Pydantic models using Pydantic's `Field`.

## Import `Field`

First, you have to import it:

```Python hl_lines="2"
{!./src/body_fields/tutorial001.py!}
```

!!! warning
    Notice that `Field` is imported directly from `pydantic`, not from `fastapi` as are all the rest (`Query`, `Path`, `Body`, etc).

## Declare model attributes

You can then use `Field` with model attributes:

```Python hl_lines="9 10"
{!./src/body_fields/tutorial001.py!}
```

`Field` works the same way as `Query`, `Path` and `Body`, it has all the same parameters, etc.

!!! note "Technical Details"
    Actually, `Query`, `Path` and others you'll see next create objects of subclasses of a common `Param` class, which is itself a subclass of Pydantic's `FieldInfo` class.

    And Pydantic's `Field` returns an instance of `FieldInfo` as well.

    `Body` also returns objects of a subclass of `FieldInfo` directly. And there are others you will see later that are subclasses of the `Body` class.

    Remember that when you import `Query`, `Path`, and others from `fastapi`, those are actually functions that return special classes.

!!! tip
    Notice how each model's attribute with a type, default value and `Field` has the same structure as a *path operation function's* parameter, with `Field` instead of `Path`, `Query` and `Body`.

## JSON Schema extras

In `Field`, `Path`, `Query`, `Body` and others you'll see later, you can declare extra parameters apart from those described before.

Those parameters will be added as-is to the output JSON Schema.

If you know JSON Schema and want to add extra information apart from what we have discussed here, you can pass that as extra keyword arguments.

!!! warning
    Have in mind that extra parameters passed won't add any validation, only annotation, for documentation purposes.

For example, you can use that functionality to pass a <a href="http://json-schema.org/latest/json-schema-validation.html#rfc.section.8.5" class="external-link" target="_blank">JSON Schema example</a> field to a body request JSON Schema:

```Python hl_lines="20 21 22 23 24 25"
{!./src/body_fields/tutorial002.py!}
```

And it would look in the `/docs` like this:

<img src="/img/tutorial/body-fields/image01.png">

## Recap

You can use Pydantic's `Field` to declare extra validations and metadata for model attributes.

You can also use the extra keyword arguments to pass additional JSON Schema metadata.

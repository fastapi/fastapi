## OpenAPI operationId

!!! warning
    If you are not an "expert" in OpenAPI, you probably don't need this.

You can set the OpenAPI `operationId` to be used in your *path operation* with the parameter `operation_id`.

You would have to make sure that it is unique for each operation.

```Python hl_lines="6"
{!./src/path_operation_advanced_configuration/tutorial001.py!}
```

### Using the *path operation function* name as the operationId

If you want to use your APIs' function names as `operationId`s, you can iterate over all of them and override each *path operation's* `operation_id` using their `APIRoute.name`.

You should do it after adding all your *path operations*.

```Python hl_lines="2 12 13 14 15 16 17 18 19 20 21 24"
{!./src/path_operation_advanced_configuration/tutorial002.py!}
```

!!! tip
    If you manually call `app.openapi()`, you should update the `operationId`s before that.

!!! warning
    If you do this, you have to make sure each one of your *path operation functions* has a unique name.

    Even if they are in different modules (Python files).

## Exclude from OpenAPI

To exclude a *path operation* from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter `include_in_schema` and set it to `False`;

```Python hl_lines="6"
{!./src/path_operation_advanced_configuration/tutorial003.py!}
```

## Advanced description from docstring

You can limit the lines used from the docstring of a *path operation function* for OpenAPI.

Adding an `\f` (an escaped "form feed" character) causes **FastAPI** to truncate the output used for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.

```Python hl_lines="19 20 21 22 23 24 25 26 27 28 29"
{!./src/path_operation_advanced_configuration/tutorial004.py!}
```

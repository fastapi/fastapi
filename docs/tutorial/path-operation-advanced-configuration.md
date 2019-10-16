## OpenAPI operationId

!!! danger
    If you are not an "expert" in OpenAPI, you probably don't need this.

You can set the OpenAPI `operationId` to be used in your path operation with the parameter `operation_id`.

You would have to make sure that it is unique for each operation.

```Python hl_lines="6"
{!./src/path_operation_advanced_configuration/tutorial001.py!}
```

## Exclude from OpenAPI

To exclude a path operation from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter `include_in_schema` and set it to `False`;

```Python hl_lines="6"
{!./src/path_operation_advanced_configuration/tutorial002.py!}
```

## Advanced description from docstring

You can limit the lines used from the docstring of a *path operation function* for OpenAPI.

Adding an `\f` (an escaped "form feed" character) causes **FastAPI** to truncate the output used for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.

```Python hl_lines="19 20 21 22 23 24 25 26 27 28 29"
{!./src/path_operation_advanced_configuration/tutorial003.py!}
```

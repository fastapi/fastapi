## OpenAPI operationId

!!! danger
    If you are not an "expert" in OpenAPI, you probably don't need this.

You can set the OpenAPI `operationId` to be used in your path operation with the parameter `operation_id`.

You would have to make sure that it is unique for each operation.

```Python hl_lines="6"
{!./tutorial/src/path_operation_advanced_configuration/tutorial001.py!}
```

## Exclude from OpenAPI

To exclude a path operation from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter `include_in_schema` and set it to `False`;

```Python hl_lines="6"
{!./tutorial/src/path_operation_advanced_configuration/tutorial002.py!}
```

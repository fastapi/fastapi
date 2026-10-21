# Query Parameter Models { #query-parameter-models }

If you have a group of **query parameters** that are related, you can create a **Pydantic model** to declare them.

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

/// note

This is supported since FastAPI version `0.115.0`. 🤓

///

## Query Parameters with a Pydantic Model { #query-parameters-with-a-pydantic-model }

Declare the **query parameters** that you need in a **Pydantic model**, and then declare the parameter as `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** will **extract** the data for **each field** from the **query parameters** in the request and give you the Pydantic model you defined.

## Check the Docs { #check-the-docs }

You can see the query parameters in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Forbid Extra Query Parameters { #forbid-extra-query-parameters }

In some special use cases (probably not very common), you might want to **restrict** the query parameters that you want to receive.

You can use Pydantic's model configuration to `forbid` any `extra` fields:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

If a client tries to send some **extra** data in the **query parameters**, they will receive an **error** response.

For example, if the client tries to send a `tool` query parameter with a value of `plumbus`, like:

```http
https://example.com/items/?limit=10&tool=plumbus
```

They will receive an **error** response telling them that the query parameter `tool` is not allowed:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Combine Parameter Models { #combine-parameter-models }

You can declare multiple query parameter models, and combine them with individual query parameters or dependencies.

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

The request parameters stay at the same level.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

There are no `pagination` or `filters` keys in the query string. Each model receives its own fields, and Pydantic applies its defaults, field validators, and model validators. The same applies when the models or individual parameters are declared in dependencies.

If models share a parameter name or alias, each model validates that request parameter independently. Use distinct names or aliases for independent values. OpenAPI lists a shared parameter once, as it does for parameters shared with dependencies, so shared declarations should describe the same type and constraints.

With `extra="forbid"`, parameters declared elsewhere in the same operation or its dependencies are allowed. Undeclared parameters are still rejected. With `extra="allow"`, undeclared parameters are included as model extras. Parameters belonging only to other declarations are not included. An unused alternative alias of a model's own field still follows that model's extra-field policy.

This also works for `Header` and `Cookie` models.

## Optional Query Parameter Models { #optional-query-parameter-models }

Declare a query parameter model with `| None` and a default of `None` to make the group optional.

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

If neither `start` nor `end` is sent, `date_range` is `None`. If either is sent, FastAPI validates the model and requires both fields.

Using `| None` without a default still makes the parameter required.

Unknown parameters follow the model's `extra` configuration. Ignored extras do not make the model present.

OpenAPI lists the group's fields individually and marks them as optional.

You can also declare optional [header parameter models](header-param-models.md#optional-header-parameter-models) and [cookie parameter models](cookie-param-models.md#optional-cookie-parameter-models).

## Summary { #summary }

You can use **Pydantic models** to declare **query parameters** in **FastAPI**. 😎

/// tip

Spoiler alert: you can also use Pydantic models to declare cookies and headers, but you will read about that later in the tutorial. 🤫

///

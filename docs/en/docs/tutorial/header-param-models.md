# Header Parameter Models

If you have a group of related **header parameters**, you can create a **Pydantic model** to declare them.

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

/// note

This is supported since FastAPI version `0.115.0`. 🤓

///

## Header Parameters with a Pydantic Model

Declare the **header parameters** that you need in a **Pydantic model**, and then declare the parameter as `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** will **extract** the data for **each field** from the **headers** in the request and give you the Pydantic model you defined.

## Check the Docs

You can see the required headers in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Forbid Extra Headers

In some special use cases (probably not very common), you might want to **restrict** the headers that you want to receive.

You can use Pydantic's model configuration to `forbid` any `extra` fields:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

If a client tries to send some **extra headers**, they will receive an **error** response.

For example, if the client tries to send a `tool` header with a value of `plumbus`, they will receive an **error** response telling them that the header parameter `tool` is not allowed:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Summary

You can use **Pydantic models** to declare **headers** in **FastAPI**. 😎

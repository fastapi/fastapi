# Header Parameter Models

If you have a group of related **header parameters**, you can create a **Pydantic model** to declare them.

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

/// note

This is supported since FastAPI version `0.115.0`. 🤓

///

## Header Parameters with a Pydantic Model

Declare the **header parameters** that you need in a **Pydantic model**, and then declare the parameter as `Header`:

//// tab | Python 3.10+

```Python hl_lines="9-14  18"
{!> ../../../docs_src/header_param_models/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9-14  18"
{!> ../../../docs_src/header_param_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10-15  19"
{!> ../../../docs_src/header_param_models/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7-12  16"
{!> ../../../docs_src/header_param_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="9-14  18"
{!> ../../../docs_src/header_param_models/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7-12  16"
{!> ../../../docs_src/header_param_models/tutorial001_py310.py!}
```

////

**FastAPI** will **extract** the data for **each field** from the **headers** in the request and give you the Pydantic model you defined.

## Check the Docs

You can see the required headers in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Forbid Extra Headers

In some special use cases (probably not very common), you might want to **restrict** the headers that you want to receive.

You can use Pydantic's model configuration to `forbid` any `extra` fields:

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../../docs_src/header_param_models/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/header_param_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/header_param_models/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8"
{!> ../../../docs_src/header_param_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="10"
{!> ../../../docs_src/header_param_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="10"
{!> ../../../docs_src/header_param_models/tutorial002.py!}
```

////

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

# Form Models { #form-models }

You can use **Pydantic models** to declare **form fields** in FastAPI.

/// info

To use forms, first install <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Make sure you create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install it, for example:

```console
$ pip install python-multipart
```

///

/// note

This is supported since FastAPI version `0.113.0`. 🤓

///

## Pydantic Models for Forms { #pydantic-models-for-forms }

You just need to declare a **Pydantic model** with the fields you want to receive as **form fields**, and then declare the parameter as `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py39.py hl[9:11,15] *}

**FastAPI** will **extract** the data for **each field** from the **form data** in the request and give you the Pydantic model you defined.

## Check the Docs { #check-the-docs }

You can verify it in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Forbid Extra Form Fields { #forbid-extra-form-fields }

In some special use cases (probably not very common), you might want to **restrict** the form fields to only those declared in the Pydantic model. And **forbid** any **extra** fields.

/// note

This is supported since FastAPI version `0.114.0`. 🤓

///

You can use Pydantic's model configuration to `forbid` any `extra` fields:

{* ../../docs_src/request_form_models/tutorial002_an_py39.py hl[12] *}

If a client tries to send some extra data, they will receive an **error** response.

For example, if the client tries to send the form fields:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

They will receive an error response telling them that the field `extra` is not allowed:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Summary { #summary }

You can use Pydantic models to declare form fields in FastAPI. 😎

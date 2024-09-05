# Form Models

You can use Pydantic models to declare form fields in FastAPI.

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

## Pydantic Models for Forms

You just need to declare a Pydantic model with the fields you want to receive as form fields, and then declare the parameter as `Form`:

//// tab | Python 3.9+

```Python hl_lines="9-11  15"
{!> ../../../docs_src/request_form_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8-10  14"
{!> ../../../docs_src/request_form_models/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7-9  13"
{!> ../../../docs_src/request_form_models/tutorial001.py!}
```

////

FastAPI will extract the data for each field from the form data in the request and give you the Pydantic model you defined.

## Check the Docs

You can verify it in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

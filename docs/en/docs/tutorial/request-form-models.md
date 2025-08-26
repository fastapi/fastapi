# Form Models

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

## Pydantic Models for Forms

You just need to declare a **Pydantic model** with the fields you want to receive as **form fields**, and then declare the parameter as `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py39.py hl[9:11,15] *}

**FastAPI** will **extract** the data for **each field** from the **form data** in the request and give you the Pydantic model you defined.

## Check the Docs

You can verify it in the docs UI at `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Forbid Extra Form Fields

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

## Default Fields

Form-encoded data has some quirks that can make working with pydantic models counterintuitive.

Say, for example, you were generating an HTML form from a model,
and that model had a boolean field in it that you wanted to display as a checkbox
with a default `True` value:

{* ../../docs_src/request_form_models/tutorial003_an_py39.py hl[11,10:23] *}

This works as expected when the checkbox remains checked,
the form encoded data in the request looks like this:

```formencoded
checkbox=on
```

and the JSON response is also correct:

```json
{"checkbox":true}
```

When the checkbox is *unchecked*, though, something strange happens.
The submitted form data is *empty*,
and the returned JSON data still shows `checkbox` still being `true`!

This is because checkboxes in HTML forms don't work exactly like the boolean inputs we expect,
when a checkbox is checked, if there is no `value` attribute, the value will be `"on"`,
and [the field will be omitted altogether if unchecked](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/checkbox).

When dealing with form models with defaults,
we need to take special care to handle cases where the field being *unset* has a specific meaning.

We also don't want to just treat any time the value is unset as ``False`` -
that would defeat the purpose of the default!
We want to specifically correct the behavior when it is used in the context of a *form.*

In some cases, we can resolve the problem by changing or removing the default,
but we don't always have that option -
particularly when the model is used in other places than the form

The recommended approach is to duplicate your model:

/// note

Take care to ensure that your duplicate models don't diverge,
e.g. if you are using sqlmodel,
where you may end up with `MyModel`, `MyModelCreate`, and `MyModelCreateForm`.

///

{* ../../docs_src/request_form_models/tutorial004_an_py39.py hl[7,13:25] *}

## Summary

You can use Pydantic models to declare form fields in FastAPI. 😎

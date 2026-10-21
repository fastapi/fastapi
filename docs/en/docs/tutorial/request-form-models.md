# Form Models { #form-models }

You can use **Pydantic models** to declare **form fields** in FastAPI.

/// note

To use forms, first install [`python-multipart`](https://github.com/Kludex/python-multipart).

Add it to your project:

```console
$ uv add python-multipart
```

///

/// note

This is supported since FastAPI version `0.113.0`. 🤓

///

## Pydantic Models for Forms { #pydantic-models-for-forms }

You just need to declare a **Pydantic model** with the fields you want to receive as **form fields**, and then declare the parameter as `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** will **extract** the data for **each field** from the **form data** in the request and give you the Pydantic model you defined.

Boolean fields follow the same [omission rules](request-forms.md#boolean-form-fields) as individual form parameters.

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

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

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

## Combine Form Models { #combine-form-models }

You can combine multiple form models with individual `Form` parameters.

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

The client sends `name`, `tags`, and `token` as form fields. Each model receives its own fields and validates them independently.

If multiple declarations use the same form field name, each validates that field's value. Use compatible types and constraints for shared fields so the OpenAPI schema can describe them consistently.

## Optional Form Models { #optional-form-models }

Declare a form model with `| None` and a default of `None` to make the group optional.

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

If neither `name` nor `age` is sent, `profile` is `None`. If either is sent, FastAPI validates the model and requires both fields. An empty submitted value also counts as supplying a field.

Using `| None` without a default still makes the parameter required.

Unknown fields follow the model's `extra` configuration. Ignored extras do not make the model present.

An optional model containing only unchecked checkboxes is omitted. Send a value such as `enabled=false` to supply it explicitly.

## Optional Unions of Form Models { #optional-unions-of-form-models }

For forms declared as a single parameter, you can also use an optional union of models.

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

If no form fields are sent, `contact` is `None`. Send `kind=person` with `name`, or `kind=company` with `company_name`. The discriminator selects which model to validate.

## Form Models and Files { #form-models-and-files }

You can also combine a form model with [file parameters](request-files.md).

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

Here the client sends the `name` field and the `avatar` file using `multipart/form-data`.

## Summary { #summary }

You can use Pydantic models to declare form fields in FastAPI. 😎

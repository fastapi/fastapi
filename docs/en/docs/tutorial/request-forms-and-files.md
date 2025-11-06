# Request Forms and Files { #request-forms-and-files }

You can define files and form fields at the same time using `File` and `Form`.

/// info

To receive uploaded files and/or form data, first install <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Make sure you create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install it, for example:

```console
$ pip install python-multipart
```

///

## Import `File` and `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## Define `File` and `Form` parameters { #define-file-and-form-parameters }

Create file and form parameters the same way you would for `Body` or `Query`:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as `bytes` and some as `UploadFile`.

/// warning

You can declare multiple `File` and `Form` parameters in a *path operation*, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

///

## Recap { #recap }

Use `File` and `Form` together when you need to receive data and files in the same request.

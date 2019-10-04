You can define files and form fields at the same time using `File` and `Form`.

!!! info
    To receive uploaded files and/or form data, first install [`python-multipart`](https://andrew-d.github.io/python-multipart/).

    E.g. `pip install python-multipart`.

## Import `File` and `Form`

```Python hl_lines="1"
{!./src/request_forms_and_files/tutorial001.py!}
```

## Define `File` and `Form` parameters

Create file and form parameters the same way you would for `Body` or `Query`:

```Python hl_lines="8"
{!./src/request_forms_and_files/tutorial001.py!}
```

The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as `bytes` and some as `UploadFile`.

!!! warning
    You can declare multiple `File` and `Form` parameters in a path operation, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

    This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

## Recap

Use `File` and `Form` together when you need to receive data and files in the same request.

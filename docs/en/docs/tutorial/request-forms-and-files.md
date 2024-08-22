# Request Forms and Files

You can define files and form fields at the same time using `File` and `Form`.

/// info

To receive uploaded files and/or form data, first install <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Make sure you create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install it, for example:

```console
$ pip install python-multipart
```

///

## Import `File` and `Form`

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

## Define `File` and `Form` parameters

Create file and form parameters the same way you would for `Body` or `Query`:

//// tab | Python 3.9+

```Python hl_lines="10-12"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="9-11"
{!> ../../../docs_src/request_forms_and_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8"
{!> ../../../docs_src/request_forms_and_files/tutorial001.py!}
```

////

The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as `bytes` and some as `UploadFile`.

/// warning

You can declare multiple `File` and `Form` parameters in a *path operation*, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

///

## Recap

Use `File` and `Form` together when you need to receive data and files in the same request.

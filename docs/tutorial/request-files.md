You can define files to be uploaded by the client using `File`.

## Import `File`

Import `File` from `fastapi`:

```Python hl_lines="1"
{!./tutorial/src/request-files/tutorial001.py!}
```

## Define `File` parameters

Create file parameters the same way you would for `Body` or `Form`:

```Python hl_lines="7"
{!./tutorial/src/request-files/tutorial001.py!}
```

The files will be uploaded as form data and you will receive the contents as `bytes`.

!!! info
    `File` is a class that inherits directly from `Form`.

!!! info
    To declare File bodies, you need to use `File`, because otherwise the parameters would be interpreted as query parameteres or body (JSON) parameters.

## "Form Data"? 

The way HTML forms (`<form></form>`) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

**FastAPI** will make sure to read that data from the right place instead of JSON.

!!! note "Technical Details"
    Data from forms is normally encoded using the "media type" `application/x-www-form-urlencoded` when it doesn't include files.

    But when the form includes files, it is encoded as `multipart/form-data`. If you use `File`, **FastAPI** will know it has to get the files from the correct part of the body.
    
    If you want to read more about these encondings and form fields, head to the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a>.


!!! warning
    You can declare multiple `File` and `Form` parameters in a path operation, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

    This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

## Recap

Use `File` to declare files to be uploaded as input parameters (as form data).

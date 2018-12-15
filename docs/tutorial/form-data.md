When you need to receive form data instead of JSON, you can use `Form`.

## Import Form

Import `Form` from `fastapi`:

```Python hl_lines="1"
{!./tutorial/src/form-data/tutorial001.py!}
```

## Define Form parameters

Create form parameters the same way you would for `Body`:

```Python hl_lines="7"
{!./tutorial/src/form-data/tutorial001.py!}
```

For example, for one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a `username` and `password` fields as form data.

The <abbr title="specification">spec</abbr> requires the fields to be specifically named `username` and `password`, and to be sent as form data, not JSON.

With `Form` you can declare the same metadata and validation as with `Body` (and `Query`, `Path`, `Cookie`).

!!! info
    `Form` is a class that inherits directly from `Body`.

!!! info
    To declare form bodies, you need to use `Form`, because otherwise the parameters would be interpreted as query parameteres or body (JSON) parameters.

## "Form Data"? 

"Form data" is the way HTML forms (`<form></form>`) send the data to the server.

!!! note "Technical Details"
    Data from forms is normally encoded using the "media type" `application/x-www-form-urlencoded`. To read more about it head to the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a>.

## Recap

Use `Form` to declare form data input parameters.

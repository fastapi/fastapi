By default, **FastAPI** will return the responses using `JSONResponse`.

You can override it by returning a `Response` directly as seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}.

But if you return a `Response` directly, the data won't be automatically converted, and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header `Content-Type` as part of the generated OpenAPI).

But you can also declare the `Response` that you want to be used, in the *path operation decorator*.

The contents that you return from your *path operation function* will be put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like is the case with the `JSONResponse` and `UJSONResponse`, the data you return will be automatically converted (and filtered) with any Pydantic `response_model` that you declared in the *path operation decorator*.

!!! note
    If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

## Use `UJSONResponse`

For example, if you are squeezing performance, you can install and use `ujson` and set the response to be `UJSONResponse`.

Import the `Response` class (sub-class) you want to use and declare it in the *path operation decorator*.

```Python hl_lines="2 7"
{!./src/custom_response/tutorial001.py!}
```

!!! info
    The parameter `response_class` will also be used to define the "media type" of the response.

    In this case, the HTTP header `Content-Type` will be set to `application/json`.

    And it will be documented as such in OpenAPI.

## HTML Response

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

* Import `HTMLResponse`.
* Pass `HTMLResponse` as the parameter `content_type` of your *path operation*.

```Python hl_lines="2 7"
{!./src/custom_response/tutorial002.py!}
```

!!! info
    The parameter `response_class` will also be used to define the "media type" of the response.

    In this case, the HTTP header `Content-Type` will be set to `text/html`.

    And it will be documented as such in OpenAPI.

### Return a `Response`

As seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}, you can also override the response directly in your *path operation*, by returning it.

The same example from above, returning an `HTMLResponse`, could look like:

```Python hl_lines="2 7 19"
{!./src/custom_response/tutorial003.py!}
```

!!! warning
    A `Response` returned directly by your *path operation function* won't be documented in OpenAPI (for example, the `Content-Type` won't be documented) and won't be visible in the automatic interactive docs.

!!! info
    Of course, the actual `Content-Type` header, status code, etc, will come from the `Response` object your returned.

### Document in OpenAPI and override `Response`

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the `response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI *path operation*, but your `Response` will be used as is.

#### Return an `HTMLResponse` directly

For example, it could be something like:

```Python hl_lines="7 23 21"
{!./src/custom_response/tutorial004.py!}
```

In this example, the function `generate_html_response()` already generates and returns a `Response` instead of returning the HTML in a `str`.

By returning the result of calling `generate_html_response()`, you are already returning a `Response` that will override the default **FastAPI** behavior.

But as you passed the `HTMLResponse` in the `response_class` too, **FastAPI** will know how to document it in OpenAPI and the interactive docs as HTML with `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Available responses

Here are some of the available responses.

Have in mind that you can use `Response` to return anything else, or even create a custom sub-class.

!!! note "Technical Details"
    You could also use `from starlette.responses import HTMLResponse`.

    **FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

### `Response`

The main `Response` class, all the other responses inherit from it.

You can return it directly.

It accepts the following parameters:

* `content` - A `str` or `bytes`.
* `status_code` - An `int` HTTP status code.
* `headers` - A `dict` of strings.
* `media_type` - A `str` giving the media type. E.g. `"text/html"`.

FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.

```Python hl_lines="1  18"
{!./src/response_directly/tutorial002.py!}
```

### `HTMLResponse`

Takes some text or bytes and returns an HTML response, as you read above.

### `PlainTextResponse`

Takes some text or bytes and returns an plain text response.

```Python hl_lines="2  7  9"
{!./src/custom_response/tutorial005.py!}
```

### `JSONResponse`

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### `UJSONResponse`

An alternative JSON response using `ujson` for faster serialization as you read above.

!!! warning
    `ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.

### `RedirectResponse`

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

```Python hl_lines="2  9"
{!./src/custom_response/tutorial006.py!}
```

### `StreamingResponse`

Takes an async generator or a normal generator/iterator and streams the response body.

```Python hl_lines="2  14"
{!./src/custom_response/tutorial007.py!}
```

#### Using `StreamingResponse` with file-like objects

If you have a file-like object (e.g. the object returned by `open()`), you can return it in a `StreamingResponse`.

This includes many libraries to interact with cloud storage, video processing, and others.

```Python hl_lines="2  10 11"
{!./src/custom_response/tutorial008.py!}
```

!!! tip
    Notice that here as we are using standard `open()` that doesn't support `async` and `await`, we declare the path operation with normal `def`.

### `FileResponse`

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:

* `path` - The filepath to the file to stream.
* `headers` - Any custom headers to include, as a dictionary.
* `media_type` - A string giving the media type. If unset, the filename or path will be used to infer a media type.
* `filename` - If set, this will be included in the response `Content-Disposition`.

File responses will include appropriate `Content-Length`, `Last-Modified` and `ETag` headers.

```Python hl_lines="2  10"
{!./src/custom_response/tutorial009.py!}
```

## Additional documentation

You can also declare the media type and many other details in OpenAPI using `responses`: [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

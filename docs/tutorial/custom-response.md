!!! warning
    This is a rather advanced topic.

    If you are starting with **FastAPI**, you might not need this.

By default, **FastAPI** will return the responses using Starlette's `JSONResponse`.

You can override it by returning a `Response` directly, <a href="https://fastapi.tiangolo.com/tutorial/response-directly/" target="_blank">as seen in a previous section</a>.

But if you return a `Response` directly, the data won't be automatically converted, and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header `Content-Type`).

But you can also declare the `Response` that you want to be used, in the *path operation decorator*.

The contents that you return from your *path operation function* will be put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like is the case with the `JSONResponse` and `UJSONResponse`, the data you return will be automatically converted (and filtered) with any Pydantic `response_model` that you declared in the *path operation decorator*.

!!! note
    If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

## Use `UJSONResponse`

For example, if you are squeezing performance, you can install and use `ujson` and set the response to be Starlette's `UJSONResponse`.

Import the `Response` class (sub-class) you want to use and declare it in the *path operation decorator*.

```Python hl_lines="2 7"
{!./src/custom_response/tutorial001.py!}
```

!!! note
    Notice that you import it directly from `starlette.responses`, not from `fastapi`.

!!! info
    The parameter `response_class` will also be used to define the "media type" of the response.

    In this case, the HTTP header `Content-Type` will be set to `application/json`.

    And it will be documented as such in OpenAPI.

## HTML Response

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

* Import `HTMLResponse`.
* Pass `HTMLResponse` as the parameter `content_type` of your path operation.

```Python hl_lines="2 7"
{!./src/custom_response/tutorial002.py!}
```

!!! note
    Notice that you import it directly from `starlette.responses`, not from `fastapi`.

!!! info
    The parameter `response_class` will also be used to define the "media type" of the response.

    In this case, the HTTP header `Content-Type` will be set to `text/html`.

    And it will be documented as such in OpenAPI.

### Return a Starlette `Response`

As seen in <a href="https://fastapi.tiangolo.com/tutorial/response-directly/" target="_blank">another section</a>, you can also override the response directly in your path operation, by returning it.

The same example from above, returning an `HTMLResponse`, could look like:

```Python hl_lines="2 7 19"
{!./src/custom_response/tutorial003.py!}
```

!!! warning
    A `Response` returned directly by your path operation function won't be documented in OpenAPI (for example, the `Content-Type` won't be documented) and won't be visible in the automatic interactive docs.

!!! info
    Of course, the actual `Content-Type` header, status code, etc, will come from the `Response` object your returned.

### Document in OpenAPI and override `Response`

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the `response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI path operation, but your `Response` will be used as is.

#### Return an `HTMLResponse` directly

For example, it could be something like:

```Python hl_lines="7 23 21"
{!./src/custom_response/tutorial004.py!}
```

In this example, the function `generate_html_response()` already generates a Starlette `Response` instead of the HTML in a `str`.

By returning the result of calling `generate_html_response()`, you are already returning a `Response` that will override the default **FastAPI** behavior.

But as you passed the `HTMLResponse` in the `response_class`, **FastAPI** will know how to document it in OpenAPI and the interactive docs as HTML with `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Additional documentation

You can also declare the media type and many other details in OpenAPI using `responses`: <a href="https://fastapi.tiangolo.com/tutorial/additional-responses/" target="_blank">Additional Responses in OpenAPI</a>.

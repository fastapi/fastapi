!!! warning
    This is a rather advanced topic.
    
    If you are starting with **FastAPI**, you might not need this.

By default, **FastAPI** will return the responses using Starlette's `JSONResponse`.

But you can override it.

## Use `UJSONResponse`

For example, if you are squeezing performance, you can use `ujson` and set the response to be Starlette's `UJSONResponse`.

### Import `UJSONResponse`

```Python hl_lines="1"
{!./tutorial/src/custom_response/tutorial001.py!}
```

!!! note
    Notice that you import it directly from `starlette.responses`, not from `fastapi`.

### Make your path operation use it

Make your path operation use `UJSONResponse` as the response class using the parameter `content_type`:

```Python hl_lines="8"
{!./tutorial/src/custom_response/tutorial001.py!}
```

!!! info
    The parameter is called `content_type` because it will also be used to define the "media type" of the response.

    And will be documented as such in OpenAPI.

## HTML Response

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

### Import `HTMLResponse`

```Python hl_lines="1"
{!./tutorial/src/custom_response/tutorial002.py!}
```

!!! note
    Notice that you import it directly from `starlette.responses`, not from `fastapi`.


### Define your `content_type` class

Pass `HTMLResponse` as the parameter `content_type` of your path operation:

```Python hl_lines="8"
{!./tutorial/src/custom_response/tutorial002.py!}
```

!!! info
    The parameter is called `content_type` because it will also be used to define the "media type" of the response.

    In this case, the HTTP header `Content-Type` will be set to `text/html`.

    And it will be documented as such in OpenAPI.


### return a Starlette `Response`

You can also override the response directly in your path operation.

If you return an object that is an instance of Starlette's `Response`, it will be used as the response directly.

The same example from above, returning an `HTMLResponse`, could look like:

```Python hl_lines="8 20"
{!./tutorial/src/custom_response/tutorial003.py!}
```

!!! info
    Of course, the `Content-Type` header will come from the the `Response` object your returned.

!!! warning
    A `Response` returned directly by your path operation function won't be documented in OpenAPI and won't be visible in the automatic interactive docs.


### Document in OpenAPI and override `Response`

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the `content_type` parameter AND return a `Response` object.

The `content_type` class will then be used only to document the OpenAPI path operation, but your `Response` will be used as is.

#### Return an `HTMLResponse` directly

For example, it could be something like:

```Python hl_lines="8 19 22"
{!./tutorial/src/custom_response/tutorial004.py!}
```

In this example, the function `generate_html_response()` already generates a Starlette `Response` instead of the HTML in a `str`.

By returning the result of calling `generate_html_response()`, you are already returning a `Response` that will override the default **FastAPI** behavior.

#### Declare `HTMLResponse` as `content_type`

But by declaring it also in the path operation decorator:

```Python hl_lines="22"
{!./tutorial/src/custom_response/tutorial004.py!}
```

#### OpenAPI knows how to document it

...**FastAPI** will be able to document it in OpenAPI and in the interactive docs as HTML with `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

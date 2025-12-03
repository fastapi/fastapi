# Custom Response - HTML, Stream, File, others { #custom-response-html-stream-file-others }

By default, **FastAPI** will return the responses using `JSONResponse`.

You can override it by returning a `Response` directly as seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}.

But if you return a `Response` directly (or any subclass, like `JSONResponse`), the data won't be automatically converted (even if you declare a `response_model`), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header `Content-Type` as part of the generated OpenAPI).

But you can also declare the `Response` that you want to be used (e.g. any `Response` subclass), in the *path operation decorator* using the `response_class` parameter.

The contents that you return from your *path operation function* will be put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like is the case with the `JSONResponse` and `UJSONResponse`, the data you return will be automatically converted (and filtered) with any Pydantic `response_model` that you declared in the *path operation decorator*.

/// note

If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

///

## Use `ORJSONResponse` { #use-orjsonresponse }

For example, if you are squeezing performance, you can install and use <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> and set the response to be `ORJSONResponse`.

Import the `Response` class (sub-class) you want to use and declare it in the *path operation decorator*.

For large responses, returning a `Response` directly is much faster than returning a dictionary.

This is because by default, FastAPI will inspect every item inside and make sure it is serializable as JSON, using the same [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} explained in the tutorial. This is what allows you to return **arbitrary objects**, for example database models.

But if you are certain that the content that you are returning is **serializable with JSON**, you can pass it directly to the response class and avoid the extra overhead that FastAPI would have by passing your return content through the `jsonable_encoder` before passing it to the response class.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info

The parameter `response_class` will also be used to define the "media type" of the response.

In this case, the HTTP header `Content-Type` will be set to `application/json`.

And it will be documented as such in OpenAPI.

///

/// tip

The `ORJSONResponse` is only available in FastAPI, not in Starlette.

///

## HTML Response { #html-response }

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

* Import `HTMLResponse`.
* Pass `HTMLResponse` as the parameter `response_class` of your *path operation decorator*.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info

The parameter `response_class` will also be used to define the "media type" of the response.

In this case, the HTTP header `Content-Type` will be set to `text/html`.

And it will be documented as such in OpenAPI.

///

### Return a `Response` { #return-a-response }

As seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}, you can also override the response directly in your *path operation*, by returning it.

The same example from above, returning an `HTMLResponse`, could look like:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

/// warning

A `Response` returned directly by your *path operation function* won't be documented in OpenAPI (for example, the `Content-Type` won't be documented) and won't be visible in the automatic interactive docs.

///

/// info

Of course, the actual `Content-Type` header, status code, etc, will come from the `Response` object you returned.

///

### Document in OpenAPI and override `Response` { #document-in-openapi-and-override-response }

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the `response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI *path operation*, but your `Response` will be used as is.

#### Return an `HTMLResponse` directly { #return-an-htmlresponse-directly }

For example, it could be something like:

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

In this example, the function `generate_html_response()` already generates and returns a `Response` instead of returning the HTML in a `str`.

By returning the result of calling `generate_html_response()`, you are already returning a `Response` that will override the default **FastAPI** behavior.

But as you passed the `HTMLResponse` in the `response_class` too, **FastAPI** will know how to document it in OpenAPI and the interactive docs as HTML with `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Available responses { #available-responses }

Here are some of the available responses.

Keep in mind that you can use `Response` to return anything else, or even create a custom sub-class.

/// note | Technical Details

You could also use `from starlette.responses import HTMLResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

///

### `Response` { #response }

The main `Response` class, all the other responses inherit from it.

You can return it directly.

It accepts the following parameters:

* `content` - A `str` or `bytes`.
* `status_code` - An `int` HTTP status code.
* `headers` - A `dict` of strings.
* `media_type` - A `str` giving the media type. E.g. `"text/html"`.

FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the `media_type` and appending a charset for text types.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Takes some text or bytes and returns an HTML response, as you read above.

### `PlainTextResponse` { #plaintextresponse }

Takes some text or bytes and returns a plain text response.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### `ORJSONResponse` { #orjsonresponse }

A fast alternative JSON response using <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, as you read above.

/// info

This requires installing `orjson` for example with `pip install orjson`.

///

### `UJSONResponse` { #ujsonresponse }

An alternative JSON response using <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// info

This requires installing `ujson` for example with `pip install ujson`.

///

/// warning

`ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip

It's possible that `ORJSONResponse` might be a faster alternative.

///

### `RedirectResponse` { #redirectresponse }

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

You can return a `RedirectResponse` directly:

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

Or you can use it in the `response_class` parameter:


{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

If you do that, then you can return the URL directly from your *path operation* function.

In this case, the `status_code` used will be the default one for the `RedirectResponse`, which is `307`.

---

You can also use the `status_code` parameter combined with the `response_class` parameter:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Takes an async generator or a normal generator/iterator and streams the response body.

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### Using `StreamingResponse` with file-like objects { #using-streamingresponse-with-file-like-objects }

If you have a <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> object (e.g. the object returned by `open()`), you can create a generator function to iterate over that file-like object.

That way, you don't have to read it all first in memory, and you can pass that generator function to the `StreamingResponse`, and return it.

This includes many libraries to interact with cloud storage, video processing, and others.

{* ../../docs_src/custom_response/tutorial008.py hl[2,10:12,14] *}

1. This is the generator function. It's a "generator function" because it contains `yield` statements inside.
2. By using a `with` block, we make sure that the file-like object is closed after the generator function is done. So, after it finishes sending the response.
3. This `yield from` tells the function to iterate over that thing named `file_like`. And then, for each part iterated, yield that part as coming from this generator function (`iterfile`).

    So, it is a generator function that transfers the "generating" work to something else internally.

    By doing it this way, we can put it in a `with` block, and that way, ensure that the file-like object is closed after finishing.

/// tip

Notice that here as we are using standard `open()` that doesn't support `async` and `await`, we declare the path operation with normal `def`.

///

### `FileResponse` { #fileresponse }

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:

* `path` - The file path to the file to stream.
* `headers` - Any custom headers to include, as a dictionary.
* `media_type` - A string giving the media type. If unset, the filename or path will be used to infer a media type.
* `filename` - If set, this will be included in the response `Content-Disposition`.

File responses will include appropriate `Content-Length`, `Last-Modified` and `ETag` headers.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

You can also use the `response_class` parameter:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

In this case, you can return the file path directly from your *path operation* function.

## Custom response class { #custom-response-class }

You can create your own custom response class, inheriting from `Response` and using it.

For example, let's say that you want to use <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, but with some custom settings not used in the included `ORJSONResponse` class.

Let's say you want it to return indented and formatted JSON, so you want to use the orjson option `orjson.OPT_INDENT_2`.

You could create a `CustomORJSONResponse`. The main thing you have to do is create a `Response.render(content)` method that returns the content as `bytes`:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

Now instead of returning:

```json
{"message": "Hello World"}
```

...this response will return:

```json
{
  "message": "Hello World"
}
```

Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉

## Default response class { #default-response-class }

When creating a **FastAPI** class instance or an `APIRouter` you can specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In the example below, **FastAPI** will use `ORJSONResponse` by default, in all *path operations*, instead of `JSONResponse`.

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip

You can still override `response_class` in *path operations* as before.

///

## Additional documentation { #additional-documentation }

You can also declare the media type and many other details in OpenAPI using `responses`: [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

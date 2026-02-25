# Custom Response - HTML, Stream, File, others { #custom-response-html-stream-file-others }

By default, **FastAPI** will return JSON responses.

You can override it by returning a `Response` directly as seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}.

But if you return a `Response` directly (or any subclass, like `JSONResponse`), the data won't be automatically converted (even if you declare a `response_model`), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header `Content-Type` as part of the generated OpenAPI).

But you can also declare the `Response` that you want to be used (e.g. any `Response` subclass), in the *path operation decorator* using the `response_class` parameter.

The contents that you return from your *path operation function* will be put inside of that `Response`.

/// note

If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

///

## JSON Responses { #json-responses }

By default FastAPI returns JSON responses.

If you declare a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} FastAPI will use it to serialize the data to JSON, using Pydantic.

If you don't declare a response model, FastAPI will use the `jsonable_encoder` explained in [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} and put it in a `JSONResponse`.

If you declare a `response_class` with a JSON media type (`application/json`), like is the case with the `JSONResponse`, the data you return will be automatically converted (and filtered) with any Pydantic `response_model` that you declared in the *path operation decorator*. But the data won't be serialized to JSON bytes with Pydantic, instead it will be converted with the `jsonable_encoder` and then passed to the `JSONResponse` class, which will serialize it to bytes using the standard JSON library in Python.

### JSON Performance { #json-performance }

In short, if you want the maximum performance, use a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} and don't declare a `response_class` in the *path operation decorator*.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML Response { #html-response }

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

* Import `HTMLResponse`.
* Pass `HTMLResponse` as the parameter `response_class` of your *path operation decorator*.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info

The parameter `response_class` will also be used to define the "media type" of the response.

In this case, the HTTP header `Content-Type` will be set to `text/html`.

And it will be documented as such in OpenAPI.

///

### Return a `Response` { #return-a-response }

As seen in [Return a Response directly](response-directly.md){.internal-link target=_blank}, you can also override the response directly in your *path operation*, by returning it.

The same example from above, returning an `HTMLResponse`, could look like:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

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

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

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

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Takes some text or bytes and returns an HTML response, as you read above.

### `PlainTextResponse` { #plaintextresponse }

Takes some text or bytes and returns a plain text response.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### `RedirectResponse` { #redirectresponse }

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

You can return a `RedirectResponse` directly:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Or you can use it in the `response_class` parameter:


{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

If you do that, then you can return the URL directly from your *path operation* function.

In this case, the `status_code` used will be the default one for the `RedirectResponse`, which is `307`.

---

You can also use the `status_code` parameter combined with the `response_class` parameter:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Takes an async generator or a normal generator/iterator and streams the response body.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[2,14] *}

#### Using `StreamingResponse` with file-like objects { #using-streamingresponse-with-file-like-objects }

If you have a <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> object (e.g. the object returned by `open()`), you can create a generator function to iterate over that file-like object.

That way, you don't have to read it all first in memory, and you can pass that generator function to the `StreamingResponse`, and return it.

This includes many libraries to interact with cloud storage, video processing, and others.

{* ../../docs_src/custom_response/tutorial008_py310.py hl[2,10:12,14] *}

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

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

You can also use the `response_class` parameter:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

In this case, you can return the file path directly from your *path operation* function.

## Custom response class { #custom-response-class }

You can create your own custom response class, inheriting from `Response` and using it.

For example, let's say that you want to use <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> with some settings.

Let's say you want it to return indented and formatted JSON, so you want to use the orjson option `orjson.OPT_INDENT_2`.

You could create a `CustomORJSONResponse`. The main thing you have to do is create a `Response.render(content)` method that returns the content as `bytes`:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

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

### `orjson` or Response Model { #orjson-or-response-model }

If what you are looking for is performance, you are probably better off using a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} than an `orjson` response.

With a response model, FastAPI will use Pydantic to serialize the data to JSON, without using intermediate steps, like converting it with `jsonable_encoder`, which would happen in any other case.

And under the hood, Pydantic uses the same underlying Rust mechanisms as `orjson` to serialize to JSON, so you will already get the best performance with a response model.

## Default response class { #default-response-class }

When creating a **FastAPI** class instance or an `APIRouter` you can specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In the example below, **FastAPI** will use `HTMLResponse` by default, in all *path operations*, instead of JSON.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip

You can still override `response_class` in *path operations* as before.

///

## Additional documentation { #additional-documentation }

You can also declare the media type and many other details in OpenAPI using `responses`: [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

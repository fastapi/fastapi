# 自定义响应 - HTML, Stream, File, 其他

默认情况下， **FastAPI** 会用 `JSONResponse` 来返回响应。

你可以直接返回`Response`覆盖它，参考[Return a Response directly](response-directly.md){.internal-link target=_blank}

但是如果你直接返回`Response`，数据不会被自动转换，文档也没法自动生成（例如，将在 HTTP 头部`Content-Type`中包含的特定“媒体类型”作为生成的 OpenAPI 的一部分）。

不过你仍可以在 *路径操作装饰器* 里声明你想要用的`Response`。

在 *路径操作函数* 里返回的内容会被放到这个`Response`里。

如果这个`Response`有 JSON 媒体类型，就像`JSONResponse`和`UJSONResponse`，返回的数据会根据你在 *路径操作装饰器* 里定义的 Pydantic 模型`response_model`自动转换（和过滤）。

!!! note
	如果你用一个没有媒体类型的 response 类，FastAPI 会认为你的响应没有内容，所以也不会将响应结构包含到生成的 OpenAPI 文档中。


## 使用 `ORJSONResponse`

举个例子，如果你想追求性能，你可以安装使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> 然后把 response 设置成`ORJSONResponse`。

引入你想用的`Response`类（子类），然后在 *路径操作装饰器* 里声明它。

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial001b.py!}
```

!!! info
    参数`response_class`也被用来定义响应的"媒体类型"。

	在这个例子里，HTTP 头部 `Content-Type` 会被设置为 `application/json`。

	它可以被 OpenAPI 文档化。

!!! tip
    `ORJSONResponse` 目前只在 FastAPI 里，不在 Starlette 里。

## HTML 响应

要从 **FastAPI** 直接返回 HTML 响应， 用 `HTMLResponse`.

* 引入 `HTMLResponse` 。
* 将 `HTMLResponse` 作为参数传入 *路径操作* 的 `content_type`。

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial002.py!}
```

!!! info
    参数`response_class`也被用来定义响应的"媒体类型"。

	在这个例子里，HTTP 头部 `Content-Type` 会被设置为 `text/html`。

	它可以被 OpenAPI 文档化。

### 返回 `Response`

正如 [Return a Response directly](response-directly.md){.internal-link target=_blank} 所见，你也可以通过直接返回响应来覆盖 *路径操作*的响应。

一个和上面类似的例子，返回 `HTMLResponse`， 可以这样写：

```Python hl_lines="2 7 19"
{!../../../docs_src/custom_response/tutorial003.py!}
```

!!! warning
	在 *路径操作* 里直接返回的 `Response`不会被 OpenAPI 文档化（例如，`Content-Type` 不会被记录），而且在自动交互文档里也不可见。

!!! info
	当然，实际的 `Content-Type` 头部，状态码等等，都会来自你返回的 `Response` 对象。

### 在 OpenAPI 中文档化，同时覆盖 `Response` 

如果想在函数内部覆盖响应，同时又想在 OpenAPI 中文档化 "媒体类型"，你可以使用 `response_class` 参数并返回 `Response` 对象。

`response_class` 只会用来文档化 OpenAPI *路径操作*，你返回的 `Response` 仍按原样使用。

#### 直接返回 `HTMLResponse`

例如，可以这样写：

```Python hl_lines="7 23 21"
{!../../../docs_src/custom_response/tutorial004.py!}
```

在这个例子里，函数 `generate_html_response()` 已经生成并返回 `Response` 来代替返回在 `str` 里的HTML。

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
{!../../../docs_src/response_directly/tutorial002.py!}
```

### `HTMLResponse`

Takes some text or bytes and returns an HTML response, as you read above.

### `PlainTextResponse`

Takes some text or bytes and returns an plain text response.

```Python hl_lines="2  7  9"
{!../../../docs_src/custom_response/tutorial005.py!}
```

### `JSONResponse`

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### `ORJSONResponse`

A fast alternative JSON response using <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, as you read above.

### `UJSONResponse`

An alternative JSON response using <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

!!! warning
    `ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial001.py!}
```

!!! tip
    It's possible that `ORJSONResponse` might be a faster alternative.

### `RedirectResponse`

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

```Python hl_lines="2  9"
{!../../../docs_src/custom_response/tutorial006.py!}
```

### `StreamingResponse`

Takes an async generator or a normal generator/iterator and streams the response body.

```Python hl_lines="2  14"
{!../../../docs_src/custom_response/tutorial007.py!}
```

#### Using `StreamingResponse` with file-like objects

If you have a file-like object (e.g. the object returned by `open()`), you can return it in a `StreamingResponse`.

This includes many libraries to interact with cloud storage, video processing, and others.

```Python hl_lines="2  10 11"
{!../../../docs_src/custom_response/tutorial008.py!}
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
{!../../../docs_src/custom_response/tutorial009.py!}
```

## Default response class

When creating a **FastAPI** class instance or an `APIRouter` you can specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In the example below, **FastAPI** will use `ORJSONResponse` by default, in all *path operations*, instead of `JSONResponse`.

```Python hl_lines="2 4"
{!../../../docs_src/custom_response/tutorial010.py!}
```

!!! tip
    You can still override `response_class` in *path operations* as before.

## Additional documentation

You can also declare the media type and many other details in OpenAPI using `responses`: [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

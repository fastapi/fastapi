# 自定义响应 - HTML，Stream，File 或其他

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

在这个例子里，函数 `generate_html_response()` 已经生成并返回 `Response` 来代替返回在 `str` 内的HTML。

通过调用 `generate_html_response` 返回的结果，就是已经是一个 `Response`了，它会覆盖 **FastAPI** 的默认行为。

不过当你在 `response_class` 也传了 `HTMLResponse`时，**FastAPI** 会知道怎么在 OpenAPI 及交互式文档里将 HTML 以 `text/html` 文档化。

<img src="/img/tutorial/custom-response/image01.png">

## 可用响应类型 

下面是一些可用的响应类型。

记住，你可以用 `Response` 来返回任何东西，或甚至创建一个自定义的子类。

!!! note “技术细节” 
	你也可以用 `from starlette.responses import JSONResponse`。

    **FastAPI** 提供了和 `starlette.responses` 一样的 `fastapi.responses`，主要是为了方便开发者。不过大多数的可用响应类型都是直接从 Starlette 里来的，`status` 也一样。

### `Response`

`Response` 基类， 所有其他的响应类都继承自它。

你可以直接返回它。

它接受以下参数：

* `content` - `str` 或 `bytes`。
* `status_code` - `int` HTTP 状态码。
* `headers` - `dict` 字符串。
* `media_type` - `str` 媒体类型， 比如 `"text/html"`。

FastAPI (实际是 Starlette) 会自动包含一个 Content-Length 响应头，还会包含一个基于媒体类型的 Content-Type 响应头，并为文本类型附加字符集。

```Python hl_lines="1  18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

### `HTMLResponse`

接收一些文本或字节并返回 HTML 响应，如上所述。

### `PlainTextResponse`

接收一些文本或字节并返回一个纯文本响应。

```Python hl_lines="2  7  9"
{!../../../docs_src/custom_response/tutorial005.py!}
```

### `JSONResponse`

接收一些数据并返回 `application/json` 编码的响应。

这是 **FastAPI** 默认使用的，如上所述。

### `ORJSONResponse`

一个快速的 JSON 响应替代方案，用的是<a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>，如上所述。

### `UJSONResponse`

一个 JSON 响应替代方案，用的是<a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>。


!!! warning
	在处理某些边界情况时，`ujson` 没有 Python 的内置实现那么谨慎。

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial001.py!}
```

!!! tip
    `ORJSONResponse` 可能是个比较快的方案。

### `RedirectResponse`

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.
返回 HTTP 重定向。默认会用 307 状态码（临时性重定向）。

```Python hl_lines="2  9"
{!../../../docs_src/custom_response/tutorial006.py!}
```

### `StreamingResponse`

Takes an async generator or a normal generator/iterator and streams the response body.
接收异步生成器或者普通生成器/迭代器并流式输出响应体。

```Python hl_lines="2  14"
{!../../../docs_src/custom_response/tutorial007.py!}
```

#### `StreamingResponse` 和类文件（file-like）对象一起使用

如果是类文件对象（比如说 `open()` 返回的对象），你可以在 `StreamingResponse` 里返回它。

这包括很多和云存储，视频处理等交互的库。

```Python hl_lines="2  10 11"
{!../../../docs_src/custom_response/tutorial008.py!}
```

!!! tip
	注意，由于这里用的标准 `open()` 不支持 `async` 和 `await`，所以我们用普通的 `def` 定义路径操作。

### `FileResponse`

异步流式输出文件作为响应。

相比其他响应类型，它接受不同的参数集来初始化。

* `path` - 要流式输出的文件的路径。
* `headers` - 任何要包含的自定义头部，字典形式。
* `media_type` - 提供媒体类型的字符串。如果不设置，会用文件名或者路径来推断媒体类型。
* `filename` - 如果设置了，会被包含在响应的 `Content-Disposition` 里。

文件响应会包含正确的 `Content-Length`，`Last-Modified` 和 `ETag` 头部。 

```Python hl_lines="2  10"
{!../../../docs_src/custom_response/tutorial009.py!}
```

## 默认响应类

在创建 **FastAPI** 类实例或 **APIRouter** 时，可以指定默认使用哪个响应类。

定义它的参数是 `default_response_class`。

在下面的例子里， **FastAPI** 会用 `ORJSONResponse` 作为默认类，在所有 *路径操作* 里代替 `JSONResponse`。

```Python hl_lines="2 4"
{!../../../docs_src/custom_response/tutorial010.py!}
```

!!! tip
	你仍可以像之前一样在 *路径操作* 里用 `response_class` 重写。

## 附加文档

你也可以用 `responses` 来定义 OpenAPI 里的媒体类型等其他细节：[Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}。

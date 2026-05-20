# 自定义响应 - HTML、流、文件等 { #custom-response-html-stream-file-others }

默认情况下，**FastAPI** 会返回 JSON 响应。

你可以像在 [直接返回响应](response-directly.md) 中那样，直接返回 `Response` 来重载它。

但如果你直接返回一个 `Response`（或其任意子类，比如 `JSONResponse`），返回的数据不会自动转换（即使你声明了 `response_model`），也不会自动生成文档（例如，在生成的 OpenAPI 中，HTTP 头 `Content-Type` 里的特定「媒体类型」不会被包含）。

你还可以在 *路径操作装饰器* 中通过 `response_class` 参数声明要使用的 `Response`（例如任意 `Response` 子类）。

你从 *路径操作函数* 中返回的内容将被放在该 `Response` 中。

/// note | 注意

如果你使用不带有媒体类型的响应类，FastAPI 会认为你的响应没有任何内容，所以不会在生成的 OpenAPI 文档中记录响应格式。

///

## JSON 响应 { #json-responses }

默认情况下 FastAPI 返回 JSON 响应。

如果你声明了一个[响应模型](../tutorial/response-model.md)，FastAPI 会使用 Pydantic 将数据序列化为 JSON。

如果你没有声明响应模型，FastAPI 会使用 [JSON 兼容编码器](../tutorial/encoder.md) 中解释的 `jsonable_encoder`，并把结果放进一个 `JSONResponse`。

如果你在 `response_class` 中声明了一个 JSON 媒体类型（`application/json`）的类（比如 `JSONResponse`），你返回的数据会使用你在 *路径操作装饰器* 中声明的任意 Pydantic `response_model` 自动转换（和过滤）。但数据不会由 Pydantic 序列化为 JSON 字节；而是先用 `jsonable_encoder` 转换后传给 `JSONResponse`，由它使用 Python 标准 JSON 库序列化为字节。

### JSON 性能 { #json-performance }

简而言之，如果你想要获得最大性能，请使用[响应模型](../tutorial/response-model.md)，并且不要在 *路径操作装饰器* 中声明 `response_class`。

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML 响应 { #html-response }

使用 `HTMLResponse` 来从 **FastAPI** 中直接返回一个 HTML 响应。

* 导入 `HTMLResponse`。
* 将 `HTMLResponse` 作为你的 *路径操作* 的 `response_class` 参数传入。

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | 信息

参数 `response_class` 也会用来定义响应的「媒体类型」。

在这个例子中，HTTP 头的 `Content-Type` 会被设置成 `text/html`。

并且在 OpenAPI 文档中也会这样记录。

///

### 返回一个 `Response` { #return-a-response }

正如你在 [直接返回响应](response-directly.md) 中了解到的，你也可以通过直接返回响应在 *路径操作* 中直接重载响应。

和上面一样的例子，返回一个 `HTMLResponse` 看起来可能是这样：

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | 警告

*路径操作函数* 直接返回的 `Response` 不会被 OpenAPI 的文档记录（比如，`Content-Type` 不会被文档记录），并且在自动化交互文档中也是不可见的。

///

/// info | 信息

当然，实际的 `Content-Type` 头、状态码等等，将来自于你返回的 `Response` 对象。

///

### 在 OpenAPI 中文档化并重载 `Response` { #document-in-openapi-and-override-response }

如果你想要在函数内重载响应，但是同时在 OpenAPI 中文档化「媒体类型」，你可以使用 `response_class` 参数并返回一个 `Response` 对象。

接着 `response_class` 参数只会被用来文档化 OpenAPI 的 *路径操作*，你的 `Response` 用来返回响应。

#### 直接返回 `HTMLResponse` { #return-an-htmlresponse-directly }

比如像这样：

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

在这个例子中，函数 `generate_html_response()` 已经生成并返回 `Response` 对象而不是在 `str` 中返回 HTML。

通过返回函数 `generate_html_response()` 的调用结果，你已经返回一个重载 **FastAPI** 默认行为的 `Response` 对象。

但如果你在 `response_class` 中也传入了 `HTMLResponse`，**FastAPI** 会知道如何在 OpenAPI 和交互式文档中使用 `text/html` 将其文档化为 HTML：

<img src="/img/tutorial/custom-response/image01.png">

## 可用响应 { #available-responses }

这里有一些可用的响应。

要记得你可以使用 `Response` 来返回任何其他东西，甚至创建一个自定义的子类。

/// note | 技术细节

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 提供了同 `fastapi.responses` 相同的 `starlette.responses` 只是为了方便开发者。但大多数可用的响应都直接来自 Starlette。

///

### `Response` { #response }

其他全部的响应都继承自主类 `Response`。

你可以直接返回它。

`Response` 类接受如下参数：

* `content` - 一个 `str` 或者 `bytes`。
* `status_code` - 一个 `int` 类型的 HTTP 状态码。
* `headers` - 一个由字符串组成的 `dict`。
* `media_type` - 一个给出媒体类型的 `str`，比如 `"text/html"`。

FastAPI（实际上是 Starlette）将自动包含 Content-Length 的头。它还将包含一个基于 `media_type` 的 Content-Type 头，并为文本类型附加一个字符集。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

如上文所述，接受文本或字节并返回 HTML 响应。

### `PlainTextResponse` { #plaintextresponse }

接受文本或字节并返回纯文本响应。

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

接受数据并返回一个 `application/json` 编码的响应。

如上文所述，这是 **FastAPI** 中使用的默认响应。

/// note | 技术细节

但如果你声明了响应模型或返回类型，将直接使用它来把数据序列化为 JSON，并直接返回一个具备正确 JSON 媒体类型的响应，而不会使用 `JSONResponse` 类。

这是获得最佳性能的理想方式。

///

### `RedirectResponse` { #redirectresponse }

返回 HTTP 重定向。默认情况下使用 307 状态码（临时重定向）。

你可以直接返回一个 `RedirectResponse`：

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

或者你可以把它用于 `response_class` 参数：

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

如果你这么做，那么你可以在 *路径操作* 函数中直接返回 URL。

在这种情况下，将使用 `RedirectResponse` 的默认 `status_code`，即 `307`。

---

你也可以将 `status_code` 参数和 `response_class` 参数结合使用：

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

采用异步生成器或普通生成器/迭代器（带有 `yield` 的函数），然后流式传输响应主体。

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | 技术细节

一个 `async` 任务只有在到达 `await` 时才能被取消。如果没有 `await`，生成器（带有 `yield` 的函数）无法被正确取消，即使已请求取消也可能继续运行。

由于这个小示例不需要任何 `await` 语句，我们添加 `await anyio.sleep(0)`，给事件循环一个处理取消的机会。

对于大型或无限流，这一点更为重要。

///

/// tip | 提示

与其直接返回 `StreamingResponse`，更推荐遵循 [流式数据](./stream-data.md) 的写法，它更方便并在幕后为你处理取消。

如果你在流式传输 JSON Lines，请参阅教程：[流式传输 JSON Lines](../tutorial/stream-json-lines.md)。

///

### `FileResponse` { #fileresponse }

异步传输文件作为响应。

与其他响应类型相比，接受不同的参数集进行实例化：

* `path` - 要流式传输的文件的文件路径。
* `headers` - 任何自定义响应头，传入字典类型。
* `media_type` - 给出媒体类型的字符串。如果未设置，则文件名或路径将用于推断媒体类型。
* `filename` - 如果给出，它将包含在响应的 `Content-Disposition` 中。

文件响应将包含适当的 `Content-Length`、`Last-Modified` 和 `ETag` 响应头。

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

你也可以使用 `response_class` 参数：

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

在这种情况下，你可以在 *路径操作* 函数中直接返回文件路径。

## 自定义响应类 { #custom-response-class }

你可以创建你自己的自定义响应类，继承自 `Response` 并使用它。

例如，假设你想用一些设置来使用 [`orjson`](https://github.com/ijl/orjson)。

假设你想让它返回带缩进、格式化的 JSON，因此你想使用 orjson 选项 `orjson.OPT_INDENT_2`。

你可以创建一个 `CustomORJSONResponse`。你需要做的主要事情是实现一个 `Response.render(content)` 方法，并返回 `bytes`：

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

现在，不再是返回：

```json
{"message": "Hello World"}
```

...这个响应将返回：

```json
{
  "message": "Hello World"
}
```

当然，你很可能会找到比格式化 JSON 更好的方式来利用这一点。😉

### `orjson` 或响应模型 { #orjson-or-response-model }

如果你追求的是性能，使用[响应模型](../tutorial/response-model.md) 往往比返回 `orjson` 响应更好。

使用响应模型时，FastAPI 会使用 Pydantic 直接把数据序列化为 JSON，不需要诸如通过 `jsonable_encoder` 转换这样的中间步骤（其他情况下会发生）。

并且在底层，Pydantic 使用与 `orjson` 相同的 Rust 机制来序列化 JSON，所以使用响应模型你已经可以获得最佳性能。

## 默认响应类 { #default-response-class }

在创建 **FastAPI** 类实例或 `APIRouter` 时，你可以指定默认要使用的响应类。

用于定义它的参数是 `default_response_class`。

在下面的示例中，**FastAPI** 会在所有 *路径操作* 中默认使用 `HTMLResponse`，而不是 JSON。

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | 提示

你仍然可以像之前一样在 *路径操作* 中重载 `response_class`。

///

## 额外文档 { #additional-documentation }

你还可以使用 `responses` 在 OpenAPI 中声明媒体类型和许多其他详细信息：[OpenAPI 中的额外响应](additional-responses.md)。

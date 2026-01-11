# 自定义响应 - HTML，流，文件和其他 { #custom-response-html-stream-file-others }

默认情况下，**FastAPI** 会使用 `JSONResponse` 返回响应。

你可以通过直接返回 `Response` 来重载它，参见 [直接返回响应](response-directly.md){.internal-link target=_blank}。

但是，如果你直接返回 `Response`（或任何子类，比如 `JSONResponse`），数据不会被自动转换（即使你声明了 `response_model`），并且也不会自动生成文档（例如，作为生成的 OpenAPI 的一部分，在 HTTP 头 `Content-Type` 中包含特定的「媒体类型」）。

不过，你也可以在 *路径操作装饰器* 中通过 `response_class` 参数声明你想要使用的 `Response`（例如任何 `Response` 子类）。

你从 *路径操作函数* 中返回的内容将被放到该 `Response` 中。

并且如果该 `Response` 有一个 JSON 媒体类型（`application/json`），比如 `JSONResponse` 和 `UJSONResponse` 的情况，你返回的数据将使用你在 *路径操作装饰器* 中声明的任何 Pydantic `response_model` 自动转换（和过滤）。

/// note | 注意

如果你使用不带有任何媒体类型的响应类，FastAPI 会认为你的响应没有任何内容，因此不会在生成的 OpenAPI 文档中记录响应格式。

///

## 使用 `ORJSONResponse` { #use-orjsonresponse }

例如，如果你在压榨性能，你可以安装并使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> 并将响应设置为 `ORJSONResponse`。

导入你想要使用的 `Response` 类（子类）然后在 *路径操作装饰器* 中声明它。

对于大型响应，直接返回 `Response` 比返回字典要快得多。

这是因为默认情况下，FastAPI 会检查其中的每一项，并使用教程中解释的同一个 [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} 确保它可以被序列化为 JSON。这也正是它允许你返回**任意对象**（例如数据库模型）的原因。

但是，如果你确定你返回的内容**可以用 JSON 序列化**，你可以直接把它传给响应类，避免 FastAPI 在将返回内容传给响应类之前，先通过 `jsonable_encoder` 处理带来的额外开销。

{* ../../docs_src/custom_response/tutorial001b_py39.py hl[2,7] *}

/// info | 信息

参数 `response_class` 也会用来定义响应的「媒体类型」。

在这个例子中，HTTP 头 `Content-Type` 会被设置成 `application/json`。

并且在 OpenAPI 文档中也会这样记录。

///

/// tip | 提示

`ORJSONResponse` 只在 FastAPI 中可用，在 Starlette 中不可用。

///

## HTML 响应 { #html-response }

要从 **FastAPI** 直接返回一个 HTML 响应，使用 `HTMLResponse`。

* 导入 `HTMLResponse`。
* 将 `HTMLResponse` 作为你的 *路径操作装饰器* 的 `response_class` 参数传入。

{* ../../docs_src/custom_response/tutorial002_py39.py hl[2,7] *}

/// info | 信息

参数 `response_class` 也会用来定义响应的「媒体类型」。

在这个例子中，HTTP 头 `Content-Type` 会被设置成 `text/html`。

并且在 OpenAPI 文档中也会这样记录。

///

### 返回一个 `Response` { #return-a-response }

正如你在 [直接返回响应](response-directly.md){.internal-link target=_blank} 中看到的，你也可以在 *路径操作* 中通过返回响应来直接重载响应。

和上面一样的例子，返回一个 `HTMLResponse` 看起来可能是这样：

{* ../../docs_src/custom_response/tutorial003_py39.py hl[2,7,19] *}

/// warning | 警告

你的 *路径操作函数* 直接返回的 `Response` 不会在 OpenAPI 中被文档化（例如，`Content-Type` 不会被记录），并且在自动交互式文档中也不可见。

///

/// info | 信息

当然，实际的 `Content-Type` 头、状态码等将来自于你返回的 `Response` 对象。

///

### 在 OpenAPI 中文档化并重载 `Response` { #document-in-openapi-and-override-response }

如果你想在函数内部重载响应，同时又要在 OpenAPI 中文档化「媒体类型」，你可以使用 `response_class` 参数并返回一个 `Response` 对象。

然后 `response_class` 只会用于文档化 OpenAPI 的 *路径操作*，而你的 `Response` 将按原样使用。

#### 直接返回一个 `HTMLResponse` { #return-an-htmlresponse-directly }

例如，它可能是这样的：

{* ../../docs_src/custom_response/tutorial004_py39.py hl[7,21,23] *}

在这个例子中，函数 `generate_html_response()` 已经生成并返回一个 `Response`，而不是在 `str` 中返回 HTML。

通过返回调用 `generate_html_response()` 的结果，你已经返回了一个会重载 **FastAPI** 默认行为的 `Response`。

但由于你也在 `response_class` 中传入了 `HTMLResponse`，**FastAPI** 会知道如何在 OpenAPI 和交互式文档中，将其以 `text/html` 作为 HTML 来文档化：

<img src="/img/tutorial/custom-response/image01.png">

## 可用响应 { #available-responses }

这里有一些可用的响应。

记住，你可以使用 `Response` 来返回任何其他东西，甚至创建一个自定义的子类。

/// note | 技术细节

你也可以使用 `from starlette.responses import HTMLResponse`。

**FastAPI** 提供与 `fastapi.responses` 相同的 `starlette.responses` 只是为了方便你（开发者）。但大多数可用的响应都直接来自 Starlette。

///

### `Response` { #response }

主 `Response` 类，其他所有响应都继承自它。

你可以直接返回它。

它接受以下参数：

* `content` - 一个 `str` 或 `bytes`。
* `status_code` - 一个 `int` 类型的 HTTP 状态码。
* `headers` - 一个由字符串组成的 `dict`。
* `media_type` - 一个给出媒体类型的 `str`。例如 `"text/html"`。

FastAPI（实际上是 Starlette）会自动包含一个 Content-Length 头。它还会基于 `media_type` 包含一个 Content-Type 头，并为文本类型追加一个 charset。

{* ../../docs_src/response_directly/tutorial002_py39.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

如上文所述，接受文本或字节并返回 HTML 响应。

### `PlainTextResponse` { #plaintextresponse }

接受文本或字节并返回纯文本响应。

{* ../../docs_src/custom_response/tutorial005_py39.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

接受数据并返回一个 `application/json` 编码的响应。

如上文所述，这是 **FastAPI** 中使用的默认响应。

### `ORJSONResponse` { #orjsonresponse }

如上文所述，一个使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> 的快速替代 JSON 响应。

/// info | 信息

这需要安装 `orjson`，例如使用 `pip install orjson`。

///

### `UJSONResponse` { #ujsonresponse }

一个使用 <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a> 的可选 JSON 响应。

/// info | 信息

这需要安装 `ujson`，例如使用 `pip install ujson`。

///

/// warning | 警告

在处理某些边缘情况时，`ujson` 不如 Python 的内置实现那么谨慎。

///

{* ../../docs_src/custom_response/tutorial001_py39.py hl[2,7] *}

/// tip | 提示

`ORJSONResponse` 可能是一个更快的替代方案。

///

### `RedirectResponse` { #redirectresponse }

返回 HTTP 重定向。默认使用 307 状态码（Temporary Redirect）。

你可以直接返回一个 `RedirectResponse`：

{* ../../docs_src/custom_response/tutorial006_py39.py hl[2,9] *}

---

或者你也可以在 `response_class` 参数中使用它：

{* ../../docs_src/custom_response/tutorial006b_py39.py hl[2,7,9] *}

如果你这么做，那么你可以直接从你的 *路径操作函数* 返回 URL。

在这种情况下，使用的 `status_code` 会是 `RedirectResponse` 的默认值，即 `307`。

---

你也可以将 `status_code` 参数与 `response_class` 参数组合使用：

{* ../../docs_src/custom_response/tutorial006c_py39.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

接受异步生成器或普通生成器/迭代器，并流式传输响应体。

{* ../../docs_src/custom_response/tutorial007_py39.py hl[2,14] *}

#### 使用 `StreamingResponse` 处理类似文件的对象 { #using-streamingresponse-with-file-like-objects }

如果你有一个 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">类似文件（file-like）</a> 的对象（例如，由 `open()` 返回的对象），你可以创建一个生成器函数来遍历那个类似文件的对象。

这样，你不必先把它全部读进内存；你可以把该生成器函数传给 `StreamingResponse` 并返回它。

这包括许多与云存储、视频处理等交互的库。

{* ../../docs_src/custom_response/tutorial008_py39.py hl[2,10:12,14] *}

1. 这是生成器函数。它之所以是「生成器函数」，是因为它内部包含 `yield` 语句。
2. 通过使用 `with` 块，我们可以确保在生成器函数结束后关闭类似文件的对象。因此，在它发送完响应之后会关闭。
3. 这个 `yield from` 告诉函数去遍历名为 `file_like` 的东西。然后，对于遍历到的每一部分，把那一部分作为来自该生成器函数（`iterfile`）的内容 `yield` 出去。

    因此，它是一个生成器函数，把「生成」的工作在内部转交给别的东西来完成。

    通过这样做，我们可以把它放在一个 `with` 块里，从而确保在完成后关闭类似文件的对象。

/// tip | 提示

注意这里，因为我们使用的是不支持 `async` 和 `await` 的标准 `open()`，我们用普通的 `def` 来声明路径操作。

///

### `FileResponse` { #fileresponse }

以异步方式将文件作为响应进行流式传输。

与其他响应类型相比，它接受一组不同的参数来实例化：

* `path` - 要流式传输的文件的文件路径。
* `headers` - 要包含的任何自定义响应头，字典类型。
* `media_type` - 给出媒体类型的字符串。如果未设置，则会使用文件名或路径来推断媒体类型。
* `filename` - 如果设置，它将包含在响应的 `Content-Disposition` 中。

文件响应会包含合适的 `Content-Length`、`Last-Modified` 和 `ETag` 头。

{* ../../docs_src/custom_response/tutorial009_py39.py hl[2,10] *}

你也可以使用 `response_class` 参数：

{* ../../docs_src/custom_response/tutorial009b_py39.py hl[2,8,10] *}

在这种情况下，你可以直接从你的 *路径操作函数* 返回文件路径。

## 自定义响应类 { #custom-response-class }

你可以创建自己的自定义响应类，继承自 `Response` 并使用它。

例如，假设你想使用 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>，但想要使用一些在内置 `ORJSONResponse` 类中未使用的自定义设置。

比如你想让它返回带缩进并格式化的 JSON，因此你想使用 orjson 选项 `orjson.OPT_INDENT_2`。

你可以创建一个 `CustomORJSONResponse`。你需要做的主要事情是创建一个 `Response.render(content)` 方法，它返回 `bytes` 形式的内容：

{* ../../docs_src/custom_response/tutorial009c_py39.py hl[9:14,17] *}

现在不再返回：

```json
{"message": "Hello World"}
```

...这个响应将会返回：

```json
{
  "message": "Hello World"
}
```

当然，你可能会发现比格式化 JSON 更好的方式来利用这一点。 😉

## 默认响应类 { #default-response-class }

在创建一个 **FastAPI** 类实例或一个 `APIRouter` 时，你可以指定默认使用哪种响应类。

定义它的参数是 `default_response_class`。

在下面的示例中，**FastAPI** 会在所有 *路径操作* 中默认使用 `ORJSONResponse`，而不是 `JSONResponse`。

{* ../../docs_src/custom_response/tutorial010_py39.py hl[2,4] *}

/// tip | 提示

你仍然可以像之前一样，在 *路径操作* 中重载 `response_class`。

///

## 额外文档 { #additional-documentation }

你还可以使用 `responses` 在 OpenAPI 中声明媒体类型和许多其他细节：[OpenAPI 中的额外响应](additional-responses.md){.internal-link target=_blank}。

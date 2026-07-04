# 响应 Cookies { #response-cookies }

## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在*路径操作函数*中声明一个类型为 `Response` 的参数。

然后你可以在这个*临时*响应对象中设置 Cookie。

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

然后你可以像平常一样返回所需的任何对象（`dict`、数据库模型等）。

如果你声明了 `response_model`，它仍会用于过滤和转换你返回的对象。

**FastAPI** 会使用这个*临时*响应来提取 Cookie（还有 header 和状态码），并将它们放入最终响应中；最终响应包含你返回的值，并经过任何 `response_model` 过滤。

你也可以在依赖项中声明 `Response` 参数，并在其中设置 Cookie（和 header）。

## 直接返回 `Response` { #return-a-response-directly }

在代码中直接返回 `Response` 时，你也可以创建 Cookie。

为此，你可以按照[直接返回 Response](response-directly.md)中的说明创建一个响应。

然后在其中设置 Cookie，并返回它：

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | 提示

请记住，如果你直接返回响应，而不是使用 `Response` 参数，FastAPI 会直接返回它。

因此，你必须确保你的数据类型正确。例如，如果你返回的是 `JSONResponse`，数据就需要兼容 JSON。

并且还要确保你没有发送本应由 `response_model` 过滤的数据。

///

### 更多信息 { #more-info }

/// note | 技术细节

你也可以使用 `from starlette.responses import Response` 或者 `from starlette.responses import JSONResponse`。

**FastAPI** 为了方便开发者，提供了与 `starlette.responses` 相同的 `fastapi.responses`。但大多数可用的响应都直接来自 Starlette。

由于 `Response` 经常用于设置 header 和 Cookie，**FastAPI** 也在 `fastapi.Response` 中提供了它。

///

要查看所有可用参数和选项，请查看 [Starlette 文档](https://www.starlette.dev/responses/#set-cookie)。

# 响应 Cookies { #response-cookies }

## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在你的 *路径操作函数* 中声明一个 `Response` 类型的参数。

然后你就可以在这个 *临时* 响应对象中设置 cookies。

{* ../../docs_src/response_cookies/tutorial002_py39.py hl[1, 8:9] *}

然后你可以像平常一样返回任何你需要的对象（`dict`、数据库 model 等）。

如果你声明了 `response_model`，它仍然会用于过滤和转换你返回的对象。

**FastAPI** 会使用这个 *临时* 响应来提取 cookies（以及 headers 和 status code），并把它们放到最终响应中；最终响应包含你返回的值，并会被任何 `response_model` 过滤。

你也可以在依赖项中声明 `Response` 参数，并在其中设置 cookies（以及 headers）。

## 直接返回 `Response` { #return-a-response-directly }

你也可以在代码中直接返回 `Response` 时创建 cookies。

要做到这一点，你可以按 [Return a Response Directly](response-directly.md){.internal-link target=_blank} 中描述的方式创建一个响应。

然后在其中设置 Cookies，接着返回它：

{* ../../docs_src/response_cookies/tutorial001_py39.py hl[10:12] *}

/// tip | 提示

请记住，如果你直接返回一个响应，而不是使用 `Response` 参数，FastAPI 将直接返回它。

因此，你必须确保你的数据是正确的类型。例如，如果你返回的是 `JSONResponse`，那么它需要与 JSON 兼容。

并且还要确保你没有发送任何本应被 `response_model` 过滤的数据。

///

### 更多信息 { #more-info }

/// note | 技术细节

你也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。

**FastAPI** 为了方便你（开发者）提供了与 `starlette.responses` 相同的 `fastapi.responses`。但大多数可用的响应都直接来自 Starlette。

并且由于 `Response` 经常被用来设置 headers 和 cookies，**FastAPI** 也在 `fastapi.Response` 中提供了它。

///

要查看所有可用的参数和选项，请查看 <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">Starlette 中的文档</a>。

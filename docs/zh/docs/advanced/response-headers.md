# 响应头 { #response-headers }

## 使用 `Response` 参数 { #use-a-response-parameter }

你可以在你的*路径操作函数*中声明一个 `Response` 类型的参数（就像你可以为 cookies 做的那样）。

然后你可以在这个*临时*响应对象中设置头部。

{* ../../docs_src/response_headers/tutorial002_py39.py hl[1, 7:8] *}

然后你可以像平常一样返回任何你需要的对象（一个 `dict`、一个数据库模型等）。

如果你声明了一个 `response_model`，它仍然会被用来过滤和转换你返回的对象。

**FastAPI** 将使用这个*临时*响应来提取头部（也包括 cookies 和状态码），并将它们放入包含你返回的值的最终响应中，该响应由任何 `response_model` 过滤。

你也可以在依赖项中声明 `Response` 参数，并在其中设置头部（和 cookies）。

## 直接返回 `Response` { #return-a-response-directly }

你也可以在直接返回 `Response` 时添加头部。

按照[直接返回响应](response-directly.md){.internal-link target=_blank}中所述创建响应，并将头部作为附加参数传递：

{* ../../docs_src/response_headers/tutorial001_py39.py hl[10:12] *}

/// note | 技术细节

你也可以使用 `from starlette.responses import Response` 或 `from starlette.responses import JSONResponse`。

**FastAPI** 提供了与 `fastapi.responses` 相同的 `starlette.responses`，只是为了方便你（开发者）。但是，大多数可用的响应都直接来自 Starlette。

由于 `Response` 经常用于设置头部和 cookies，因此 **FastAPI** 还在 `fastapi.Response` 中提供了它。

///

## 自定义头部 { #custom-headers }

请记住，可以<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">使用 `X-` 前缀</a>添加自定义专有头部。

但是，如果你有自定义头部，你希望浏览器中的客户端能够看到它们，你需要将它们添加到你的 CORS 配置中（在[CORS（跨源资源共享）](../tutorial/cors.md){.internal-link target=_blank}中阅读更多），使用在 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 的 CORS 文档</a>中记录的参数 `expose_headers`。

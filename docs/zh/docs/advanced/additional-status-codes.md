# 额外的状态码 { #additional-status-codes }

默认情况下，**FastAPI** 会使用 `JSONResponse` 返回响应，把你从 *路径操作* 返回的内容放到该 `JSONResponse` 里。

它会使用默认的状态码，或者使用你在 *路径操作* 中设置的状态码。

## 额外的状态码 { #additional-status-codes_1 }

如果你想在主要状态码之外返回额外的状态码，你可以通过直接返回一个 `Response` 来实现，比如 `JSONResponse`，然后直接设置额外的状态码。

例如，假设你想要一个允许更新条目的 *路径操作*，并且在成功时返回 200 “OK” 的 HTTP 状态码。

但你也希望它能够接受新条目。而当这些条目之前不存在时，它会创建它们，并返回 201 “Created” 的 HTTP 状态码。

要实现这一点，导入 `JSONResponse`，并直接在其中返回你的内容，设置你想要的 `status_code`：

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | 警告

当你直接返回一个 `Response`（如上面的示例）时，它会被直接返回。

它不会使用模型等进行序列化。

确保它包含你希望包含的数据，并且这些值是合法的 JSON（如果你使用 `JSONResponse` 的话）。

///

/// note | 技术细节

你也可以使用 `from starlette.responses import JSONResponse`。

**FastAPI** 为了方便你（开发者）使用，提供了与 `starlette.responses` 相同的 `fastapi.responses`。但大多数可用的响应都直接来自 Starlette。`status` 也是一样。

///

## OpenAPI 和 API 文档 { #openapi-and-api-docs }

如果你直接返回额外的状态码和响应，它们不会包含在 OpenAPI schema（API 文档）中，因为 FastAPI 没办法预先知道你将要返回什么。

但你可以在代码中使用：[额外的响应](additional-responses.md){.internal-link target=_blank} 来记录这些内容。

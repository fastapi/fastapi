# 额外的状态码

**FastAPI** 默认使用 `JSONResponse` 返回一个响应，将你的 *路径操作* 中的返回内容放到该 `JSONResponse` 中。

**FastAPI** 会自动使用默认的状态码或者使用你在 *路径操作* 中设置的状态码。

## 额外的状态码

如果你想要返回主要状态码之外的状态码，你可以通过直接返回一个 `Response` 来实现，比如 `JSONResponse`，然后直接设置额外的状态码。

例如，假设你想有一个 *路径操作* 能够更新条目，并且更新成功时返回 200 「成功」 的 HTTP 状态码。

但是你也希望它能够接受新的条目。并且当这些条目不存在时，会自动创建并返回 201 「创建」的 HTTP 状态码。

要实现它，导入 `JSONResponse`，然后在其中直接返回你的内容，并将 `status_code` 设置为为你要的值。

{* ../../docs_src/additional_status_codes/tutorial001.py hl[4,25] *}

/// warning | 警告

当你直接返回一个像上面例子中的 `Response` 对象时，它会直接返回。

FastAPI 不会用模型等对该响应进行序列化。

确保其中有你想要的数据，且返回的值为合法的 JSON（如果你使用 `JSONResponse` 的话）。

///

/// note | 技术细节

你也可以使用 `from starlette.responses import JSONResponse`。　

出于方便，**FastAPI** 为开发者提供同 `starlette.responses` 一样的 `fastapi.responses`。但是大多数可用的响应都是直接来自 Starlette。`status` 也是一样。

///

## OpenAPI 和 API 文档

如果你直接返回额外的状态码和响应，它们不会包含在 OpenAPI 方案（API 文档）中，因为 FastAPI 没办法预先知道你要返回什么。

但是你可以使用 [额外的响应](additional-responses.md){.internal-link target=_blank} 在代码中记录这些内容。

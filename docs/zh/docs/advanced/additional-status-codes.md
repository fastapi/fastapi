# 附加状态码

默认情况下， **FastAPI** 会用 `JSONResponse` 来返回响应， *路径操作* 返回的内容会被放到这个 `JSONResponse`里。

它会用默认的状态码，或者你自己在 *路径操作* 里设置的状态码。

## 附加状态码

如果要返回主返回码之外的其他状态代码，可以通过直接返回一个`Response`（例如`JSONResponse`），并设置成其他状态代码来实现。

例如，假设你有一个 *路径操作* 要能更新项目，然后在成功时要返回 200 "OK" 的 HTTP 状态代码。

但你也想要它能接收新项目，如果这些新项目之前不存在就创建，并且返回 201 "Created" 的 HTTP 状态码。

为此可以引入 `JSONResponse` ，然后用它直接返回内容，把`status_code`设置成想要的。
To achieve that, import `JSONResponse`, and return your content there directly, setting the `status_code` that you want:

```Python hl_lines="4  23"
{!../../../docs_src/additional_status_codes/tutorial001.py!}
```

!!! warning
	当你像上面的例子那样直接返回一个`Response`时，它会被直接返回。

    它不会被 model 什么的序列化。
    
	所以确保里面有所需的数据，并且值是有效的 JSON（如果你用的是 `JSONResponse`）。

!!! note "技术细节"
	你也能这么写 `from starlette.responses import JSONResponse`。

    **FastAPI** 提供了和 `starlette.responses` 一样的 `fastapi.responses`，主要是为了方便开发者。不过大多数的可用响应类型都是直接从 Starlette 里来的， `status` 也一样。

## OpenAPI 和 API 文档

如果你直接返回其他状态码和响应，它们不会被包含在 OpenAPI 结构（API文档）中，因为 FastAPI 事先不知道你要返回什么。

不过你可以自己在代码里标注: [Additional Responses](additional-responses.md){.internal-link target=_blank}.

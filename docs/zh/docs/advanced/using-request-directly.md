# 直接使用 Request { #using-the-request-directly }

到目前为止，你一直在使用类型来声明你需要的请求各个部分。

从以下位置获取数据：

* 路径参数
* 请求头
* Cookies
* 等

通过这样做，**FastAPI** 会验证这些数据、转换它，并为你的 API 自动生成文档。

但在某些情况下，你可能需要直接访问 `Request` 对象。

## `Request` 对象的细节 { #details-about-the-request-object }

由于 **FastAPI** 底层实际上是 **Starlette**，并在其上层提供了若干工具层，因此在需要时，你可以直接使用 Starlette 的 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> 对象。

这也意味着，如果你直接从 `Request` 对象获取数据（例如，读取请求体），这些数据将不会被 FastAPI 验证、转换或记录到文档中（使用 OpenAPI，用于自动的 API 用户界面）。

尽管任何其他正常声明的参数（例如，使用 Pydantic 模型的请求体）仍然会被验证、转换、注解等。

但在某些特定情况下，获取 `Request` 对象会很有用。

## 直接使用 `Request` 对象 { #use-the-request-object-directly }

让我们想象一下，你想在*路径操作函数*内部获取客户端的 IP 地址/主机。

为此，你需要直接访问请求。

{* ../../docs_src/using_request_directly/tutorial001_py39.py hl[1,7:8] *}

通过将*路径操作函数*的一个参数声明为 `Request` 类型，**FastAPI** 就会知道要把 `Request` 传入该参数。

/// tip | 提示

注意，在这种情况下，我们在请求参数旁边还声明了一个路径参数。

因此，路径参数会被提取、验证、转换为指定类型，并使用 OpenAPI 进行注解。

同样地，你可以像平常一样声明任何其他参数，并额外获取 `Request`。

///

## `Request` 文档 { #request-documentation }

你可以在 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette 官方文档站点中的 `Request` 对象</a> 阅读更多细节。

/// note | 技术细节

你也可以使用 `from starlette.requests import Request`。

**FastAPI** 直接提供它只是为了方便你（开发者）。但它实际上直接来自 Starlette。

///

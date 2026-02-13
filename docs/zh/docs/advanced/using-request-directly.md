# 直接使用 Request { #using-the-request-directly }

至此，我们已经使用多种类型声明了请求的各种组件。

并从以下对象中提取数据：

* 路径参数
* 请求头
* Cookies
* 等

**FastAPI** 使用这种方式验证数据、转换数据，并自动生成 API 文档。

但有时，我们也需要直接访问 `Request` 对象。

## `Request` 对象的细节 { #details-about-the-request-object }

实际上，**FastAPI** 的底层是 **Starlette**，**FastAPI** 只不过是在  **Starlette** 顶层提供了一些工具，所以能直接使用 Starlette 的  <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> 对象。

但直接从 `Request` 对象提取数据时（例如，读取请求体），这些数据不会被 **FastAPI** 验证、转换或文档化（使用 OpenAPI，为自动的 API 用户界面）。

不过，仍可以验证、转换与注释（使用 Pydantic 模型的请求体等）其它正常声明的参数。

但在某些特定情况下，还是需要提取 `Request` 对象。

## 直接使用 `Request` 对象 { #use-the-request-object-directly }

假设要在*路径操作函数*中获取客户端 IP 地址和主机。

此时，需要直接访问请求。

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

把*路径操作函数*的参数类型声明为 `Request`，**FastAPI** 就能把 `Request` 传递到参数里。

/// tip | 提示

注意，本例除了声明请求参数之外，还声明了路径参数。

因此，能够提取、验证路径参数、并转换为指定类型，还可以用 OpenAPI 注释。

同样，您也可以正常声明其它参数，而且还可以提取 `Request`。

///

## `Request` 文档 { #request-documentation }

更多细节详见 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette 官档 - `Request` 对象</a>。

/// note | 技术细节

您也可以使用 `from starlette.requests import Request`。

**FastAPI** 直接提供它只是为了方便开发者，但它直接来自 Starlette。

///

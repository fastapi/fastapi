# 自定义 Request 和 APIRoute 类 { #custom-request-and-apiroute-class }

在某些情况下，你可能想要重写 `Request` 和 `APIRoute` 类使用的逻辑。

尤其是，当你本来会把这些逻辑放到中间件里时，这是一个不错的替代方案。

例如，如果你想在应用处理之前读取或操作请求体。

/// danger | 危险

这是一个“高级”特性。

如果你刚开始使用 **FastAPI**，可以先跳过本节。

///

## 使用场景 { #use-cases }

一些使用场景包括：

* 将非 JSON 的请求体转换为 JSON（例如 <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>）。
* 解压缩使用 gzip 压缩的请求体。
* 自动记录所有请求体日志。

## 处理自定义请求体编码 { #handling-custom-request-body-encodings }

来看如何用自定义的 `Request` 子类来解压 gzip 请求。

以及一个 `APIRoute` 子类来使用该自定义请求类。

### 创建自定义 `GzipRequest` 类 { #create-a-custom-gziprequest-class }

/// tip | 提示

这是一个演示工作原理的示例。如果你需要 Gzip 支持，可以直接使用提供的 [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank}。

///

首先，我们创建一个 `GzipRequest` 类，它会重写 `Request.body()` 方法：当请求头中存在相应标记时对请求体进行解压。

如果请求头中没有 `gzip`，则不会尝试解压。

这样，同一个路由类即可同时处理 gzip 压缩和未压缩的请求。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### 创建自定义 `GzipRoute` 类 { #create-a-custom-gziproute-class }

接着，我们创建 `fastapi.routing.APIRoute` 的自定义子类来使用 `GzipRequest`。

这次，我们会重写 `APIRoute.get_route_handler()` 方法。

该方法返回一个函数，这个函数负责接收请求并返回响应。

这里我们用它把原始请求包装为 `GzipRequest`。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | 技术细节

`Request` 拥有 `request.scope` 属性，它就是一个 Python `dict`，包含与请求相关的元数据。

`Request` 还包含 `request.receive`，它是一个用于“接收”请求体的函数。

`scope` 字典和 `receive` 函数都是 ASGI 规范的一部分。

创建一个新的 `Request` 实例需要这两样：`scope` 和 `receive`。

想了解更多关于 `Request` 的信息，请查看 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette 的 Request 文档</a>。

///

由 `GzipRequest.get_route_handler` 返回的函数唯一不同之处是把 `Request` 转换为 `GzipRequest`。

这样，在传给我们的路径操作之前，`GzipRequest` 会（在需要时）负责解压数据。

之后，其余处理逻辑完全相同。

但由于我们修改了 `GzipRequest.body`，在 **FastAPI** 需要读取时，请求体会被自动解压。

## 在异常处理器中访问请求体 { #accessing-the-request-body-in-an-exception-handler }

/// tip | 提示

要解决类似问题，使用 `RequestValidationError` 的自定义处理器中的 `body` 往往更简单（[处理错误](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}）。

但本示例同样有效，并展示了如何与内部组件交互。

///

我们也可以用相同的方法在异常处理器中访问请求体。

所需仅是在 `try`/`except` 块中处理请求：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

如果发生异常，`Request` 实例仍在作用域内，因此我们可以在处理错误时读取并使用请求体：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## 在路由器中自定义 `APIRoute` 类 { #custom-apiroute-class-in-a-router }

你也可以设置 `APIRouter` 的 `route_class` 参数：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

在此示例中，`router` 下的路径操作将使用自定义的 `TimedRoute` 类，响应中会多一个 `X-Response-Time` 头，包含生成响应所用的时间：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}

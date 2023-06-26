# 自定义请求与 APIRoute 类

有时，我们要覆盖 `Request` 与 `APIRoute` 类使用的逻辑。

尤其是中间件里的逻辑。

例如，在应用处理请求体前，预先读取或操控请求体。

!!! danger "危险"

    本章内容**较难**。

    **FastAPI** 新手可跳过本章。

## 用例

常见用例如下：

* 把 <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a> 等非 JSON 请求体转换为 JSON
* 解压 gzip 压缩的请求体
* 自动记录所有请求体的日志

## 处理自定义请求体编码

下面学习如何使用自定义 `Request` 子类压缩 gizp 请求。

并在自定义请求的类中使用 `APIRoute` 子类。

### 创建自定义 `GzipRequest` 类

!!! tip "提示"

    本例只是为了说明 `GzipRequest` 类如何运作。如需 Gzip 支持，请使用 [`GzipMiddleware`](./middleware.md#gzipmiddleware){.internal-link target=_blank}。

首先，创建 `GzipRequest` 类，覆盖解压请求头中请求体的 `Request.body()` 方法。

请求头中没有 `gzip` 时，`GzipRequest` 不会解压请求体。

这样就可以让同一个路由类处理 gzip 压缩的请求或未压缩的请求。

```Python hl_lines="8-15"
{!../../../docs_src/custom_request_and_route/tutorial001.py!}
```

### 创建自定义 `GzipRoute` 类

接下来，创建使用 `GzipRequest` 的 `fastapi.routing.APIRoute  ` 的自定义子类。

此时，这个自定义子类会覆盖 `APIRoute.get_route_handler()`。

`APIRoute.get_route_handler()` 方法返回的是函数，并且返回的函数接收请求并返回响应。

本例用它根据原始请求创建 `GzipRequest`。

```Python hl_lines="18-26"
{!../../../docs_src/custom_request_and_route/tutorial001.py!}
```

!!! note "技术细节"

    `Request` 的 `request.scope` 属性是包含关联请求元数据的字典。

    `Request` 的 `request.receive` 方法是**接收**请求体的函数。

    `scope` 字典与 `receive` 函数都是 ASGI 规范的内容。

    `scope` 与 `receive` 也是创建新的 `Request` 实例所需的。

    `Request` 的更多内容详见 <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">Starlette 官档 - 请求</a>。

`GzipRequest.get_route_handler` 返回函数的唯一区别是把 `Request` 转换成了 `GzipRequest`。

如此一来，`GzipRequest` 把数据传递给*路径操作*前，就会解压数据（如需）。

之后，所有处理逻辑都一样。

但因为改变了 `GzipRequest.body`，**FastAPI** 加载请求体时会自动解压。

## 在异常处理器中访问请求体

!!! tip "提示"

    为了解决同样的问题，在 `RequestValidationError` 的自定义处理器使用 `body`  （[处理错误](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}）可能会更容易。

    但本例仍然可行，而且本例展示了如何与内部组件进行交互。

同样也可以在异常处理器中访问请求体。

此时要做的只是处理 `try`/`except` 中的请求：

```Python hl_lines="13  15"
{!../../../docs_src/custom_request_and_route/tutorial002.py!}
```

发生异常时，`Request` 实例仍在作用域内，因此处理错误时可以读取和使用请求体：

```Python hl_lines="16-18"
{!../../../docs_src/custom_request_and_route/tutorial002.py!}
```

## 在路由中自定义 `APIRoute` 类

您还可以设置 `APIRoute` 的 `route_class` 参数：

```Python hl_lines="26"
{!../../../docs_src/custom_request_and_route/tutorial003.py!}
```

本例中，*路径操作*下的 `router` 使用自定义的 `TimedRoute` 类，并在响应中包含输出生成响应时间的 `X-Response-Time` 响应头：

```Python hl_lines="13-20"
{!../../../docs_src/custom_request_and_route/tutorial003.py!}
```

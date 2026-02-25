# 中间件 { #middleware }

你可以向 **FastAPI** 应用添加中间件。

“中间件”是一个函数，它会在每个特定的*路径操作*处理每个**请求**之前运行，也会在返回每个**响应**之前运行。

* 它接收你的应用的每一个**请求**。
* 然后它可以对这个**请求**做一些事情或者执行任何需要的代码。
* 然后它将这个**请求**传递给应用程序的其他部分（某个*路径操作*）处理。
* 之后它获取应用程序生成的**响应**（由某个*路径操作*产生）。
* 它可以对该**响应**做一些事情或者执行任何需要的代码。
* 然后它返回这个**响应**。

/// note | 技术细节

如果你有使用 `yield` 的依赖，依赖中的退出代码会在中间件之后运行。

如果有任何后台任务（会在[后台任务](background-tasks.md){.internal-link target=_blank}一节中介绍，你稍后会看到），它们会在所有中间件之后运行。

///

## 创建中间件 { #create-a-middleware }

要创建中间件，你可以在函数的顶部使用装饰器 `@app.middleware("http")`。

中间件函数会接收：

* `request`。
* 一个函数 `call_next`，它会把 `request` 作为参数接收。
    * 这个函数会把 `request` 传递给相应的*路径操作*。
    * 然后它返回由相应*路径操作*生成的 `response`。
* 在返回之前，你可以进一步修改 `response`。

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip

请记住可以<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">使用 `X-` 前缀</a>添加专有自定义请求头。

但是如果你有希望让浏览器中的客户端可见的自定义请求头，你需要把它们加到你的 CORS 配置（[CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}）的 `expose_headers` 参数中，参见 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 的 CORS 文档</a>。

///

/// note | 技术细节

你也可以使用 `from starlette.requests import Request`。

**FastAPI** 为了开发者方便提供了该对象，但它直接来自 Starlette。

///

### 在 `response` 之前与之后 { #before-and-after-the-response }

你可以在任何*路径操作*接收 `request` 之前，添加要与该 `request` 一起运行的代码。

也可以在生成 `response` 之后、返回之前添加代码。

例如，你可以添加一个自定义请求头 `X-Process-Time`，其值为处理请求并生成响应所花费的秒数：

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip

这里我们使用 <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> 而不是 `time.time()`，因为在这类场景中它可能更精确。🤓

///

## 多个中间件的执行顺序 { #multiple-middleware-execution-order }

当你使用 `@app.middleware()` 装饰器或 `app.add_middleware()` 方法添加多个中间件时，每个新中间件都会包裹应用，形成一个栈。最后添加的中间件是“最外层”的，最先添加的是“最内层”的。

在请求路径上，最外层的中间件先运行。

在响应路径上，它最后运行。

例如：

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

这会产生如下执行顺序：

* 请求：MiddlewareB → MiddlewareA → 路由

* 响应：路由 → MiddlewareA → MiddlewareB

这种栈式行为确保中间件按可预测且可控的顺序执行。

## 其他中间件 { #other-middlewares }

你可以稍后在[高级用户指南：高级中间件](../advanced/middleware.md){.internal-link target=_blank}中阅读更多关于其他中间件的内容。

你将在下一节中了解如何使用中间件处理 <abbr title="Cross-Origin Resource Sharing - 跨域资源共享">CORS</abbr>。

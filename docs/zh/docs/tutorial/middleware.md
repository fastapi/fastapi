# 中间件 { #middleware }

你可以向 **FastAPI** 应用添加中间件。

“中间件”是一个函数，它会在每个 **请求** 被任何特定的 *路径操作* 处理之前运行，并且也会在每个 **响应** 返回之前运行。

* 它会接收进入你应用的每个 **请求**。
* 然后它可以对该 **请求** 做一些事情或运行任何需要的代码。
* 然后它把 **请求** 交给应用的其余部分处理（通过某个 *路径操作*）。
* 然后它会接收由应用生成的 **响应**（通过某个 *路径操作*）。
* 它可以对该 **响应** 做些什么或运行任何需要的代码。
* 然后它返回 **响应**。

/// note | 注意

如果你有使用 `yield` 的依赖项，退出代码会在中间件 *之后* 运行。

如果有任何后台任务（在 [后台任务](background-tasks.md){.internal-link target=_blank} 一节中介绍，你稍后会看到），它们会在所有中间件 *之后* 运行。

///

## 创建中间件 { #create-a-middleware }

要创建中间件，你可以在函数顶部使用装饰器 `@app.middleware("http")`。

中间件函数接收：

* `request`。
* 一个函数 `call_next`，它会接收 `request` 作为参数。
    * 该函数会把 `request` 传递给对应的 *路径操作*。
    * 然后它返回由对应 *路径操作* 生成的 `response`。
* 然后你可以在返回 `response` 之前进一步修改它。

{* ../../docs_src/middleware/tutorial001_py39.py hl[8:9,11,14] *}

/// tip | 提示

请记住，可以 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">使用 `X-` 前缀</a> 添加自定义专有请求头。

但是如果你有自定义请求头，并希望浏览器中的客户端能够看到它们，你需要把它们加入到你的 CORS 配置（[CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}）中，使用 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette 的 CORS 文档</a> 中记录的参数 `expose_headers`。

///

/// note | 注意

你也可以使用 `from starlette.requests import Request`。

**FastAPI** 为你（开发者）提供它作为便利，但它直接来自 Starlette。

///

### 在 `response` 的前和后 { #before-and-after-the-response }

你可以添加与 `request` 一起运行的代码，在任何 *路径操作* 接收它之前运行。

也可以在生成 `response` 之后、返回之前运行代码。

例如，你可以添加一个自定义请求头 `X-Process-Time`，包含处理请求并生成响应所花费的秒数：

{* ../../docs_src/middleware/tutorial001_py39.py hl[10,12:13] *}

/// tip | 提示

这里我们使用 <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> 而不是 `time.time()`，因为在这些用例中它可能更精确。🤓

///

## 多个中间件的执行顺序 { #multiple-middleware-execution-order }

当你使用 `@app.middleware()` 装饰器或 `app.add_middleware()` 方法添加多个中间件时，每新增一个中间件都会包裹应用，形成一个栈。最后添加的中间件是 *最外层*，第一个添加的中间件是 *最内层*。

在请求路径上，*最外层* 的中间件最先运行。

在响应路径上，它最后运行。

例如：

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

这会产生如下执行顺序：

* **请求**：MiddlewareB → MiddlewareA → route

* **响应**：route → MiddlewareA → MiddlewareB

这种栈式行为确保中间件以可预测且可控的顺序执行。

## 其他中间件 { #other-middlewares }

你可以稍后在 [Advanced User Guide: Advanced Middleware](../advanced/middleware.md){.internal-link target=_blank} 阅读更多关于其他中间件的内容。

你将在下一节中学习如何使用中间件处理 <abbr title="Cross-Origin Resource Sharing">CORS</abbr>。

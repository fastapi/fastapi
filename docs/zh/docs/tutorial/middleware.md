# 中间件

你可以向 **FastAPI** 应用添加中间件.

"middleware"是一个函数,它在处理每个特定*路径操作*的**request**前工作,并且在每个**response**返回之前工作.

* 它接收你的应用程序的每一个**request**.
* 然后它可以对这个**request**做一些事情或者执行任何需要的代码.
* 然后它将**request**传递给应用程序的其他部分 (通过某种*路径操作*).
* 然后它获取应用程序生产的**response** (通过某种*路径操作*).
* 它可以对该**response**做些什么或者执行任何需要的代码.
* 然后它返回这个 **response**.

!!! note "技术细节"
    如果你依赖了 `yield`, 退出代码将在执行中间件*后*执行.

    如果有任何后台任务(稍后记录), 它们将在执行中间件*后*运行.

## 创建中间件

要创建中间件你可以在函数的顶部使用装饰器 `@app.middleware("http")`.

中间件参数接收:

* `request`.
* 一个函数 `call_next` 它将接收 `request` 作为参数.
    * 这个函数将 `request` 传递个相应的 *路径操作*.
    * 然后它将返回由相应的*路径操作*生成的 `response`.
* 然后你可以在返回 `response` 前进一步修改它.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! tip
    请记住可以 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">用'X-' 前缀</a>添加专有自定义请求头.

    但是如果你想让浏览器中的客户端看到你的自定义请求头, 你需要把它们加到 CORS 配置 ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) 的 `expose_headers` 参数中,在 <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>文档中.

!!! note "技术细节"
    你也可以使用 `from starlette.requests import Request`.

    **FastAPI** 为开发者提供了方便. 但是你也可以直接使用Starlette.

### 在 `response` 的前和后

在任何*路径操作*收到`request`前,可以添加要和请求一起运行的代码.

也可以在*response*生成但是返回之前添加代码.

例如你可以添加自定义请求头 `X-Process-Time` 包含以秒为单位的接收请求和生成相应的时间:

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## 其他中间件

你可以稍后再 [Advanced User Guide: Advanced Middleware](../advanced/middleware.md){.internal-link target=_blank}阅读更过关于中间件的教程.

你将在下一节中学习如何使用中间件处理 <abbr title="Cross-Origin Resource Sharing">CORS</abbr> .

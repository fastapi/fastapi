# 高级中间件

用户指南介绍了如何为应用添加[自定义中间件](../tutorial/middleware.md){.internal-link target=_blank} 。

以及如何[使用 `CORSMiddleware` 处理 CORS](../tutorial/cors.md){.internal-link target=_blank}。

本章学习如何使用其它中间件。

## 添加 ASGI 中间件

因为 **FastAPI** 基于 Starlette，且执行 <abbr title="Asynchronous Server Gateway Interface，异步服务器网关界面">ASGI</abbr> 规范，所以可以使用任意 ASGI 中间件。

中间件不必是专为 FastAPI 或 Starlette 定制的，只要遵循 ASGI 规范即可。

总之，ASGI 中间件是类，并把 ASGI 应用作为第一个参数。

因此，有些第三方 ASGI 中间件的文档推荐以如下方式使用中间件：

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

但 FastAPI（实际上是 Starlette）提供了一种更简单的方式，能让内部中间件在处理服务器错误的同时，还能让自定义异常处理器正常运作。

为此，要使用 `app.add_middleware()` （与 CORS 中的示例一样）。

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` 的第一个参数是中间件的类，其它参数则是要传递给中间件的参数。

## 集成中间件

**FastAPI** 为常见用例提供了一些中间件，下面介绍怎么使用这些中间件。

/// note | 技术细节

以下几个示例中也可以使用 `from starlette.middleware.something import SomethingMiddleware`。

**FastAPI** 在 `fastapi.middleware` 中提供的中间件只是为了方便开发者使用，但绝大多数可用的中间件都直接继承自 Starlette。

///

## `HTTPSRedirectMiddleware`

强制所有传入请求必须是 `https` 或 `wss`。

任何传向 `http` 或 `ws` 的请求都会被重定向至安全方案。

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware`

强制所有传入请求都必须正确设置 `Host` 请求头，以防 HTTP 主机头攻击。

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

支持以下参数：

* `allowed_hosts` - 允许的域名（主机名）列表。`*.example.com` 等通配符域名可以匹配子域名，或使用 `allowed_hosts=["*"]` 允许任意主机名，或省略中间件。

如果传入的请求没有通过验证，则发送 `400` 响应。

## `GZipMiddleware`

处理 `Accept-Encoding` 请求头中包含 `gzip` 请求的 GZip 响应。

中间件会处理标准响应与流响应。

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

支持以下参数：

* `minimum_size` - 小于最小字节的响应不使用 GZip。 默认值是 `500`。

## 其它中间件

除了上述中间件外，FastAPI 还支持其它ASGI 中间件。

例如：

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn 的 `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

其它可用中间件详见 <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Starlette 官档 -  中间件</a> 及 <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome 列表</a>。

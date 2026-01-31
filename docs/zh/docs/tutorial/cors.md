# CORS（跨域资源共享） { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS 或者“跨域资源共享”</a> 指的是：在浏览器中运行的前端包含与后端通信的 JavaScript 代码，而后端与前端处于不同“源（origin）”的情况。

## 源（Origin） { #origin }

源是协议（`http`、`https`）、域名（`myapp.com`、`localhost`、`localhost.tiangolo.com`）以及端口（`80`、`443`、`8080`）的组合。

因此，这些都是不同的源：

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

即使它们都在 `localhost`，但使用了不同的协议或端口，所以它们是不同的“源”。

## 步骤 { #steps }

假设你的浏览器中有一个前端运行在 `http://localhost:8080`，并且它的 JavaScript 正在尝试与运行在 `http://localhost` 的后端通信（因为我们没有指定端口，浏览器会假定默认端口为 `80`）。

然后，浏览器会向 `:80` 后端发送一个 HTTP `OPTIONS` 请求，如果后端发送了合适的 headers 来授权来自这个不同源（`http://localhost:8080`）的通信，那么 `:8080` 的浏览器就会允许前端的 JavaScript 将请求发送到 `:80` 后端。

要实现这一点，`:80` 后端必须有一个“允许的源”列表。

在这种情况下，该列表必须包含 `http://localhost:8080`，`:8080` 前端才能正常工作。

## 通配符 { #wildcards }

也可以将该列表声明为 `"*"`（一个“通配符”），表示允许所有源。

但这只会允许某些类型的通信，不包括任何涉及凭据的内容：Cookies、使用 Bearer Token 的 Authorization headers 等。

因此，为了让一切都能正确工作，最好显式指定允许的源。

## 使用 `CORSMiddleware` { #use-corsmiddleware }

你可以在 **FastAPI** 应用中使用 `CORSMiddleware` 来配置它。

* 导入 `CORSMiddleware`。
* 创建一个允许的源列表（字符串列表）。
* 将其作为“middleware”添加到你的 **FastAPI** 应用中。

你也可以指定后端是否允许：

* 凭据（Authorization headers、Cookies 等）。
* 特定的 HTTP 方法（`POST`、`PUT`），或使用通配符 `"*"` 允许全部方法。
* 特定的 HTTP headers，或使用通配符 `"*"` 允许全部 headers。

{* ../../docs_src/cors/tutorial001_py39.py hl[2,6:11,13:19] *}


`CORSMiddleware` 实现使用的默认参数默认是比较严格的，因此你需要显式启用特定的源、方法或 headers，浏览器才会被允许在跨域上下文中使用它们。

支持以下参数：

* `allow_origins` - 允许发起跨域请求的源列表。例如 `['https://example.org', 'https://www.example.org']`。你可以使用 `['*']` 允许任何源。
* `allow_origin_regex` - 用于匹配允许发起跨域请求的源的正则表达式字符串。例如 `'https://.*\.example\.org'`。
* `allow_methods` - 允许跨域请求的 HTTP 方法列表。默认为 `['GET']`。你可以使用 `['*']` 允许所有标准方法。
* `allow_headers` - 允许跨域请求的 HTTP 请求头列表。默认为 `[]`。你可以使用 `['*']` 允许所有 headers。`Accept`、`Accept-Language`、`Content-Language` 以及 `Content-Type` headers 在 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">简单 CORS 请求</a> 中总是被允许。
* `allow_credentials` - 指示跨域请求是否应支持 cookies。默认为 `False`。

    如果 `allow_credentials` 设为 `True`，那么 `allow_origins`、`allow_methods` 和 `allow_headers` 都不能设为 `['*']`。它们都必须<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">显式指定</a>。

* `expose_headers` - 指示哪些响应头应允许被浏览器访问。默认为 `[]`。
* `max_age` - 设置浏览器缓存 CORS 响应的最长时间（秒）。默认为 `600`。

该中间件会响应两种特定类型的 HTTP 请求...

### CORS 预检请求 { #cors-preflight-requests }

这是任何带有 `Origin` 和 `Access-Control-Request-Method` headers 的 `OPTIONS` 请求。

在这种情况下，中间件将拦截传入的请求并用适当的 CORS headers 进行响应，并出于提供信息的目的返回 `200` 或 `400` 响应。

### 简单请求 { #simple-requests }

任何带有 `Origin` header 的请求。在这种情况下，中间件会像往常一样传递请求，但会在响应中包含适当的 CORS headers。

## 更多信息 { #more-info }

更多关于 <abbr title="Cross-Origin Resource Sharing - 跨域资源共享">CORS</abbr> 的信息，请查看 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS 文档</a>。

/// note | 技术细节

你也可以使用 `from starlette.middleware.cors import CORSMiddleware`。

**FastAPI** 在 `fastapi.middleware` 中提供了几个中间件，仅仅是为了方便你（开发者）。但大多数可用的中间件都直接来自 Starlette。

///

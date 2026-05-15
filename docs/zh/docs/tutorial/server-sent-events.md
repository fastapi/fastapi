# 服务器发送事件（SSE） { #server-sent-events-sse }

你可以使用**服务器发送事件**（SSE）向客户端流式发送数据。

这类似于[流式传输 JSON Lines](stream-json-lines.md)，但使用 `text/event-stream` 格式，浏览器原生通过 [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 支持。

/// info | 信息

新增于 FastAPI 0.135.0。

///

## 什么是服务器发送事件？ { #what-are-server-sent-events }

SSE 是一种通过 HTTP 从服务器向客户端流式传输数据的标准。

每个事件是一个带有 `data`、`event`、`id` 和 `retry` 等“字段”的小文本块，以空行分隔。

看起来像这样：

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE 常用于 AI 聊天流式输出、实时通知、日志与可观测性，以及其他服务器向客户端推送更新的场景。

/// tip | 提示

如果你想流式传输二进制数据（例如视频或音频），请查看高级指南：[流式传输数据](../advanced/stream-data.md)。

///

## 使用 FastAPI 流式传输 SSE { #stream-sse-with-fastapi }

要在 FastAPI 中流式传输 SSE，在你的*路径操作函数*中使用 `yield`，并设置 `response_class=EventSourceResponse`。

从 `fastapi.sse` 导入 `EventSourceResponse`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

每个被 yield 的项会被编码为 JSON，并放入 SSE 事件的 `data:` 字段发送。

如果你将返回类型声明为 `AsyncIterable[Item]`，FastAPI 将使用它通过 Pydantic对数据进行**校验**、**文档化**和**序列化**。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | 提示

由于 Pydantic 会在**Rust** 端序列化它，相比未声明返回类型，你将获得更高的**性能**。

///

### 非 async 的*路径操作函数* { #non-async-path-operation-functions }

你也可以使用常规的 `def` 函数（没有 `async`），并以同样的方式使用 `yield`。

FastAPI 会确保其正确运行，从而不阻塞事件循环。

由于此时函数不是 async，正确的返回类型应为 `Iterable[Item]`：

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### 无返回类型 { #no-return-type }

你也可以省略返回类型。FastAPI 将使用 [`jsonable_encoder`](./encoder.md) 转换数据并发送。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

如果你需要设置 `event`、`id`、`retry` 或 `comment` 等 SSE 字段，你可以 yield `ServerSentEvent` 对象，而不是直接返回数据。

从 `fastapi.sse` 导入 `ServerSentEvent`：

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` 字段始终会被编码为 JSON。你可以传入任何可被序列化为 JSON 的值，包括 Pydantic 模型。

## 原始数据 { #raw-data }

如果你需要发送**不**进行 JSON 编码的数据，请使用 `raw_data` 而不是 `data`。

这对于发送预格式化文本、日志行或特殊的 <dfn title="用于指示特殊条件或状态的值">"哨兵"</dfn> 值（例如 `[DONE]`）很有用。

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | 注意

`data` 和 `raw_data` 是互斥的。每个 `ServerSentEvent` 上只能设置其中一个。

///

## 使用 `Last-Event-ID` 恢复 { #resuming-with-last-event-id }

当连接中断后浏览器重新连接时，会在 `Last-Event-ID` 头中发送上次收到的 `id`。

你可以将其读取为一个请求头参数，并据此从客户端离开的地方恢复流：

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## 使用 POST 的 SSE { #sse-with-post }

SSE 适用于**任意 HTTP 方法**，不仅仅是 `GET`。

这对像 [MCP](https://modelcontextprotocol.io) 这样通过 `POST` 传输 SSE 的协议很有用：

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## 技术细节 { #technical-details }

FastAPI 开箱即用地实现了一些 SSE 的最佳实践。

- 当 15 秒内没有任何消息时，发送一个**保活 `ping` 注释**，以防某些代理关闭连接，正如 [HTML 规范：Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) 中建议的那样。
- 设置 `Cache-Control: no-cache` 响应头，**防止缓存**流。
- 设置特殊响应头 `X-Accel-Buffering: no`，以**防止**某些代理（如 Nginx）**缓冲**。

你无需做任何事，它开箱即用。🤓

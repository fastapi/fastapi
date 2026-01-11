# WebSockets { #websockets }

你可以在 **FastAPI** 中使用 <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a>。

## 安装 `websockets` { #install-websockets }

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，并安装 `websockets`（一个 Python 库，让你更容易使用 "WebSocket" 协议）：

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets 客户端 { #websockets-client }

### 在生产环境中 { #in-production }

在你的生产系统中，你可能有一个使用 React、Vue.js 或 Angular 等现代框架创建的前端。

并且，为了通过 WebSockets 与后端通信，你可能会使用前端的工具。

或者，你可能有一个原生移动应用程序，直接用原生代码与你的 WebSocket 后端通信。

或者，你可能有任何其他方式与 WebSocket endpoint 通信。

---

但是，在本示例中，我们将使用一个非常简单的 HTML 文档，其中包含一些 JavaScript，全部放在一个长字符串中。

当然，这并不是最优的做法，你不会在生产环境中使用它。

在生产环境中，你会使用上面的一种选项。

但这是专注于 WebSockets 的服务端并提供一个可工作的示例的最简单方式：

{* ../../docs_src/websockets/tutorial001_py39.py hl[2,6:38,41:43] *}

## 创建 `websocket` { #create-a-websocket }

在你的 **FastAPI** 应用程序中，创建一个 `websocket`：

{* ../../docs_src/websockets/tutorial001_py39.py hl[1,46:47] *}

/// note | 技术细节

你也可以使用 `from starlette.websockets import WebSocket`。

**FastAPI** 直接提供了相同的 `WebSocket`，只是为了方便你（开发者）。但它直接来自 Starlette。

///

## 等待消息并发送消息 { #await-for-messages-and-send-messages }

在你的 WebSocket 路由中，你可以 `await` 等待消息并发送消息。

{* ../../docs_src/websockets/tutorial001_py39.py hl[48:52] *}

你可以接收和发送二进制、文本和 JSON 数据。

## 尝试一下 { #try-it }

如果你的文件名为 `main.py`，请使用以下命令运行应用程序：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在浏览器中打开 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

你将看到一个简单的页面，如下所示：

<img src="/img/tutorial/websockets/image01.png">

你可以在输入框中输入消息并发送：

<img src="/img/tutorial/websockets/image02.png">

然后，你的带有 WebSockets 的 **FastAPI** 应用程序将响应：

<img src="/img/tutorial/websockets/image03.png">

你可以发送（和接收）多条消息：

<img src="/img/tutorial/websockets/image04.png">

并且它们都会使用同一个 WebSocket 连接。

## 使用 `Depends` 和其他 { #using-depends-and-others }

在 WebSocket endpoints 中，你可以从 `fastapi` 导入并使用：

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

它们的工作方式与其他 FastAPI endpoints/*路径操作* 相同：

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info

由于这是一个 WebSocket，抛出 `HTTPException` 并不是很合理，而是抛出 `WebSocketException`。

你可以使用 <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">规范中定义的有效代码</a> 中的关闭代码。

///

### 尝试带有依赖项的 WebSockets { #try-the-websockets-with-dependencies }

如果你的文件名为 `main.py`，请使用以下命令运行应用程序：

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

在浏览器中打开 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

在那里你可以设置：

* "Item ID"，用于路径中。
* "Token"，作为查询参数使用。

/// tip | 提示

注意，查询 `token` 将由依赖项处理。

///

这样你就可以连接 WebSocket，然后发送和接收消息：

<img src="/img/tutorial/websockets/image05.png">

## 处理断开连接和多个客户端 { #handling-disconnections-and-multiple-clients }

当 WebSocket 连接关闭时，`await websocket.receive_text()` 将引发 `WebSocketDisconnect` 异常，你可以像本示例一样捕获并处理该异常。

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

尝试以下操作：

* 使用多个浏览器选项卡打开应用程序。
* 从它们发送消息。
* 然后关闭其中一个选项卡。

这将引发 `WebSocketDisconnect` 异常，并且所有其他客户端都会收到类似以下的消息：

```
Client #1596980209979 left the chat
```

/// tip | 提示

上面的应用程序是一个最小且简单的示例，用于演示如何处理并向多个 WebSocket 连接广播消息。

但请记住，由于所有内容都在内存中以单个列表的形式处理，因此它只能在进程运行时工作，并且只能在单进程下工作。

如果你需要更容易与 FastAPI 集成但更健壮、支持 Redis、PostgreSQL 或其他的方案，请查看 <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>。

///

## 更多信息 { #more-info }

要了解更多选项，请查看 Starlette 的文档：

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">`WebSocket` 类</a>。
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">基于类的 WebSocket 处理</a>。

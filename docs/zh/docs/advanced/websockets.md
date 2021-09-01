# WebSockets 接口

**FastAPI** 支持使用 <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSocket</a>。

## WebSocket 客户端

### 生产环境

生产环境下，您可能要使用 React、Vue.js、Angular 等现代前端框架。

并且使用 WebSocket 与后端通信时，还可能要使用前端工具。

本地移动应用也有可能在本地代码（native code）中使用 WebSocket 与后端直接通信。

当然您还有可能以其它方式与 WebSocket 端点通信。

---

但在本例中，我们使用非常简单的 HTML 文档，该文档只包含了一些 JavaScript，所有内容都在一个长字符串中。

这种方式肯定不好，在生产环境中最好不要这样做。

生产环境下要使用前端框架等方式。

但本例的这种方式可以用最简单的形式，让我们集中精力了解服务器端的 WebSocket，而且还能正常运行：

```Python hl_lines="2  6-38  41-43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## 创建 `websocket`

在 **FastAPI** 应用中创建 `websocket`：

```Python hl_lines="1  46-47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "技术细节"

    您也可以使用 `from starlette.websockets import WebSocket`。
    
    **FastAPI** 的 `WebSocket` 只是为开发者提供的快捷方式，但它其实直接继承自 Starlette。

## 等待信息与发送信息

在 WebSocket 路由里可以使用 `await` 接收或发送信息。

```Python hl_lines="48-52"
{!../../../docs_src/websockets/tutorial001.py!}
```

并可以接收和发送二进制、文本、JSON 等格式的数据。

## 运行

如果文件名为 `main.py`，则以如下命令运行应用：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

打开浏览器 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000。</a>

可以看到如下简单页面：

<img src="/img/tutorial/websockets/image01.png">

在输入框中输入并发送信息：

<img src="/img/tutorial/websockets/image02.png">

**FastAPI** 应用使用 WebSocket 返回如下响应：

<img src="/img/tutorial/websockets/image03.png">

发送与接收信息：

<img src="/img/tutorial/websockets/image04.png">

所有操作都使用同一个 WebSocket 连接。

## 使用 `Depends` 等函数

在 WebSocket 端点中，从 `fastapi` 导入并使用以下函数：

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

此处与其它 FastAPI 端点/路径操作的工作方式相同：

```Python hl_lines="58-65  68-83"
{!../../../docs_src/websockets/tutorial002.py!}
```

!!! info "说明"

    Websocket 不会真的触发 `HTTPException`，因此最好直接关闭 WebSocket 连接。
    
    此时，可以使用<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">规范定义的有效代码</a>中的关闭代码。
    
    今后, 还有可能添加可在任意位置触发的 `WebSocketException` 及其异常处理器。但这些都取决于 Starlette 的 <a href="https://github.com/encode/starlette/pull/527" class="external-link" target="_blank">PR #527</a>。

### WebSocket 与依赖项

如果文件名为 `main.py`，则以如下命令运行服务：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

打开浏览器 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000。</a>

设置：

* **Item ID**, 在路径中使用
* **Token**，用作查询参数

!!! tip "提示"

    注意，查询 `token` 由依赖项处理。

使用该依赖项可以连接 WebSocket，然后发送与接收信息：

<img src="/img/tutorial/websockets/image05.png">

## 处理断开连接与多个客户端

WebSocket 连接关闭时， `await websocket.receive_text()` 触发 `WebSocketDisconnect` 异常，然后就可以像本例一样捕获和处理异常。

```Python hl_lines="81-83"
{!../../../docs_src/websockets/tutorial003.py!}
```

尝试以下操作：

* 用多个浏览器标签页打开应用
* 在多个标签页中写入信息
* 然后关闭其中一个标签页

此时会触发 `WebSocketDisconnect` 异常，其它客户端会接收到如下信息：

```
Client #1596980209979 left the chat
```

!!! tip "提示"

    上述应用是最简单的例子，只是为了演示如何处理与广播信息给多个 WebSocket 连接。
    
    注意，所有操作都是在内存的单列表中处理，因此它只在进程运行时工作，且只使用单进程工作。
    
    如果需要为 FastAPI 集成一些由 Redis、PostgreSQL 等数据库支持的、且更成熟稳定的功能，请参阅<a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">编码/广播</a>。

## 更多信息

更多选项详见 Starlette 文档：

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank">`WebSocket` 类</a>
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">基于类的  WebSocket 处理方式</a>

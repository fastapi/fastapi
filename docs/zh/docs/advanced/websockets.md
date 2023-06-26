# WebSockets

您可以在 **FastAPI** 中使用 [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)。

## 安装 `WebSockets`

首先，您需要安装 `WebSockets`：

```console
$ pip install websockets

---> 100%
```

## WebSockets 客户端

### 在生产环境中

在您的生产系统中，您可能使用现代框架（如React、Vue.js或Angular）创建了一个前端。

要使用 WebSockets 与后端进行通信，您可能会使用前端的工具。

或者，您可能有一个原生移动应用程序，直接使用原生代码与 WebSocket 后端通信。

或者，您可能有其他与 WebSocket 终端通信的方式。

---

但是，在本示例中，我们将使用一个非常简单的HTML文档，其中包含一些JavaScript，全部放在一个长字符串中。

当然，这并不是最优的做法，您不应该在生产环境中使用它。

在生产环境中，您应该选择上述任一选项。

但这是一种专注于 WebSockets 的服务器端并提供一个工作示例的最简单方式：

```Python hl_lines="2  6-38  41-43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## 创建 `websocket`

在您的 **FastAPI** 应用程序中，创建一个 `websocket`：

```Python hl_lines="1  46-47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "技术细节"
    您也可以使用 `from starlette.websockets import WebSocket`。

    **FastAPI** 直接提供了相同的 `WebSocket`，只是为了方便开发人员。但它直接来自 Starlette。

## 等待消息并发送消息

在您的 WebSocket 路由中，您可以使用 `await` 等待消息并发送消息。

```Python hl_lines="48-52"
{!../../../docs_src/websockets/tutorial001.py!}
```

您可以接收和发送二进制、文本和 JSON 数据。

## 尝试一下

如果您的文件名为 `main.py`，请使用以下命令运行应用程序：

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

在浏览器中打开 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

您将看到一个简单的页面，如下所示：

<img src="/img/tutorial/websockets/image01.png">

您可以在输入框中输入消息并发送：

<img src="/img/tutorial/websockets/image02.png">

您的 **FastAPI** 应用程序将回复：

<img src="/img/tutorial/websockets/image03.png">

您可以发送（和接收）多条消息：

<img src="/img/tutorial/websockets/image04.png">

所有这些消息都将使用同一个 WebSocket 连

接。

## 使用 `Depends` 和其他依赖项

在 WebSocket 端点中，您可以从 `fastapi` 导入并使用以下内容：

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

它们的工作方式与其他 FastAPI 端点/ *路径操作* 相同：

=== "Python 3.10+"

    ```Python hl_lines="68-69  82"
    {!> ../../../docs_src/websockets/tutorial002_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="68-69  82"
    {!> ../../../docs_src/websockets/tutorial002_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="69-70  83"
    {!> ../../../docs_src/websockets/tutorial002_an.py!}
    ```

=== "Python 3.10+ 非带注解版本"

    !!! tip
        如果可能，请尽量使用 `Annotated` 版本。

    ```Python hl_lines="66-67  79"
    {!> ../../../docs_src/websockets/tutorial002_py310.py!}
    ```

=== "Python 3.6+ 非带注解版本"

    !!! tip
        如果可能，请尽量使用 `Annotated` 版本。

    ```Python hl_lines="68-69  81"
    {!> ../../../docs_src/websockets/tutorial002.py!}
    ```

!!! info
    由于这是一个 WebSocket，抛出 `HTTPException` 并不是很合理，而是抛出 `WebSocketException`。

    您可以使用<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">规范中定义的有效代码</a>。

### 尝试带有依赖项的 WebSockets

如果您的文件名为 `main.py`，请使用以下命令运行应用程序：

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

在浏览器中打开 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

在页面中，您可以设置：

* "Item ID"，用于路径。
* "Token"，作为查询参数。

!!! tip
    注意，查询参数 `token` 将由依赖项处理。

通过这样，您可以连接 WebSocket，然后发送和接收消息：

<img src="/img/tutorial/websockets/image05.png">

## 处理断开连接和多个客户端

当 WebSocket 连接关闭时，`await websocket.receive_text()` 将引发 `WebSocketDisconnect` 异常，您可以捕获并处理该异常，就像本示例中的示例一样。

=== "Python 3.9+"

    ```Python hl_lines="79-81"
    {!> ../../../docs_src/websockets/tutorial003_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="81-83"
    {!> ../../../docs_src/websockets/tutorial003.py!}
    ```

尝试以下操作：

* 使用多个浏览器选项卡打开应用程序。
* 从这些选项卡中发送消息。
* 然后关闭其中一个选项卡。

这将引发 `WebSocketDisconnect` 异常，并且所有其他客户端都会收到类似以下的消息：

```
Client #1596980209979 left the chat
```

!!! tip
    上面的应用程序是一个最小和简单的示例，用于演示如何处理和向多个 WebSocket 连接广播消息。

    但请记住，由于所有内容都在内存中以单个列表的形式处理，因此它只能在进程运行时工作，并且只能使用单个进程。

    如果您需要与 FastAPI 集成更简单但更强大的功能，支持 Redis、PostgreSQL 或其他功能，请查看 [encode/broadcaster](https://github.com/encode/broadcaster)。

## 更多信息

要了解更多选项，请查看 Starlette 的文档：

* [WebSocket 类](https://www.starlette.io/websockets/)
* [基于类的 WebSocket 处理](https://www.starlette.io/endpoints/#websocketendpoint)。

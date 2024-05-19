# WebSockets

在定义 WebSockets 时，通常要声明一个 `WebSocket` 类型的参数，通过它可以从客户端读取数据并向其发送数据。

它由 Starlette 直接提供，但也可以从 `fastapi` 中导入：

```python
from fastapi import WebSocket
```

!!! tip
    如果要定义同时与 HTTP 和 WebSockets 兼容的依赖关系，可以定义一个使用 "HTTPConnection "而不是 "Request "或 "WebSocket "的参数。

::: fastapi.WebSocket
    options:
        members:
            - scope
            - app
            - url
            - base_url
            - headers
            - query_params
            - path_params
            - cookies
            - client
            - state
            - url_for
            - client_state
            - application_state
            - receive
            - send
            - accept
            - receive_text
            - receive_bytes
            - receive_json
            - iter_text
            - iter_bytes
            - iter_json
            - send_text
            - send_bytes
            - send_json
            - close

当客户端断开连接时，会产生一个 `WebSocketDisconnect` 异常，你可以捕获它。

你可以直接从 `fastapi` 中导入：

```python
from fastapi import WebSocketDisconnect
```

::: fastapi.WebSocketDisconnect

### WebSockets - 附加类

用于处理 WebSockets 的附加类。

由 Starlette 直接提供，但也可以从 `fastapi` 中导入：

```python
from fastapi.websockets import WebSocketDisconnect, WebSocketState
```

::: fastapi.websockets.WebSocketDisconnect

::: fastapi.websockets.WebSocketState

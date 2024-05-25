# `HTTPConnection` 类

当你想定义同时兼容 HTTP 和 WebSockets 的依赖关系时，你可以定义一个使用 `HTTPConnection` 而不是 `Request` 或 `WebSocket` 的参数。

您可以从 `fastapi.requests` 中导入：

```python
from fastapi.requests import HTTPConnection
```

::: fastapi.requests.HTTPConnection

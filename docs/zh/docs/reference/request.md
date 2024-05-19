# `Request` 类

您可以将*路径操作函数*或依赖关系中的参数声明为 `Request`类型，这样就可以直接访问原始请求对象，而无需任何操作，例如验证。

你可以直接从 `fastapi` 导入：

```python
from fastapi import Request
```

!!! tip
    如果要定义同时与 HTTP 和 WebSockets 兼容的依赖关系，可以定义一个使用 "HTTPConnection "而不是 "Request "或 "WebSocket "的参数。

::: fastapi.Request

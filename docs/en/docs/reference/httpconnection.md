# `HTTPConnection` class

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

You can import it from `fastapi.requests`:

```python
from fastapi.requests import HTTPConnection
```

::: fastapi.requests.HTTPConnection

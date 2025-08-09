# `Request` class

You can declare a parameter in a *path operation function* or dependency to be of type `Request` and then you can access the raw request object directly, without any validation, etc.

You can import it directly from `fastapi`:

```python
from fastapi import Request
```

/// tip

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

///

::: fastapi.Request

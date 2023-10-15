# `HTTPConnection` class

When you want to define dependencies that should be compatible with both HTTP and
WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a
`Request` or a `WebSocket`.

You can import it from `fastapi.requests`:

```python
from fastapi.requests import HTTPConnection
```

::: starlette.requests.HTTPConnection
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
            - method
            - receive
            - url_for
            - is_disconnected

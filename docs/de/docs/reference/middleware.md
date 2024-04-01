# Middleware

Es gibt mehrere Middlewares, die direkt von Starlette bereitgestellt werden.

Lesen Sie mehr darüber in der [FastAPI-Dokumentation über Middleware](../advanced/middleware.md).

::: fastapi.middleware.cors.CORSMiddleware

Kann von `fastapi` importiert werden:

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: fastapi.middleware.gzip.GZipMiddleware

Kann von `fastapi` importiert werden:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware

Kann von `fastapi` importiert werden:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: fastapi.middleware.trustedhost.TrustedHostMiddleware

Kann von `fastapi` importiert werden:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

::: fastapi.middleware.wsgi.WSGIMiddleware

Kann von `fastapi` importiert werden:

```python
from fastapi.middleware.wsgi import WSGIMiddleware
```

# Middleware

There are several middlewares available provided by Starlette directly.

Read more about them in the
[FastAPI docs for Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

::: starlette.middleware.cors.CORSMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: starlette.middleware.gzip.GZipMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: starlette.middleware.httpsredirect.HTTPSRedirectMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: starlette.middleware.trustedhost.TrustedHostMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

::: starlette.middleware.wsgi.WSGIMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.wsgi import WSGIMiddleware
```

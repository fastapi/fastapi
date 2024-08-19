# Middleware

There are several middlewares available provided by Starlette directly.

Read more about them in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

::: fastapi.middleware.cors.CORSMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: fastapi.middleware.gzip.GZipMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: fastapi.middleware.trustedhost.TrustedHostMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

::: fastapi.middleware.wsgi.WSGIMiddleware

It can be imported from `fastapi`:

```python
from fastapi.middleware.wsgi import WSGIMiddleware
```

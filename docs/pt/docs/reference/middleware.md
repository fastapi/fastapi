# Middleware

Existem diversos middlewares disponíveis diretamente pelo Starlette.

Leia mais sobre isso em [FastAPI documentação para Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

::: fastapi.middleware.cors.CORSMiddleware

Pode ser importado de `fastapi`:

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: fastapi.middleware.gzip.GZipMiddleware

Pode ser importado de `fastapi`:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware

Pode ser importado de `fastapi`:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: fastapi.middleware.trustedhost.TrustedHostMiddleware

Pode ser importado de `fastapi`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

::: fastapi.middleware.wsgi.WSGIMiddleware

Pode ser importado de `fastapi`:

```python
from fastapi.middleware.wsgi import WSGIMiddleware
```

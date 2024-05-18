# 中间件

Starlette 可直接提供多个中间件。

请参阅 [FastAPI docs for Middleware](https://fastapi.tiangolo.com/zh/advanced/middleware/).

::: fastapi.middleware.cors.CORSMiddleware

可以这样从 `fastapi` 中导入它：

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: fastapi.middleware.gzip.GZipMiddleware

可以这样从 `fastapi` 中导入它：

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware

可以这样从 `fastapi` 中导入它：

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: fastapi.middleware.trustedhost.TrustedHostMiddleware

可以这样从 `fastapi` 中导入它：

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

::: fastapi.middleware.wsgi.WSGIMiddleware

可以这样从 `fastapi` 中导入它：

```python
from fastapi.middleware.wsgi import WSGIMiddleware
```

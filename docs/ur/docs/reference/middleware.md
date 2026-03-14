# Middleware

Starlette کی طرف سے براہ راست فراہم کردہ کئی middlewares دستیاب ہیں۔

ان کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں Middleware](https://fastapi.tiangolo.com/advanced/middleware/)۔

::: fastapi.middleware.cors.CORSMiddleware

اسے `fastapi` سے import کیا جا سکتا ہے:

```python
from fastapi.middleware.cors import CORSMiddleware
```

::: fastapi.middleware.gzip.GZipMiddleware

اسے `fastapi` سے import کیا جا سکتا ہے:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

::: fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware

اسے `fastapi` سے import کیا جا سکتا ہے:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

::: fastapi.middleware.trustedhost.TrustedHostMiddleware

اسے `fastapi` سے import کیا جا سکتا ہے:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

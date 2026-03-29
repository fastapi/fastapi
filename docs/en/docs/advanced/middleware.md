# Advanced Middleware { #advanced-middleware }

In the main tutorial you read how to add [Custom Middleware](../tutorial/middleware.md) to your application.

And then you also read how to handle [CORS with the `CORSMiddleware`](../tutorial/cors.md).

In this section we'll see how to use other middlewares.

## Adding ASGI middlewares { #adding-asgi-middlewares }

As **FastAPI** is based on Starlette and implements the <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr> specification, you can use any ASGI middleware.

A middleware doesn't have to be made for FastAPI or Starlette to work, as long as it follows the ASGI spec.

In general, ASGI middlewares are classes that expect to receive an ASGI app as the first argument.

So, in the documentation for third-party ASGI middlewares they will probably tell you to do something like:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

But FastAPI (actually Starlette) provides a simpler way to do it that makes sure that the internal middlewares handle server errors and custom exception handlers work properly.

For that, you use `app.add_middleware()` (as in the example for CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` receives a middleware class as the first argument and any additional arguments to be passed to the middleware.

## Integrated middlewares { #integrated-middlewares }

**FastAPI** includes several middlewares for common use cases, we'll see next how to use them.

/// note | Technical Details

For the next examples, you could also use `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** provides several middlewares in `fastapi.middleware` just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Enforces that all incoming requests must either be `https` or `wss`.

Any incoming request to `http` or `ws` will be redirected to the secure scheme instead.

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Enforces that all incoming requests have a correctly set `Host` header, in order to guard against HTTP Host Header attacks.

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

The following arguments are supported:

* `allowed_hosts` - A list of domain names that should be allowed as hostnames. Wildcard domains such as `*.example.com` are supported for matching subdomains. To allow any hostname either use `allowed_hosts=["*"]` or omit the middleware.
* `www_redirect` - If set to True, requests to non-www versions of the allowed hosts will be redirected to their www counterparts. Defaults to `True`.

If an incoming request does not validate correctly then a `400` response will be sent.

## `GZipMiddleware` { #gzipmiddleware }

Handles GZip responses for any request that includes `"gzip"` in the `Accept-Encoding` header.

The middleware will handle both standard and streaming responses.

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

The following arguments are supported:

* `minimum_size` - Do not GZip responses that are smaller than this minimum size in bytes. Defaults to `500`.
* `compresslevel` - Used during GZip compression. It is an integer ranging from 1 to 9. Defaults to `9`. Lower value results in faster compression but larger file sizes, while higher value results in slower compression but smaller file sizes.

## Other middlewares { #other-middlewares }

There are many other ASGI middlewares.

For example:

* [Uvicorn's `ProxyHeadersMiddleware`](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)
* [MessagePack](https://github.com/florimondmanca/msgpack-asgi)

To see other available middlewares check [Starlette's Middleware docs](https://www.starlette.dev/middleware/) and the [ASGI Awesome List](https://github.com/florimondmanca/awesome-asgi).

## Custom Middleware Examples { #custom-middleware-examples }

The following examples demonstrate common middleware patterns used in production FastAPI applications. Each middleware is self-contained and can be added directly to your application.

### Timing Middleware { #timing-middleware }

Track how long each request takes to process. The elapsed time is added as an `X-Process-Time` response header, which is useful for performance monitoring and APM tools.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Measure request processing time and expose it via response header.

    The header value is in seconds (float), e.g. 0.023 for 23 milliseconds.
    Compatible with Prometheus, Datadog, and most APM agents.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response
```

You can read this header in your frontend or monitoring system:

```python
# Client-side example
import httpx

async with httpx.AsyncClient() as client:
    r = await client.get("http://localhost:8000/items/")
    print(f"Server processing time: {r.headers['x-process-time']}s")
```

### Request ID Middleware { #request-id-middleware }

Assign a unique identifier to every incoming request. This is essential for distributed tracing across microservices and for correlating log entries.

```python
import uuid
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Assign a UUID4 request ID to every request.

    The ID is available in:
    - request.state.request_id (accessible in route handlers and dependencies)
    - X-Request-ID response header (returned to the client)

    Usage in a route handler:
        @app.get("/items/")
        async def get_items(request: Request):
            rid = request.state.request_id
            logger.info("Handling request", extra={"request_id": rid})
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

/// tip

If the client sends an `X-Request-ID` header (e.g., from a load balancer), you can honour it:

```python
request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
```

///

### Rate Limiting Middleware { #rate-limiting-middleware }

A simple in-memory rate limiter that restricts each IP address to a configurable number of requests per time window. For production use, replace the in-memory store with Redis.

```python
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuration
RATE_LIMIT_REQUESTS = 100   # Max requests
RATE_LIMIT_WINDOW = 60      # Per 60 seconds

# In-memory store: {ip: [timestamp, timestamp, ...]}
_request_counts: dict[str, list[float]] = defaultdict(list)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Sliding window rate limiter per client IP address.

    Returns HTTP 429 Too Many Requests when the limit is exceeded.
    Adds X-RateLimit-* headers to all responses for client awareness.

    For production: replace _request_counts with a Redis-backed solution
    (e.g., slowapi library or a custom Redis INCR + EXPIRE approach).
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    # Remove timestamps outside the current window
    _request_counts[client_ip] = [
        ts for ts in _request_counts[client_ip] if ts > window_start
    ]

    request_count = len(_request_counts[client_ip])

    if request_count >= RATE_LIMIT_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."},
            headers={
                "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(RATE_LIMIT_WINDOW),
            },
        )

    _request_counts[client_ip].append(now)
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(
        RATE_LIMIT_REQUESTS - request_count - 1
    )
    return response
```

### Combining Multiple Middlewares { #combining-multiple-middlewares }

Middlewares are applied in reverse registration order (last registered = outermost). Here is a recommended ordering:

```python
from fastapi import FastAPI

app = FastAPI()

# Order matters: add_request_id runs first (outermost),
# rate_limit_middleware runs second,
# add_process_time_header runs last (innermost, closest to the route handler).

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header_dispatch)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_dispatch)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_request_id_dispatch)
```

/// warning | Performance note

Each `BaseHTTPMiddleware` layer adds a small overhead due to Python async context switching. For high-throughput applications (> 1000 req/s), consider using Starlette's `@app.middleware("http")` decorator or pure ASGI middleware for the most performance-critical layers.

///

### Accessing Middleware State in Route Handlers { #accessing-middleware-state-in-route-handlers }

State set on `request.state` in middleware is accessible throughout the entire request lifecycle:

```python
from fastapi import FastAPI, Request
import uuid

app = FastAPI()


@app.middleware("http")
async def set_request_context(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    request.state.user_agent = request.headers.get("user-agent", "unknown")
    return await call_next(request)


@app.get("/debug")
async def debug_endpoint(request: Request):
    return {
        "request_id": request.state.request_id,
        "user_agent": request.state.user_agent,
    }
```

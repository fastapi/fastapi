import time

from fastapi import APIRouter, FastAPI

# Setup Router
app = FastAPI()
router = APIRouter()

# 50 Static Routes
for i in range(50):

    @router.get(f"/static-{i}")
    def static_route(i=i):
        return {"route": f"static-{i}"}


# 50 Dynamic Routes
for i in range(50):

    @router.get(f"/dynamic-{i}/{{item_id}}")
    def dynamic_route(item_id: int, i=i):
        return {"route": f"dynamic-{i}", "item_id": item_id}


app.include_router(router)
from contextlib import AsyncExitStack

import anyio


# Mock ASGI stack
async def mock_receive():
    return {"type": "http.request", "body": b"", "more_body": False}


async def mock_send(message):
    pass


scope_static = {
    "type": "http",
    "method": "GET",
    "path": "/static-49",
    "headers": [],
    "query_string": b"",
    "client": ("127.0.0.1", 1234),
    "server": ("127.0.0.1", 80),
    "fastapi_middleware_astack": AsyncExitStack(),
    "fastapi_inner_astack": AsyncExitStack(),
    "fastapi_function_astack": AsyncExitStack(),
}

scope_dynamic = {
    "type": "http",
    "method": "GET",
    "path": "/dynamic-49/12345",
    "headers": [],
    "query_string": b"",
    "client": ("127.0.0.1", 1234),
    "server": ("127.0.0.1", 80),
    "fastapi_middleware_astack": AsyncExitStack(),
    "fastapi_inner_astack": AsyncExitStack(),
    "fastapi_function_astack": AsyncExitStack(),
}


async def run_benchmark():
    # Warmup
    for _ in range(100):
        await app.router.app(dict(scope_static), mock_receive, mock_send)
        await app.router.app(dict(scope_dynamic), mock_receive, mock_send)

    print("Running Static Route Benchmark (10,000 iterations)...")

    # 1. Caching Enabled (standard flow)
    # Warmup cache
    await app.router.app(dict(scope_static), mock_receive, mock_send)
    start_time = time.perf_counter()
    for _ in range(10000):
        await app.router.app(dict(scope_static), mock_receive, mock_send)
    cache_enabled_time = time.perf_counter() - start_time

    # 2. Caching Disabled (clear cache before each request)
    start_time = time.perf_counter()
    for _ in range(10000):
        app.router._route_cache.clear()
        await app.router.app(dict(scope_static), mock_receive, mock_send)
    cache_disabled_time = time.perf_counter() - start_time

    print(f"Static Route - Cache Enabled:  {cache_enabled_time:.4f} seconds")
    print(f"Static Route - Cache Disabled: {cache_disabled_time:.4f} seconds")
    print(f"Speedup: {cache_disabled_time / cache_enabled_time:.2f}x")

    print("\nRunning Dynamic Route Benchmark (10,000 iterations)...")

    # Caching has no effect on dynamic routes
    start_time = time.perf_counter()
    for _ in range(10000):
        await app.router.app(dict(scope_dynamic), mock_receive, mock_send)
    dynamic_time = time.perf_counter() - start_time
    print(f"Dynamic Route time: {dynamic_time:.4f} seconds")


if __name__ == "__main__":
    anyio.run(run_benchmark)

import sys
import threading
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.routing import _IncludedRouter
from fastapi.testclient import TestClient

N_ROUTES = 120
N_THREADS = 6


def build_app() -> FastAPI:
    app = FastAPI()
    router = APIRouter()
    for i in range(N_ROUTES):

        def endpoint(i: int = i) -> dict[str, int]:
            return {"i": i}

        router.add_api_route(f"/r{i}", endpoint, methods=["GET"])
    app.include_router(router)
    return app


def test_concurrent_first_requests_do_not_corrupt_candidate_cache() -> None:
    app = build_app()
    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-5)
    try:
        barrier = threading.Barrier(N_THREADS)
        statuses: list[int] = []

        def worker() -> None:
            client = TestClient(app)
            barrier.wait()
            statuses.append(client.get(f"/r{N_ROUTES - 1}").status_code)

        threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    finally:
        sys.setswitchinterval(old_interval)

    assert statuses == [200] * N_THREADS
    included = next(
        route for route in app.router.routes if isinstance(route, _IncludedRouter)
    )
    assert len(included.effective_candidates()) == N_ROUTES


def get_included_router(app: FastAPI) -> _IncludedRouter:
    return next(
        route for route in app.router.routes if isinstance(route, _IncludedRouter)
    )


class StampCacheOnEnter:
    """Lock stand-in simulating another thread finishing the rebuild first.

    Entering the lock stamps the cache and its version, the same state a
    waiting thread observes after losing the rebuild race.
    """

    def __init__(
        self,
        included: _IncludedRouter,
        list_attr: str,
        version_attr: str,
        cache: list,
    ) -> None:
        self.included = included
        self.list_attr = list_attr
        self.version_attr = version_attr
        self.cache = cache

    def __enter__(self) -> None:
        version = self.included.original_router._get_routes_version()
        setattr(self.included, self.list_attr, self.cache)
        setattr(self.included, self.version_attr, version)

    def __exit__(self, *args: Any) -> None:
        return None


def test_candidates_rebuilt_while_waiting_for_lock_are_reused() -> None:
    app = FastAPI()
    router = APIRouter()
    router.add_api_route("/a", lambda: {}, methods=["GET"])
    app.include_router(router)
    included = get_included_router(app)
    cache: list = []
    included._rebuild_lock = StampCacheOnEnter(  # type: ignore[assignment]
        included, "_effective_candidates", "_effective_candidates_version", cache
    )
    assert included.effective_candidates() is cache


def test_low_priority_routes_rebuilt_while_waiting_for_lock_are_reused() -> None:
    app = FastAPI()
    router = APIRouter()
    router.add_api_route("/a", lambda: {}, methods=["GET"])
    app.include_router(router)
    included = get_included_router(app)
    cache: list = []
    included._rebuild_lock = StampCacheOnEnter(  # type: ignore[assignment]
        included,
        "_effective_low_priority_routes",
        "_effective_low_priority_routes_version",
        cache,
    )
    assert included.effective_low_priority_routes() is cache

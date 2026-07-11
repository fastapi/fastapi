import sys
import threading

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

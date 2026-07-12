"""Test thread safety of _IncludedRouter cache rebuild."""

import sys
import threading

from fastapi import APIRouter, FastAPI
from fastapi.routing import _IncludedRouter
from fastapi.testclient import TestClient


def test_effective_candidates_thread_safety():
    """Verify concurrent cache rebuilds don't produce duplicate candidates."""
    N_ROUTES = 120
    N_THREADS = 6

    app = FastAPI()
    router = APIRouter()
    for i in range(N_ROUTES):

        def endpoint(i: int = i):
            return {"i": i}

        router.add_api_route(f"/r{i}", endpoint, methods=["GET"])
    app.include_router(router)

    sys.setswitchinterval(1e-5)  # widen the rebuild window
    barrier = threading.Barrier(N_THREADS)
    errors = []

    def worker(idx: int):
        try:
            client = TestClient(app)
            barrier.wait()
            resp = client.get(f"/r{N_ROUTES - 1}")
            if resp.status_code != 200:
                errors.append(f"Thread {idx}: got {resp.status_code}")
        except Exception as e:
            errors.append(f"Thread {idx}: {e}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Errors during concurrent requests: {errors}"

    included = next(r for r in app.router.routes if isinstance(r, _IncludedRouter))
    n_candidates = len(included._effective_candidates)
    assert n_candidates == N_ROUTES, (
        f"Expected {N_ROUTES} cached candidates, got {n_candidates}"
    )


def test_effective_low_priority_thread_safety():
    """Verify concurrent low-priority route rebuilds don't duplicate."""
    N_ROUTES = 50
    N_THREADS = 4

    app = FastAPI()
    router = APIRouter()
    for i in range(N_ROUTES):

        def endpoint(i: int = i):
            return {"i": i}

        router.add_api_route(
            f"/r{i}", endpoint, methods=["GET"], include_in_schema=False
        )
    app.include_router(router)

    sys.setswitchinterval(1e-5)
    barrier = threading.Barrier(N_THREADS)
    errors = []

    def worker(idx: int):
        try:
            client = TestClient(app)
            barrier.wait()
            # Access low priority routes indirectly
            resp = client.get("/openapi.json")
            if resp.status_code != 200:
                errors.append(f"Thread {idx}: got {resp.status_code}")
        except Exception as e:
            errors.append(f"Thread {idx}: {e}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Errors during concurrent requests: {errors}"


if __name__ == "__main__":
    test_effective_candidates_thread_safety()
    print("PASS: effective_candidates thread safety")
    test_effective_low_priority_thread_safety()
    print("PASS: effective_low_priority_routes thread safety")

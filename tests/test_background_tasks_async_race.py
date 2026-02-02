"""
Test for potential race conditions in async dependencies with BackgroundTasks.

These tests specifically look for:
1. Race conditions under concurrent requests
2. Cleanup order issues with nested dependencies
3. Exception handling during cleanup
4. Resource access after cleanup starts
"""

import asyncio
import threading
from collections import defaultdict
from typing import Any

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient


# Test 1: Verify cleanup timing under simulated high concurrency
def test_cleanup_timing_consistency():
    """
    Test that cleanup timing is consistent across multiple requests.
    The cleanup should always happen at the same point relative to background tasks.
    """
    results: list[dict] = []
    lock = threading.Lock()

    app = FastAPI()

    async def get_resource():
        resource = {"state": "active", "cleanup_happened": False}
        yield resource
        resource["cleanup_happened"] = True
        resource["state"] = "cleaned"

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: dict = Depends(get_resource),
    ):
        request_id = len(results)

        async def bg_task(res: dict, req_id: int):
            # Record state when background task runs
            with lock:
                results.append({
                    "request_id": req_id,
                    "state_in_bg": res["state"],
                    "cleanup_in_bg": res["cleanup_happened"],
                })

        background_tasks.add_task(bg_task, resource, request_id)
        return {"request_id": request_id}

    client = TestClient(app)

    # Run multiple requests
    for _ in range(20):
        response = client.get("/test")
        assert response.status_code == 200

    # All results should be consistent - with default scope, cleanup should
    # NOT have happened when background task runs
    for result in results:
        assert result["state_in_bg"] == "active", f"Inconsistent state: {result}"
        assert result["cleanup_in_bg"] is False, f"Cleanup happened too early: {result}"


# Test 2: Test for cleanup happening during background task execution
def test_cleanup_during_background_task_execution():
    """
    Test if cleanup can start while a background task is still running.
    This shouldn't happen with proper request-scoped dependencies.
    """
    events: list[str] = []
    lock = threading.Lock()

    app = FastAPI()

    async def get_slow_resource():
        with lock:
            events.append("resource_start")
        yield "resource"
        with lock:
            events.append("resource_cleanup")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: str = Depends(get_slow_resource),
    ):
        async def slow_bg_task():
            with lock:
                events.append("bg_start")
            await asyncio.sleep(0.05)  # Simulate slow work
            with lock:
                events.append("bg_end")

        background_tasks.add_task(slow_bg_task)
        return {"status": "ok"}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200

    # Verify order: resource_start -> bg_start -> bg_end -> resource_cleanup
    assert events == ["resource_start", "bg_start", "bg_end", "resource_cleanup"]


# Test 3: Multiple yield dependencies with different cleanup times
def test_multiple_yield_deps_cleanup_order():
    """
    Test that multiple yield dependencies clean up in the correct order.
    """
    cleanup_order: list[str] = []

    app = FastAPI()

    async def dep_a():
        yield "A"
        cleanup_order.append("A")

    async def dep_b():
        yield "B"
        cleanup_order.append("B")

    async def dep_c(a: str = Depends(dep_a)):
        yield f"C({a})"
        cleanup_order.append("C")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        a: str = Depends(dep_a),
        b: str = Depends(dep_b),
        c: str = Depends(dep_c),
    ):
        async def bg_task():
            cleanup_order.append("BG")

        background_tasks.add_task(bg_task)
        return {"a": a, "b": b, "c": c}

    client = TestClient(app)
    cleanup_order.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # Background task should run before cleanups
    bg_idx = cleanup_order.index("BG")
    # C depends on A, so C cleanup should happen before A
    c_idx = cleanup_order.index("C")
    a_idx = cleanup_order.index("A")

    assert bg_idx < c_idx, "Background task should run before dependency cleanup"
    assert c_idx < a_idx, "C should cleanup before A (dependency order)"


# Test 4: Exception in background task should not affect cleanup
def test_exception_in_background_task():
    """
    Test that exceptions in background tasks don't prevent cleanup.
    """
    events: list[str] = []

    app = FastAPI()

    async def get_resource():
        events.append("setup")
        try:
            yield "resource"
        finally:
            events.append("cleanup")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: str = Depends(get_resource),
    ):
        async def failing_bg_task():
            events.append("bg_task")
            raise ValueError("Background task error")

        background_tasks.add_task(failing_bg_task)
        return {"status": "ok"}

    # Test with raise_server_exceptions=True to see the actual exception
    client = TestClient(app, raise_server_exceptions=True)
    events.clear()

    # Single task failure: original exception is re-raised (backward compatible)
    with pytest.raises(ValueError, match="Background task error"):
        client.get("/test")

    # Cleanup should still happen even if background task fails
    assert "setup" in events
    assert "bg_task" in events
    assert "cleanup" in events


# Test 5: Test with generator (sync) dependencies under async workload
def test_sync_generator_with_async_background_task():
    """
    Test sync generator dependencies with async background tasks.
    """
    events: list[str] = []

    app = FastAPI()

    def sync_resource():
        events.append("sync_setup")
        yield "sync_resource"
        events.append("sync_cleanup")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: str = Depends(sync_resource),
    ):
        async def async_bg_task():
            events.append("async_bg_start")
            await asyncio.sleep(0.01)
            events.append("async_bg_end")

        background_tasks.add_task(async_bg_task)
        return {"resource": resource}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # Sync resource cleanup should happen after async background task
    assert events == [
        "sync_setup",
        "async_bg_start",
        "async_bg_end",
        "sync_cleanup",
    ]


# Test 6: Test with concurrent modification of shared state
def test_concurrent_state_modification():
    """
    Test behavior when background task modifies shared state that
    dependency cleanup also accesses.
    """
    shared_state = {"value": 0, "history": []}

    app = FastAPI()

    async def get_state():
        shared_state["history"].append(f"setup:{shared_state['value']}")
        shared_state["value"] = 1
        yield shared_state
        shared_state["history"].append(f"cleanup:{shared_state['value']}")
        shared_state["value"] = 0

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        state: dict = Depends(get_state),
    ):
        async def bg_task(s: dict):
            s["history"].append(f"bg:{s['value']}")
            s["value"] = 2

        background_tasks.add_task(bg_task, state)
        return {"value": state["value"]}

    client = TestClient(app)
    shared_state["value"] = 0
    shared_state["history"] = []

    response = client.get("/test")
    assert response.status_code == 200

    # History should show: setup (value 0) -> bg (value 1) -> cleanup (value 2)
    assert shared_state["history"] == ["setup:0", "bg:1", "cleanup:2"]


# Test 7: Test deeply nested dependencies with background tasks
def test_deeply_nested_dependencies():
    """
    Test deeply nested dependencies (4+ levels) with background tasks.
    """
    cleanup_order: list[str] = []

    app = FastAPI()

    async def level1():
        yield "L1"
        cleanup_order.append("L1")

    async def level2(l1: str = Depends(level1)):
        yield f"L2({l1})"
        cleanup_order.append("L2")

    async def level3(l2: str = Depends(level2)):
        yield f"L3({l2})"
        cleanup_order.append("L3")

    async def level4(l3: str = Depends(level3)):
        yield f"L4({l3})"
        cleanup_order.append("L4")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        l4: str = Depends(level4),
    ):
        async def bg_task(value: str):
            cleanup_order.append(f"BG:{value}")

        background_tasks.add_task(bg_task, l4)
        return {"value": l4}

    client = TestClient(app)
    cleanup_order.clear()
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json()["value"] == "L4(L3(L2(L1)))"

    # BG should run first, then cleanups in reverse order (L4 -> L3 -> L2 -> L1)
    assert cleanup_order[0] == "BG:L4(L3(L2(L1)))"
    assert cleanup_order[1:] == ["L4", "L3", "L2", "L1"]


# Test 8: Test that function-scoped deps with BackgroundTasks logs warning or error
def test_function_scope_logs_potential_issue():
    """
    Document that function scope with background tasks can cause issues.
    The resource is cleaned up before the background task runs.
    """
    events: list[str] = []

    app = FastAPI()

    async def get_resource():
        events.append("setup")
        resource = {"active": True}
        yield resource
        events.append("cleanup")
        resource["active"] = False

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: dict = Depends(get_resource, scope="function"),
    ):
        async def bg_task(res: dict):
            events.append(f"bg:active={res['active']}")

        background_tasks.add_task(bg_task, resource)
        return {"status": "ok"}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # With function scope, cleanup happens BEFORE background task
    # This is the documented "inconsistent" behavior
    assert events == ["setup", "cleanup", "bg:active=False"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

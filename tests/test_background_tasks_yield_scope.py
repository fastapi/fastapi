"""
Test for async dependencies with cleanup (yield) and BackgroundTasks interaction.

This tests the scenario where dependencies with cleanup logic (yield) may behave
inconsistently when used inside BackgroundTasks under different scope settings.

The key issue:
- Dependencies with scope="function" have cleanup run BEFORE BackgroundTasks execute
- Dependencies with scope="request" (default) have cleanup run AFTER BackgroundTasks execute

This can lead to inconsistent behavior where a resource is cleaned up before
a background task that depends on it has a chance to run.
"""

import asyncio
from typing import Any

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.testclient import TestClient


# Track cleanup and background task execution order
execution_log: list[str] = []


def reset_log():
    execution_log.clear()


# Test 1: Default scope (request) - cleanup should happen AFTER background task
def test_background_task_with_request_scope_yield_dependency():
    """
    With default (request) scope, dependency cleanup should happen AFTER
    the background task completes.
    """
    reset_log()
    app = FastAPI()
    resource_value = {"status": "initialized"}

    async def get_resource():
        execution_log.append("resource_setup")
        resource_value["status"] = "active"
        yield resource_value
        execution_log.append("resource_cleanup")
        resource_value["status"] = "cleaned_up"

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: dict = Depends(get_resource),
    ):
        async def bg_task(res: dict):
            execution_log.append(f"bg_task_start:status={res['status']}")
            await asyncio.sleep(0.01)  # Simulate async work
            execution_log.append(f"bg_task_end:status={res['status']}")

        background_tasks.add_task(bg_task, resource)
        return {"status": resource["status"]}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

    # Verify order: setup -> bg_task -> cleanup
    assert execution_log == [
        "resource_setup",
        "bg_task_start:status=active",
        "bg_task_end:status=active",
        "resource_cleanup",
    ]


# Test 2: Function scope - cleanup happens BEFORE background task (BUG!)
def test_background_task_with_function_scope_yield_dependency():
    """
    With scope="function", dependency cleanup happens BEFORE the background task,
    which is inconsistent and potentially problematic.

    This test demonstrates the issue: the resource is cleaned up before
    the background task runs, so the background task sees the cleaned up state.
    """
    reset_log()
    app = FastAPI()
    resource_value = {"status": "initialized"}

    async def get_resource():
        execution_log.append("resource_setup")
        resource_value["status"] = "active"
        yield resource_value
        execution_log.append("resource_cleanup")
        resource_value["status"] = "cleaned_up"

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        resource: dict = Depends(get_resource, scope="function"),
    ):
        async def bg_task(res: dict):
            execution_log.append(f"bg_task_start:status={res['status']}")
            await asyncio.sleep(0.01)
            execution_log.append(f"bg_task_end:status={res['status']}")

        background_tasks.add_task(bg_task, resource)
        return {"status": resource["status"]}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

    # With function scope, cleanup happens BEFORE background task runs
    # This is the inconsistent behavior!
    assert execution_log == [
        "resource_setup",
        "resource_cleanup",  # Cleanup happens first!
        "bg_task_start:status=cleaned_up",  # BG task sees cleaned up state
        "bg_task_end:status=cleaned_up",
    ]


# Test 3: Database-like connection scenario with function scope
def test_database_connection_closed_before_background_task():
    """
    Simulates a real-world scenario where a database connection is closed
    before a background task that needs it runs.
    """
    reset_log()
    app = FastAPI()

    class FakeDBConnection:
        def __init__(self):
            self.is_open = False
            self.data = []

        def open(self):
            self.is_open = True
            execution_log.append("db_opened")

        def close(self):
            self.is_open = False
            execution_log.append("db_closed")

        def query(self):
            if not self.is_open:
                execution_log.append("db_query_failed:connection_closed")
                raise RuntimeError("Connection closed")
            execution_log.append("db_query_success")
            return {"result": "data"}

    db = FakeDBConnection()

    async def get_db():
        db.open()
        yield db
        db.close()

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        conn: FakeDBConnection = Depends(get_db, scope="function"),
    ):
        async def bg_task(connection: FakeDBConnection):
            try:
                result = connection.query()
                execution_log.append(f"bg_task_got_result")
            except RuntimeError as e:
                execution_log.append(f"bg_task_error:{e}")

        background_tasks.add_task(bg_task, conn)
        return {"status": "task_queued"}

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/test")
    assert response.status_code == 200

    # The background task fails because connection was closed before it ran
    assert "db_closed" in execution_log
    assert execution_log.index("db_closed") < execution_log.index("db_query_failed:connection_closed")


# Test 4: Nested dependencies with mixed scopes
def test_nested_dependencies_mixed_scopes():
    """
    Test nested dependencies where outer has request scope and inner has function scope.
    """
    reset_log()
    app = FastAPI()

    async def outer_resource():
        execution_log.append("outer_setup")
        yield "outer_active"
        execution_log.append("outer_cleanup")

    async def inner_resource(outer: str = Depends(outer_resource)):
        execution_log.append(f"inner_setup:outer={outer}")
        yield f"inner_active:outer={outer}"
        execution_log.append("inner_cleanup")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        inner: str = Depends(inner_resource, scope="function"),
    ):
        async def bg_task(value: str):
            execution_log.append(f"bg_task:{value}")

        background_tasks.add_task(bg_task, inner)
        return {"value": inner}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200

    # Check execution order - inner cleanup should happen before outer
    # and before background task due to function scope
    print("Execution log:", execution_log)
    assert "inner_cleanup" in execution_log
    assert "outer_cleanup" in execution_log


# Test 5: Multiple background tasks with function scope dependency
def test_multiple_background_tasks_function_scope():
    """
    Multiple background tasks all trying to use a function-scoped dependency.
    """
    reset_log()
    app = FastAPI()
    counter = {"value": 0}

    async def get_counter():
        counter["value"] = 1
        execution_log.append("counter_setup")
        yield counter
        execution_log.append("counter_cleanup")
        counter["value"] = 0

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        cnt: dict = Depends(get_counter, scope="function"),
    ):
        async def increment(c: dict):
            execution_log.append(f"increment:value={c['value']}")
            c["value"] += 1

        background_tasks.add_task(increment, cnt)
        background_tasks.add_task(increment, cnt)
        background_tasks.add_task(increment, cnt)
        return {"initial_value": cnt["value"]}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"initial_value": 1}

    # Check that cleanup happened before background tasks ran
    cleanup_idx = execution_log.index("counter_cleanup")
    increment_indices = [
        i for i, log in enumerate(execution_log) if log.startswith("increment")
    ]

    # With function scope, cleanup happens before all increments
    assert all(cleanup_idx < idx for idx in increment_indices)


# Test 6: Async workload with concurrent requests
def test_concurrent_requests_with_yield_dependencies():
    """
    Test behavior under concurrent async workload.
    """
    reset_log()
    app = FastAPI()
    shared_state = {"active_connections": 0, "max_connections": 0}

    async def get_connection():
        shared_state["active_connections"] += 1
        shared_state["max_connections"] = max(
            shared_state["max_connections"], shared_state["active_connections"]
        )
        execution_log.append(f"conn_open:active={shared_state['active_connections']}")
        yield shared_state["active_connections"]
        shared_state["active_connections"] -= 1
        execution_log.append(f"conn_close:active={shared_state['active_connections']}")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        conn_id: int = Depends(get_connection, scope="function"),
    ):
        async def bg_task(id: int):
            await asyncio.sleep(0.01)
            execution_log.append(f"bg_task:conn_id={id}:active={shared_state['active_connections']}")

        background_tasks.add_task(bg_task, conn_id)
        return {"conn_id": conn_id}

    client = TestClient(app)

    # Make a single request first
    response = client.get("/test")
    assert response.status_code == 200

    # Verify that connection was closed before background task ran
    # (due to function scope)
    conn_close_indices = [
        i for i, log in enumerate(execution_log) if log.startswith("conn_close")
    ]
    bg_task_indices = [
        i for i, log in enumerate(execution_log) if log.startswith("bg_task")
    ]

    if conn_close_indices and bg_task_indices:
        # Function scope: close happens before bg_task
        assert conn_close_indices[0] < bg_task_indices[0]


# Test 7: Verify request scope works correctly (control test)
def test_request_scope_preserves_resource_for_background_task():
    """
    Control test: request scope should keep resource active during background task.
    """
    reset_log()
    app = FastAPI()
    resource = {"is_active": False}

    async def get_resource():
        resource["is_active"] = True
        execution_log.append("resource_activated")
        yield resource
        resource["is_active"] = False
        execution_log.append("resource_deactivated")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        res: dict = Depends(get_resource),  # Default request scope
    ):
        async def bg_task(r: dict):
            execution_log.append(f"bg_task:is_active={r['is_active']}")

        background_tasks.add_task(bg_task, res)
        return {"is_active": res["is_active"]}

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200

    # Background task should see is_active=True because cleanup happens after
    assert "bg_task:is_active=True" in execution_log


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

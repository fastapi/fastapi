"""
Test accessing dependencies from within BackgroundTasks.

This tests scenarios where background tasks try to access dependency-provided
resources directly, which can lead to inconsistent behavior if the dependency
has been cleaned up.
"""

import asyncio
from typing import Any

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.testclient import TestClient


# Scenario 1: Background task accessing a resource passed to it
def test_bg_task_with_passed_resource():
    """
    Test that a resource passed to a background task remains valid
    when using default (request) scope.
    """
    events: list[str] = []

    app = FastAPI()

    class DatabaseConnection:
        def __init__(self):
            self.connected = False
            self.queries: list[str] = []

        def connect(self):
            self.connected = True
            events.append("db_connected")

        def disconnect(self):
            self.connected = False
            events.append("db_disconnected")

        def query(self, sql: str) -> str:
            if not self.connected:
                events.append(f"query_failed:{sql}")
                raise RuntimeError("Not connected")
            events.append(f"query_success:{sql}")
            self.queries.append(sql)
            return f"result:{sql}"

    async def get_db():
        db = DatabaseConnection()
        db.connect()
        yield db
        db.disconnect()

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        db: DatabaseConnection = Depends(get_db),
    ):
        async def bg_query(conn: DatabaseConnection):
            # This should work because default scope keeps db alive
            result = conn.query("SELECT * FROM bg_table")
            events.append(f"bg_got:{result}")

        background_tasks.add_task(bg_query, db)
        return {"status": "queued"}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # Verify query succeeded in background task
    assert "db_connected" in events
    assert "query_success:SELECT * FROM bg_table" in events
    assert "bg_got:result:SELECT * FROM bg_table" in events
    assert "db_disconnected" in events

    # Verify order: connect -> query -> disconnect
    connect_idx = events.index("db_connected")
    query_idx = events.index("query_success:SELECT * FROM bg_table")
    disconnect_idx = events.index("db_disconnected")
    assert connect_idx < query_idx < disconnect_idx


# Scenario 2: Background task accessing function-scoped resource (FAILS)
def test_bg_task_with_function_scoped_resource():
    """
    Test that a function-scoped resource is cleaned up before background task runs.
    This demonstrates the potential pitfall of using scope="function" with BackgroundTasks.
    """
    events: list[str] = []

    app = FastAPI()

    class DatabaseConnection:
        def __init__(self):
            self.connected = False

        def connect(self):
            self.connected = True
            events.append("db_connected")

        def disconnect(self):
            self.connected = False
            events.append("db_disconnected")

        def query(self, sql: str) -> str:
            if not self.connected:
                events.append(f"query_failed:{sql}")
                return "ERROR: Not connected"
            events.append(f"query_success:{sql}")
            return f"result:{sql}"

    async def get_db():
        db = DatabaseConnection()
        db.connect()
        yield db
        db.disconnect()

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        db: DatabaseConnection = Depends(get_db, scope="function"),
    ):
        async def bg_query(conn: DatabaseConnection):
            # This will FAIL because function scope cleans up before bg task
            result = conn.query("SELECT * FROM bg_table")
            events.append(f"bg_got:{result}")

        background_tasks.add_task(bg_query, db)
        return {"status": "queued"}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # With function scope, db is disconnected BEFORE bg task runs
    assert "db_connected" in events
    assert "db_disconnected" in events
    assert "query_failed:SELECT * FROM bg_table" in events

    # Verify problematic order: connect -> disconnect -> query_failed
    connect_idx = events.index("db_connected")
    disconnect_idx = events.index("db_disconnected")
    query_idx = events.index("query_failed:SELECT * FROM bg_table")
    assert connect_idx < disconnect_idx < query_idx


# Scenario 3: Multiple concurrent requests with shared mutable state
def test_concurrent_requests_shared_state():
    """
    Test behavior when multiple concurrent requests share mutable state
    through a dependency.
    """
    events: list[str] = []
    request_counter = {"value": 0}

    app = FastAPI()

    async def get_request_id():
        request_counter["value"] += 1
        request_id = request_counter["value"]
        events.append(f"setup:{request_id}")
        yield request_id
        events.append(f"cleanup:{request_id}")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        request_id: int = Depends(get_request_id),
    ):
        async def bg_task(rid: int):
            await asyncio.sleep(0.01)  # Small delay
            events.append(f"bg:{rid}")

        background_tasks.add_task(bg_task, request_id)
        return {"request_id": request_id}

    client = TestClient(app)
    events.clear()
    request_counter["value"] = 0

    # Make multiple sequential requests
    for _ in range(3):
        response = client.get("/test")
        assert response.status_code == 200

    # Verify each request has proper setup -> bg -> cleanup sequence
    # (Note: with default scope, cleanup happens after bg task)
    assert len([e for e in events if e.startswith("setup:")]) == 3
    assert len([e for e in events if e.startswith("bg:")]) == 3
    assert len([e for e in events if e.startswith("cleanup:")]) == 3


# Scenario 4: Nested async generators with background tasks
def test_nested_async_generators_with_bg_tasks():
    """
    Test deeply nested async generators and their interaction with background tasks.
    """
    events: list[str] = []

    app = FastAPI()

    async def outer():
        events.append("outer_start")
        yield "outer"
        events.append("outer_end")

    async def middle(outer_val: str = Depends(outer)):
        events.append(f"middle_start:{outer_val}")
        yield f"middle({outer_val})"
        events.append("middle_end")

    async def inner(middle_val: str = Depends(middle)):
        events.append(f"inner_start:{middle_val}")
        yield f"inner({middle_val})"
        events.append("inner_end")

    @app.get("/test")
    async def endpoint(
        background_tasks: BackgroundTasks,
        value: str = Depends(inner),
    ):
        async def bg_task(val: str):
            events.append(f"bg:{val}")

        background_tasks.add_task(bg_task, value)
        return {"value": value}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json()["value"] == "inner(middle(outer))"

    # Verify setup order: outer -> middle -> inner
    assert events.index("outer_start") < events.index("middle_start:outer")
    assert events.index("middle_start:outer") < events.index("inner_start:middle(outer)")

    # Verify bg task runs before cleanup
    bg_idx = events.index("bg:inner(middle(outer))")
    assert bg_idx < events.index("inner_end")

    # Verify cleanup order (reverse): inner -> middle -> outer
    assert events.index("inner_end") < events.index("middle_end")
    assert events.index("middle_end") < events.index("outer_end")


# Scenario 5: Background task that adds more background tasks
def test_bg_task_adding_more_bg_tasks():
    """
    Test a background task that adds additional background tasks.
    """
    events: list[str] = []

    app = FastAPI()

    async def get_resource():
        events.append("resource_setup")
        yield {"active": True}
        events.append("resource_cleanup")

    @app.get("/test")
    async def endpoint(
        request: Request,
        background_tasks: BackgroundTasks,
        resource: dict = Depends(get_resource),
    ):
        async def first_bg_task(res: dict, tasks: BackgroundTasks):
            events.append(f"first_bg:active={res['active']}")
            # Note: Adding tasks from within a task might not work as expected
            # because the BackgroundTasks object is tied to the response

        async def second_bg_task(res: dict):
            events.append(f"second_bg:active={res['active']}")

        background_tasks.add_task(first_bg_task, resource, background_tasks)
        background_tasks.add_task(second_bg_task, resource)
        return {"status": "ok"}

    client = TestClient(app)
    events.clear()
    response = client.get("/test")
    assert response.status_code == 200

    # Both background tasks should see active=True (default scope)
    assert "first_bg:active=True" in events
    assert "second_bg:active=True" in events
    assert "resource_cleanup" in events


# Scenario 6: Error in one background task doesn't affect others
def test_error_in_one_bg_task_others_continue():
    """
    Test that an error in one background task doesn't prevent cleanup or other tasks.
    Note: Cleanup code MUST be in a finally block to run when exceptions occur.

    With the fix, all tasks run even if one fails.
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
        async def failing_task():
            events.append("failing_start")
            raise ValueError("Task failed")

        async def succeeding_task():
            events.append("succeeding")

        background_tasks.add_task(failing_task)
        background_tasks.add_task(succeeding_task)
        return {"status": "ok"}

    client = TestClient(app, raise_server_exceptions=True)
    events.clear()

    # Single task failure: original exception re-raised (backward compatible)
    with pytest.raises(ValueError, match="Task failed"):
        client.get("/test")

    # Cleanup should still happen
    assert "setup" in events
    assert "failing_start" in events
    assert "cleanup" in events
    # FIXED: Second task now runs even though first task failed
    assert "succeeding" in events


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

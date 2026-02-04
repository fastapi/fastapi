"""
Tests reproducing actual bugs related to BackgroundTasks and yield dependencies.

Based on GitHub issues:
1. #14137 - Background tasks added after yield not executed
2. Starlette #2640 - If first background task fails, remaining tasks don't run
3. Starlette #1438 - Background tasks cancelled on client disconnect
"""

import asyncio
import logging
from typing import Generator

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.testclient import TestClient


class TestBackgroundTasksAfterYield:
    """
    Bug: Background tasks added after yield are not executed.

    When code after `yield` in a dependency adds a background task,
    that task is silently ignored because the response cycle has completed.
    """

    def test_bg_task_added_before_yield_executes(self):
        """Control test: tasks added before yield should execute."""
        executed = []

        app = FastAPI()

        async def dependency_with_yield(background_tasks: BackgroundTasks):
            background_tasks.add_task(lambda: executed.append("before_yield"))
            yield "value"

        @app.get("/test")
        async def endpoint(dep: str = Depends(dependency_with_yield)):
            return {"dep": dep}

        client = TestClient(app)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200
        assert "before_yield" in executed

    def test_bg_task_added_after_yield_warns_and_not_executed(self, caplog):
        """
        FIXED: Tasks added after yield now log a warning instead of being silently dropped.

        Previously, this was a silent failure. Now users get a clear warning
        explaining why the task won't run.
        """
        executed = []

        app = FastAPI()

        async def dependency_with_yield(background_tasks: BackgroundTasks):
            executed.append("before_yield")
            yield "value"
            # This code runs during cleanup
            executed.append("after_yield_code_runs")
            # Now this logs a warning instead of silently failing
            background_tasks.add_task(lambda: executed.append("after_yield_task"))

        @app.get("/test")
        async def endpoint(dep: str = Depends(dependency_with_yield)):
            return {"dep": dep}

        client = TestClient(app)
        executed.clear()

        with caplog.at_level(logging.WARNING, logger="fastapi.background"):
            response = client.get("/test")

        assert response.status_code == 200

        # The code after yield runs...
        assert "after_yield_code_runs" in executed
        # ...the background task does NOT execute (as before)
        assert "after_yield_task" not in executed
        # BUT now we get a log warning about it (FIX!)
        assert any(
            "Background task added after tasks have already been executed" in r.message
            for r in caplog.records
        )


class TestBackgroundTaskFailureCascade:
    """
    Bug: If first background task fails, remaining tasks don't run.

    From Starlette Discussion #2640: When one background task raises
    an exception, subsequent tasks in the queue are skipped.
    """

    def test_first_task_failure_does_not_stop_remaining_tasks(self):
        """
        FIXED: Remaining tasks now run even if an earlier task fails.

        Previously, if the first task failed, subsequent tasks wouldn't run.
        With the fix, all tasks are attempted regardless of earlier failures.
        """
        executed = []

        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def failing_task():
                executed.append("task1_start")
                raise ValueError("Task 1 failed")

            async def task2():
                executed.append("task2_executed")

            async def task3():
                executed.append("task3_executed")

            background_tasks.add_task(failing_task)
            background_tasks.add_task(task2)
            background_tasks.add_task(task3)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        executed.clear()
        response = client.get("/test")

        # Response succeeds because error happens in background
        assert response.status_code == 200

        # First task starts
        assert "task1_start" in executed

        # FIXED: task2 and task3 now execute even though task1 failed
        assert "task2_executed" in executed
        assert "task3_executed" in executed

    def test_independent_tasks_all_run(self):
        """
        FIXED: Independent tasks now all run regardless of others failing.

        With the fix, task3 runs even though the preceding task failed.
        """
        executed = []

        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def task1():
                executed.append("task1")

            async def failing_task():
                executed.append("failing_start")
                raise ValueError("I failed")

            async def task3():
                executed.append("task3")

            background_tasks.add_task(task1)
            background_tasks.add_task(failing_task)
            background_tasks.add_task(task3)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Task 1 runs
        assert "task1" in executed
        # Failing task starts
        assert "failing_start" in executed
        # FIXED: Task 3 now runs even though the preceding task failed
        assert "task3" in executed


class TestDependencyCleanupWithFailingTasks:
    """
    Test that dependency cleanup happens even when background tasks fail.
    """

    def test_cleanup_happens_despite_bg_task_failure(self):
        """
        Verify that yield dependency cleanup runs even if a background task fails.
        """
        events = []

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
                events.append("task_start")
                raise ValueError("Task failed")

            background_tasks.add_task(failing_task)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        events.clear()
        response = client.get("/test")

        # Response should succeed (bg task error is after response)
        assert response.status_code == 200
        assert "setup" in events
        assert "task_start" in events
        # Cleanup should happen even though task failed
        assert "cleanup" in events


class TestCleanupOrderConsistency:
    """
    Test that cleanup order is consistent and predictable.
    """

    def test_cleanup_order_with_multiple_dependencies(self):
        """
        Verify cleanup happens in reverse order of setup.
        """
        events = []

        app = FastAPI()

        async def dep_a():
            events.append("setup_a")
            try:
                yield "A"
            finally:
                events.append("cleanup_a")

        async def dep_b(a: str = Depends(dep_a)):
            events.append("setup_b")
            try:
                yield f"B({a})"
            finally:
                events.append("cleanup_b")

        async def dep_c(b: str = Depends(dep_b)):
            events.append("setup_c")
            try:
                yield f"C({b})"
            finally:
                events.append("cleanup_c")

        @app.get("/test")
        async def endpoint(
            background_tasks: BackgroundTasks,
            c: str = Depends(dep_c),
        ):
            async def bg_task():
                events.append("bg_task")

            background_tasks.add_task(bg_task)
            return {"c": c}

        client = TestClient(app)
        events.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Verify setup order: A -> B -> C
        assert events.index("setup_a") < events.index("setup_b")
        assert events.index("setup_b") < events.index("setup_c")

        # Background task runs after endpoint but before cleanup
        assert events.index("bg_task") > events.index("setup_c")
        assert events.index("bg_task") < events.index("cleanup_c")

        # Verify cleanup order: C -> B -> A (reverse of setup)
        assert events.index("cleanup_c") < events.index("cleanup_b")
        assert events.index("cleanup_b") < events.index("cleanup_a")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

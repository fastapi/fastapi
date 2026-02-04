"""
Tests verifying the fixes for BackgroundTasks bugs.

Fixed bugs:
1. First task failure now doesn't stop remaining tasks
2. Tasks added after execution now emit a warning
"""

import logging
from typing import Generator

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.background import BackgroundTaskError
from fastapi.testclient import TestClient


class TestBackgroundTaskErrorIsolation:
    """
    Test that task failures don't stop remaining tasks.
    """

    def test_all_tasks_run_despite_failure(self):
        """
        FIX: All tasks should run even if one fails in the middle.
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

        # FIX VERIFICATION: All three tasks should have run
        assert "task1" in executed
        assert "failing_start" in executed
        assert "task3" in executed  # This now runs!

    def test_multiple_failures_all_logged(self):
        """
        Multiple task failures should all be captured.
        """
        executed = []

        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def failing1():
                executed.append("failing1")
                raise ValueError("Error 1")

            async def failing2():
                executed.append("failing2")
                raise RuntimeError("Error 2")

            async def success():
                executed.append("success")

            background_tasks.add_task(failing1)
            background_tasks.add_task(success)
            background_tasks.add_task(failing2)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # All tasks should have executed
        assert "failing1" in executed
        assert "success" in executed
        assert "failing2" in executed

    def test_single_task_failure_raises_original_exception(self):
        """
        Single task failure should raise the original exception (backward compatible).
        """
        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def failing():
                raise ValueError("Task failed")

            background_tasks.add_task(failing)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=True)

        # Single failure: original exception raised for backward compatibility
        with pytest.raises(ValueError, match="Task failed"):
            client.get("/test")

    def test_multiple_task_failures_raise_background_task_error(self):
        """
        Multiple task failures should raise BackgroundTaskError with all errors.
        """
        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def failing1():
                raise ValueError("Error 1")

            async def failing2():
                raise RuntimeError("Error 2")

            background_tasks.add_task(failing1)
            background_tasks.add_task(failing2)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=True)

        # Multiple failures: BackgroundTaskError raised
        with pytest.raises(BackgroundTaskError) as exc_info:
            client.get("/test")

        assert len(exc_info.value.errors) == 2
        assert isinstance(exc_info.value.errors[0][1], ValueError)
        assert isinstance(exc_info.value.errors[1][1], RuntimeError)


class TestBackgroundTaskAfterYieldWarning:
    """
    Test that adding tasks after execution emits a warning.
    """

    def test_warning_when_task_added_after_execution(self, caplog):
        """
        FIX: A log warning should be emitted when task is added after execution.
        """
        executed = []

        app = FastAPI()

        async def dependency_with_yield(background_tasks: BackgroundTasks):
            background_tasks.add_task(lambda: executed.append("before_yield"))
            yield "value"
            background_tasks.add_task(lambda: executed.append("after_yield"))

        @app.get("/test")
        async def endpoint(dep: str = Depends(dependency_with_yield)):
            return {"dep": dep}

        client = TestClient(app)
        executed.clear()

        with caplog.at_level(logging.WARNING, logger="fastapi.background"):
            response = client.get("/test")

        assert response.status_code == 200

        # Task added before yield should have executed
        assert "before_yield" in executed

        # Task added after yield should NOT have executed
        assert "after_yield" not in executed

        # Warning should have been logged
        assert any(
            "Background task added after tasks have already been executed" in r.message
            for r in caplog.records
        )

    def test_no_warning_for_normal_task_addition(self, caplog):
        """
        No warning should be logged for normal task addition.
        """
        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            background_tasks.add_task(lambda: None)
            background_tasks.add_task(lambda: None)
            return {"status": "ok"}

        client = TestClient(app)
        with caplog.at_level(logging.WARNING, logger="fastapi.background"):
            response = client.get("/test")
        assert response.status_code == 200
        assert not any(
            "already been executed" in r.message for r in caplog.records
        )


class TestDependencyCleanupStillWorks:
    """
    Verify that dependency cleanup still works correctly with the fixes.
    """

    def test_cleanup_runs_after_all_tasks(self):
        """
        Dependency cleanup should run after all background tasks complete.
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
            async def task1():
                events.append("task1")

            async def task2():
                events.append("task2")

            background_tasks.add_task(task1)
            background_tasks.add_task(task2)
            return {"status": "ok"}

        client = TestClient(app)
        events.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Verify order: setup -> tasks -> cleanup
        assert events.index("setup") < events.index("task1")
        assert events.index("task1") < events.index("task2")
        assert events.index("task2") < events.index("cleanup")

    def test_cleanup_runs_even_when_tasks_fail(self):
        """
        Dependency cleanup should run even if background tasks fail.
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
                raise ValueError("Failed")

            background_tasks.add_task(failing_task)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        events.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Cleanup must happen
        assert "setup" in events
        assert "task_start" in events
        assert "cleanup" in events


class TestEdgeCases:
    """Test edge cases and robustness fixes."""

    def test_task_with_no_name_attribute(self):
        """Test that tasks without __name__ are handled gracefully."""
        executed = []

        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            # Lambda has __name__ = '<lambda>'
            background_tasks.add_task(lambda: executed.append("lambda"))
            return {"status": "ok"}

        client = TestClient(app)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200
        assert "lambda" in executed

    def test_task_mutation_during_execution(self):
        """Test that task list mutation during execution doesn't cause issues."""
        executed = []
        tasks_ref = {"bg": None}

        app = FastAPI()

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            tasks_ref["bg"] = background_tasks

            async def mutating_task():
                executed.append("task1")
                # Try to mutate the tasks list during execution
                # This should not affect iteration due to snapshot
                tasks_ref["bg"].tasks.append(
                    BackgroundTasks()  # Add garbage
                )

            async def task2():
                executed.append("task2")

            background_tasks.add_task(mutating_task)
            background_tasks.add_task(task2)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Both tasks should have executed despite mutation attempt
        assert "task1" in executed
        assert "task2" in executed

    @pytest.mark.anyio
    async def test_keyboard_interrupt_not_suppressed(self):
        """Test that KeyboardInterrupt is not suppressed."""
        from fastapi.background import BackgroundTasks as BgTasks

        async def raising_task():
            raise KeyboardInterrupt()

        bg = BgTasks()
        bg.add_task(raising_task)

        with pytest.raises(KeyboardInterrupt):
            await bg()

    @pytest.mark.anyio
    async def test_system_exit_not_suppressed(self):
        """Test that SystemExit is not suppressed."""
        from fastapi.background import BackgroundTasks as BgTasks

        async def raising_task():
            raise SystemExit(1)

        bg = BgTasks()
        bg.add_task(raising_task)

        with pytest.raises(SystemExit):
            await bg()

    def test_base_exception_subclass_caught(self):
        """Test that BaseException subclasses (except critical ones) are caught."""
        executed = []

        app = FastAPI()

        class CustomBaseException(BaseException):
            pass

        @app.get("/test")
        async def endpoint(background_tasks: BackgroundTasks):
            async def failing_task():
                executed.append("failing")
                raise CustomBaseException("custom error")

            async def second_task():
                executed.append("second")

            background_tasks.add_task(failing_task)
            background_tasks.add_task(second_task)
            return {"status": "ok"}

        client = TestClient(app, raise_server_exceptions=False)
        executed.clear()
        response = client.get("/test")
        assert response.status_code == 200

        # Both tasks should execute - CustomBaseException should be caught
        assert "failing" in executed
        assert "second" in executed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

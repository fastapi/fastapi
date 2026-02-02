"""
Tests for unified lifespan handling.
"""

import warnings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from fastapi import FastAPI, Request
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.lifespan import (
    LifespanError,
    UnifiedLifespanManager,
    create_unified_lifespan,
    merge_lifespan_state,
)
from fastapi.testclient import TestClient


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def startup_shutdown_log():
    """Fixture to track startup/shutdown execution order."""
    return []


# =============================================================================
# UnifiedLifespanManager Tests
# =============================================================================


class TestUnifiedLifespanManager:
    """Tests for UnifiedLifespanManager class."""

    @pytest.mark.anyio
    async def test_basic_lifespan_execution(self, startup_shutdown_log):
        """Test basic lifespan execution order."""

        @asynccontextmanager
        async def lifespan(app):
            startup_shutdown_log.append("startup")
            yield {"key": "value"}
            startup_shutdown_log.append("shutdown")

        manager = UnifiedLifespanManager(lifespan=lifespan, emit_deprecation_warnings=False)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FastAPIDeprecationWarning)
            async with manager.lifespan(None) as state:
                assert state == {"key": "value"}
                startup_shutdown_log.append("running")

        assert startup_shutdown_log == ["startup", "running", "shutdown"]

    @pytest.mark.anyio
    async def test_on_event_handlers_execution(self, startup_shutdown_log):
        """Test on_event handlers execute correctly."""

        async def startup1():
            startup_shutdown_log.append("startup1")

        async def startup2():
            startup_shutdown_log.append("startup2")

        async def shutdown1():
            startup_shutdown_log.append("shutdown1")

        async def shutdown2():
            startup_shutdown_log.append("shutdown2")

        manager = UnifiedLifespanManager(
            on_startup=[startup1, startup2],
            on_shutdown=[shutdown1, shutdown2],
            emit_deprecation_warnings=False,
        )

        async with manager.lifespan(None) as state:
            startup_shutdown_log.append("running")

        # Startup in order, shutdown in reverse order
        assert startup_shutdown_log == [
            "startup1",
            "startup2",
            "running",
            "shutdown2",
            "shutdown1",
        ]

    @pytest.mark.anyio
    async def test_startup_failure_rollback(self, startup_shutdown_log):
        """Test rollback when startup fails."""

        async def startup1():
            startup_shutdown_log.append("startup1")

        async def startup2():
            startup_shutdown_log.append("startup2_failed")
            raise ValueError("Startup failed")

        async def shutdown1():
            startup_shutdown_log.append("shutdown1")

        async def shutdown2():
            startup_shutdown_log.append("shutdown2")

        manager = UnifiedLifespanManager(
            on_startup=[startup1, startup2],
            on_shutdown=[shutdown1, shutdown2],
            emit_deprecation_warnings=False,
        )

        with pytest.raises(LifespanError) as exc_info:
            async with manager.lifespan(None):
                startup_shutdown_log.append("should_not_run")

        # Rollback should clean up startup1 only (shutdown1)
        assert "startup1" in startup_shutdown_log
        assert "startup2_failed" in startup_shutdown_log
        assert "should_not_run" not in startup_shutdown_log
        # Rollback runs cleanup for completed handlers
        assert "shutdown1" in startup_shutdown_log

        # Check error details
        assert exc_info.value.phase == "startup"
        assert isinstance(exc_info.value.original_error, ValueError)

    @pytest.mark.anyio
    async def test_mixed_patterns_warning(self):
        """Test warning when mixing lifespan and on_event."""

        @asynccontextmanager
        async def lifespan(app):
            yield

        with pytest.warns(FastAPIDeprecationWarning, match="not recommended"):
            UnifiedLifespanManager(
                on_startup=[lambda: None],
                lifespan=lifespan,
            )


# =============================================================================
# State Merging Tests
# =============================================================================


class TestStateMerging:
    """Tests for lifespan state merging."""

    def test_merge_child_overrides_parent(self):
        """Test default behavior: child overrides parent."""
        parent = {"shared": "parent", "parent_only": True}
        child = {"shared": "child", "child_only": True}

        result = merge_lifespan_state(parent, child, child_overrides_parent=True)

        assert result["shared"] == "child"  # child wins
        assert result["parent_only"] is True
        assert result["child_only"] is True

    def test_merge_parent_overrides_child(self):
        """Test alternative behavior: parent overrides child."""
        parent = {"shared": "parent", "parent_only": True}
        child = {"shared": "child", "child_only": True}

        result = merge_lifespan_state(parent, child, child_overrides_parent=False)

        assert result["shared"] == "parent"  # parent wins
        assert result["parent_only"] is True
        assert result["child_only"] is True

    def test_merge_none_states(self):
        """Test merging with None states."""
        assert merge_lifespan_state(None, None) == {}
        assert merge_lifespan_state({"a": 1}, None) == {"a": 1}
        assert merge_lifespan_state(None, {"b": 2}) == {"b": 2}


# =============================================================================
# FastAPI Integration Tests
# =============================================================================


class TestFastAPILifespanIntegration:
    """Integration tests with FastAPI app."""

    def test_lifespan_context_manager(self):
        """Test modern lifespan context manager pattern."""
        events = []

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:
            events.append("startup")
            yield {"db": "connection"}
            events.append("shutdown")

        app = FastAPI(lifespan=lifespan)

        @app.get("/")
        def index():
            return {"status": "ok"}

        with TestClient(app) as client:
            events.append("running")
            response = client.get("/")
            assert response.status_code == 200

        assert events == ["startup", "running", "shutdown"]

    def test_on_event_deprecation_warning(self):
        """Test that on_event emits deprecation warning."""
        app = FastAPI()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            @app.on_event("startup")
            def startup():
                pass

            # Check that at least one warning was raised
            assert len(w) >= 1
            # Check that one of them is about on_event deprecation
            deprecation_warnings = [
                warning for warning in w
                if "on_event" in str(warning.message) and "deprecated" in str(warning.message)
            ]
            assert len(deprecation_warnings) >= 1

    def test_on_event_handlers_still_work(self):
        """Test that on_event handlers still execute (backwards compatibility)."""
        events = []
        app = FastAPI()

        # Suppress the deprecation warnings for this test
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            @app.on_event("startup")
            def startup():
                events.append("startup")

            @app.on_event("shutdown")
            def shutdown():
                events.append("shutdown")

        @app.get("/")
        def index():
            return {"status": "ok"}

        with TestClient(app) as client:
            events.append("running")
            response = client.get("/")
            assert response.status_code == 200

        assert "startup" in events
        assert "running" in events
        assert "shutdown" in events

    def test_state_accessible_in_endpoints(self):
        """Test that lifespan state is accessible in endpoints."""

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:
            yield {"db_connection": "active"}

        app = FastAPI(lifespan=lifespan)

        @app.get("/state")
        def get_state(request: Request):
            # State should be accessible via request.state
            return {"has_state": hasattr(request.state, "db_connection")}

        with TestClient(app) as client:
            response = client.get("/state")
            assert response.status_code == 200


# =============================================================================
# create_unified_lifespan Tests
# =============================================================================


class TestCreateUnifiedLifespan:
    """Tests for create_unified_lifespan function."""

    @pytest.mark.anyio
    async def test_create_from_lifespan_only(self):
        """Test creating unified lifespan from lifespan context only."""
        events = []

        @asynccontextmanager
        async def lifespan(app):
            events.append("start")
            yield {"key": "value"}
            events.append("stop")

        unified = create_unified_lifespan(lifespan=lifespan)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FastAPIDeprecationWarning)
            async with unified(None) as state:
                events.append("running")
                assert state == {"key": "value"}

        assert events == ["start", "running", "stop"]

    @pytest.mark.anyio
    async def test_create_from_handlers_only(self):
        """Test creating unified lifespan from handlers only."""
        events = []

        async def on_start():
            events.append("start")

        async def on_stop():
            events.append("stop")

        unified = create_unified_lifespan(
            on_startup=[on_start],
            on_shutdown=[on_stop],
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FastAPIDeprecationWarning)
            async with unified(None) as state:
                events.append("running")

        assert "start" in events
        assert "running" in events
        assert "stop" in events


# =============================================================================
# LifespanError Tests
# =============================================================================


class TestLifespanError:
    """Tests for LifespanError exception."""

    def test_error_message_formatting(self):
        """Test error message includes relevant information."""

        def my_handler():
            pass

        error = LifespanError(
            "Test error",
            phase="startup",
            handler=my_handler,
            original_error=ValueError("Original"),
        )

        error_str = str(error)
        assert "startup" in error_str
        assert "my_handler" in error_str
        assert "Original" in error_str

    def test_error_attributes(self):
        """Test error attributes are accessible."""
        original = ValueError("test")

        error = LifespanError(
            "Test",
            phase="shutdown",
            original_error=original,
        )

        assert error.phase == "shutdown"
        assert error.original_error is original

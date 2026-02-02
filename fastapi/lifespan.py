"""Unified lifespan management for FastAPI."""

import warnings
from collections.abc import AsyncGenerator, Callable, Sequence
from contextlib import asynccontextmanager
from typing import Any, Optional, TypeVar

from starlette.types import ASGIApp, Lifespan

from fastapi.exceptions import FastAPIDeprecationWarning

AppType = TypeVar("AppType", bound="ASGIApp")


class LifespanError(Exception):
    """Exception raised when lifespan handling fails."""

    def __init__(
        self,
        message: str,
        *,
        phase: str,
        handler: Optional[Callable[..., Any]] = None,
        original_error: Optional[BaseException] = None,
    ):
        super().__init__(message)
        self.phase = phase
        self.handler = handler
        self.original_error = original_error

    def __str__(self) -> str:
        base = f"Lifespan {self.phase} failed"
        if self.handler:
            handler_name = getattr(self.handler, "__name__", str(self.handler))
            base += f" in handler '{handler_name}'"
        if self.original_error:
            base += f": {self.original_error}"
        return base


def _emit_on_event_deprecation_warning(event_type: str) -> None:
    warnings.warn(
        f"on_event('{event_type}') is deprecated. Use the lifespan context manager.",
        FastAPIDeprecationWarning,
        stacklevel=4,
    )


class UnifiedLifespanManager:
    """Manages unified lifespan handling with rollback semantics."""

    def __init__(
        self,
        *,
        on_startup: Optional[Sequence[Callable[..., Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
        lifespan: Optional[Lifespan[AppType]] = None,
        emit_deprecation_warnings: bool = True,
    ):
        self._on_startup = list(on_startup or [])
        self._on_shutdown = list(on_shutdown or [])
        self._lifespan = lifespan
        self._emit_warnings = emit_deprecation_warnings
        self._completed_startup_handlers: list[Callable[..., Any]] = []

        if lifespan and (on_startup or on_shutdown):
            warnings.warn(
                "Using both 'lifespan' and 'on_startup'/'on_shutdown' is not recommended.",
                FastAPIDeprecationWarning,
                stacklevel=2,
            )

    @asynccontextmanager
    async def lifespan(self, app: AppType) -> AsyncGenerator[dict[str, Any], None]:
        """Unified lifespan context manager with rollback semantics."""
        state: dict[str, Any] = {}
        self._completed_startup_handlers = []
        lifespan_cm = None

        try:
            await self._execute_startup_handlers()

            if self._lifespan:
                lifespan_cm = self._lifespan(app)
                lifespan_state = await lifespan_cm.__aenter__()
                if lifespan_state:
                    state.update(lifespan_state)

            try:
                yield state
            finally:
                shutdown_errors: list[tuple[str, BaseException]] = []

                if lifespan_cm is not None:
                    try:
                        await lifespan_cm.__aexit__(None, None, None)
                    except Exception as e:
                        shutdown_errors.append(("lifespan context", e))

                handler_errors = await self._execute_shutdown_handlers()
                shutdown_errors.extend(handler_errors)

                if shutdown_errors:
                    error_msgs = [f"{name}: {err}" for name, err in shutdown_errors]
                    warnings.warn(
                        f"Errors during shutdown: {'; '.join(error_msgs)}",
                        RuntimeWarning,
                        stacklevel=2,
                    )

        except BaseException as startup_error:
            await self._rollback_startup(startup_error)
            raise

    async def _execute_startup_handlers(self) -> None:
        for handler in self._on_startup:
            if self._emit_warnings:
                _emit_on_event_deprecation_warning("startup")

            try:
                result = handler()
                if hasattr(result, "__await__"):
                    await result
                self._completed_startup_handlers.append(handler)
            except Exception as e:
                raise LifespanError(
                    f"Startup handler failed",
                    phase="startup",
                    handler=handler,
                    original_error=e,
                ) from e

    async def _execute_shutdown_handlers(self) -> list[tuple[str, BaseException]]:
        errors: list[tuple[str, BaseException]] = []
        for handler in reversed(self._on_shutdown):
            if self._emit_warnings:
                _emit_on_event_deprecation_warning("shutdown")

            try:
                result = handler()
                if hasattr(result, "__await__"):
                    await result
            except Exception as e:
                handler_name = getattr(handler, "__name__", str(handler))
                errors.append((handler_name, e))
        return errors

    async def _rollback_startup(self, original_error: BaseException) -> None:
        if not self._completed_startup_handlers:
            return

        completed_count = len(self._completed_startup_handlers)
        handlers_to_cleanup = list(reversed(self._on_shutdown[:completed_count]))

        for handler in handlers_to_cleanup:
            try:
                result = handler()
                if hasattr(result, "__await__"):
                    await result
            except Exception as cleanup_error:
                handler_name = getattr(handler, "__name__", str(handler))
                warnings.warn(
                    f"Error during rollback in '{handler_name}': {cleanup_error}",
                    RuntimeWarning,
                    stacklevel=2,
                )

    def add_startup_handler(self, handler: Callable[..., Any]) -> None:
        self._on_startup.append(handler)

    def add_shutdown_handler(self, handler: Callable[..., Any]) -> None:
        self._on_shutdown.append(handler)


def create_unified_lifespan(
    *,
    on_startup: Optional[Sequence[Callable[..., Any]]] = None,
    on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
    lifespan: Optional[Lifespan[AppType]] = None,
) -> Lifespan[AppType]:
    """Create a unified lifespan from mixed inputs."""
    manager = UnifiedLifespanManager(
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        lifespan=lifespan,
    )
    return manager.lifespan  # type: ignore


def merge_lifespan_state(
    parent_state: Optional[dict[str, Any]],
    child_state: Optional[dict[str, Any]],
    *,
    child_overrides_parent: bool = True,
) -> dict[str, Any]:
    """Merge lifespan state dictionaries."""
    parent = parent_state or {}
    child = child_state or {}

    if child_overrides_parent:
        return {**parent, **child}
    else:
        return {**child, **parent}

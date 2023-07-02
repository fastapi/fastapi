from __future__ import annotations

import math
from types import TracebackType
from warnings import warn

from ..abc._tasks import TaskGroup, TaskStatus
from ._compat import (
    DeprecatedAsyncContextManager,
    DeprecatedAwaitable,
    DeprecatedAwaitableFloat,
)
from ._eventloop import get_asynclib


class _IgnoredTaskStatus(TaskStatus[object]):
    def started(self, value: object = None) -> None:
        pass


TASK_STATUS_IGNORED = _IgnoredTaskStatus()


class CancelScope(DeprecatedAsyncContextManager["CancelScope"]):
    """
    Wraps a unit of work that can be made separately cancellable.

    :param deadline: The time (clock value) when this scope is cancelled automatically
    :param shield: ``True`` to shield the cancel scope from external cancellation
    """

    def __new__(
        cls, *, deadline: float = math.inf, shield: bool = False
    ) -> CancelScope:
        return get_asynclib().CancelScope(shield=shield, deadline=deadline)

    def cancel(self) -> DeprecatedAwaitable:
        """Cancel this scope immediately."""
        raise NotImplementedError

    @property
    def deadline(self) -> float:
        """
        The time (clock value) when this scope is cancelled automatically.

        Will be ``float('inf')`` if no timeout has been set.

        """
        raise NotImplementedError

    @deadline.setter
    def deadline(self, value: float) -> None:
        raise NotImplementedError

    @property
    def cancel_called(self) -> bool:
        """``True`` if :meth:`cancel` has been called."""
        raise NotImplementedError

    @property
    def shield(self) -> bool:
        """
        ``True`` if this scope is shielded from external cancellation.

        While a scope is shielded, it will not receive cancellations from outside.

        """
        raise NotImplementedError

    @shield.setter
    def shield(self, value: bool) -> None:
        raise NotImplementedError

    def __enter__(self) -> CancelScope:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        raise NotImplementedError


def open_cancel_scope(*, shield: bool = False) -> CancelScope:
    """
    Open a cancel scope.

    :param shield: ``True`` to shield the cancel scope from external cancellation
    :return: a cancel scope

    .. deprecated:: 3.0
       Use :class:`~CancelScope` directly.

    """
    warn(
        "open_cancel_scope() is deprecated -- use CancelScope() directly",
        DeprecationWarning,
    )
    return get_asynclib().CancelScope(shield=shield)


class FailAfterContextManager(DeprecatedAsyncContextManager[CancelScope]):
    def __init__(self, cancel_scope: CancelScope):
        self._cancel_scope = cancel_scope

    def __enter__(self) -> CancelScope:
        return self._cancel_scope.__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        retval = self._cancel_scope.__exit__(exc_type, exc_val, exc_tb)
        if self._cancel_scope.cancel_called:
            raise TimeoutError

        return retval


def fail_after(delay: float | None, shield: bool = False) -> FailAfterContextManager:
    """
    Create a context manager which raises a :class:`TimeoutError` if does not finish in time.

    :param delay: maximum allowed time (in seconds) before raising the exception, or ``None`` to
        disable the timeout
    :param shield: ``True`` to shield the cancel scope from external cancellation
    :return: a context manager that yields a cancel scope
    :rtype: :class:`~typing.ContextManager`\\[:class:`~anyio.abc.CancelScope`\\]

    """
    deadline = (
        (get_asynclib().current_time() + delay) if delay is not None else math.inf
    )
    cancel_scope = get_asynclib().CancelScope(deadline=deadline, shield=shield)
    return FailAfterContextManager(cancel_scope)


def move_on_after(delay: float | None, shield: bool = False) -> CancelScope:
    """
    Create a cancel scope with a deadline that expires after the given delay.

    :param delay: maximum allowed time (in seconds) before exiting the context block, or ``None``
        to disable the timeout
    :param shield: ``True`` to shield the cancel scope from external cancellation
    :return: a cancel scope

    """
    deadline = (
        (get_asynclib().current_time() + delay) if delay is not None else math.inf
    )
    return get_asynclib().CancelScope(deadline=deadline, shield=shield)


def current_effective_deadline() -> DeprecatedAwaitableFloat:
    """
    Return the nearest deadline among all the cancel scopes effective for the current task.

    :return: a clock value from the event loop's internal clock (or ``float('inf')`` if
        there is no deadline in effect, or ``float('-inf')`` if the current scope has
        been cancelled)
    :rtype: float

    """
    return DeprecatedAwaitableFloat(
        get_asynclib().current_effective_deadline(), current_effective_deadline
    )


def create_task_group() -> TaskGroup:
    """
    Create a task group.

    :return: a task group

    """
    return get_asynclib().TaskGroup()

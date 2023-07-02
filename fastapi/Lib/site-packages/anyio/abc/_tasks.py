from __future__ import annotations

import sys
from abc import ABCMeta, abstractmethod
from types import TracebackType
from typing import TYPE_CHECKING, Any, Awaitable, Callable, TypeVar, overload
from warnings import warn

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

if TYPE_CHECKING:
    from anyio._core._tasks import CancelScope

T_Retval = TypeVar("T_Retval")
T_contra = TypeVar("T_contra", contravariant=True)


class TaskStatus(Protocol[T_contra]):
    @overload
    def started(self: TaskStatus[None]) -> None:
        ...

    @overload
    def started(self, value: T_contra) -> None:
        ...

    def started(self, value: T_contra | None = None) -> None:
        """
        Signal that the task has started.

        :param value: object passed back to the starter of the task
        """


class TaskGroup(metaclass=ABCMeta):
    """
    Groups several asynchronous tasks together.

    :ivar cancel_scope: the cancel scope inherited by all child tasks
    :vartype cancel_scope: CancelScope
    """

    cancel_scope: CancelScope

    async def spawn(
        self,
        func: Callable[..., Awaitable[Any]],
        *args: object,
        name: object = None,
    ) -> None:
        """
        Start a new task in this task group.

        :param func: a coroutine function
        :param args: positional arguments to call the function with
        :param name: name of the task, for the purposes of introspection and debugging

        .. deprecated:: 3.0
           Use :meth:`start_soon` instead. If your code needs AnyIO 2 compatibility, you
           can keep using this until AnyIO 4.

        """
        warn(
            'spawn() is deprecated -- use start_soon() (without the "await") instead',
            DeprecationWarning,
        )
        self.start_soon(func, *args, name=name)

    @abstractmethod
    def start_soon(
        self,
        func: Callable[..., Awaitable[Any]],
        *args: object,
        name: object = None,
    ) -> None:
        """
        Start a new task in this task group.

        :param func: a coroutine function
        :param args: positional arguments to call the function with
        :param name: name of the task, for the purposes of introspection and debugging

        .. versionadded:: 3.0
        """

    @abstractmethod
    async def start(
        self,
        func: Callable[..., Awaitable[Any]],
        *args: object,
        name: object = None,
    ) -> Any:
        """
        Start a new task and wait until it signals for readiness.

        :param func: a coroutine function
        :param args: positional arguments to call the function with
        :param name: name of the task, for the purposes of introspection and debugging
        :return: the value passed to ``task_status.started()``
        :raises RuntimeError: if the task finishes without calling ``task_status.started()``

        .. versionadded:: 3.0
        """

    @abstractmethod
    async def __aenter__(self) -> TaskGroup:
        """Enter the task group context and allow starting new tasks."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the task group context waiting for all tasks to finish."""

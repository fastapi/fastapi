from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from types import TracebackType
from warnings import warn

from ..lowlevel import cancel_shielded_checkpoint, checkpoint, checkpoint_if_cancelled
from ._compat import DeprecatedAwaitable
from ._eventloop import get_asynclib
from ._exceptions import BusyResourceError, WouldBlock
from ._tasks import CancelScope
from ._testing import TaskInfo, get_current_task


@dataclass(frozen=True)
class EventStatistics:
    """
    :ivar int tasks_waiting: number of tasks waiting on :meth:`~.Event.wait`
    """

    tasks_waiting: int


@dataclass(frozen=True)
class CapacityLimiterStatistics:
    """
    :ivar int borrowed_tokens: number of tokens currently borrowed by tasks
    :ivar float total_tokens: total number of available tokens
    :ivar tuple borrowers: tasks or other objects currently holding tokens borrowed from this
        limiter
    :ivar int tasks_waiting: number of tasks waiting on :meth:`~.CapacityLimiter.acquire` or
        :meth:`~.CapacityLimiter.acquire_on_behalf_of`
    """

    borrowed_tokens: int
    total_tokens: float
    borrowers: tuple[object, ...]
    tasks_waiting: int


@dataclass(frozen=True)
class LockStatistics:
    """
    :ivar bool locked: flag indicating if this lock is locked or not
    :ivar ~anyio.TaskInfo owner: task currently holding the lock (or ``None`` if the lock is not
        held by any task)
    :ivar int tasks_waiting: number of tasks waiting on :meth:`~.Lock.acquire`
    """

    locked: bool
    owner: TaskInfo | None
    tasks_waiting: int


@dataclass(frozen=True)
class ConditionStatistics:
    """
    :ivar int tasks_waiting: number of tasks blocked on :meth:`~.Condition.wait`
    :ivar ~anyio.LockStatistics lock_statistics: statistics of the underlying :class:`~.Lock`
    """

    tasks_waiting: int
    lock_statistics: LockStatistics


@dataclass(frozen=True)
class SemaphoreStatistics:
    """
    :ivar int tasks_waiting: number of tasks waiting on :meth:`~.Semaphore.acquire`

    """

    tasks_waiting: int


class Event:
    def __new__(cls) -> Event:
        return get_asynclib().Event()

    def set(self) -> DeprecatedAwaitable:
        """Set the flag, notifying all listeners."""
        raise NotImplementedError

    def is_set(self) -> bool:
        """Return ``True`` if the flag is set, ``False`` if not."""
        raise NotImplementedError

    async def wait(self) -> None:
        """
        Wait until the flag has been set.

        If the flag has already been set when this method is called, it returns immediately.

        """
        raise NotImplementedError

    def statistics(self) -> EventStatistics:
        """Return statistics about the current state of this event."""
        raise NotImplementedError


class Lock:
    _owner_task: TaskInfo | None = None

    def __init__(self) -> None:
        self._waiters: deque[tuple[TaskInfo, Event]] = deque()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()

    async def acquire(self) -> None:
        """Acquire the lock."""
        await checkpoint_if_cancelled()
        try:
            self.acquire_nowait()
        except WouldBlock:
            task = get_current_task()
            event = Event()
            token = task, event
            self._waiters.append(token)
            try:
                await event.wait()
            except BaseException:
                if not event.is_set():
                    self._waiters.remove(token)
                elif self._owner_task == task:
                    self.release()

                raise

            assert self._owner_task == task
        else:
            try:
                await cancel_shielded_checkpoint()
            except BaseException:
                self.release()
                raise

    def acquire_nowait(self) -> None:
        """
        Acquire the lock, without blocking.

        :raises ~WouldBlock: if the operation would block

        """
        task = get_current_task()
        if self._owner_task == task:
            raise RuntimeError("Attempted to acquire an already held Lock")

        if self._owner_task is not None:
            raise WouldBlock

        self._owner_task = task

    def release(self) -> DeprecatedAwaitable:
        """Release the lock."""
        if self._owner_task != get_current_task():
            raise RuntimeError("The current task is not holding this lock")

        if self._waiters:
            self._owner_task, event = self._waiters.popleft()
            event.set()
        else:
            del self._owner_task

        return DeprecatedAwaitable(self.release)

    def locked(self) -> bool:
        """Return True if the lock is currently held."""
        return self._owner_task is not None

    def statistics(self) -> LockStatistics:
        """
        Return statistics about the current state of this lock.

        .. versionadded:: 3.0
        """
        return LockStatistics(self.locked(), self._owner_task, len(self._waiters))


class Condition:
    _owner_task: TaskInfo | None = None

    def __init__(self, lock: Lock | None = None):
        self._lock = lock or Lock()
        self._waiters: deque[Event] = deque()

    async def __aenter__(self) -> None:
        await self.acquire()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()

    def _check_acquired(self) -> None:
        if self._owner_task != get_current_task():
            raise RuntimeError("The current task is not holding the underlying lock")

    async def acquire(self) -> None:
        """Acquire the underlying lock."""
        await self._lock.acquire()
        self._owner_task = get_current_task()

    def acquire_nowait(self) -> None:
        """
        Acquire the underlying lock, without blocking.

        :raises ~WouldBlock: if the operation would block

        """
        self._lock.acquire_nowait()
        self._owner_task = get_current_task()

    def release(self) -> DeprecatedAwaitable:
        """Release the underlying lock."""
        self._lock.release()
        return DeprecatedAwaitable(self.release)

    def locked(self) -> bool:
        """Return True if the lock is set."""
        return self._lock.locked()

    def notify(self, n: int = 1) -> None:
        """Notify exactly n listeners."""
        self._check_acquired()
        for _ in range(n):
            try:
                event = self._waiters.popleft()
            except IndexError:
                break

            event.set()

    def notify_all(self) -> None:
        """Notify all the listeners."""
        self._check_acquired()
        for event in self._waiters:
            event.set()

        self._waiters.clear()

    async def wait(self) -> None:
        """Wait for a notification."""
        await checkpoint()
        event = Event()
        self._waiters.append(event)
        self.release()
        try:
            await event.wait()
        except BaseException:
            if not event.is_set():
                self._waiters.remove(event)

            raise
        finally:
            with CancelScope(shield=True):
                await self.acquire()

    def statistics(self) -> ConditionStatistics:
        """
        Return statistics about the current state of this condition.

        .. versionadded:: 3.0
        """
        return ConditionStatistics(len(self._waiters), self._lock.statistics())


class Semaphore:
    def __init__(self, initial_value: int, *, max_value: int | None = None):
        if not isinstance(initial_value, int):
            raise TypeError("initial_value must be an integer")
        if initial_value < 0:
            raise ValueError("initial_value must be >= 0")
        if max_value is not None:
            if not isinstance(max_value, int):
                raise TypeError("max_value must be an integer or None")
            if max_value < initial_value:
                raise ValueError(
                    "max_value must be equal to or higher than initial_value"
                )

        self._value = initial_value
        self._max_value = max_value
        self._waiters: deque[Event] = deque()

    async def __aenter__(self) -> Semaphore:
        await self.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()

    async def acquire(self) -> None:
        """Decrement the semaphore value, blocking if necessary."""
        await checkpoint_if_cancelled()
        try:
            self.acquire_nowait()
        except WouldBlock:
            event = Event()
            self._waiters.append(event)
            try:
                await event.wait()
            except BaseException:
                if not event.is_set():
                    self._waiters.remove(event)
                else:
                    self.release()

                raise
        else:
            try:
                await cancel_shielded_checkpoint()
            except BaseException:
                self.release()
                raise

    def acquire_nowait(self) -> None:
        """
        Acquire the underlying lock, without blocking.

        :raises ~WouldBlock: if the operation would block

        """
        if self._value == 0:
            raise WouldBlock

        self._value -= 1

    def release(self) -> DeprecatedAwaitable:
        """Increment the semaphore value."""
        if self._max_value is not None and self._value == self._max_value:
            raise ValueError("semaphore released too many times")

        if self._waiters:
            self._waiters.popleft().set()
        else:
            self._value += 1

        return DeprecatedAwaitable(self.release)

    @property
    def value(self) -> int:
        """The current value of the semaphore."""
        return self._value

    @property
    def max_value(self) -> int | None:
        """The maximum value of the semaphore."""
        return self._max_value

    def statistics(self) -> SemaphoreStatistics:
        """
        Return statistics about the current state of this semaphore.

        .. versionadded:: 3.0
        """
        return SemaphoreStatistics(len(self._waiters))


class CapacityLimiter:
    def __new__(cls, total_tokens: float) -> CapacityLimiter:
        return get_asynclib().CapacityLimiter(total_tokens)

    async def __aenter__(self) -> None:
        raise NotImplementedError

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        raise NotImplementedError

    @property
    def total_tokens(self) -> float:
        """
        The total number of tokens available for borrowing.

        This is a read-write property. If the total number of tokens is increased, the
        proportionate number of tasks waiting on this limiter will be granted their tokens.

        .. versionchanged:: 3.0
            The property is now writable.

        """
        raise NotImplementedError

    @total_tokens.setter
    def total_tokens(self, value: float) -> None:
        raise NotImplementedError

    async def set_total_tokens(self, value: float) -> None:
        warn(
            "CapacityLimiter.set_total_tokens has been deprecated. Set the value of the"
            '"total_tokens" attribute directly.',
            DeprecationWarning,
        )
        self.total_tokens = value

    @property
    def borrowed_tokens(self) -> int:
        """The number of tokens that have currently been borrowed."""
        raise NotImplementedError

    @property
    def available_tokens(self) -> float:
        """The number of tokens currently available to be borrowed"""
        raise NotImplementedError

    def acquire_nowait(self) -> DeprecatedAwaitable:
        """
        Acquire a token for the current task without waiting for one to become available.

        :raises ~anyio.WouldBlock: if there are no tokens available for borrowing

        """
        raise NotImplementedError

    def acquire_on_behalf_of_nowait(self, borrower: object) -> DeprecatedAwaitable:
        """
        Acquire a token without waiting for one to become available.

        :param borrower: the entity borrowing a token
        :raises ~anyio.WouldBlock: if there are no tokens available for borrowing

        """
        raise NotImplementedError

    async def acquire(self) -> None:
        """
        Acquire a token for the current task, waiting if necessary for one to become available.

        """
        raise NotImplementedError

    async def acquire_on_behalf_of(self, borrower: object) -> None:
        """
        Acquire a token, waiting if necessary for one to become available.

        :param borrower: the entity borrowing a token

        """
        raise NotImplementedError

    def release(self) -> None:
        """
        Release the token held by the current task.
        :raises RuntimeError: if the current task has not borrowed a token from this limiter.

        """
        raise NotImplementedError

    def release_on_behalf_of(self, borrower: object) -> None:
        """
        Release the token held by the given borrower.

        :raises RuntimeError: if the borrower has not borrowed a token from this limiter.

        """
        raise NotImplementedError

    def statistics(self) -> CapacityLimiterStatistics:
        """
        Return statistics about the current state of this limiter.

        .. versionadded:: 3.0

        """
        raise NotImplementedError


def create_lock() -> Lock:
    """
    Create an asynchronous lock.

    :return: a lock object

    .. deprecated:: 3.0
       Use :class:`~Lock` directly.

    """
    warn("create_lock() is deprecated -- use Lock() directly", DeprecationWarning)
    return Lock()


def create_condition(lock: Lock | None = None) -> Condition:
    """
    Create an asynchronous condition.

    :param lock: the lock to base the condition object on
    :return: a condition object

    .. deprecated:: 3.0
       Use :class:`~Condition` directly.

    """
    warn(
        "create_condition() is deprecated -- use Condition() directly",
        DeprecationWarning,
    )
    return Condition(lock=lock)


def create_event() -> Event:
    """
    Create an asynchronous event object.

    :return: an event object

    .. deprecated:: 3.0
       Use :class:`~Event` directly.

    """
    warn("create_event() is deprecated -- use Event() directly", DeprecationWarning)
    return get_asynclib().Event()


def create_semaphore(value: int, *, max_value: int | None = None) -> Semaphore:
    """
    Create an asynchronous semaphore.

    :param value: the semaphore's initial value
    :param max_value: if set, makes this a "bounded" semaphore that raises :exc:`ValueError` if the
        semaphore's value would exceed this number
    :return: a semaphore object

    .. deprecated:: 3.0
       Use :class:`~Semaphore` directly.

    """
    warn(
        "create_semaphore() is deprecated -- use Semaphore() directly",
        DeprecationWarning,
    )
    return Semaphore(value, max_value=max_value)


def create_capacity_limiter(total_tokens: float) -> CapacityLimiter:
    """
    Create a capacity limiter.

    :param total_tokens: the total number of tokens available for borrowing (can be an integer or
        :data:`math.inf`)
    :return: a capacity limiter object

    .. deprecated:: 3.0
       Use :class:`~CapacityLimiter` directly.

    """
    warn(
        "create_capacity_limiter() is deprecated -- use CapacityLimiter() directly",
        DeprecationWarning,
    )
    return get_asynclib().CapacityLimiter(total_tokens)


class ResourceGuard:
    __slots__ = "action", "_guarded"

    def __init__(self, action: str):
        self.action = action
        self._guarded = False

    def __enter__(self) -> None:
        if self._guarded:
            raise BusyResourceError(self.action)

        self._guarded = True

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self._guarded = False
        return None

import sys
from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
)
from multiprocessing.connection import Connection
from multiprocessing.context import BaseContext, Process
from multiprocessing.queues import Queue, SimpleQueue
from threading import Lock, Semaphore, Thread
from types import TracebackType
from typing import Any, Generic, TypeVar
from weakref import ref

from ._base import BrokenExecutor, Executor, Future

_T = TypeVar("_T")

_threads_wakeups: MutableMapping[Any, Any]
_global_shutdown: bool

class _ThreadWakeup:
    _closed: bool
    _reader: Connection
    _writer: Connection
    def close(self) -> None: ...
    def wakeup(self) -> None: ...
    def clear(self) -> None: ...

def _python_exit() -> None: ...

EXTRA_QUEUED_CALLS: int

_MAX_WINDOWS_WORKERS: int

class _RemoteTraceback(Exception):
    tb: str
    def __init__(self, tb: TracebackType) -> None: ...

class _ExceptionWithTraceback:
    exc: BaseException
    tb: TracebackType
    def __init__(self, exc: BaseException, tb: TracebackType) -> None: ...
    def __reduce__(self) -> str | tuple[Any, ...]: ...

def _rebuild_exc(exc: Exception, tb: str) -> Exception: ...

class _WorkItem(Generic[_T]):
    future: Future[_T]
    fn: Callable[..., _T]
    args: Iterable[Any]
    kwargs: Mapping[str, Any]
    def __init__(
        self,
        future: Future[_T],
        fn: Callable[..., _T],
        args: Iterable[Any],
        kwargs: Mapping[str, Any],
    ) -> None: ...

class _ResultItem:
    work_id: int
    exception: Exception
    result: Any
    if sys.version_info >= (3, 11):
        exit_pid: int | None
        def __init__(
            self,
            work_id: int,
            exception: Exception | None = None,
            result: Any | None = None,
            exit_pid: int | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            work_id: int,
            exception: Exception | None = None,
            result: Any | None = None,
        ) -> None: ...

class _CallItem:
    work_id: int
    fn: Callable[..., Any]
    args: Iterable[Any]
    kwargs: Mapping[str, Any]
    def __init__(
        self,
        work_id: int,
        fn: Callable[..., Any],
        args: Iterable[Any],
        kwargs: Mapping[str, Any],
    ) -> None: ...

class _SafeQueue(Queue[Future[Any]]):
    pending_work_items: dict[int, _WorkItem[Any]]
    shutdown_lock: Lock
    thread_wakeup: _ThreadWakeup
    if sys.version_info >= (3, 9):
        def __init__(
            self,
            max_size: int | None = 0,
            *,
            ctx: BaseContext,
            pending_work_items: dict[int, _WorkItem[Any]],
            shutdown_lock: Lock,
            thread_wakeup: _ThreadWakeup,
        ) -> None: ...
    else:
        def __init__(
            self,
            max_size: int | None = 0,
            *,
            ctx: BaseContext,
            pending_work_items: dict[int, _WorkItem[Any]],
        ) -> None: ...

    def _on_queue_feeder_error(self, e: Exception, obj: _CallItem) -> None: ...

def _get_chunks(
    *iterables: Any, chunksize: int
) -> Generator[tuple[Any, ...], None, None]: ...
def _process_chunk(
    fn: Callable[..., _T], chunk: Iterable[tuple[Any, ...]]
) -> list[_T]: ...

if sys.version_info >= (3, 11):
    def _sendback_result(
        result_queue: SimpleQueue[_WorkItem[Any]],
        work_id: int,
        result: Any | None = None,
        exception: Exception | None = None,
        exit_pid: int | None = None,
    ) -> None: ...

else:
    def _sendback_result(
        result_queue: SimpleQueue[_WorkItem[Any]],
        work_id: int,
        result: Any | None = None,
        exception: Exception | None = None,
    ) -> None: ...

if sys.version_info >= (3, 11):
    def _process_worker(
        call_queue: Queue[_CallItem],
        result_queue: SimpleQueue[_ResultItem],
        initializer: Callable[..., object] | None,
        initargs: tuple[Any, ...],
        max_tasks: int | None = None,
    ) -> None: ...

else:
    def _process_worker(
        call_queue: Queue[_CallItem],
        result_queue: SimpleQueue[_ResultItem],
        initializer: Callable[..., object] | None,
        initargs: tuple[Any, ...],
    ) -> None: ...

if sys.version_info >= (3, 9):
    class _ExecutorManagerThread(Thread):
        thread_wakeup: _ThreadWakeup
        shutdown_lock: Lock
        executor_reference: ref[Any]
        processes: MutableMapping[int, Process]
        call_queue: Queue[_CallItem]
        result_queue: SimpleQueue[_ResultItem]
        work_ids_queue: Queue[int]
        pending_work_items: dict[int, _WorkItem[Any]]
        def __init__(self, executor: ProcessPoolExecutor) -> None: ...
        def run(self) -> None: ...
        def add_call_item_to_queue(self) -> None: ...
        def wait_result_broken_or_wakeup(self) -> tuple[Any, bool, str]: ...
        def process_result_item(self, result_item: int | _ResultItem) -> None: ...
        def is_shutting_down(self) -> bool: ...
        def terminate_broken(self, cause: str) -> None: ...
        def flag_executor_shutting_down(self) -> None: ...
        def shutdown_workers(self) -> None: ...
        def join_executor_internals(self) -> None: ...
        def get_n_children_alive(self) -> int: ...

_system_limits_checked: bool
_system_limited: bool | None

def _check_system_limits() -> None: ...
def _chain_from_iterable_of_lists(iterable: Iterable[MutableSequence[Any]]) -> Any: ...

class BrokenProcessPool(BrokenExecutor): ...

class ProcessPoolExecutor(Executor):
    _mp_context: BaseContext | None
    _initializer: Callable[..., None] | None
    _initargs: tuple[Any, ...]
    _executor_manager_thread: _ThreadWakeup
    _processes: MutableMapping[int, Process]
    _shutdown_thread: bool
    _shutdown_lock: Lock
    _idle_worker_semaphore: Semaphore
    _broken: bool
    _queue_count: int
    _pending_work_items: dict[int, _WorkItem[Any]]
    _cancel_pending_futures: bool
    _executor_manager_thread_wakeup: _ThreadWakeup
    _result_queue: SimpleQueue[Any]
    _work_ids: Queue[Any]
    if sys.version_info >= (3, 11):
        def __init__(
            self,
            max_workers: int | None = None,
            mp_context: BaseContext | None = None,
            initializer: Callable[..., object] | None = None,
            initargs: tuple[Any, ...] = (),
            *,
            max_tasks_per_child: int | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            max_workers: int | None = None,
            mp_context: BaseContext | None = None,
            initializer: Callable[..., object] | None = None,
            initargs: tuple[Any, ...] = (),
        ) -> None: ...
    if sys.version_info >= (3, 9):
        def _start_executor_manager_thread(self) -> None: ...

    def _adjust_process_count(self) -> None: ...

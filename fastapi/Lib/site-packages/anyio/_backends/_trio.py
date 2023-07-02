from __future__ import annotations

import array
import math
import socket
from concurrent.futures import Future
from contextvars import copy_context
from dataclasses import dataclass
from functools import partial
from io import IOBase
from os import PathLike
from signal import Signals
from types import TracebackType
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Generic,
    Iterable,
    Mapping,
    NoReturn,
    Sequence,
    TypeVar,
    cast,
)

import sniffio
import trio.from_thread
from outcome import Error, Outcome, Value
from trio.socket import SocketType as TrioSocketType
from trio.to_thread import run_sync

from .. import CapacityLimiterStatistics, EventStatistics, TaskInfo, abc
from .._core._compat import DeprecatedAsyncContextManager, DeprecatedAwaitable
from .._core._eventloop import claim_worker_thread
from .._core._exceptions import (
    BrokenResourceError,
    BusyResourceError,
    ClosedResourceError,
    EndOfStream,
)
from .._core._exceptions import ExceptionGroup as BaseExceptionGroup
from .._core._sockets import convert_ipv6_sockaddr
from .._core._synchronization import CapacityLimiter as BaseCapacityLimiter
from .._core._synchronization import Event as BaseEvent
from .._core._synchronization import ResourceGuard
from .._core._tasks import CancelScope as BaseCancelScope
from ..abc import IPSockAddrType, UDPPacketType

if TYPE_CHECKING:
    from trio_typing import TaskStatus

try:
    from trio import lowlevel as trio_lowlevel
except ImportError:
    from trio import hazmat as trio_lowlevel  # type: ignore[no-redef]
    from trio.hazmat import wait_readable, wait_writable
else:
    from trio.lowlevel import wait_readable, wait_writable

try:
    trio_open_process = trio_lowlevel.open_process
except AttributeError:
    # isort: off
    from trio import (  # type: ignore[attr-defined, no-redef]
        open_process as trio_open_process,
    )

T_Retval = TypeVar("T_Retval")
T_SockAddr = TypeVar("T_SockAddr", str, IPSockAddrType)


#
# Event loop
#

run = trio.run
current_token = trio.lowlevel.current_trio_token
RunVar = trio.lowlevel.RunVar


#
# Miscellaneous
#

sleep = trio.sleep


#
# Timeouts and cancellation
#


class CancelScope(BaseCancelScope):
    def __new__(
        cls, original: trio.CancelScope | None = None, **kwargs: object
    ) -> CancelScope:
        return object.__new__(cls)

    def __init__(self, original: trio.CancelScope | None = None, **kwargs: Any) -> None:
        self.__original = original or trio.CancelScope(**kwargs)

    def __enter__(self) -> CancelScope:
        self.__original.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        # https://github.com/python-trio/trio-typing/pull/79
        return self.__original.__exit__(  # type: ignore[func-returns-value]
            exc_type, exc_val, exc_tb
        )

    def cancel(self) -> DeprecatedAwaitable:
        self.__original.cancel()
        return DeprecatedAwaitable(self.cancel)

    @property
    def deadline(self) -> float:
        return self.__original.deadline

    @deadline.setter
    def deadline(self, value: float) -> None:
        self.__original.deadline = value

    @property
    def cancel_called(self) -> bool:
        return self.__original.cancel_called

    @property
    def shield(self) -> bool:
        return self.__original.shield

    @shield.setter
    def shield(self, value: bool) -> None:
        self.__original.shield = value


CancelledError = trio.Cancelled
checkpoint = trio.lowlevel.checkpoint
checkpoint_if_cancelled = trio.lowlevel.checkpoint_if_cancelled
cancel_shielded_checkpoint = trio.lowlevel.cancel_shielded_checkpoint
current_effective_deadline = trio.current_effective_deadline
current_time = trio.current_time


#
# Task groups
#


class ExceptionGroup(BaseExceptionGroup, trio.MultiError):
    pass


class TaskGroup(abc.TaskGroup):
    def __init__(self) -> None:
        self._active = False
        self._nursery_manager = trio.open_nursery()
        self.cancel_scope = None  # type: ignore[assignment]

    async def __aenter__(self) -> TaskGroup:
        self._active = True
        self._nursery = await self._nursery_manager.__aenter__()
        self.cancel_scope = CancelScope(self._nursery.cancel_scope)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        try:
            return await self._nursery_manager.__aexit__(exc_type, exc_val, exc_tb)
        except trio.MultiError as exc:
            raise ExceptionGroup(exc.exceptions) from None
        finally:
            self._active = False

    def start_soon(
        self, func: Callable[..., Awaitable[Any]], *args: object, name: object = None
    ) -> None:
        if not self._active:
            raise RuntimeError(
                "This task group is not active; no new tasks can be started."
            )

        self._nursery.start_soon(func, *args, name=name)

    async def start(
        self, func: Callable[..., Awaitable[Any]], *args: object, name: object = None
    ) -> object:
        if not self._active:
            raise RuntimeError(
                "This task group is not active; no new tasks can be started."
            )

        return await self._nursery.start(func, *args, name=name)


#
# Threads
#


async def run_sync_in_worker_thread(
    func: Callable[..., T_Retval],
    *args: object,
    cancellable: bool = False,
    limiter: trio.CapacityLimiter | None = None,
) -> T_Retval:
    def wrapper() -> T_Retval:
        with claim_worker_thread("trio"):
            return func(*args)

    # TODO: remove explicit context copying when trio 0.20 is the minimum requirement
    context = copy_context()
    context.run(sniffio.current_async_library_cvar.set, None)
    return await run_sync(
        context.run, wrapper, cancellable=cancellable, limiter=limiter
    )


# TODO: remove this workaround when trio 0.20 is the minimum requirement
def run_async_from_thread(
    fn: Callable[..., Awaitable[T_Retval]], *args: Any
) -> T_Retval:
    async def wrapper() -> T_Retval:
        retval: T_Retval

        async def inner() -> None:
            nonlocal retval
            __tracebackhide__ = True
            retval = await fn(*args)

        async with trio.open_nursery() as n:
            context.run(n.start_soon, inner)

        __tracebackhide__ = True
        return retval  # noqa: F821

    context = copy_context()
    context.run(sniffio.current_async_library_cvar.set, "trio")
    return trio.from_thread.run(wrapper)


def run_sync_from_thread(fn: Callable[..., T_Retval], *args: Any) -> T_Retval:
    # TODO: remove explicit context copying when trio 0.20 is the minimum requirement
    retval = trio.from_thread.run_sync(copy_context().run, fn, *args)
    return cast(T_Retval, retval)


class BlockingPortal(abc.BlockingPortal):
    def __new__(cls) -> BlockingPortal:
        return object.__new__(cls)

    def __init__(self) -> None:
        super().__init__()
        self._token = trio.lowlevel.current_trio_token()

    def _spawn_task_from_thread(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict[str, Any],
        name: object,
        future: Future,
    ) -> None:
        context = copy_context()
        context.run(sniffio.current_async_library_cvar.set, "trio")
        trio.from_thread.run_sync(
            context.run,
            partial(self._task_group.start_soon, name=name),
            self._call_func,
            func,
            args,
            kwargs,
            future,
            trio_token=self._token,
        )


#
# Subprocesses
#


@dataclass(eq=False)
class ReceiveStreamWrapper(abc.ByteReceiveStream):
    _stream: trio.abc.ReceiveStream

    async def receive(self, max_bytes: int | None = None) -> bytes:
        try:
            data = await self._stream.receive_some(max_bytes)
        except trio.ClosedResourceError as exc:
            raise ClosedResourceError from exc.__cause__
        except trio.BrokenResourceError as exc:
            raise BrokenResourceError from exc.__cause__

        if data:
            return data
        else:
            raise EndOfStream

    async def aclose(self) -> None:
        await self._stream.aclose()


@dataclass(eq=False)
class SendStreamWrapper(abc.ByteSendStream):
    _stream: trio.abc.SendStream

    async def send(self, item: bytes) -> None:
        try:
            await self._stream.send_all(item)
        except trio.ClosedResourceError as exc:
            raise ClosedResourceError from exc.__cause__
        except trio.BrokenResourceError as exc:
            raise BrokenResourceError from exc.__cause__

    async def aclose(self) -> None:
        await self._stream.aclose()


@dataclass(eq=False)
class Process(abc.Process):
    _process: trio.Process
    _stdin: abc.ByteSendStream | None
    _stdout: abc.ByteReceiveStream | None
    _stderr: abc.ByteReceiveStream | None

    async def aclose(self) -> None:
        if self._stdin:
            await self._stdin.aclose()
        if self._stdout:
            await self._stdout.aclose()
        if self._stderr:
            await self._stderr.aclose()

        await self.wait()

    async def wait(self) -> int:
        return await self._process.wait()

    def terminate(self) -> None:
        self._process.terminate()

    def kill(self) -> None:
        self._process.kill()

    def send_signal(self, signal: Signals) -> None:
        self._process.send_signal(signal)

    @property
    def pid(self) -> int:
        return self._process.pid

    @property
    def returncode(self) -> int | None:
        return self._process.returncode

    @property
    def stdin(self) -> abc.ByteSendStream | None:
        return self._stdin

    @property
    def stdout(self) -> abc.ByteReceiveStream | None:
        return self._stdout

    @property
    def stderr(self) -> abc.ByteReceiveStream | None:
        return self._stderr


async def open_process(
    command: str | bytes | Sequence[str | bytes],
    *,
    shell: bool,
    stdin: int | IO[Any] | None,
    stdout: int | IO[Any] | None,
    stderr: int | IO[Any] | None,
    cwd: str | bytes | PathLike | None = None,
    env: Mapping[str, str] | None = None,
    start_new_session: bool = False,
) -> Process:
    process = await trio_open_process(  # type: ignore[misc]
        command,  # type: ignore[arg-type]
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
        cwd=cwd,
        env=env,
        start_new_session=start_new_session,
    )
    stdin_stream = SendStreamWrapper(process.stdin) if process.stdin else None
    stdout_stream = ReceiveStreamWrapper(process.stdout) if process.stdout else None
    stderr_stream = ReceiveStreamWrapper(process.stderr) if process.stderr else None
    return Process(process, stdin_stream, stdout_stream, stderr_stream)


class _ProcessPoolShutdownInstrument(trio.abc.Instrument):
    def after_run(self) -> None:
        super().after_run()


current_default_worker_process_limiter: RunVar = RunVar(
    "current_default_worker_process_limiter"
)


async def _shutdown_process_pool(workers: set[Process]) -> None:
    process: Process
    try:
        await sleep(math.inf)
    except trio.Cancelled:
        for process in workers:
            if process.returncode is None:
                process.kill()

        with CancelScope(shield=True):
            for process in workers:
                await process.aclose()


def setup_process_pool_exit_at_shutdown(workers: set[Process]) -> None:
    trio.lowlevel.spawn_system_task(_shutdown_process_pool, workers)


#
# Sockets and networking
#


class _TrioSocketMixin(Generic[T_SockAddr]):
    def __init__(self, trio_socket: TrioSocketType) -> None:
        self._trio_socket = trio_socket
        self._closed = False

    def _check_closed(self) -> None:
        if self._closed:
            raise ClosedResourceError
        if self._trio_socket.fileno() < 0:
            raise BrokenResourceError

    @property
    def _raw_socket(self) -> socket.socket:
        return self._trio_socket._sock  # type: ignore[attr-defined]

    async def aclose(self) -> None:
        if self._trio_socket.fileno() >= 0:
            self._closed = True
            self._trio_socket.close()

    def _convert_socket_error(self, exc: BaseException) -> NoReturn:
        if isinstance(exc, trio.ClosedResourceError):
            raise ClosedResourceError from exc
        elif self._trio_socket.fileno() < 0 and self._closed:
            raise ClosedResourceError from None
        elif isinstance(exc, OSError):
            raise BrokenResourceError from exc
        else:
            raise exc


class SocketStream(_TrioSocketMixin, abc.SocketStream):
    def __init__(self, trio_socket: TrioSocketType) -> None:
        super().__init__(trio_socket)
        self._receive_guard = ResourceGuard("reading from")
        self._send_guard = ResourceGuard("writing to")

    async def receive(self, max_bytes: int = 65536) -> bytes:
        with self._receive_guard:
            try:
                data = await self._trio_socket.recv(max_bytes)
            except BaseException as exc:
                self._convert_socket_error(exc)

            if data:
                return data
            else:
                raise EndOfStream

    async def send(self, item: bytes) -> None:
        with self._send_guard:
            view = memoryview(item)
            while view:
                try:
                    bytes_sent = await self._trio_socket.send(view)
                except BaseException as exc:
                    self._convert_socket_error(exc)

                view = view[bytes_sent:]

    async def send_eof(self) -> None:
        self._trio_socket.shutdown(socket.SHUT_WR)


class UNIXSocketStream(SocketStream, abc.UNIXSocketStream):
    async def receive_fds(self, msglen: int, maxfds: int) -> tuple[bytes, list[int]]:
        if not isinstance(msglen, int) or msglen < 0:
            raise ValueError("msglen must be a non-negative integer")
        if not isinstance(maxfds, int) or maxfds < 1:
            raise ValueError("maxfds must be a positive integer")

        fds = array.array("i")
        await checkpoint()
        with self._receive_guard:
            while True:
                try:
                    message, ancdata, flags, addr = await self._trio_socket.recvmsg(
                        msglen, socket.CMSG_LEN(maxfds * fds.itemsize)
                    )
                except BaseException as exc:
                    self._convert_socket_error(exc)
                else:
                    if not message and not ancdata:
                        raise EndOfStream

                    break

        for cmsg_level, cmsg_type, cmsg_data in ancdata:
            if cmsg_level != socket.SOL_SOCKET or cmsg_type != socket.SCM_RIGHTS:
                raise RuntimeError(
                    f"Received unexpected ancillary data; message = {message!r}, "
                    f"cmsg_level = {cmsg_level}, cmsg_type = {cmsg_type}"
                )

            fds.frombytes(cmsg_data[: len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])

        return message, list(fds)

    async def send_fds(self, message: bytes, fds: Collection[int | IOBase]) -> None:
        if not message:
            raise ValueError("message must not be empty")
        if not fds:
            raise ValueError("fds must not be empty")

        filenos: list[int] = []
        for fd in fds:
            if isinstance(fd, int):
                filenos.append(fd)
            elif isinstance(fd, IOBase):
                filenos.append(fd.fileno())

        fdarray = array.array("i", filenos)
        await checkpoint()
        with self._send_guard:
            while True:
                try:
                    await self._trio_socket.sendmsg(
                        [message],
                        [
                            (
                                socket.SOL_SOCKET,
                                socket.SCM_RIGHTS,  # type: ignore[list-item]
                                fdarray,
                            )
                        ],
                    )
                    break
                except BaseException as exc:
                    self._convert_socket_error(exc)


class TCPSocketListener(_TrioSocketMixin, abc.SocketListener):
    def __init__(self, raw_socket: socket.socket):
        super().__init__(trio.socket.from_stdlib_socket(raw_socket))
        self._accept_guard = ResourceGuard("accepting connections from")

    async def accept(self) -> SocketStream:
        with self._accept_guard:
            try:
                trio_socket, _addr = await self._trio_socket.accept()
            except BaseException as exc:
                self._convert_socket_error(exc)

        trio_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return SocketStream(trio_socket)


class UNIXSocketListener(_TrioSocketMixin, abc.SocketListener):
    def __init__(self, raw_socket: socket.socket):
        super().__init__(trio.socket.from_stdlib_socket(raw_socket))
        self._accept_guard = ResourceGuard("accepting connections from")

    async def accept(self) -> UNIXSocketStream:
        with self._accept_guard:
            try:
                trio_socket, _addr = await self._trio_socket.accept()
            except BaseException as exc:
                self._convert_socket_error(exc)

        return UNIXSocketStream(trio_socket)


class UDPSocket(_TrioSocketMixin[IPSockAddrType], abc.UDPSocket):
    def __init__(self, trio_socket: TrioSocketType) -> None:
        super().__init__(trio_socket)
        self._receive_guard = ResourceGuard("reading from")
        self._send_guard = ResourceGuard("writing to")

    async def receive(self) -> tuple[bytes, IPSockAddrType]:
        with self._receive_guard:
            try:
                data, addr = await self._trio_socket.recvfrom(65536)
                return data, convert_ipv6_sockaddr(addr)
            except BaseException as exc:
                self._convert_socket_error(exc)

    async def send(self, item: UDPPacketType) -> None:
        with self._send_guard:
            try:
                await self._trio_socket.sendto(*item)
            except BaseException as exc:
                self._convert_socket_error(exc)


class ConnectedUDPSocket(_TrioSocketMixin[IPSockAddrType], abc.ConnectedUDPSocket):
    def __init__(self, trio_socket: TrioSocketType) -> None:
        super().__init__(trio_socket)
        self._receive_guard = ResourceGuard("reading from")
        self._send_guard = ResourceGuard("writing to")

    async def receive(self) -> bytes:
        with self._receive_guard:
            try:
                return await self._trio_socket.recv(65536)
            except BaseException as exc:
                self._convert_socket_error(exc)

    async def send(self, item: bytes) -> None:
        with self._send_guard:
            try:
                await self._trio_socket.send(item)
            except BaseException as exc:
                self._convert_socket_error(exc)


async def connect_tcp(
    host: str, port: int, local_address: IPSockAddrType | None = None
) -> SocketStream:
    family = socket.AF_INET6 if ":" in host else socket.AF_INET
    trio_socket = trio.socket.socket(family)
    trio_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    if local_address:
        await trio_socket.bind(local_address)

    try:
        await trio_socket.connect((host, port))
    except BaseException:
        trio_socket.close()
        raise

    return SocketStream(trio_socket)


async def connect_unix(path: str) -> UNIXSocketStream:
    trio_socket = trio.socket.socket(socket.AF_UNIX)
    try:
        await trio_socket.connect(path)
    except BaseException:
        trio_socket.close()
        raise

    return UNIXSocketStream(trio_socket)


async def create_udp_socket(
    family: socket.AddressFamily,
    local_address: IPSockAddrType | None,
    remote_address: IPSockAddrType | None,
    reuse_port: bool,
) -> UDPSocket | ConnectedUDPSocket:
    trio_socket = trio.socket.socket(family=family, type=socket.SOCK_DGRAM)

    if reuse_port:
        trio_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    if local_address:
        await trio_socket.bind(local_address)

    if remote_address:
        await trio_socket.connect(remote_address)
        return ConnectedUDPSocket(trio_socket)
    else:
        return UDPSocket(trio_socket)


getaddrinfo = trio.socket.getaddrinfo
getnameinfo = trio.socket.getnameinfo


async def wait_socket_readable(sock: socket.socket) -> None:
    try:
        await wait_readable(sock)
    except trio.ClosedResourceError as exc:
        raise ClosedResourceError().with_traceback(exc.__traceback__) from None
    except trio.BusyResourceError:
        raise BusyResourceError("reading from") from None


async def wait_socket_writable(sock: socket.socket) -> None:
    try:
        await wait_writable(sock)
    except trio.ClosedResourceError as exc:
        raise ClosedResourceError().with_traceback(exc.__traceback__) from None
    except trio.BusyResourceError:
        raise BusyResourceError("writing to") from None


#
# Synchronization
#


class Event(BaseEvent):
    def __new__(cls) -> Event:
        return object.__new__(cls)

    def __init__(self) -> None:
        self.__original = trio.Event()

    def is_set(self) -> bool:
        return self.__original.is_set()

    async def wait(self) -> None:
        return await self.__original.wait()

    def statistics(self) -> EventStatistics:
        orig_statistics = self.__original.statistics()
        return EventStatistics(tasks_waiting=orig_statistics.tasks_waiting)

    def set(self) -> DeprecatedAwaitable:
        self.__original.set()
        return DeprecatedAwaitable(self.set)


class CapacityLimiter(BaseCapacityLimiter):
    def __new__(cls, *args: object, **kwargs: object) -> CapacityLimiter:
        return object.__new__(cls)

    def __init__(
        self, *args: Any, original: trio.CapacityLimiter | None = None
    ) -> None:
        self.__original = original or trio.CapacityLimiter(*args)

    async def __aenter__(self) -> None:
        return await self.__original.__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.__original.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def total_tokens(self) -> float:
        return self.__original.total_tokens

    @total_tokens.setter
    def total_tokens(self, value: float) -> None:
        self.__original.total_tokens = value

    @property
    def borrowed_tokens(self) -> int:
        return self.__original.borrowed_tokens

    @property
    def available_tokens(self) -> float:
        return self.__original.available_tokens

    def acquire_nowait(self) -> DeprecatedAwaitable:
        self.__original.acquire_nowait()
        return DeprecatedAwaitable(self.acquire_nowait)

    def acquire_on_behalf_of_nowait(self, borrower: object) -> DeprecatedAwaitable:
        self.__original.acquire_on_behalf_of_nowait(borrower)
        return DeprecatedAwaitable(self.acquire_on_behalf_of_nowait)

    async def acquire(self) -> None:
        await self.__original.acquire()

    async def acquire_on_behalf_of(self, borrower: object) -> None:
        await self.__original.acquire_on_behalf_of(borrower)

    def release(self) -> None:
        return self.__original.release()

    def release_on_behalf_of(self, borrower: object) -> None:
        return self.__original.release_on_behalf_of(borrower)

    def statistics(self) -> CapacityLimiterStatistics:
        orig = self.__original.statistics()
        return CapacityLimiterStatistics(
            borrowed_tokens=orig.borrowed_tokens,
            total_tokens=orig.total_tokens,
            borrowers=orig.borrowers,
            tasks_waiting=orig.tasks_waiting,
        )


_capacity_limiter_wrapper: RunVar = RunVar("_capacity_limiter_wrapper")


def current_default_thread_limiter() -> CapacityLimiter:
    try:
        return _capacity_limiter_wrapper.get()
    except LookupError:
        limiter = CapacityLimiter(
            original=trio.to_thread.current_default_thread_limiter()
        )
        _capacity_limiter_wrapper.set(limiter)
        return limiter


#
# Signal handling
#


class _SignalReceiver(DeprecatedAsyncContextManager["_SignalReceiver"]):
    _iterator: AsyncIterator[int]

    def __init__(self, signals: tuple[Signals, ...]):
        self._signals = signals

    def __enter__(self) -> _SignalReceiver:
        self._cm = trio.open_signal_receiver(*self._signals)
        self._iterator = self._cm.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        return self._cm.__exit__(exc_type, exc_val, exc_tb)

    def __aiter__(self) -> _SignalReceiver:
        return self

    async def __anext__(self) -> Signals:
        signum = await self._iterator.__anext__()
        return Signals(signum)


def open_signal_receiver(*signals: Signals) -> _SignalReceiver:
    return _SignalReceiver(signals)


#
# Testing and debugging
#


def get_current_task() -> TaskInfo:
    task = trio_lowlevel.current_task()

    parent_id = None
    if task.parent_nursery and task.parent_nursery.parent_task:
        parent_id = id(task.parent_nursery.parent_task)

    return TaskInfo(id(task), parent_id, task.name, task.coro)


def get_running_tasks() -> list[TaskInfo]:
    root_task = trio_lowlevel.current_root_task()
    task_infos = [TaskInfo(id(root_task), None, root_task.name, root_task.coro)]
    nurseries = root_task.child_nurseries
    while nurseries:
        new_nurseries: list[trio.Nursery] = []
        for nursery in nurseries:
            for task in nursery.child_tasks:
                task_infos.append(
                    TaskInfo(id(task), id(nursery.parent_task), task.name, task.coro)
                )
                new_nurseries.extend(task.child_nurseries)

        nurseries = new_nurseries

    return task_infos


def wait_all_tasks_blocked() -> Awaitable[None]:
    import trio.testing

    return trio.testing.wait_all_tasks_blocked()


class TestRunner(abc.TestRunner):
    def __init__(self, **options: Any) -> None:
        from collections import deque
        from queue import Queue

        self._call_queue: Queue[Callable[..., object]] = Queue()
        self._result_queue: deque[Outcome] = deque()
        self._stop_event: trio.Event | None = None
        self._nursery: trio.Nursery | None = None
        self._options = options

    async def _trio_main(self) -> None:
        self._stop_event = trio.Event()
        async with trio.open_nursery() as self._nursery:
            await self._stop_event.wait()

    async def _call_func(
        self, func: Callable[..., Awaitable[object]], args: tuple, kwargs: dict
    ) -> None:
        try:
            retval = await func(*args, **kwargs)
        except BaseException as exc:
            self._result_queue.append(Error(exc))
        else:
            self._result_queue.append(Value(retval))

    def _main_task_finished(self, outcome: object) -> None:
        self._nursery = None

    def _get_nursery(self) -> trio.Nursery:
        if self._nursery is None:
            trio.lowlevel.start_guest_run(
                self._trio_main,
                run_sync_soon_threadsafe=self._call_queue.put,
                done_callback=self._main_task_finished,
                **self._options,
            )
            while self._nursery is None:
                self._call_queue.get()()

        return self._nursery

    def _call(
        self, func: Callable[..., Awaitable[T_Retval]], *args: object, **kwargs: object
    ) -> T_Retval:
        self._get_nursery().start_soon(self._call_func, func, args, kwargs)
        while not self._result_queue:
            self._call_queue.get()()

        outcome = self._result_queue.pop()
        return outcome.unwrap()

    def close(self) -> None:
        if self._stop_event:
            self._stop_event.set()
            while self._nursery is not None:
                self._call_queue.get()()

    def run_asyncgen_fixture(
        self,
        fixture_func: Callable[..., AsyncGenerator[T_Retval, Any]],
        kwargs: dict[str, Any],
    ) -> Iterable[T_Retval]:
        async def fixture_runner(*, task_status: TaskStatus[T_Retval]) -> None:
            agen = fixture_func(**kwargs)
            retval = await agen.asend(None)
            task_status.started(retval)
            await teardown_event.wait()
            try:
                await agen.asend(None)
            except StopAsyncIteration:
                pass
            else:
                await agen.aclose()
                raise RuntimeError("Async generator fixture did not stop")

        teardown_event = trio.Event()
        fixture_value = self._call(lambda: self._get_nursery().start(fixture_runner))
        yield fixture_value
        teardown_event.set()

    def run_fixture(
        self,
        fixture_func: Callable[..., Coroutine[Any, Any, T_Retval]],
        kwargs: dict[str, Any],
    ) -> T_Retval:
        return self._call(fixture_func, **kwargs)

    def run_test(
        self, test_func: Callable[..., Coroutine[Any, Any, Any]], kwargs: dict[str, Any]
    ) -> None:
        self._call(test_func, **kwargs)

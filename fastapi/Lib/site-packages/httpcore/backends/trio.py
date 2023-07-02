import ssl
import typing

import trio

from .._exceptions import (
    ConnectError,
    ConnectTimeout,
    ExceptionMapping,
    ReadError,
    ReadTimeout,
    WriteError,
    WriteTimeout,
    map_exceptions,
)
from .base import SOCKET_OPTION, AsyncNetworkBackend, AsyncNetworkStream


class TrioStream(AsyncNetworkStream):
    def __init__(self, stream: trio.abc.Stream) -> None:
        self._stream = stream

    async def read(
        self, max_bytes: int, timeout: typing.Optional[float] = None
    ) -> bytes:
        timeout_or_inf = float("inf") if timeout is None else timeout
        exc_map: ExceptionMapping = {
            trio.TooSlowError: ReadTimeout,
            trio.BrokenResourceError: ReadError,
            trio.ClosedResourceError: ReadError,
        }
        with map_exceptions(exc_map):
            with trio.fail_after(timeout_or_inf):
                data: bytes = await self._stream.receive_some(max_bytes=max_bytes)
                return data

    async def write(
        self, buffer: bytes, timeout: typing.Optional[float] = None
    ) -> None:
        if not buffer:
            return

        timeout_or_inf = float("inf") if timeout is None else timeout
        exc_map: ExceptionMapping = {
            trio.TooSlowError: WriteTimeout,
            trio.BrokenResourceError: WriteError,
            trio.ClosedResourceError: WriteError,
        }
        with map_exceptions(exc_map):
            with trio.fail_after(timeout_or_inf):
                await self._stream.send_all(data=buffer)

    async def aclose(self) -> None:
        await self._stream.aclose()

    async def start_tls(
        self,
        ssl_context: ssl.SSLContext,
        server_hostname: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
    ) -> AsyncNetworkStream:
        timeout_or_inf = float("inf") if timeout is None else timeout
        exc_map: ExceptionMapping = {
            trio.TooSlowError: ConnectTimeout,
            trio.BrokenResourceError: ConnectError,
        }
        ssl_stream = trio.SSLStream(
            self._stream,
            ssl_context=ssl_context,
            server_hostname=server_hostname,
            https_compatible=True,
            server_side=False,
        )
        with map_exceptions(exc_map):
            try:
                with trio.fail_after(timeout_or_inf):
                    await ssl_stream.do_handshake()
            except Exception as exc:  # pragma: nocover
                await self.aclose()
                raise exc
        return TrioStream(ssl_stream)

    def get_extra_info(self, info: str) -> typing.Any:
        if info == "ssl_object" and isinstance(self._stream, trio.SSLStream):
            # Type checkers cannot see `_ssl_object` attribute because trio._ssl.SSLStream uses __getattr__/__setattr__.
            # Tracked at https://github.com/python-trio/trio/issues/542
            return self._stream._ssl_object  # type: ignore[attr-defined]
        if info == "client_addr":
            return self._get_socket_stream().socket.getsockname()
        if info == "server_addr":
            return self._get_socket_stream().socket.getpeername()
        if info == "socket":
            stream = self._stream
            while isinstance(stream, trio.SSLStream):
                stream = stream.transport_stream
            assert isinstance(stream, trio.SocketStream)
            return stream.socket
        if info == "is_readable":
            socket = self.get_extra_info("socket")
            return socket.is_readable()
        return None

    def _get_socket_stream(self) -> trio.SocketStream:
        stream = self._stream
        while isinstance(stream, trio.SSLStream):
            stream = stream.transport_stream
        assert isinstance(stream, trio.SocketStream)
        return stream


class TrioBackend(AsyncNetworkBackend):
    async def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: typing.Optional[float] = None,
        local_address: typing.Optional[str] = None,
        socket_options: typing.Optional[typing.Iterable[SOCKET_OPTION]] = None,
    ) -> AsyncNetworkStream:
        # By default for TCP sockets, trio enables TCP_NODELAY.
        # https://trio.readthedocs.io/en/stable/reference-io.html#trio.SocketStream
        if socket_options is None:
            socket_options = []  # pragma: no cover
        timeout_or_inf = float("inf") if timeout is None else timeout
        exc_map: ExceptionMapping = {
            trio.TooSlowError: ConnectTimeout,
            trio.BrokenResourceError: ConnectError,
            OSError: ConnectError,
        }
        with map_exceptions(exc_map):
            with trio.fail_after(timeout_or_inf):
                stream: trio.abc.Stream = await trio.open_tcp_stream(
                    host=host, port=port, local_address=local_address
                )
                for option in socket_options:
                    stream.setsockopt(*option)  # type: ignore[attr-defined] # pragma: no cover
        return TrioStream(stream)

    async def connect_unix_socket(
        self,
        path: str,
        timeout: typing.Optional[float] = None,
        socket_options: typing.Optional[typing.Iterable[SOCKET_OPTION]] = None,
    ) -> AsyncNetworkStream:  # pragma: nocover
        if socket_options is None:
            socket_options = []
        timeout_or_inf = float("inf") if timeout is None else timeout
        exc_map: ExceptionMapping = {
            trio.TooSlowError: ConnectTimeout,
            trio.BrokenResourceError: ConnectError,
            OSError: ConnectError,
        }
        with map_exceptions(exc_map):
            with trio.fail_after(timeout_or_inf):
                stream: trio.abc.Stream = await trio.open_unix_socket(path)
                for option in socket_options:
                    stream.setsockopt(*option)  # type: ignore[attr-defined] # pragma: no cover
        return TrioStream(stream)

    async def sleep(self, seconds: float) -> None:
        await trio.sleep(seconds)  # pragma: nocover

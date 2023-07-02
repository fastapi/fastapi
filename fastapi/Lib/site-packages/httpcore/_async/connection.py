import itertools
import logging
import ssl
from types import TracebackType
from typing import Iterable, Iterator, Optional, Type

from .._exceptions import ConnectError, ConnectionNotAvailable, ConnectTimeout
from .._models import Origin, Request, Response
from .._ssl import default_ssl_context
from .._synchronization import AsyncLock
from .._trace import Trace
from ..backends.auto import AutoBackend
from ..backends.base import SOCKET_OPTION, AsyncNetworkBackend, AsyncNetworkStream
from .http11 import AsyncHTTP11Connection
from .interfaces import AsyncConnectionInterface

RETRIES_BACKOFF_FACTOR = 0.5  # 0s, 0.5s, 1s, 2s, 4s, etc.


logger = logging.getLogger("httpcore.connection")


def exponential_backoff(factor: float) -> Iterator[float]:
    yield 0
    for n in itertools.count(2):
        yield factor * (2 ** (n - 2))


class AsyncHTTPConnection(AsyncConnectionInterface):
    def __init__(
        self,
        origin: Origin,
        ssl_context: Optional[ssl.SSLContext] = None,
        keepalive_expiry: Optional[float] = None,
        http1: bool = True,
        http2: bool = False,
        retries: int = 0,
        local_address: Optional[str] = None,
        uds: Optional[str] = None,
        network_backend: Optional[AsyncNetworkBackend] = None,
        socket_options: Optional[Iterable[SOCKET_OPTION]] = None,
    ) -> None:
        self._origin = origin
        self._ssl_context = ssl_context
        self._keepalive_expiry = keepalive_expiry
        self._http1 = http1
        self._http2 = http2
        self._retries = retries
        self._local_address = local_address
        self._uds = uds

        self._network_backend: AsyncNetworkBackend = (
            AutoBackend() if network_backend is None else network_backend
        )
        self._connection: Optional[AsyncConnectionInterface] = None
        self._connect_failed: bool = False
        self._request_lock = AsyncLock()
        self._socket_options = socket_options

    async def handle_async_request(self, request: Request) -> Response:
        if not self.can_handle_request(request.url.origin):
            raise RuntimeError(
                f"Attempted to send request to {request.url.origin} on connection to {self._origin}"
            )

        async with self._request_lock:
            if self._connection is None:
                try:
                    stream = await self._connect(request)

                    ssl_object = stream.get_extra_info("ssl_object")
                    http2_negotiated = (
                        ssl_object is not None
                        and ssl_object.selected_alpn_protocol() == "h2"
                    )
                    if http2_negotiated or (self._http2 and not self._http1):
                        from .http2 import AsyncHTTP2Connection

                        self._connection = AsyncHTTP2Connection(
                            origin=self._origin,
                            stream=stream,
                            keepalive_expiry=self._keepalive_expiry,
                        )
                    else:
                        self._connection = AsyncHTTP11Connection(
                            origin=self._origin,
                            stream=stream,
                            keepalive_expiry=self._keepalive_expiry,
                        )
                except Exception as exc:
                    self._connect_failed = True
                    raise exc
            elif not self._connection.is_available():
                raise ConnectionNotAvailable()

        return await self._connection.handle_async_request(request)

    async def _connect(self, request: Request) -> AsyncNetworkStream:
        timeouts = request.extensions.get("timeout", {})
        sni_hostname = request.extensions.get("sni_hostname", None)
        timeout = timeouts.get("connect", None)

        retries_left = self._retries
        delays = exponential_backoff(factor=RETRIES_BACKOFF_FACTOR)

        while True:
            try:
                if self._uds is None:
                    kwargs = {
                        "host": self._origin.host.decode("ascii"),
                        "port": self._origin.port,
                        "local_address": self._local_address,
                        "timeout": timeout,
                        "socket_options": self._socket_options,
                    }
                    async with Trace("connect_tcp", logger, request, kwargs) as trace:
                        stream = await self._network_backend.connect_tcp(**kwargs)
                        trace.return_value = stream
                else:
                    kwargs = {
                        "path": self._uds,
                        "timeout": timeout,
                        "socket_options": self._socket_options,
                    }
                    async with Trace(
                        "connect_unix_socket", logger, request, kwargs
                    ) as trace:
                        stream = await self._network_backend.connect_unix_socket(
                            **kwargs
                        )
                        trace.return_value = stream

                if self._origin.scheme == b"https":
                    ssl_context = (
                        default_ssl_context()
                        if self._ssl_context is None
                        else self._ssl_context
                    )
                    alpn_protocols = ["http/1.1", "h2"] if self._http2 else ["http/1.1"]
                    ssl_context.set_alpn_protocols(alpn_protocols)

                    kwargs = {
                        "ssl_context": ssl_context,
                        "server_hostname": sni_hostname
                        or self._origin.host.decode("ascii"),
                        "timeout": timeout,
                    }
                    async with Trace("start_tls", logger, request, kwargs) as trace:
                        stream = await stream.start_tls(**kwargs)
                        trace.return_value = stream
                return stream
            except (ConnectError, ConnectTimeout):
                if retries_left <= 0:
                    raise
                retries_left -= 1
                delay = next(delays)
                async with Trace("retry", logger, request, kwargs) as trace:
                    await self._network_backend.sleep(delay)

    def can_handle_request(self, origin: Origin) -> bool:
        return origin == self._origin

    async def aclose(self) -> None:
        if self._connection is not None:
            async with Trace("close", logger, None, {}):
                await self._connection.aclose()

    def is_available(self) -> bool:
        if self._connection is None:
            # If HTTP/2 support is enabled, and the resulting connection could
            # end up as HTTP/2 then we should indicate the connection as being
            # available to service multiple requests.
            return (
                self._http2
                and (self._origin.scheme == b"https" or not self._http1)
                and not self._connect_failed
            )
        return self._connection.is_available()

    def has_expired(self) -> bool:
        if self._connection is None:
            return self._connect_failed
        return self._connection.has_expired()

    def is_idle(self) -> bool:
        if self._connection is None:
            return self._connect_failed
        return self._connection.is_idle()

    def is_closed(self) -> bool:
        if self._connection is None:
            return self._connect_failed
        return self._connection.is_closed()

    def info(self) -> str:
        if self._connection is None:
            return "CONNECTION FAILED" if self._connect_failed else "CONNECTING"
        return self._connection.info()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.info()}]>"

    # These context managers are not used in the standard flow, but are
    # useful for testing or working with connection instances directly.

    async def __aenter__(self) -> "AsyncHTTPConnection":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.aclose()

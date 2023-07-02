import logging
import ssl
import typing

from socksio import socks5

from .._exceptions import ConnectionNotAvailable, ProxyError
from .._models import URL, Origin, Request, Response, enforce_bytes, enforce_url
from .._ssl import default_ssl_context
from .._synchronization import AsyncLock
from .._trace import Trace
from ..backends.auto import AutoBackend
from ..backends.base import AsyncNetworkBackend, AsyncNetworkStream
from .connection_pool import AsyncConnectionPool
from .http11 import AsyncHTTP11Connection
from .interfaces import AsyncConnectionInterface

logger = logging.getLogger("httpcore.socks")


AUTH_METHODS = {
    b"\x00": "NO AUTHENTICATION REQUIRED",
    b"\x01": "GSSAPI",
    b"\x02": "USERNAME/PASSWORD",
    b"\xff": "NO ACCEPTABLE METHODS",
}

REPLY_CODES = {
    b"\x00": "Succeeded",
    b"\x01": "General SOCKS server failure",
    b"\x02": "Connection not allowed by ruleset",
    b"\x03": "Network unreachable",
    b"\x04": "Host unreachable",
    b"\x05": "Connection refused",
    b"\x06": "TTL expired",
    b"\x07": "Command not supported",
    b"\x08": "Address type not supported",
}


async def _init_socks5_connection(
    stream: AsyncNetworkStream,
    *,
    host: bytes,
    port: int,
    auth: typing.Optional[typing.Tuple[bytes, bytes]] = None,
) -> None:
    conn = socks5.SOCKS5Connection()

    # Auth method request
    auth_method = (
        socks5.SOCKS5AuthMethod.NO_AUTH_REQUIRED
        if auth is None
        else socks5.SOCKS5AuthMethod.USERNAME_PASSWORD
    )
    conn.send(socks5.SOCKS5AuthMethodsRequest([auth_method]))
    outgoing_bytes = conn.data_to_send()
    await stream.write(outgoing_bytes)

    # Auth method response
    incoming_bytes = await stream.read(max_bytes=4096)
    response = conn.receive_data(incoming_bytes)
    assert isinstance(response, socks5.SOCKS5AuthReply)
    if response.method != auth_method:
        requested = AUTH_METHODS.get(auth_method, "UNKNOWN")
        responded = AUTH_METHODS.get(response.method, "UNKNOWN")
        raise ProxyError(
            f"Requested {requested} from proxy server, but got {responded}."
        )

    if response.method == socks5.SOCKS5AuthMethod.USERNAME_PASSWORD:
        # Username/password request
        assert auth is not None
        username, password = auth
        conn.send(socks5.SOCKS5UsernamePasswordRequest(username, password))
        outgoing_bytes = conn.data_to_send()
        await stream.write(outgoing_bytes)

        # Username/password response
        incoming_bytes = await stream.read(max_bytes=4096)
        response = conn.receive_data(incoming_bytes)
        assert isinstance(response, socks5.SOCKS5UsernamePasswordReply)
        if not response.success:
            raise ProxyError("Invalid username/password")

    # Connect request
    conn.send(
        socks5.SOCKS5CommandRequest.from_address(
            socks5.SOCKS5Command.CONNECT, (host, port)
        )
    )
    outgoing_bytes = conn.data_to_send()
    await stream.write(outgoing_bytes)

    # Connect response
    incoming_bytes = await stream.read(max_bytes=4096)
    response = conn.receive_data(incoming_bytes)
    assert isinstance(response, socks5.SOCKS5Reply)
    if response.reply_code != socks5.SOCKS5ReplyCode.SUCCEEDED:
        reply_code = REPLY_CODES.get(response.reply_code, "UNKOWN")
        raise ProxyError(f"Proxy Server could not connect: {reply_code}.")


class AsyncSOCKSProxy(AsyncConnectionPool):
    """
    A connection pool that sends requests via an HTTP proxy.
    """

    def __init__(
        self,
        proxy_url: typing.Union[URL, bytes, str],
        proxy_auth: typing.Optional[
            typing.Tuple[typing.Union[bytes, str], typing.Union[bytes, str]]
        ] = None,
        ssl_context: typing.Optional[ssl.SSLContext] = None,
        max_connections: typing.Optional[int] = 10,
        max_keepalive_connections: typing.Optional[int] = None,
        keepalive_expiry: typing.Optional[float] = None,
        http1: bool = True,
        http2: bool = False,
        retries: int = 0,
        network_backend: typing.Optional[AsyncNetworkBackend] = None,
    ) -> None:
        """
        A connection pool for making HTTP requests.

        Parameters:
            proxy_url: The URL to use when connecting to the proxy server.
                For example `"http://127.0.0.1:8080/"`.
            ssl_context: An SSL context to use for verifying connections.
                If not specified, the default `httpcore.default_ssl_context()`
                will be used.
            max_connections: The maximum number of concurrent HTTP connections that
                the pool should allow. Any attempt to send a request on a pool that
                would exceed this amount will block until a connection is available.
            max_keepalive_connections: The maximum number of idle HTTP connections
                that will be maintained in the pool.
            keepalive_expiry: The duration in seconds that an idle HTTP connection
                may be maintained for before being expired from the pool.
            http1: A boolean indicating if HTTP/1.1 requests should be supported
                by the connection pool. Defaults to True.
            http2: A boolean indicating if HTTP/2 requests should be supported by
                the connection pool. Defaults to False.
            retries: The maximum number of retries when trying to establish
                a connection.
            local_address: Local address to connect from. Can also be used to
                connect using a particular address family. Using
                `local_address="0.0.0.0"` will connect using an `AF_INET` address
                (IPv4), while using `local_address="::"` will connect using an
                `AF_INET6` address (IPv6).
            uds: Path to a Unix Domain Socket to use instead of TCP sockets.
            network_backend: A backend instance to use for handling network I/O.
        """
        super().__init__(
            ssl_context=ssl_context,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
            http1=http1,
            http2=http2,
            network_backend=network_backend,
            retries=retries,
        )
        self._ssl_context = ssl_context
        self._proxy_url = enforce_url(proxy_url, name="proxy_url")
        if proxy_auth is not None:
            username, password = proxy_auth
            username_bytes = enforce_bytes(username, name="proxy_auth")
            password_bytes = enforce_bytes(password, name="proxy_auth")
            self._proxy_auth: typing.Optional[typing.Tuple[bytes, bytes]] = (
                username_bytes,
                password_bytes,
            )
        else:
            self._proxy_auth = None

    def create_connection(self, origin: Origin) -> AsyncConnectionInterface:
        return AsyncSocks5Connection(
            proxy_origin=self._proxy_url.origin,
            remote_origin=origin,
            proxy_auth=self._proxy_auth,
            ssl_context=self._ssl_context,
            keepalive_expiry=self._keepalive_expiry,
            http1=self._http1,
            http2=self._http2,
            network_backend=self._network_backend,
        )


class AsyncSocks5Connection(AsyncConnectionInterface):
    def __init__(
        self,
        proxy_origin: Origin,
        remote_origin: Origin,
        proxy_auth: typing.Optional[typing.Tuple[bytes, bytes]] = None,
        ssl_context: typing.Optional[ssl.SSLContext] = None,
        keepalive_expiry: typing.Optional[float] = None,
        http1: bool = True,
        http2: bool = False,
        network_backend: typing.Optional[AsyncNetworkBackend] = None,
    ) -> None:
        self._proxy_origin = proxy_origin
        self._remote_origin = remote_origin
        self._proxy_auth = proxy_auth
        self._ssl_context = ssl_context
        self._keepalive_expiry = keepalive_expiry
        self._http1 = http1
        self._http2 = http2

        self._network_backend: AsyncNetworkBackend = (
            AutoBackend() if network_backend is None else network_backend
        )
        self._connect_lock = AsyncLock()
        self._connection: typing.Optional[AsyncConnectionInterface] = None
        self._connect_failed = False

    async def handle_async_request(self, request: Request) -> Response:
        timeouts = request.extensions.get("timeout", {})
        timeout = timeouts.get("connect", None)

        async with self._connect_lock:
            if self._connection is None:
                try:
                    # Connect to the proxy
                    kwargs = {
                        "host": self._proxy_origin.host.decode("ascii"),
                        "port": self._proxy_origin.port,
                        "timeout": timeout,
                    }
                    with Trace("connect_tcp", logger, request, kwargs) as trace:
                        stream = await self._network_backend.connect_tcp(**kwargs)
                        trace.return_value = stream

                    # Connect to the remote host using socks5
                    kwargs = {
                        "stream": stream,
                        "host": self._remote_origin.host.decode("ascii"),
                        "port": self._remote_origin.port,
                        "auth": self._proxy_auth,
                    }
                    with Trace(
                        "setup_socks5_connection", logger, request, kwargs
                    ) as trace:
                        await _init_socks5_connection(**kwargs)
                        trace.return_value = stream

                    # Upgrade the stream to SSL
                    if self._remote_origin.scheme == b"https":
                        ssl_context = (
                            default_ssl_context()
                            if self._ssl_context is None
                            else self._ssl_context
                        )
                        alpn_protocols = (
                            ["http/1.1", "h2"] if self._http2 else ["http/1.1"]
                        )
                        ssl_context.set_alpn_protocols(alpn_protocols)

                        kwargs = {
                            "ssl_context": ssl_context,
                            "server_hostname": self._remote_origin.host.decode("ascii"),
                            "timeout": timeout,
                        }
                        async with Trace("start_tls", logger, request, kwargs) as trace:
                            stream = await stream.start_tls(**kwargs)
                            trace.return_value = stream

                    # Determine if we should be using HTTP/1.1 or HTTP/2
                    ssl_object = stream.get_extra_info("ssl_object")
                    http2_negotiated = (
                        ssl_object is not None
                        and ssl_object.selected_alpn_protocol() == "h2"
                    )

                    # Create the HTTP/1.1 or HTTP/2 connection
                    if http2_negotiated or (
                        self._http2 and not self._http1
                    ):  # pragma: nocover
                        from .http2 import AsyncHTTP2Connection

                        self._connection = AsyncHTTP2Connection(
                            origin=self._remote_origin,
                            stream=stream,
                            keepalive_expiry=self._keepalive_expiry,
                        )
                    else:
                        self._connection = AsyncHTTP11Connection(
                            origin=self._remote_origin,
                            stream=stream,
                            keepalive_expiry=self._keepalive_expiry,
                        )
                except Exception as exc:
                    self._connect_failed = True
                    raise exc
            elif not self._connection.is_available():  # pragma: nocover
                raise ConnectionNotAvailable()

        return await self._connection.handle_async_request(request)

    def can_handle_request(self, origin: Origin) -> bool:
        return origin == self._remote_origin

    async def aclose(self) -> None:
        if self._connection is not None:
            await self._connection.aclose()

    def is_available(self) -> bool:
        if self._connection is None:  # pragma: nocover
            # If HTTP/2 support is enabled, and the resulting connection could
            # end up as HTTP/2 then we should indicate the connection as being
            # available to service multiple requests.
            return (
                self._http2
                and (self._remote_origin.scheme == b"https" or not self._http1)
                and not self._connect_failed
            )
        return self._connection.is_available()

    def has_expired(self) -> bool:
        if self._connection is None:  # pragma: nocover
            return self._connect_failed
        return self._connection.has_expired()

    def is_idle(self) -> bool:
        if self._connection is None:  # pragma: nocover
            return self._connect_failed
        return self._connection.is_idle()

    def is_closed(self) -> bool:
        if self._connection is None:  # pragma: nocover
            return self._connect_failed
        return self._connection.is_closed()

    def info(self) -> str:
        if self._connection is None:  # pragma: nocover
            return "CONNECTION FAILED" if self._connect_failed else "CONNECTING"
        return self._connection.info()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.info()}]>"

from .connection import AsyncHTTPConnection
from .connection_pool import AsyncConnectionPool
from .http11 import AsyncHTTP11Connection
from .http_proxy import AsyncHTTPProxy
from .interfaces import AsyncConnectionInterface

try:
    from .http2 import AsyncHTTP2Connection
except ImportError:  # pragma: nocover

    class AsyncHTTP2Connection:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # type: ignore
            raise RuntimeError(
                "Attempted to use http2 support, but the `h2` package is not "
                "installed. Use 'pip install httpcore[http2]'."
            )


try:
    from .socks_proxy import AsyncSOCKSProxy
except ImportError:  # pragma: nocover

    class AsyncSOCKSProxy:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # type: ignore
            raise RuntimeError(
                "Attempted to use SOCKS support, but the `socksio` package is not "
                "installed. Use 'pip install httpcore[socks]'."
            )


__all__ = [
    "AsyncHTTPConnection",
    "AsyncConnectionPool",
    "AsyncHTTPProxy",
    "AsyncHTTP11Connection",
    "AsyncHTTP2Connection",
    "AsyncConnectionInterface",
    "AsyncSOCKSProxy",
]

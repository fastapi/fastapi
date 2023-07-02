"""
Our exception hierarchy:

* HTTPError
  x RequestError
    + TransportError
      - TimeoutException
        · ConnectTimeout
        · ReadTimeout
        · WriteTimeout
        · PoolTimeout
      - NetworkError
        · ConnectError
        · ReadError
        · WriteError
        · CloseError
      - ProtocolError
        · LocalProtocolError
        · RemoteProtocolError
      - ProxyError
      - UnsupportedProtocol
    + DecodingError
    + TooManyRedirects
  x HTTPStatusError
* InvalidURL
* CookieConflict
* StreamError
  x StreamConsumed
  x StreamClosed
  x ResponseNotRead
  x RequestNotRead
"""
import contextlib
import typing

if typing.TYPE_CHECKING:
    from ._models import Request, Response  # pragma: no cover


class HTTPError(Exception):
    """
    Base class for `RequestError` and `HTTPStatusError`.

    Useful for `try...except` blocks when issuing a request,
    and then calling `.raise_for_status()`.

    For example:

    ```
    try:
        response = httpx.get("https://www.example.com")
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"HTTP Exception for {exc.request.url} - {exc}")
    ```
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._request: typing.Optional["Request"] = None

    @property
    def request(self) -> "Request":
        if self._request is None:
            raise RuntimeError("The .request property has not been set.")
        return self._request

    @request.setter
    def request(self, request: "Request") -> None:
        self._request = request


class RequestError(HTTPError):
    """
    Base class for all exceptions that may occur when issuing a `.request()`.
    """

    def __init__(
        self, message: str, *, request: typing.Optional["Request"] = None
    ) -> None:
        super().__init__(message)
        # At the point an exception is raised we won't typically have a request
        # instance to associate it with.
        #
        # The 'request_context' context manager is used within the Client and
        # Response methods in order to ensure that any raised exceptions
        # have a `.request` property set on them.
        self._request = request


class TransportError(RequestError):
    """
    Base class for all exceptions that occur at the level of the Transport API.
    """


# Timeout exceptions...


class TimeoutException(TransportError):
    """
    The base class for timeout errors.

    An operation has timed out.
    """


class ConnectTimeout(TimeoutException):
    """
    Timed out while connecting to the host.
    """


class ReadTimeout(TimeoutException):
    """
    Timed out while receiving data from the host.
    """


class WriteTimeout(TimeoutException):
    """
    Timed out while sending data to the host.
    """


class PoolTimeout(TimeoutException):
    """
    Timed out waiting to acquire a connection from the pool.
    """


# Core networking exceptions...


class NetworkError(TransportError):
    """
    The base class for network-related errors.

    An error occurred while interacting with the network.
    """


class ReadError(NetworkError):
    """
    Failed to receive data from the network.
    """


class WriteError(NetworkError):
    """
    Failed to send data through the network.
    """


class ConnectError(NetworkError):
    """
    Failed to establish a connection.
    """


class CloseError(NetworkError):
    """
    Failed to close a connection.
    """


# Other transport exceptions...


class ProxyError(TransportError):
    """
    An error occurred while establishing a proxy connection.
    """


class UnsupportedProtocol(TransportError):
    """
    Attempted to make a request to an unsupported protocol.

    For example issuing a request to `ftp://www.example.com`.
    """


class ProtocolError(TransportError):
    """
    The protocol was violated.
    """


class LocalProtocolError(ProtocolError):
    """
    A protocol was violated by the client.

    For example if the user instantiated a `Request` instance explicitly,
    failed to include the mandatory `Host:` header, and then issued it directly
    using `client.send()`.
    """


class RemoteProtocolError(ProtocolError):
    """
    The protocol was violated by the server.

    For example, returning malformed HTTP.
    """


# Other request exceptions...


class DecodingError(RequestError):
    """
    Decoding of the response failed, due to a malformed encoding.
    """


class TooManyRedirects(RequestError):
    """
    Too many redirects.
    """


# Client errors


class HTTPStatusError(HTTPError):
    """
    The response had an error HTTP status of 4xx or 5xx.

    May be raised when calling `response.raise_for_status()`
    """

    def __init__(
        self, message: str, *, request: "Request", response: "Response"
    ) -> None:
        super().__init__(message)
        self.request = request
        self.response = response


class InvalidURL(Exception):
    """
    URL is improperly formed or cannot be parsed.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CookieConflict(Exception):
    """
    Attempted to lookup a cookie by name, but multiple cookies existed.

    Can occur when calling `response.cookies.get(...)`.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


# Stream exceptions...

# These may occur as the result of a programming error, by accessing
# the request/response stream in an invalid manner.


class StreamError(RuntimeError):
    """
    The base class for stream exceptions.

    The developer made an error in accessing the request stream in
    an invalid way.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class StreamConsumed(StreamError):
    """
    Attempted to read or stream content, but the content has already
    been streamed.
    """

    def __init__(self) -> None:
        message = (
            "Attempted to read or stream some content, but the content has "
            "already been streamed. For requests, this could be due to passing "
            "a generator as request content, and then receiving a redirect "
            "response or a secondary request as part of an authentication flow."
            "For responses, this could be due to attempting to stream the response "
            "content more than once."
        )
        super().__init__(message)


class StreamClosed(StreamError):
    """
    Attempted to read or stream response content, but the request has been
    closed.
    """

    def __init__(self) -> None:
        message = (
            "Attempted to read or stream content, but the stream has " "been closed."
        )
        super().__init__(message)


class ResponseNotRead(StreamError):
    """
    Attempted to access streaming response content, without having called `read()`.
    """

    def __init__(self) -> None:
        message = "Attempted to access streaming response content, without having called `read()`."
        super().__init__(message)


class RequestNotRead(StreamError):
    """
    Attempted to access streaming request content, without having called `read()`.
    """

    def __init__(self) -> None:
        message = "Attempted to access streaming request content, without having called `read()`."
        super().__init__(message)


@contextlib.contextmanager
def request_context(
    request: typing.Optional["Request"] = None,
) -> typing.Iterator[None]:
    """
    A context manager that can be used to attach the given request context
    to any `RequestError` exceptions that are raised within the block.
    """
    try:
        yield
    except RequestError as exc:
        if request is not None:
            exc.request = request
        raise exc

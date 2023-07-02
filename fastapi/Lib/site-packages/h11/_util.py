from typing import Any, Dict, NoReturn, Pattern, Tuple, Type, TypeVar, Union

__all__ = [
    "ProtocolError",
    "LocalProtocolError",
    "RemoteProtocolError",
    "validate",
    "bytesify",
]


class ProtocolError(Exception):
    """Exception indicating a violation of the HTTP/1.1 protocol.

    This as an abstract base class, with two concrete base classes:
    :exc:`LocalProtocolError`, which indicates that you tried to do something
    that HTTP/1.1 says is illegal, and :exc:`RemoteProtocolError`, which
    indicates that the remote peer tried to do something that HTTP/1.1 says is
    illegal. See :ref:`error-handling` for details.

    In addition to the normal :exc:`Exception` features, it has one attribute:

    .. attribute:: error_status_hint

       This gives a suggestion as to what status code a server might use if
       this error occurred as part of a request.

       For a :exc:`RemoteProtocolError`, this is useful as a suggestion for
       how you might want to respond to a misbehaving peer, if you're
       implementing a server.

       For a :exc:`LocalProtocolError`, this can be taken as a suggestion for
       how your peer might have responded to *you* if h11 had allowed you to
       continue.

       The default is 400 Bad Request, a generic catch-all for protocol
       violations.

    """

    def __init__(self, msg: str, error_status_hint: int = 400) -> None:
        if type(self) is ProtocolError:
            raise TypeError("tried to directly instantiate ProtocolError")
        Exception.__init__(self, msg)
        self.error_status_hint = error_status_hint


# Strategy: there are a number of public APIs where a LocalProtocolError can
# be raised (send(), all the different event constructors, ...), and only one
# public API where RemoteProtocolError can be raised
# (receive_data()). Therefore we always raise LocalProtocolError internally,
# and then receive_data will translate this into a RemoteProtocolError.
#
# Internally:
#   LocalProtocolError is the generic "ProtocolError".
# Externally:
#   LocalProtocolError is for local errors and RemoteProtocolError is for
#   remote errors.
class LocalProtocolError(ProtocolError):
    def _reraise_as_remote_protocol_error(self) -> NoReturn:
        # After catching a LocalProtocolError, use this method to re-raise it
        # as a RemoteProtocolError. This method must be called from inside an
        # except: block.
        #
        # An easy way to get an equivalent RemoteProtocolError is just to
        # modify 'self' in place.
        self.__class__ = RemoteProtocolError  # type: ignore
        # But the re-raising is somewhat non-trivial -- you might think that
        # now that we've modified the in-flight exception object, that just
        # doing 'raise' to re-raise it would be enough. But it turns out that
        # this doesn't work, because Python tracks the exception type
        # (exc_info[0]) separately from the exception object (exc_info[1]),
        # and we only modified the latter. So we really do need to re-raise
        # the new type explicitly.
        # On py3, the traceback is part of the exception object, so our
        # in-place modification preserved it and we can just re-raise:
        raise self


class RemoteProtocolError(ProtocolError):
    pass


def validate(
    regex: Pattern[bytes], data: bytes, msg: str = "malformed data", *format_args: Any
) -> Dict[str, bytes]:
    match = regex.fullmatch(data)
    if not match:
        if format_args:
            msg = msg.format(*format_args)
        raise LocalProtocolError(msg)
    return match.groupdict()


# Sentinel values
#
# - Inherit identity-based comparison and hashing from object
# - Have a nice repr
# - Have a *bonus property*: type(sentinel) is sentinel
#
# The bonus property is useful if you want to take the return value from
# next_event() and do some sort of dispatch based on type(event).

_T_Sentinel = TypeVar("_T_Sentinel", bound="Sentinel")


class Sentinel(type):
    def __new__(
        cls: Type[_T_Sentinel],
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwds: Any,
    ) -> _T_Sentinel:
        assert bases == (Sentinel,)
        v = super().__new__(cls, name, bases, namespace, **kwds)
        v.__class__ = v  # type: ignore
        return v

    def __repr__(self) -> str:
        return self.__name__


# Used for methods, request targets, HTTP versions, header names, and header
# values. Accepts ascii-strings, or bytes/bytearray/memoryview/..., and always
# returns bytes.
def bytesify(s: Union[bytes, bytearray, memoryview, int, str]) -> bytes:
    # Fast-path:
    if type(s) is bytes:
        return s
    if isinstance(s, str):
        s = s.encode("ascii")
    if isinstance(s, int):
        raise TypeError("expected bytes-like object, not int")
    return bytes(s)

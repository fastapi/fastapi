from .. import socket as tsocket
from .._highlevel_socket import SocketStream


async def open_stream_to_socket_listener(socket_listener):
    """Connect to the given :class:`~trio.SocketListener`.

    This is particularly useful in tests when you want to let a server pick
    its own port, and then connect to it::

        listeners = await trio.open_tcp_listeners(0)
        client = await trio.testing.open_stream_to_socket_listener(listeners[0])

    Args:
      socket_listener (~trio.SocketListener): The
          :class:`~trio.SocketListener` to connect to.

    Returns:
      SocketStream: a stream connected to the given listener.

    """
    family = socket_listener.socket.family
    sockaddr = socket_listener.socket.getsockname()
    if family in (tsocket.AF_INET, tsocket.AF_INET6):
        sockaddr = list(sockaddr)
        if sockaddr[0] == "0.0.0.0":
            sockaddr[0] = "127.0.0.1"
        if sockaddr[0] == "::":
            sockaddr[0] = "::1"
        sockaddr = tuple(sockaddr)

    sock = tsocket.socket(family=family)
    await sock.connect(sockaddr)
    return SocketStream(sock)

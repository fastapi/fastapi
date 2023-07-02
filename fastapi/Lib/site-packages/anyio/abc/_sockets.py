from __future__ import annotations

import socket
from abc import abstractmethod
from contextlib import AsyncExitStack
from io import IOBase
from ipaddress import IPv4Address, IPv6Address
from socket import AddressFamily
from typing import (
    Any,
    Callable,
    Collection,
    Mapping,
    Tuple,
    TypeVar,
    Union,
)

from .._core._tasks import create_task_group
from .._core._typedattr import (
    TypedAttributeProvider,
    TypedAttributeSet,
    typed_attribute,
)
from ._streams import ByteStream, Listener, UnreliableObjectStream
from ._tasks import TaskGroup

IPAddressType = Union[str, IPv4Address, IPv6Address]
IPSockAddrType = Tuple[str, int]
SockAddrType = Union[IPSockAddrType, str]
UDPPacketType = Tuple[bytes, IPSockAddrType]
T_Retval = TypeVar("T_Retval")


class SocketAttribute(TypedAttributeSet):
    #: the address family of the underlying socket
    family: AddressFamily = typed_attribute()
    #: the local socket address of the underlying socket
    local_address: SockAddrType = typed_attribute()
    #: for IP addresses, the local port the underlying socket is bound to
    local_port: int = typed_attribute()
    #: the underlying stdlib socket object
    raw_socket: socket.socket = typed_attribute()
    #: the remote address the underlying socket is connected to
    remote_address: SockAddrType = typed_attribute()
    #: for IP addresses, the remote port the underlying socket is connected to
    remote_port: int = typed_attribute()


class _SocketProvider(TypedAttributeProvider):
    @property
    def extra_attributes(self) -> Mapping[Any, Callable[[], Any]]:
        from .._core._sockets import convert_ipv6_sockaddr as convert

        attributes: dict[Any, Callable[[], Any]] = {
            SocketAttribute.family: lambda: self._raw_socket.family,
            SocketAttribute.local_address: lambda: convert(
                self._raw_socket.getsockname()
            ),
            SocketAttribute.raw_socket: lambda: self._raw_socket,
        }
        try:
            peername: tuple[str, int] | None = convert(self._raw_socket.getpeername())
        except OSError:
            peername = None

        # Provide the remote address for connected sockets
        if peername is not None:
            attributes[SocketAttribute.remote_address] = lambda: peername

        # Provide local and remote ports for IP based sockets
        if self._raw_socket.family in (AddressFamily.AF_INET, AddressFamily.AF_INET6):
            attributes[
                SocketAttribute.local_port
            ] = lambda: self._raw_socket.getsockname()[1]
            if peername is not None:
                remote_port = peername[1]
                attributes[SocketAttribute.remote_port] = lambda: remote_port

        return attributes

    @property
    @abstractmethod
    def _raw_socket(self) -> socket.socket:
        pass


class SocketStream(ByteStream, _SocketProvider):
    """
    Transports bytes over a socket.

    Supports all relevant extra attributes from :class:`~SocketAttribute`.
    """


class UNIXSocketStream(SocketStream):
    @abstractmethod
    async def send_fds(self, message: bytes, fds: Collection[int | IOBase]) -> None:
        """
        Send file descriptors along with a message to the peer.

        :param message: a non-empty bytestring
        :param fds: a collection of files (either numeric file descriptors or open file or socket
            objects)
        """

    @abstractmethod
    async def receive_fds(self, msglen: int, maxfds: int) -> tuple[bytes, list[int]]:
        """
        Receive file descriptors along with a message from the peer.

        :param msglen: length of the message to expect from the peer
        :param maxfds: maximum number of file descriptors to expect from the peer
        :return: a tuple of (message, file descriptors)
        """


class SocketListener(Listener[SocketStream], _SocketProvider):
    """
    Listens to incoming socket connections.

    Supports all relevant extra attributes from :class:`~SocketAttribute`.
    """

    @abstractmethod
    async def accept(self) -> SocketStream:
        """Accept an incoming connection."""

    async def serve(
        self,
        handler: Callable[[SocketStream], Any],
        task_group: TaskGroup | None = None,
    ) -> None:
        async with AsyncExitStack() as exit_stack:
            if task_group is None:
                task_group = await exit_stack.enter_async_context(create_task_group())

            while True:
                stream = await self.accept()
                task_group.start_soon(handler, stream)


class UDPSocket(UnreliableObjectStream[UDPPacketType], _SocketProvider):
    """
    Represents an unconnected UDP socket.

    Supports all relevant extra attributes from :class:`~SocketAttribute`.
    """

    async def sendto(self, data: bytes, host: str, port: int) -> None:
        """Alias for :meth:`~.UnreliableObjectSendStream.send` ((data, (host, port)))."""
        return await self.send((data, (host, port)))


class ConnectedUDPSocket(UnreliableObjectStream[bytes], _SocketProvider):
    """
    Represents an connected UDP socket.

    Supports all relevant extra attributes from :class:`~SocketAttribute`.
    """

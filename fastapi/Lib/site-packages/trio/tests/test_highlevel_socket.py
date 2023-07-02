import errno
import socket as stdlib_socket
import sys

import pytest

from .. import _core
from .. import socket as tsocket
from .._highlevel_socket import *
from ..testing import (
    assert_checkpoints,
    check_half_closeable_stream,
    wait_all_tasks_blocked,
)


async def test_SocketStream_basics():
    # stdlib socket bad (even if connected)
    a, b = stdlib_socket.socketpair()
    with a, b:
        with pytest.raises(TypeError):
            SocketStream(a)

    # DGRAM socket bad
    with tsocket.socket(type=tsocket.SOCK_DGRAM) as sock:
        with pytest.raises(ValueError):
            SocketStream(sock)

    a, b = tsocket.socketpair()
    with a, b:
        s = SocketStream(a)
        assert s.socket is a

    # Use a real, connected socket to test socket options, because
    # socketpair() might give us a unix socket that doesn't support any of
    # these options
    with tsocket.socket() as listen_sock:
        await listen_sock.bind(("127.0.0.1", 0))
        listen_sock.listen(1)
        with tsocket.socket() as client_sock:
            await client_sock.connect(listen_sock.getsockname())

            s = SocketStream(client_sock)

            # TCP_NODELAY enabled by default
            assert s.getsockopt(tsocket.IPPROTO_TCP, tsocket.TCP_NODELAY)
            # We can disable it though
            s.setsockopt(tsocket.IPPROTO_TCP, tsocket.TCP_NODELAY, False)
            assert not s.getsockopt(tsocket.IPPROTO_TCP, tsocket.TCP_NODELAY)

            b = s.getsockopt(tsocket.IPPROTO_TCP, tsocket.TCP_NODELAY, 1)
            assert isinstance(b, bytes)


async def test_SocketStream_send_all():
    BIG = 10000000

    a_sock, b_sock = tsocket.socketpair()
    with a_sock, b_sock:
        a = SocketStream(a_sock)
        b = SocketStream(b_sock)

        # Check a send_all that has to be split into multiple parts (on most
        # platforms... on Windows every send() either succeeds or fails as a
        # whole)
        async def sender():
            data = bytearray(BIG)
            await a.send_all(data)
            # send_all uses memoryviews internally, which temporarily "lock"
            # the object they view. If it doesn't clean them up properly, then
            # some bytearray operations might raise an error afterwards, which
            # would be a pretty weird and annoying side-effect to spring on
            # users. So test that this doesn't happen, by forcing the
            # bytearray's underlying buffer to be realloc'ed:
            data += bytes(BIG)
            # (Note: the above line of code doesn't do a very good job at
            # testing anything, because:
            # - on CPython, the refcount GC generally cleans up memoryviews
            #   for us even if we're sloppy.
            # - on PyPy3, at least as of 5.7.0, the memoryview code and the
            #   bytearray code conspire so that resizing never fails – if
            #   resizing forces the bytearray's internal buffer to move, then
            #   all memoryview references are automagically updated (!!).
            #   See:
            #   https://gist.github.com/njsmith/0ffd38ec05ad8e34004f34a7dc492227
            # But I'm leaving the test here in hopes that if this ever changes
            # and we break our implementation of send_all, then we'll get some
            # early warning...)

        async def receiver():
            # Make sure the sender fills up the kernel buffers and blocks
            await wait_all_tasks_blocked()
            nbytes = 0
            while nbytes < BIG:
                nbytes += len(await b.receive_some(BIG))
            assert nbytes == BIG

        async with _core.open_nursery() as nursery:
            nursery.start_soon(sender)
            nursery.start_soon(receiver)

        # We know that we received BIG bytes of NULs so far. Make sure that
        # was all the data in there.
        await a.send_all(b"e")
        assert await b.receive_some(10) == b"e"
        await a.send_eof()
        assert await b.receive_some(10) == b""


async def fill_stream(s):
    async def sender():
        while True:
            await s.send_all(b"x" * 10000)

    async def waiter(nursery):
        await wait_all_tasks_blocked()
        nursery.cancel_scope.cancel()

    async with _core.open_nursery() as nursery:
        nursery.start_soon(sender)
        nursery.start_soon(waiter, nursery)


async def test_SocketStream_generic():
    async def stream_maker():
        left, right = tsocket.socketpair()
        return SocketStream(left), SocketStream(right)

    async def clogged_stream_maker():
        left, right = await stream_maker()
        await fill_stream(left)
        await fill_stream(right)
        return left, right

    await check_half_closeable_stream(stream_maker, clogged_stream_maker)


async def test_SocketListener():
    # Not a Trio socket
    with stdlib_socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        s.listen(10)
        with pytest.raises(TypeError):
            SocketListener(s)

    # Not a SOCK_STREAM
    with tsocket.socket(type=tsocket.SOCK_DGRAM) as s:
        await s.bind(("127.0.0.1", 0))
        with pytest.raises(ValueError) as excinfo:
            SocketListener(s)
        excinfo.match(r".*SOCK_STREAM")

    # Didn't call .listen()
    # macOS has no way to check for this, so skip testing it there.
    if sys.platform != "darwin":
        with tsocket.socket() as s:
            await s.bind(("127.0.0.1", 0))
            with pytest.raises(ValueError) as excinfo:
                SocketListener(s)
            excinfo.match(r".*listen")

    listen_sock = tsocket.socket()
    await listen_sock.bind(("127.0.0.1", 0))
    listen_sock.listen(10)
    listener = SocketListener(listen_sock)

    assert listener.socket is listen_sock

    client_sock = tsocket.socket()
    await client_sock.connect(listen_sock.getsockname())
    with assert_checkpoints():
        server_stream = await listener.accept()
    assert isinstance(server_stream, SocketStream)
    assert server_stream.socket.getsockname() == listen_sock.getsockname()
    assert server_stream.socket.getpeername() == client_sock.getsockname()

    with assert_checkpoints():
        await listener.aclose()

    with assert_checkpoints():
        await listener.aclose()

    with assert_checkpoints():
        with pytest.raises(_core.ClosedResourceError):
            await listener.accept()

    client_sock.close()
    await server_stream.aclose()


async def test_SocketListener_socket_closed_underfoot():
    listen_sock = tsocket.socket()
    await listen_sock.bind(("127.0.0.1", 0))
    listen_sock.listen(10)
    listener = SocketListener(listen_sock)

    # Close the socket, not the listener
    listen_sock.close()

    # SocketListener gives correct error
    with assert_checkpoints():
        with pytest.raises(_core.ClosedResourceError):
            await listener.accept()


async def test_SocketListener_accept_errors():
    class FakeSocket(tsocket.SocketType):
        def __init__(self, events):
            self._events = iter(events)

        type = tsocket.SOCK_STREAM

        # Fool the check for SO_ACCEPTCONN in SocketListener.__init__
        def getsockopt(self, level, opt):
            return True

        def setsockopt(self, level, opt, value):
            pass

        async def accept(self):
            await _core.checkpoint()
            event = next(self._events)
            if isinstance(event, BaseException):
                raise event
            else:
                return event, None

    fake_server_sock = FakeSocket([])

    fake_listen_sock = FakeSocket(
        [
            OSError(errno.ECONNABORTED, "Connection aborted"),
            OSError(errno.EPERM, "Permission denied"),
            OSError(errno.EPROTO, "Bad protocol"),
            fake_server_sock,
            OSError(errno.EMFILE, "Out of file descriptors"),
            OSError(errno.EFAULT, "attempt to write to read-only memory"),
            OSError(errno.ENOBUFS, "out of buffers"),
            fake_server_sock,
        ]
    )

    l = SocketListener(fake_listen_sock)

    with assert_checkpoints():
        s = await l.accept()
        assert s.socket is fake_server_sock

    for code in [errno.EMFILE, errno.EFAULT, errno.ENOBUFS]:
        with assert_checkpoints():
            with pytest.raises(OSError) as excinfo:
                await l.accept()
            assert excinfo.value.errno == code

    with assert_checkpoints():
        s = await l.accept()
        assert s.socket is fake_server_sock


async def test_socket_stream_works_when_peer_has_already_closed():
    sock_a, sock_b = tsocket.socketpair()
    with sock_a, sock_b:
        await sock_b.send(b"x")
        sock_b.close()
        stream = SocketStream(sock_a)
        assert await stream.receive_some(1) == b"x"
        assert await stream.receive_some(1) == b""

import os
import socket
import tempfile

import pytest

from trio import Path, open_unix_socket
from trio._highlevel_open_unix_stream import close_on_error

if not hasattr(socket, "AF_UNIX"):
    pytestmark = pytest.mark.skip("Needs unix socket support")


def test_close_on_error():
    class CloseMe:
        closed = False

        def close(self):
            self.closed = True

    with close_on_error(CloseMe()) as c:
        pass
    assert not c.closed

    with pytest.raises(RuntimeError):
        with close_on_error(CloseMe()) as c:
            raise RuntimeError
    assert c.closed


@pytest.mark.parametrize("filename", [4, 4.5])
async def test_open_with_bad_filename_type(filename):
    with pytest.raises(TypeError):
        await open_unix_socket(filename)


async def test_open_bad_socket():
    # mktemp is marked as insecure, but that's okay, we don't want the file to
    # exist
    name = tempfile.mktemp()
    with pytest.raises(FileNotFoundError):
        await open_unix_socket(name)


async def test_open_unix_socket():
    for name_type in [Path, str]:
        name = tempfile.mktemp()
        serv_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with serv_sock:
            serv_sock.bind(name)
            try:
                serv_sock.listen(1)

                # The actual function we're testing
                unix_socket = await open_unix_socket(name_type(name))

                async with unix_socket:
                    client, _ = serv_sock.accept()
                    with client:
                        await unix_socket.send_all(b"test")
                        assert client.recv(2048) == b"test"

                        client.sendall(b"response")
                        received = await unix_socket.receive_some(2048)
                        assert received == b"response"
            finally:
                os.unlink(name)

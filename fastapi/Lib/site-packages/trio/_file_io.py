import io
from functools import partial

import trio

from ._util import async_wraps
from .abc import AsyncResource

# This list is also in the docs, make sure to keep them in sync
_FILE_SYNC_ATTRS = {
    "closed",
    "encoding",
    "errors",
    "fileno",
    "isatty",
    "newlines",
    "readable",
    "seekable",
    "writable",
    # not defined in *IOBase:
    "buffer",
    "raw",
    "line_buffering",
    "closefd",
    "name",
    "mode",
    "getvalue",
    "getbuffer",
}

# This list is also in the docs, make sure to keep them in sync
_FILE_ASYNC_METHODS = {
    "flush",
    "read",
    "read1",
    "readall",
    "readinto",
    "readline",
    "readlines",
    "seek",
    "tell",
    "truncate",
    "write",
    "writelines",
    # not defined in *IOBase:
    "readinto1",
    "peek",
}


class AsyncIOWrapper(AsyncResource):
    """A generic :class:`~io.IOBase` wrapper that implements the :term:`asynchronous
    file object` interface. Wrapped methods that could block are executed in
    :meth:`trio.to_thread.run_sync`.

    All properties and methods defined in in :mod:`~io` are exposed by this
    wrapper, if they exist in the wrapped file object.

    """

    def __init__(self, file):
        self._wrapped = file

    @property
    def wrapped(self):
        """object: A reference to the wrapped file object"""

        return self._wrapped

    def __getattr__(self, name):
        if name in _FILE_SYNC_ATTRS:
            return getattr(self._wrapped, name)
        if name in _FILE_ASYNC_METHODS:
            meth = getattr(self._wrapped, name)

            @async_wraps(self.__class__, self._wrapped.__class__, name)
            async def wrapper(*args, **kwargs):
                func = partial(meth, *args, **kwargs)
                return await trio.to_thread.run_sync(func)

            # cache the generated method
            setattr(self, name, wrapper)
            return wrapper

        raise AttributeError(name)

    def __dir__(self):
        attrs = set(super().__dir__())
        attrs.update(a for a in _FILE_SYNC_ATTRS if hasattr(self.wrapped, a))
        attrs.update(a for a in _FILE_ASYNC_METHODS if hasattr(self.wrapped, a))
        return attrs

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.readline()
        if line:
            return line
        else:
            raise StopAsyncIteration

    async def detach(self):
        """Like :meth:`io.BufferedIOBase.detach`, but async.

        This also re-wraps the result in a new :term:`asynchronous file object`
        wrapper.

        """

        raw = await trio.to_thread.run_sync(self._wrapped.detach)
        return wrap_file(raw)

    async def aclose(self):
        """Like :meth:`io.IOBase.close`, but async.

        This is also shielded from cancellation; if a cancellation scope is
        cancelled, the wrapped file object will still be safely closed.

        """

        # ensure the underling file is closed during cancellation
        with trio.CancelScope(shield=True):
            await trio.to_thread.run_sync(self._wrapped.close)

        await trio.lowlevel.checkpoint_if_cancelled()


async def open_file(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    """Asynchronous version of :func:`io.open`.

    Returns:
        An :term:`asynchronous file object`

    Example::

        async with await trio.open_file(filename) as f:
            async for line in f:
                pass

        assert f.closed

    See also:
      :func:`trio.Path.open`

    """
    _file = wrap_file(
        await trio.to_thread.run_sync(
            io.open, file, mode, buffering, encoding, errors, newline, closefd, opener
        )
    )
    return _file


def wrap_file(file):
    """This wraps any file object in a wrapper that provides an asynchronous
    file object interface.

    Args:
        file: a :term:`file object`

    Returns:
        An :term:`asynchronous file object` that wraps ``file``

    Example::

        async_file = trio.wrap_file(StringIO('asdf'))

        assert await async_file.read() == 'asdf'

    """

    def has(attr):
        return hasattr(file, attr) and callable(getattr(file, attr))

    if not (has("close") and (has("read") or has("write"))):
        raise TypeError(
            "{} does not implement required duck-file methods: "
            "close and (read or write)".format(file)
        )

    return AsyncIOWrapper(file)

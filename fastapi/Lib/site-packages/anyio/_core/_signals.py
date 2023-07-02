from __future__ import annotations

from typing import AsyncIterator

from ._compat import DeprecatedAsyncContextManager
from ._eventloop import get_asynclib


def open_signal_receiver(
    *signals: int,
) -> DeprecatedAsyncContextManager[AsyncIterator[int]]:
    """
    Start receiving operating system signals.

    :param signals: signals to receive (e.g. ``signal.SIGINT``)
    :return: an asynchronous context manager for an asynchronous iterator which yields signal
        numbers

    .. warning:: Windows does not support signals natively so it is best to avoid relying on this
        in cross-platform applications.

    .. warning:: On asyncio, this permanently replaces any previous signal handler for the given
        signals, as set via :meth:`~asyncio.loop.add_signal_handler`.

    """
    return get_asynclib().open_signal_receiver(*signals)

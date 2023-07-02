from contextlib import contextmanager

from .. import _core


@contextmanager
def _assert_yields_or_not(expected):
    __tracebackhide__ = True
    task = _core.current_task()
    orig_cancel = task._cancel_points
    orig_schedule = task._schedule_points
    try:
        yield
        if expected and (
            task._cancel_points == orig_cancel or task._schedule_points == orig_schedule
        ):
            raise AssertionError("assert_checkpoints block did not yield!")
    finally:
        if not expected and (
            task._cancel_points != orig_cancel or task._schedule_points != orig_schedule
        ):
            raise AssertionError("assert_no_checkpoints block yielded!")


def assert_checkpoints():
    """Use as a context manager to check that the code inside the ``with``
    block either exits with an exception or executes at least one
    :ref:`checkpoint <checkpoints>`.

    Raises:
      AssertionError: if no checkpoint was executed.

    Example:
      Check that :func:`trio.sleep` is a checkpoint, even if it doesn't
      block::

         with trio.testing.assert_checkpoints():
             await trio.sleep(0)

    """
    __tracebackhide__ = True
    return _assert_yields_or_not(True)


def assert_no_checkpoints():
    """Use as a context manager to check that the code inside the ``with``
    block does not execute any :ref:`checkpoints <checkpoints>`.

    Raises:
      AssertionError: if a checkpoint was executed.

    Example:
      Synchronous code never contains any checkpoints, but we can double-check
      that::

         send_channel, receive_channel = trio.open_memory_channel(10)
         with trio.testing.assert_no_checkpoints():
             send_channel.send_nowait(None)

    """
    __tracebackhide__ = True
    return _assert_yields_or_not(False)

# These are the only functions that ever yield back to the task runner.

import enum
import types

import attr
import outcome

from . import _run


# Helper for the bottommost 'yield'. You can't use 'yield' inside an async
# function, but you can inside a generator, and if you decorate your generator
# with @types.coroutine, then it's even awaitable. However, it's still not a
# real async function: in particular, it isn't recognized by
# inspect.iscoroutinefunction, and it doesn't trigger the unawaited coroutine
# tracking machinery. Since our traps are public APIs, we make them real async
# functions, and then this helper takes care of the actual yield:
@types.coroutine
def _async_yield(obj):
    return (yield obj)


# This class object is used as a singleton.
# Not exported in the trio._core namespace, but imported directly by _run.
class CancelShieldedCheckpoint:
    pass


async def cancel_shielded_checkpoint():
    """Introduce a schedule point, but not a cancel point.

    This is *not* a :ref:`checkpoint <checkpoints>`, but it is half of a
    checkpoint, and when combined with :func:`checkpoint_if_cancelled` it can
    make a full checkpoint.

    Equivalent to (but potentially more efficient than)::

        with trio.CancelScope(shield=True):
            await trio.lowlevel.checkpoint()

    """
    return (await _async_yield(CancelShieldedCheckpoint)).unwrap()


# Return values for abort functions
class Abort(enum.Enum):
    """:class:`enum.Enum` used as the return value from abort functions.

    See :func:`wait_task_rescheduled` for details.

    .. data:: SUCCEEDED
              FAILED

    """

    SUCCEEDED = 1
    FAILED = 2


# Not exported in the trio._core namespace, but imported directly by _run.
@attr.s(frozen=True)
class WaitTaskRescheduled:
    abort_func = attr.ib()


async def wait_task_rescheduled(abort_func):
    """Put the current task to sleep, with cancellation support.

    This is the lowest-level API for blocking in Trio. Every time a
    :class:`~trio.lowlevel.Task` blocks, it does so by calling this function
    (usually indirectly via some higher-level API).

    This is a tricky interface with no guard rails. If you can use
    :class:`ParkingLot` or the built-in I/O wait functions instead, then you
    should.

    Generally the way it works is that before calling this function, you make
    arrangements for "someone" to call :func:`reschedule` on the current task
    at some later point.

    Then you call :func:`wait_task_rescheduled`, passing in ``abort_func``, an
    "abort callback".

    (Terminology: in Trio, "aborting" is the process of attempting to
    interrupt a blocked task to deliver a cancellation.)

    There are two possibilities for what happens next:

    1. "Someone" calls :func:`reschedule` on the current task, and
       :func:`wait_task_rescheduled` returns or raises whatever value or error
       was passed to :func:`reschedule`.

    2. The call's context transitions to a cancelled state (e.g. due to a
       timeout expiring). When this happens, the ``abort_func`` is called. Its
       interface looks like::

           def abort_func(raise_cancel):
               ...
               return trio.lowlevel.Abort.SUCCEEDED  # or FAILED

       It should attempt to clean up any state associated with this call, and
       in particular, arrange that :func:`reschedule` will *not* be called
       later. If (and only if!) it is successful, then it should return
       :data:`Abort.SUCCEEDED`, in which case the task will automatically be
       rescheduled with an appropriate :exc:`~trio.Cancelled` error.

       Otherwise, it should return :data:`Abort.FAILED`. This means that the
       task can't be cancelled at this time, and still has to make sure that
       "someone" eventually calls :func:`reschedule`.

       At that point there are again two possibilities. You can simply ignore
       the cancellation altogether: wait for the operation to complete and
       then reschedule and continue as normal. (For example, this is what
       :func:`trio.to_thread.run_sync` does if cancellation is disabled.)
       The other possibility is that the ``abort_func`` does succeed in
       cancelling the operation, but for some reason isn't able to report that
       right away. (Example: on Windows, it's possible to request that an
       async ("overlapped") I/O operation be cancelled, but this request is
       *also* asynchronous – you don't find out until later whether the
       operation was actually cancelled or not.)  To report a delayed
       cancellation, then you should reschedule the task yourself, and call
       the ``raise_cancel`` callback passed to ``abort_func`` to raise a
       :exc:`~trio.Cancelled` (or possibly :exc:`KeyboardInterrupt`) exception
       into this task. Either of the approaches sketched below can work::

          # Option 1:
          # Catch the exception from raise_cancel and inject it into the task.
          # (This is what Trio does automatically for you if you return
          # Abort.SUCCEEDED.)
          trio.lowlevel.reschedule(task, outcome.capture(raise_cancel))

          # Option 2:
          # wait to be woken by "someone", and then decide whether to raise
          # the error from inside the task.
          outer_raise_cancel = None
          def abort(inner_raise_cancel):
              nonlocal outer_raise_cancel
              outer_raise_cancel = inner_raise_cancel
              TRY_TO_CANCEL_OPERATION()
              return trio.lowlevel.Abort.FAILED
          await wait_task_rescheduled(abort)
          if OPERATION_WAS_SUCCESSFULLY_CANCELLED:
              # raises the error
              outer_raise_cancel()

       In any case it's guaranteed that we only call the ``abort_func`` at most
       once per call to :func:`wait_task_rescheduled`.

    Sometimes, it's useful to be able to share some mutable sleep-related data
    between the sleeping task, the abort function, and the waking task. You
    can use the sleeping task's :data:`~Task.custom_sleep_data` attribute to
    store this data, and Trio won't touch it, except to make sure that it gets
    cleared when the task is rescheduled.

    .. warning::

       If your ``abort_func`` raises an error, or returns any value other than
       :data:`Abort.SUCCEEDED` or :data:`Abort.FAILED`, then Trio will crash
       violently. Be careful! Similarly, it is entirely possible to deadlock a
       Trio program by failing to reschedule a blocked task, or cause havoc by
       calling :func:`reschedule` too many times. Remember what we said up
       above about how you should use a higher-level API if at all possible?

    """
    return (await _async_yield(WaitTaskRescheduled(abort_func))).unwrap()


# Not exported in the trio._core namespace, but imported directly by _run.
@attr.s(frozen=True)
class PermanentlyDetachCoroutineObject:
    final_outcome = attr.ib()


async def permanently_detach_coroutine_object(final_outcome):
    """Permanently detach the current task from the Trio scheduler.

    Normally, a Trio task doesn't exit until its coroutine object exits. When
    you call this function, Trio acts like the coroutine object just exited
    and the task terminates with the given outcome. This is useful if you want
    to permanently switch the coroutine object over to a different coroutine
    runner.

    When the calling coroutine enters this function it's running under Trio,
    and when the function returns it's running under the foreign coroutine
    runner.

    You should make sure that the coroutine object has released any
    Trio-specific resources it has acquired (e.g. nurseries).

    Args:
      final_outcome (outcome.Outcome): Trio acts as if the current task exited
          with the given return value or exception.

    Returns or raises whatever value or exception the new coroutine runner
    uses to resume the coroutine.

    """
    if _run.current_task().child_nurseries:
        raise RuntimeError(
            "can't permanently detach a coroutine object with open nurseries"
        )
    return await _async_yield(PermanentlyDetachCoroutineObject(final_outcome))


async def temporarily_detach_coroutine_object(abort_func):
    """Temporarily detach the current coroutine object from the Trio
    scheduler.

    When the calling coroutine enters this function it's running under Trio,
    and when the function returns it's running under the foreign coroutine
    runner.

    The Trio :class:`Task` will continue to exist, but will be suspended until
    you use :func:`reattach_detached_coroutine_object` to resume it. In the
    mean time, you can use another coroutine runner to schedule the coroutine
    object. In fact, you have to – the function doesn't return until the
    coroutine is advanced from outside.

    Note that you'll need to save the current :class:`Task` object to later
    resume; you can retrieve it with :func:`current_task`. You can also use
    this :class:`Task` object to retrieve the coroutine object – see
    :data:`Task.coro`.

    Args:
      abort_func: Same as for :func:`wait_task_rescheduled`, except that it
          must return :data:`Abort.FAILED`. (If it returned
          :data:`Abort.SUCCEEDED`, then Trio would attempt to reschedule the
          detached task directly without going through
          :func:`reattach_detached_coroutine_object`, which would be bad.)
          Your ``abort_func`` should still arrange for whatever the coroutine
          object is doing to be cancelled, and then reattach to Trio and call
          the ``raise_cancel`` callback, if possible.

    Returns or raises whatever value or exception the new coroutine runner
    uses to resume the coroutine.

    """
    return await _async_yield(WaitTaskRescheduled(abort_func))


async def reattach_detached_coroutine_object(task, yield_value):
    """Reattach a coroutine object that was detached using
    :func:`temporarily_detach_coroutine_object`.

    When the calling coroutine enters this function it's running under the
    foreign coroutine runner, and when the function returns it's running under
    Trio.

    This must be called from inside the coroutine being resumed, and yields
    whatever value you pass in. (Presumably you'll pass a value that will
    cause the current coroutine runner to stop scheduling this task.) Then the
    coroutine is resumed by the Trio scheduler at the next opportunity.

    Args:
      task (Task): The Trio task object that the current coroutine was
          detached from.
      yield_value (object): The object to yield to the current coroutine
          runner.

    """
    # This is a kind of crude check – in particular, it can fail if the
    # passed-in task is where the coroutine *runner* is running. But this is
    # an experts-only interface, and there's no easy way to do a more accurate
    # check, so I guess that's OK.
    if not task.coro.cr_running:
        raise RuntimeError("given task does not match calling coroutine")
    _run.reschedule(task, outcome.Value("reattaching"))
    value = await _async_yield(yield_value)
    assert value == outcome.Value("reattaching")

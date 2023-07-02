import signal

import pytest

import trio

from .. import _core
from .._signals import _signal_handler, open_signal_receiver
from .._util import signal_raise


async def test_open_signal_receiver():
    orig = signal.getsignal(signal.SIGILL)
    with open_signal_receiver(signal.SIGILL) as receiver:
        # Raise it a few times, to exercise signal coalescing, both at the
        # call_soon level and at the SignalQueue level
        signal_raise(signal.SIGILL)
        signal_raise(signal.SIGILL)
        await _core.wait_all_tasks_blocked()
        signal_raise(signal.SIGILL)
        await _core.wait_all_tasks_blocked()
        async for signum in receiver:  # pragma: no branch
            assert signum == signal.SIGILL
            break
        assert receiver._pending_signal_count() == 0
        signal_raise(signal.SIGILL)
        async for signum in receiver:  # pragma: no branch
            assert signum == signal.SIGILL
            break
        assert receiver._pending_signal_count() == 0
    with pytest.raises(RuntimeError):
        await receiver.__anext__()
    assert signal.getsignal(signal.SIGILL) is orig


async def test_open_signal_receiver_restore_handler_after_one_bad_signal():
    orig = signal.getsignal(signal.SIGILL)
    with pytest.raises(ValueError):
        with open_signal_receiver(signal.SIGILL, 1234567):
            pass  # pragma: no cover
    # Still restored even if we errored out
    assert signal.getsignal(signal.SIGILL) is orig


async def test_open_signal_receiver_empty_fail():
    with pytest.raises(TypeError, match="No signals were provided"):
        with open_signal_receiver():
            pass


async def test_open_signal_receiver_restore_handler_after_duplicate_signal():
    orig = signal.getsignal(signal.SIGILL)
    with open_signal_receiver(signal.SIGILL, signal.SIGILL):
        pass
    # Still restored correctly
    assert signal.getsignal(signal.SIGILL) is orig


async def test_catch_signals_wrong_thread():
    async def naughty():
        with open_signal_receiver(signal.SIGINT):
            pass  # pragma: no cover

    with pytest.raises(RuntimeError):
        await trio.to_thread.run_sync(trio.run, naughty)


async def test_open_signal_receiver_conflict():
    with pytest.raises(trio.BusyResourceError):
        with open_signal_receiver(signal.SIGILL) as receiver:
            async with trio.open_nursery() as nursery:
                nursery.start_soon(receiver.__anext__)
                nursery.start_soon(receiver.__anext__)


# Blocks until all previous calls to run_sync_soon(idempotent=True) have been
# processed.
async def wait_run_sync_soon_idempotent_queue_barrier():
    ev = trio.Event()
    token = _core.current_trio_token()
    token.run_sync_soon(ev.set, idempotent=True)
    await ev.wait()


async def test_open_signal_receiver_no_starvation():
    # Set up a situation where there are always 2 pending signals available to
    # report, and make sure that instead of getting the same signal reported
    # over and over, it alternates between reporting both of them.
    with open_signal_receiver(signal.SIGILL, signal.SIGFPE) as receiver:
        try:
            print(signal.getsignal(signal.SIGILL))
            previous = None
            for _ in range(10):
                signal_raise(signal.SIGILL)
                signal_raise(signal.SIGFPE)
                await wait_run_sync_soon_idempotent_queue_barrier()
                if previous is None:
                    previous = await receiver.__anext__()
                else:
                    got = await receiver.__anext__()
                    assert got in [signal.SIGILL, signal.SIGFPE]
                    assert got != previous
                    previous = got
            # Clear out the last signal so it doesn't get redelivered
            while receiver._pending_signal_count() != 0:
                await receiver.__anext__()
        except:  # pragma: no cover
            # If there's an unhandled exception above, then exiting the
            # open_signal_receiver block might cause the signal to be
            # redelivered and give us a core dump instead of a traceback...
            import traceback

            traceback.print_exc()


async def test_catch_signals_race_condition_on_exit():
    delivered_directly = set()

    def direct_handler(signo, frame):
        delivered_directly.add(signo)

    print(1)
    # Test the version where the call_soon *doesn't* have a chance to run
    # before we exit the with block:
    with _signal_handler({signal.SIGILL, signal.SIGFPE}, direct_handler):
        with open_signal_receiver(signal.SIGILL, signal.SIGFPE) as receiver:
            signal_raise(signal.SIGILL)
            signal_raise(signal.SIGFPE)
        await wait_run_sync_soon_idempotent_queue_barrier()
    assert delivered_directly == {signal.SIGILL, signal.SIGFPE}
    delivered_directly.clear()

    print(2)
    # Test the version where the call_soon *does* have a chance to run before
    # we exit the with block:
    with _signal_handler({signal.SIGILL, signal.SIGFPE}, direct_handler):
        with open_signal_receiver(signal.SIGILL, signal.SIGFPE) as receiver:
            signal_raise(signal.SIGILL)
            signal_raise(signal.SIGFPE)
            await wait_run_sync_soon_idempotent_queue_barrier()
            assert receiver._pending_signal_count() == 2
    assert delivered_directly == {signal.SIGILL, signal.SIGFPE}
    delivered_directly.clear()

    # Again, but with a SIG_IGN signal:

    print(3)
    with _signal_handler({signal.SIGILL}, signal.SIG_IGN):
        with open_signal_receiver(signal.SIGILL) as receiver:
            signal_raise(signal.SIGILL)
        await wait_run_sync_soon_idempotent_queue_barrier()
    # test passes if the process reaches this point without dying

    print(4)
    with _signal_handler({signal.SIGILL}, signal.SIG_IGN):
        with open_signal_receiver(signal.SIGILL) as receiver:
            signal_raise(signal.SIGILL)
            await wait_run_sync_soon_idempotent_queue_barrier()
            assert receiver._pending_signal_count() == 1
    # test passes if the process reaches this point without dying

    # Check exception chaining if there are multiple exception-raising
    # handlers
    def raise_handler(signum, _):
        raise RuntimeError(signum)

    with _signal_handler({signal.SIGILL, signal.SIGFPE}, raise_handler):
        with pytest.raises(RuntimeError) as excinfo:
            with open_signal_receiver(signal.SIGILL, signal.SIGFPE) as receiver:
                signal_raise(signal.SIGILL)
                signal_raise(signal.SIGFPE)
                await wait_run_sync_soon_idempotent_queue_barrier()
                assert receiver._pending_signal_count() == 2
        exc = excinfo.value
        signums = {exc.args[0]}
        assert isinstance(exc.__context__, RuntimeError)
        signums.add(exc.__context__.args[0])
        assert signums == {signal.SIGILL, signal.SIGFPE}

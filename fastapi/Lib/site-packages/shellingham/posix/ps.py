import errno
import subprocess
import sys

from ._core import Process


class PsNotAvailable(EnvironmentError):
    pass


def get_process_mapping():
    """Try to look up the process tree via the output of `ps`."""
    try:
        cmd = ["ps", "-ww", "-o", "pid=", "-o", "ppid=", "-o", "args="]
        output = subprocess.check_output(cmd)
    except OSError as e:  # Python 2-compatible FileNotFoundError.
        if e.errno != errno.ENOENT:
            raise
        raise PsNotAvailable("ps not found")
    except subprocess.CalledProcessError as e:
        # `ps` can return 1 if the process list is completely empty.
        # (sarugaku/shellingham#15)
        if not e.output.strip():
            return {}
        raise
    if not isinstance(output, str):
        encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
        output = output.decode(encoding)
    processes = {}
    for line in output.split("\n"):
        try:
            pid, ppid, args = line.strip().split(None, 2)
            # XXX: This is not right, but we are really out of options.
            # ps does not offer a sane way to decode the argument display,
            # and this is "Good Enough" for obtaining shell names. Hopefully
            # people don't name their shell with a space, or have something
            # like "/usr/bin/xonsh is uber". (sarugaku/shellingham#14)
            args = tuple(a.strip() for a in args.split(" "))
        except ValueError:
            continue
        processes[pid] = Process(args=args, pid=pid, ppid=ppid)
    return processes

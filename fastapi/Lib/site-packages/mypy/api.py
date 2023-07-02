"""This module makes it possible to use mypy as part of a Python application.

Since mypy still changes, the API was kept utterly simple and non-intrusive.
It just mimics command line activation without starting a new interpreter.
So the normal docs about the mypy command line apply.
Changes in the command line version of mypy will be immediately usable.

Just import this module and then call the 'run' function with a parameter of
type List[str], containing what normally would have been the command line
arguments to mypy.

Function 'run' returns a Tuple[str, str, int], namely
(<normal_report>, <error_report>, <exit_status>),
in which <normal_report> is what mypy normally writes to sys.stdout,
<error_report> is what mypy normally writes to sys.stderr and exit_status is
the exit status mypy normally returns to the operating system.

Any pretty formatting is left to the caller.

The 'run_dmypy' function is similar, but instead mimics invocation of
dmypy. Note that run_dmypy is not thread-safe and modifies sys.stdout
and sys.stderr during its invocation.

Note that these APIs don't support incremental generation of error
messages.

Trivial example of code using this module:

import sys
from mypy import api

result = api.run(sys.argv[1:])

if result[0]:
    print('\nType checking report:\n')
    print(result[0])  # stdout

if result[1]:
    print('\nError report:\n')
    print(result[1])  # stderr

print('\nExit status:', result[2])

"""

from __future__ import annotations

import sys
from io import StringIO
from typing import Callable, TextIO


def _run(main_wrapper: Callable[[TextIO, TextIO], None]) -> tuple[str, str, int]:
    stdout = StringIO()
    stderr = StringIO()

    try:
        main_wrapper(stdout, stderr)
        exit_status = 0
    except SystemExit as system_exit:
        assert isinstance(system_exit.code, int)
        exit_status = system_exit.code

    return stdout.getvalue(), stderr.getvalue(), exit_status


def run(args: list[str]) -> tuple[str, str, int]:
    # Lazy import to avoid needing to import all of mypy to call run_dmypy
    from mypy.main import main

    return _run(
        lambda stdout, stderr: main(
            args=args, stdout=stdout, stderr=stderr, clean_exit=True
        )
    )


def run_dmypy(args: list[str]) -> tuple[str, str, int]:
    from mypy.dmypy.client import main

    # A bunch of effort has been put into threading stdout and stderr
    # through the main API to avoid the threadsafety problems of
    # modifying sys.stdout/sys.stderr, but that hasn't been done for
    # the dmypy client, so we just do the non-threadsafe thing.
    def f(stdout: TextIO, stderr: TextIO) -> None:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = stdout
            sys.stderr = stderr
            main(args)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    return _run(f)

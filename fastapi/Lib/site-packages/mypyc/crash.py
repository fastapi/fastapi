from __future__ import annotations

import sys
import traceback
from contextlib import contextmanager
from typing import Iterator, NoReturn


@contextmanager
def catch_errors(module_path: str, line: int) -> Iterator[None]:
    try:
        yield
    except Exception:
        crash_report(module_path, line)


def crash_report(module_path: str, line: int) -> NoReturn:
    # Adapted from report_internal_error in mypy
    err = sys.exc_info()[1]
    tb = traceback.extract_stack()[:-4]
    # Excise all the traceback from the test runner
    for i, x in enumerate(tb):
        if x.name == "pytest_runtest_call":
            tb = tb[i + 1 :]
            break
    tb2 = traceback.extract_tb(sys.exc_info()[2])[1:]
    print("Traceback (most recent call last):")
    for s in traceback.format_list(tb + tb2):
        print(s.rstrip("\n"))
    print(f"{module_path}:{line}: {type(err).__name__}: {err}")
    raise SystemExit(2)

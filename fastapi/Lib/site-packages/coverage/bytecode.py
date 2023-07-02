# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Bytecode manipulation for coverage.py"""

from __future__ import annotations

from types import CodeType
from typing import Iterator


def code_objects(code: CodeType) -> Iterator[CodeType]:
    """Iterate over all the code objects in `code`."""
    stack = [code]
    while stack:
        # We're going to return the code object on the stack, but first
        # push its children for later returning.
        code = stack.pop()
        for c in code.co_consts:
            if isinstance(c, CodeType):
                stack.append(c)
        yield code

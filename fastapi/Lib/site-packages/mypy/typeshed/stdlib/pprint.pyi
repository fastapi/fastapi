import sys
from typing import IO

if sys.version_info >= (3, 8):
    __all__ = [
        "pprint",
        "pformat",
        "isreadable",
        "isrecursive",
        "saferepr",
        "PrettyPrinter",
        "pp",
    ]
else:
    __all__ = [
        "pprint",
        "pformat",
        "isreadable",
        "isrecursive",
        "saferepr",
        "PrettyPrinter",
    ]

if sys.version_info >= (3, 10):
    def pformat(
        object: object,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
        sort_dicts: bool = True,
        underscore_numbers: bool = False,
    ) -> str: ...

elif sys.version_info >= (3, 8):
    def pformat(
        object: object,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
        sort_dicts: bool = True,
    ) -> str: ...

else:
    def pformat(
        object: object,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
    ) -> str: ...

if sys.version_info >= (3, 10):
    def pp(
        object: object,
        stream: IO[str] | None = ...,
        indent: int = ...,
        width: int = ...,
        depth: int | None = ...,
        *,
        compact: bool = ...,
        sort_dicts: bool = False,
        underscore_numbers: bool = ...,
    ) -> None: ...

elif sys.version_info >= (3, 8):
    def pp(
        object: object,
        stream: IO[str] | None = ...,
        indent: int = ...,
        width: int = ...,
        depth: int | None = ...,
        *,
        compact: bool = ...,
        sort_dicts: bool = False,
    ) -> None: ...

if sys.version_info >= (3, 10):
    def pprint(
        object: object,
        stream: IO[str] | None = None,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
        sort_dicts: bool = True,
        underscore_numbers: bool = False,
    ) -> None: ...

elif sys.version_info >= (3, 8):
    def pprint(
        object: object,
        stream: IO[str] | None = None,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
        sort_dicts: bool = True,
    ) -> None: ...

else:
    def pprint(
        object: object,
        stream: IO[str] | None = None,
        indent: int = 1,
        width: int = 80,
        depth: int | None = None,
        *,
        compact: bool = False,
    ) -> None: ...

def isreadable(object: object) -> bool: ...
def isrecursive(object: object) -> bool: ...
def saferepr(object: object) -> str: ...

class PrettyPrinter:
    if sys.version_info >= (3, 10):
        def __init__(
            self,
            indent: int = 1,
            width: int = 80,
            depth: int | None = None,
            stream: IO[str] | None = None,
            *,
            compact: bool = False,
            sort_dicts: bool = True,
            underscore_numbers: bool = False,
        ) -> None: ...
    elif sys.version_info >= (3, 8):
        def __init__(
            self,
            indent: int = 1,
            width: int = 80,
            depth: int | None = None,
            stream: IO[str] | None = None,
            *,
            compact: bool = False,
            sort_dicts: bool = True,
        ) -> None: ...
    else:
        def __init__(
            self,
            indent: int = 1,
            width: int = 80,
            depth: int | None = None,
            stream: IO[str] | None = None,
            *,
            compact: bool = False,
        ) -> None: ...

    def pformat(self, object: object) -> str: ...
    def pprint(self, object: object) -> None: ...
    def isreadable(self, object: object) -> bool: ...
    def isrecursive(self, object: object) -> bool: ...
    def format(
        self, object: object, context: dict[int, int], maxlevels: int, level: int
    ) -> tuple[str, bool, bool]: ...

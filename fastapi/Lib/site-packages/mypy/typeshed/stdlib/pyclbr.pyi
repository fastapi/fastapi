import sys
from collections.abc import Sequence

__all__ = ["readmodule", "readmodule_ex", "Class", "Function"]

class Class:
    module: str
    name: str
    super: list[Class | str] | None
    methods: dict[str, int]
    file: int
    lineno: int

    if sys.version_info >= (3, 10):
        end_lineno: int | None

    parent: Class | None
    children: dict[str, Class | Function]

    if sys.version_info >= (3, 10):
        def __init__(
            self,
            module: str,
            name: str,
            super_: list[Class | str] | None,
            file: str,
            lineno: int,
            parent: Class | None = None,
            *,
            end_lineno: int | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            module: str,
            name: str,
            super: list[Class | str] | None,
            file: str,
            lineno: int,
            parent: Class | None = None,
        ) -> None: ...

class Function:
    module: str
    name: str
    file: int
    lineno: int

    if sys.version_info >= (3, 10):
        end_lineno: int | None
        is_async: bool

    parent: Function | Class | None
    children: dict[str, Class | Function]

    if sys.version_info >= (3, 10):
        def __init__(
            self,
            module: str,
            name: str,
            file: str,
            lineno: int,
            parent: Function | Class | None = None,
            is_async: bool = False,
            *,
            end_lineno: int | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            module: str,
            name: str,
            file: str,
            lineno: int,
            parent: Function | Class | None = None,
        ) -> None: ...

def readmodule(module: str, path: Sequence[str] | None = None) -> dict[str, Class]: ...
def readmodule_ex(
    module: str, path: Sequence[str] | None = None
) -> dict[str, Class | Function | list[str]]: ...

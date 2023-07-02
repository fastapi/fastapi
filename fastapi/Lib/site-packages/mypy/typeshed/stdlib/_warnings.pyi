from typing import Any, overload

_defaultaction: str
_onceregistry: dict[Any, Any]
filters: list[tuple[str, str | None, type[Warning], str | None, int]]

@overload
def warn(
    message: str,
    category: type[Warning] | None = None,
    stacklevel: int = 1,
    source: Any | None = None,
) -> None: ...
@overload
def warn(
    message: Warning,
    category: Any = None,
    stacklevel: int = 1,
    source: Any | None = None,
) -> None: ...
@overload
def warn_explicit(
    message: str,
    category: type[Warning],
    filename: str,
    lineno: int,
    module: str | None = ...,
    registry: dict[str | tuple[str, type[Warning], int], int] | None = ...,
    module_globals: dict[str, Any] | None = ...,
    source: Any | None = ...,
) -> None: ...
@overload
def warn_explicit(
    message: Warning,
    category: Any,
    filename: str,
    lineno: int,
    module: str | None = ...,
    registry: dict[str | tuple[str, type[Warning], int], int] | None = ...,
    module_globals: dict[str, Any] | None = ...,
    source: Any | None = ...,
) -> None: ...

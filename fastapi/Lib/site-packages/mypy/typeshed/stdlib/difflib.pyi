import sys
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Any, AnyStr, Generic, NamedTuple, TypeVar, overload

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = [
    "get_close_matches",
    "ndiff",
    "restore",
    "SequenceMatcher",
    "Differ",
    "IS_CHARACTER_JUNK",
    "IS_LINE_JUNK",
    "context_diff",
    "unified_diff",
    "diff_bytes",
    "HtmlDiff",
    "Match",
]

_T = TypeVar("_T")

class Match(NamedTuple):
    a: int
    b: int
    size: int

class SequenceMatcher(Generic[_T]):
    @overload
    def __init__(
        self,
        isjunk: Callable[[_T], bool] | None,
        a: Sequence[_T],
        b: Sequence[_T],
        autojunk: bool = True,
    ) -> None: ...
    @overload
    def __init__(
        self, *, a: Sequence[_T], b: Sequence[_T], autojunk: bool = True
    ) -> None: ...
    @overload
    def __init__(
        self: SequenceMatcher[str],
        isjunk: Callable[[str], bool] | None = None,
        a: Sequence[str] = "",
        b: Sequence[str] = "",
        autojunk: bool = True,
    ) -> None: ...
    def set_seqs(self, a: Sequence[_T], b: Sequence[_T]) -> None: ...
    def set_seq1(self, a: Sequence[_T]) -> None: ...
    def set_seq2(self, b: Sequence[_T]) -> None: ...
    if sys.version_info >= (3, 9):
        def find_longest_match(
            self,
            alo: int = 0,
            ahi: int | None = None,
            blo: int = 0,
            bhi: int | None = None,
        ) -> Match: ...
    else:
        def find_longest_match(
            self, alo: int, ahi: int, blo: int, bhi: int
        ) -> Match: ...

    def get_matching_blocks(self) -> list[Match]: ...
    def get_opcodes(self) -> list[tuple[str, int, int, int, int]]: ...
    def get_grouped_opcodes(
        self, n: int = 3
    ) -> Iterable[list[tuple[str, int, int, int, int]]]: ...
    def ratio(self) -> float: ...
    def quick_ratio(self) -> float: ...
    def real_quick_ratio(self) -> float: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

@overload
def get_close_matches(
    word: AnyStr, possibilities: Iterable[AnyStr], n: int = 3, cutoff: float = 0.6
) -> list[AnyStr]: ...
@overload
def get_close_matches(
    word: Sequence[_T],
    possibilities: Iterable[Sequence[_T]],
    n: int = 3,
    cutoff: float = 0.6,
) -> list[Sequence[_T]]: ...

class Differ:
    def __init__(
        self,
        linejunk: Callable[[str], bool] | None = None,
        charjunk: Callable[[str], bool] | None = None,
    ) -> None: ...
    def compare(self, a: Sequence[str], b: Sequence[str]) -> Iterator[str]: ...

def IS_LINE_JUNK(line: str, pat: Any = ...) -> bool: ...  # pat is undocumented
def IS_CHARACTER_JUNK(ch: str, ws: str = " \t") -> bool: ...  # ws is undocumented
def unified_diff(
    a: Sequence[str],
    b: Sequence[str],
    fromfile: str = "",
    tofile: str = "",
    fromfiledate: str = "",
    tofiledate: str = "",
    n: int = 3,
    lineterm: str = "\n",
) -> Iterator[str]: ...
def context_diff(
    a: Sequence[str],
    b: Sequence[str],
    fromfile: str = "",
    tofile: str = "",
    fromfiledate: str = "",
    tofiledate: str = "",
    n: int = 3,
    lineterm: str = "\n",
) -> Iterator[str]: ...
def ndiff(
    a: Sequence[str],
    b: Sequence[str],
    linejunk: Callable[[str], bool] | None = None,
    charjunk: Callable[[str], bool] | None = ...,
) -> Iterator[str]: ...

class HtmlDiff:
    def __init__(
        self,
        tabsize: int = 8,
        wrapcolumn: int | None = None,
        linejunk: Callable[[str], bool] | None = None,
        charjunk: Callable[[str], bool] | None = ...,
    ) -> None: ...
    def make_file(
        self,
        fromlines: Sequence[str],
        tolines: Sequence[str],
        fromdesc: str = "",
        todesc: str = "",
        context: bool = False,
        numlines: int = 5,
        *,
        charset: str = "utf-8",
    ) -> str: ...
    def make_table(
        self,
        fromlines: Sequence[str],
        tolines: Sequence[str],
        fromdesc: str = "",
        todesc: str = "",
        context: bool = False,
        numlines: int = 5,
    ) -> str: ...

def restore(delta: Iterable[str], which: int) -> Iterator[str]: ...
def diff_bytes(
    dfunc: Callable[
        [Sequence[str], Sequence[str], str, str, str, str, int, str], Iterator[str]
    ],
    a: Iterable[bytes | bytearray],
    b: Iterable[bytes | bytearray],
    fromfile: bytes | bytearray = b"",
    tofile: bytes | bytearray = b"",
    fromfiledate: bytes | bytearray = b"",
    tofiledate: bytes | bytearray = b"",
    n: int = 3,
    lineterm: bytes | bytearray = b"\n",
) -> Iterator[bytes]: ...

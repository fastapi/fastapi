from _typeshed import StrPath
from typing_extensions import Self, TypeAlias

_Label: TypeAlias = tuple[int, str | None]
_DFA: TypeAlias = list[list[tuple[int, int]]]
_DFAS: TypeAlias = tuple[_DFA, dict[int, int]]

class Grammar:
    symbol2number: dict[str, int]
    number2symbol: dict[int, str]
    states: list[_DFA]
    dfas: dict[int, _DFAS]
    labels: list[_Label]
    keywords: dict[str, int]
    tokens: dict[int, int]
    symbol2label: dict[str, int]
    start: int
    def dump(self, filename: StrPath) -> None: ...
    def load(self, filename: StrPath) -> None: ...
    def copy(self) -> Self: ...
    def report(self) -> None: ...

opmap_raw: str
opmap: dict[str, str]

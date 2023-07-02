from re import Pattern
from sre_constants import *
from sre_constants import _NamedIntConstant
from sre_parse import SubPattern
from typing import Any

MAXCODE: int

def dis(code: list[_NamedIntConstant]) -> None: ...
def isstring(obj: Any) -> bool: ...
def compile(p: str | bytes | SubPattern, flags: int = 0) -> Pattern[Any]: ...

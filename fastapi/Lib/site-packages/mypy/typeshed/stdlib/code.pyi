from codeop import CommandCompiler
from collections.abc import Callable, Mapping
from types import CodeType
from typing import Any

__all__ = [
    "InteractiveInterpreter",
    "InteractiveConsole",
    "interact",
    "compile_command",
]

class InteractiveInterpreter:
    locals: Mapping[str, Any]  # undocumented
    compile: CommandCompiler  # undocumented
    def __init__(self, locals: Mapping[str, Any] | None = None) -> None: ...
    def runsource(
        self, source: str, filename: str = "<input>", symbol: str = "single"
    ) -> bool: ...
    def runcode(self, code: CodeType) -> None: ...
    def showsyntaxerror(self, filename: str | None = None) -> None: ...
    def showtraceback(self) -> None: ...
    def write(self, data: str) -> None: ...

class InteractiveConsole(InteractiveInterpreter):
    buffer: list[str]  # undocumented
    filename: str  # undocumented
    def __init__(
        self, locals: Mapping[str, Any] | None = None, filename: str = "<console>"
    ) -> None: ...
    def interact(
        self, banner: str | None = None, exitmsg: str | None = None
    ) -> None: ...
    def push(self, line: str) -> bool: ...
    def resetbuffer(self) -> None: ...
    def raw_input(self, prompt: str = "") -> str: ...

def interact(
    banner: str | None = None,
    readfunc: Callable[[str], str] | None = None,
    local: Mapping[str, Any] | None = None,
    exitmsg: str | None = None,
) -> None: ...
def compile_command(
    source: str, filename: str = "<input>", symbol: str = "single"
) -> CodeType | None: ...

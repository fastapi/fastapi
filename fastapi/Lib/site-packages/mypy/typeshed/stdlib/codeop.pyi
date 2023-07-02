from types import CodeType

__all__ = ["compile_command", "Compile", "CommandCompiler"]

def compile_command(
    source: str, filename: str = "<input>", symbol: str = "single"
) -> CodeType | None: ...

class Compile:
    flags: int
    def __call__(self, source: str, filename: str, symbol: str) -> CodeType: ...

class CommandCompiler:
    compiler: Compile
    def __call__(
        self, source: str, filename: str = "<input>", symbol: str = "single"
    ) -> CodeType | None: ...

import sys
from typing import Any

class ParserBase:
    def reset(self) -> None: ...
    def getpos(self) -> tuple[int, int]: ...
    def unknown_decl(self, data: str) -> None: ...
    def parse_comment(self, i: int, report: int = 1) -> int: ...  # undocumented
    def parse_declaration(self, i: int) -> int: ...  # undocumented
    def parse_marked_section(self, i: int, report: int = 1) -> int: ...  # undocumented
    def updatepos(self, i: int, j: int) -> int: ...  # undocumented
    if sys.version_info < (3, 10):
        # Removed from ParserBase: https://bugs.python.org/issue31844
        def error(self, message: str) -> Any: ...  # undocumented
    lineno: int  # undocumented
    offset: int  # undocumented

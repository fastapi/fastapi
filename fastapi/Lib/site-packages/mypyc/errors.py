from __future__ import annotations

import mypy.errors
from mypy.options import Options


class Errors:
    def __init__(self, options: Options) -> None:
        self.num_errors = 0
        self.num_warnings = 0
        self._errors = mypy.errors.Errors(options, hide_error_codes=True)

    def error(self, msg: str, path: str, line: int) -> None:
        self._errors.report(line, None, msg, severity="error", file=path)
        self.num_errors += 1

    def note(self, msg: str, path: str, line: int) -> None:
        self._errors.report(line, None, msg, severity="note", file=path)

    def warning(self, msg: str, path: str, line: int) -> None:
        self._errors.report(line, None, msg, severity="warning", file=path)
        self.num_warnings += 1

    def new_messages(self) -> list[str]:
        return self._errors.new_messages()

    def flush_errors(self) -> None:
        for error in self.new_messages():
            print(error)

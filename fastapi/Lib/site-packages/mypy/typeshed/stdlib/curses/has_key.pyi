import sys

if sys.platform != "win32":
    def has_key(ch: int | str) -> bool: ...

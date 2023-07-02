from collections.abc import Iterable
from email.charset import Charset
from typing import Any

__all__ = ["Header", "decode_header", "make_header"]

class Header:
    def __init__(
        self,
        s: bytes | bytearray | str | None = None,
        charset: Charset | str | None = None,
        maxlinelen: int | None = None,
        header_name: str | None = None,
        continuation_ws: str = " ",
        errors: str = "strict",
    ) -> None: ...
    def append(
        self,
        s: bytes | bytearray | str,
        charset: Charset | str | None = None,
        errors: str = "strict",
    ) -> None: ...
    def encode(
        self,
        splitchars: str = ";, \t",
        maxlinelen: int | None = None,
        linesep: str = "\n",
    ) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, __value: object) -> bool: ...

# decode_header() either returns list[tuple[str, None]] if the header
# contains no encoded parts, or list[tuple[bytes, str | None]] if the header
# contains at least one encoded part.
def decode_header(header: Header | str) -> list[tuple[Any, Any | None]]: ...
def make_header(
    decoded_seq: Iterable[tuple[bytes | bytearray | str, str | None]],
    maxlinelen: int | None = None,
    header_name: str | None = None,
    continuation_ws: str = " ",
) -> Header: ...

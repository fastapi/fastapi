__all__ = [
    "body_decode",
    "body_encode",
    "decode",
    "decodestring",
    "header_encode",
    "header_length",
]

from _typeshed import ReadableBuffer

def header_length(bytearray: str | bytes | bytearray) -> int: ...
def header_encode(
    header_bytes: str | ReadableBuffer, charset: str = "iso-8859-1"
) -> str: ...

# First argument should be a buffer that supports slicing and len().
def body_encode(s: bytes | bytearray, maxlinelen: int = 76, eol: str = "\n") -> str: ...
def decode(string: str | ReadableBuffer) -> bytes: ...

body_decode = decode
decodestring = decode

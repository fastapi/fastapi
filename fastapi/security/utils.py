import hashlib
from typing import Callable, Tuple

from _typeshed import ReadableBuffer


def get_authorization_scheme_param(authorization_header_value: str) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


# TODO(Marcelo): Decide the returned value.
def get_digest_algorithm(algorithm: str):
    if algorithm in ("MD5", "MD5-sess"):
        return hashlib.md5
    if algorithm in ("SHA-256", "SHA-256-sess"):
        return hashlib.sha256
    if algorithm in ("SHA-512-256", "SHA-512-256-sess"):
        return hashlib.sha512
    raise ValueError("Algorithm is not valid")

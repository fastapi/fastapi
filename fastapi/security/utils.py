import binascii
import hashlib
import time
from base64 import b64decode, b64encode
from typing import Optional, Tuple

from starlette.requests import Request


def get_authorization_scheme_param(
    authorization_header_value: Optional[str],
) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


def make_nonce(request: Request, secret: Optional[str] = None) -> str:
    """
    Create a nonce for HTTP digest access authentication.

    This implementation is based on RFC 7616, section 3.3 which suggests, a
    nonce value `H(timestamp ":" ETag ":" secret-data)`. However, because
    the ETag is not available, we use the more readily available
    request.url.path. Additionally, to limit the length of the nonce, we use the
    first 10 characters of the MD5 hash of both the path and the secret.

    Args:
        request (Request): The HTTP request.
        secret (str | None): The secret to use for the nonce.

    Returns:
        str: The nonce.
    """

    now = int(time.time() * 1000)
    path = hashlib.md5(request.url.path.encode()).hexdigest()[:10]
    secret = secret or ""
    secret = hashlib.md5(secret.encode()).hexdigest()[:10]
    return b64encode(f"{now}:{path}:{secret}".encode()).decode()


def check_nonce(
    nonce: str,
    request: Request,
    valid_for_seconds: int = 300,
    secret: Optional[str] = None,
) -> bool:
    """
    Check if a nonce is valid.

    Args:
        nonce (str): The nonce to check.
        request (Request): The HTTP request.
        valid_for_seconds (int): The number of seconds the nonce is valid for.
        secret (str | None): The secret to use for the nonce.

    Returns:
        bool: True if the nonce is valid, False otherwise.
    """

    try:
        parsed = b64decode(nonce).decode("ascii")
        parts = parsed.split(":")
    except (binascii.Error, UnicodeDecodeError):
        return False

    # Check legnth
    if len(parts) != 3:
        return False

    _ts, _path, _secret = parts

    if (
        (
            not _ts.isnumeric()
            or abs(time.time() * 1000 - int(_ts)) > valid_for_seconds * 1000
        )
        or (_path != hashlib.md5(request.url.path.encode()).hexdigest()[:10])
        or (secret and _secret != hashlib.md5(secret.encode()).hexdigest()[:10])
    ):
        return False

    return True

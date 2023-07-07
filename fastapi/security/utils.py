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


def digest_access_response(
    request_method: str,
    request_uri: str,
    request_body: Optional[bytes],
    username: str,
    password: str,
    realm: str,
    nonce: str,
    cnonce: str,
    nc: str,
    qop: str,
    algo: Optional[str],
) -> str:
    """
    Create a digest access authentication response.

    The HTTP Digest Access Authentication response is specified in:
        - RFC 7616, section 3.4.1
        - RFC 2617, section 3.2.2.1
        - RFC 2069, section 2.1.2

    Briefly, the response is defined as:

        IF <qop> is one of "auth" or "auth-int" THEN
            response = H(<HA1>:<nonce>:<nc>:<cnonce>:<qop>:<HA2>)
        OTHERWISE:
            response = H(<HA1>:<nonce>:<HA2>)

        WHERE:
            H() = The hashing algorithm specified by the <algo> directive.

            HA1 =
                IF <algo> endwith '-sess' THEN
                    H(<username>:<realm>:<password>):<nonce>:<cnonce>
                OTHERWISE:
                    H(<username>:<realm>:<password>)

            HA2 =
                IF <qop> is 'auth-int' THEN
                    H(<method>:<digestURI>:H(<request-body>))
                ELSE:
                    H(<method>:<digestURI>)

    Args:
        request_method (str): The HTTP request method.
        request_uri (str): The HTTP request URI.
        request_body (str | None): The HTTP request body.
        username (str): The username. Note this may potentailly be hashed.
        password (str): The password.
        realm (str): The realm under protection.
        nonce (str): The nonce.
        cnonce (str): The cnonce (client-nonce).
        nc (str): The nc (nonce counter).
        qop (str | None): The qop (quality-of-protection).
        algo (str | None): The algorithm. Include suffix '-sess' for session.

    Raises:
        ValueError: If either:
            - the algo is not supported by hashlib.
            - the qop is not supported (None, "auth", "auth-int")
    """

    # Check and clean ALGO
    algo = algo.lower() if algo else "md5"
    if algo.endswith("-sess"):
        algo_sess = True
        algo = algo[:-5]
    else:
        algo_sess = False

    algo = algo.replace("-", "")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported algorithm '{algo}'")

    def digest_fn(x: str) -> str:
        return hashlib.new(algo, x.encode()).hexdigest()

    # Check QOP
    # TODO: Support auth-int. There may be challenges with this due, as this
    #       requires the entity-body to be included in the response. This is
    #       different to the message-body (before Transfer-Encoding). Starlette
    #       does not seem to provide access to such entity-body.
    if qop not in (
        None,
        "auth",
    ):
        raise ValueError(f"Unsupported qop '{qop}'")

    # Calculate HA1
    a1 = f"{username}:{realm}:{password}"
    if algo_sess:
        a1 = f"{digest_fn(a1)}:{nonce}:{cnonce}"
    ha1 = digest_fn(a1)

    # Calculate HA2
    a2 = f"{request_method}:{request_uri}"
    ha2 = digest_fn(a2)

    # Calculate and return response
    return digest_fn(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")

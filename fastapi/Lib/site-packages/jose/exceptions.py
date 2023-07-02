class JOSEError(Exception):
    pass


class JWSError(JOSEError):
    pass


class JWSSignatureError(JWSError):
    pass


class JWSAlgorithmError(JWSError):
    pass


class JWTError(JOSEError):
    pass


class JWTClaimsError(JWTError):
    pass


class ExpiredSignatureError(JWTError):
    pass


class JWKError(JOSEError):
    pass


class JWEError(JOSEError):
    """Base error for all JWE errors"""

    pass


class JWEParseError(JWEError):
    """Could not parse the JWE string provided"""

    pass


class JWEInvalidAuth(JWEError):
    """
    The authentication tag did not match the protected sections of the
    JWE string provided
    """

    pass


class JWEAlgorithmUnsupportedError(JWEError):
    """
    The JWE algorithm is not supported by the backend
    """

    pass

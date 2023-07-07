import pytest
from fastapi.security import HTTPDigest


def test_security_http_digest_raises_on_qop_auth_int():
    with pytest.raises(ValueError):
        HTTPDigest(qop=("auth-int",))


def test_security_http_digest_raises_on_invalid_algo():
    with pytest.raises(ValueError):
        HTTPDigest(algorithm="sha-48")

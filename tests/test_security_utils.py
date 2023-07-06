from base64 import b64encode
from unittest.mock import MagicMock, patch

import pytest
from fastapi.security.utils import check_nonce, make_nonce


def test_nonce_with_secret():
    # GIVEN: A mocked request and a secret
    request = MagicMock()
    request.url.path = "/api/v1/health"
    secret = "s0m4verysecure5eREt"

    # WHEN: we create a nonce
    nonce = make_nonce(request, secret)

    # THEN: the nonce is valid
    assert nonce
    assert len(nonce) > 0

    # WHEN: we check the nonce
    valid_result = check_nonce(nonce, request, secret=secret)

    # THEN: the nonce is valid
    assert valid_result

    # WHEN: we check the nonce with a different secret
    invalid_result = check_nonce(nonce, request, secret=secret[:-1])

    # THEN: the nonce is invalid
    assert not invalid_result


def test_nonce_time_expiry():
    # GIVEN: A mocked request, a secret, and a fixed timestamp
    request = MagicMock()
    request.url.path = "/api/v1/health"
    secret = "s0m4verysecure5eREt"
    timestamp = 1610000000000.10

    # WHEN: we create a nonce
    with patch("time.time", return_value=timestamp):
        nonce = make_nonce(request, secret)

    # THEN: the nonce is valid
    assert nonce
    assert len(nonce) > 0

    # WHEN: we check the nonce within the validity period
    with patch("time.time", return_value=timestamp + 300):
        valid_result = check_nonce(nonce, request, secret=secret)

    # THEN: the nonce is valid
    assert valid_result

    # WHEN: we check the nonce outside the validity period
    with patch("time.time", return_value=timestamp + 301):
        invalid_result = check_nonce(nonce, request, secret=secret)

    # THEN: the nonce is invalid
    assert not invalid_result


@pytest.mark.parametrize(
    "timestamp,path,secret",
    [
        pytest.param(
            "not_a_timestamp",
            "/api/v1/health",
            "s0m4verysecure5eREt",
            id="invalid-timestamp",
        ),
        pytest.param(
            "1688716388",
            "/api/v1/health",
            None,
            id="invalid-length",
        ),
        pytest.param(
            None,
            None,
            None,
            id="invalid-length",
        ),
    ],
)
def test_invalid_nonces(timestamp, path, secret):
    # GIVEN: A nonce by base64 encoding the parts
    nonce_data = ""
    if timestamp:
        nonce_data += f"{timestamp}"
    if path:
        nonce_data += f":{path}"
    if secret:
        nonce_data += f":{secret}"
    if nonce_data:
        nonce = b64encode(nonce_data.encode()).decode()
    else:
        nonce = "random-string"

    # GIVEN: A fixed timestamp (2023-01-01)
    with patch("time.time", return_value=1688716388):
        # WHEN: we check the nonce
        valid_result = check_nonce(nonce, MagicMock(), secret=secret)

    # THEN: the nonce is invalid
    assert not valid_result

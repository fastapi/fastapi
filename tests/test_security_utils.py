from base64 import b64encode
from unittest.mock import MagicMock, patch

import pytest
from fastapi.security.utils import check_nonce, digest_access_response, make_nonce


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


@pytest.mark.parametrize(
    "method,uri,body,username,password,realm,nonce,cnonce,nc,qop,algo,expected_response",
    [
        pytest.param(
            "GET",
            "/dir/index.html",
            None,
            "Mufasa",
            "Circle of Life",
            "http-auth@example.org",
            "7ypf/xlj9XXwfDPEoM4URrv/xwf94BcCAzFZH4GiTo0v",
            "f2/wE4q74E6zIJEtWaHKaf5wv/H5QzzpXusqGemxURZJ",
            "00000001",
            "auth",
            "md5",
            "8ca523f5e9506fed4657c9700eebdbec",
            id="rfc-7617-example-auth-md5",
        ),
        pytest.param(
            "GET",
            "/dir/index.html",
            None,
            "Mufasa",
            "Circle of Life",
            "http-auth@example.org",
            "7ypf/xlj9XXwfDPEoM4URrv/xwf94BcCAzFZH4GiTo0v",
            "f2/wE4q74E6zIJEtWaHKaf5wv/H5QzzpXusqGemxURZJ",
            "00000001",
            "auth",
            "sha-256",
            "753927fa0e85d155564e2e272a28d1802ca10daf4496794697cf8db5856cb6c1",
            id="rfc-7617-example-auth-sha256",
        ),
        pytest.param(
            "GET",
            "/",
            None,
            "johndoe@gmail.com",
            "password",
            "somewhere.in.fancy-realm@example.org",
            "5d155564e2e272a28d1802ca10daf4496794697",
            "NDk1YmFmYmMxOGFjYTY2MzMwNTFiMjg1NWNjM2U5MDk=",
            "00000001",
            "auth",
            "md5-sess",
            "4d7333875d888c57a149ca3e5b275970",
            id="md5-sess",
        ),
    ],
)
def test_digest_access_response(
    method,
    uri,
    body,
    username,
    password,
    realm,
    nonce,
    cnonce,
    nc,
    qop,
    algo,
    expected_response,
):
    actual = digest_access_response(
        request_method=method,
        request_uri=uri,
        request_body=body,
        username=username,
        password=password,
        realm=realm,
        nonce=nonce,
        cnonce=cnonce,
        nc=nc,
        qop=qop,
        algo=algo,
    )
    assert actual == expected_response


def test_digest_access_response_raises_invalid_algo():
    with pytest.raises(ValueError):
        digest_access_response(
            request_method="GET",
            request_uri="/",
            request_body=None,
            username="hello",
            password="world",
            realm="example.org",
            nonce="1234567890",
            cnonce="1234567890",
            nc="00000001",
            qop="auth",
            algo="invalid",
        )


def test_digest_access_response_raises_invalid_qop():
    with pytest.raises(ValueError):
        digest_access_response(
            request_method="GET",
            request_uri="/",
            request_body=None,
            username="hello",
            password="world",
            realm="example.org",
            nonce="1234567890",
            cnonce="1234567890",
            nc="00000001",
            qop="invalid",
            algo="md5",
        )

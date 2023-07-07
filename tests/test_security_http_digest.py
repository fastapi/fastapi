import binascii
import os
import re
from typing import Optional
from unittest.mock import patch

import pytest
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPDigest, HTTPDigestCredentials
from fastapi.security.utils import digest_access_response
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPDigest(realm="somewhere@host.com")


@app.get("/users/me")
async def read_current_user(digest: HTTPDigestCredentials = Security(security)):
    if not await digest.authenticate("johndoe", "password1"):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"scheme": digest.scheme, "credentials": digest.credentials}


client = TestClient(app)


def _get_authorization_header(
    digest: str,
    method: str,
    uri: str,
    username: str,
    password: str,
    body: Optional[str] = None,
    realm: str = "somewhere@host.com",
    qop: str = "auth",
    algo: str = "md5",
) -> str:
    nonce = re.search(r'nonce="([^"]+)"', digest).group(1)
    opaque = re.search(r'opaque="([^"]+)"', digest).group(1)

    cnonce = binascii.b2a_hex(os.urandom(15))

    challenge_response_items = {
        "username": username,
        "realm": realm,
        "uri": uri,
        "opaque": opaque,
        "nonce": nonce,
        "cnonce": cnonce,
        "nc": "00000001",
        "qop": qop,
        "algorithm": algo,
        "response": digest_access_response(
            request_method=method,
            request_uri=uri,
            request_body=body,
            username=username,
            password=password,
            realm=realm,
            nonce=nonce,
            cnonce=cnonce,
            nc="00000001",
            qop=qop,
            algo=algo,
        ),
    }

    return "Digest " + ", ".join(
        f'{k}="{v}"' for k, v in challenge_response_items.items()
    )


def test_security_http_digest_challenge_is_valid():
    """
    Validate the challenge returned is consistent with RFC 7616.
    """
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]
    assert www_authenticate.startswith("Digest ")
    assert 'realm="somewhere@host.com"' in www_authenticate
    assert 'nonce="' in www_authenticate
    assert 'opaque="' in www_authenticate
    assert 'algorithm="md5"' in www_authenticate
    assert 'qop="auth"' in www_authenticate


def test_security_http_digest_authenticate():
    """
    Validate the challenge-response authentication is consistent with RFC 7616.
    """

    # GIVEN: The initial challenge from the server
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # WHEN: The client sends the response with the correct credentials.
    response = client.get(
        "/users/me",
        headers={
            "Authorization": _get_authorization_header(
                digest=www_authenticate,
                method="GET",
                uri="/users/me",
                username="johndoe",
                password="password1",
            )
        },
    )

    # THEN: The server responds with a 200 OK response.
    assert response.status_code == 200


def test_security_http_digest_invalid_password():
    # GIVEN: The initial challenge from the server
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # WHEN: The client sends the response with an incorrect password.
    response = client.get(
        "/users/me",
        headers={
            "Authorization": _get_authorization_header(
                digest=www_authenticate,
                method="GET",
                uri="/users/me",
                username="johndoe",
                password="incorrect password",
            )
        },
    )

    # THEN: The server responds with a 401 Unauthorized response.
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_security_http_digest_invalid_username():
    # GIVEN: The initial challenge from the server
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # WHEN: The client sends the response with an incorrect username.
    response = client.get(
        "/users/me",
        headers={
            "Authorization": _get_authorization_header(
                digest=www_authenticate,
                method="GET",
                uri="/users/me",
                username="maryjane",
                password="password1",
            )
        },
    )

    # THEN: The server responds with a 401 Unauthorized response.
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_security_http_digest_stale_nonce():
    """
    Validate the challenge-response authentication fails when the nonce is used
    after the expiration time (5 minutes).
    """

    # GIVEN: A fixed timestamp (2023-01-01 00:00:00)
    fixed_time = 1672498800

    # GIVEN: The initial challenge from the server
    with patch("time.time", return_value=fixed_time):
        challenge = client.get(
            "/users/me",
        )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # WHEN: The client sends the response 301 seconds (5 minutes and 1 second)
    #       after the initial challenge; i.e. 1 second after the nonce expires.
    with patch("time.time", return_value=fixed_time + 301):
        response = client.get(
            "/users/me",
            headers={
                "Authorization": _get_authorization_header(
                    digest=www_authenticate,
                    method="GET",
                    uri="/users/me",
                    username="johndoe",
                    password="password1",
                )
            },
        )

    # THEN: The server responds with a 401 Unauthorized response.
    assert response.status_code == 401
    assert response.json() == {"detail": "Stale nonce"}


def test_security_http_digest_invalid_scheme():
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer 1234567890"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}


@pytest.mark.parametrize(
    "remove_field,expected_messsage",
    [
        ("username", "Invalid username"),
        ("qop", "Unsupported QOP"),
        ("realm", "Invalid realm"),
        ("uri", "Invalid URI"),
        ("cnonce", "Invalid authentication credentials"),
        ("nc", "Invalid authentication credentials"),
        ("response", "Invalid authentication credentials"),
    ],
)
def test_security_http_digest_missing_fields(remove_field, expected_messsage):
    # GIVEN: The initial challenge from the server
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # GIVEN: The response with a missing field
    auth = _get_authorization_header(
        digest=www_authenticate,
        method="GET",
        uri="/users/me",
        username="johndoe",
        password="password1",
        qop="auth",
    )
    auth = re.sub(rf"{remove_field}=\"[^\"]*\"", "", auth)

    # WHEN: The client attempts to access the protected resource.
    response = client.get(
        "/users/me",
        headers={"Authorization": auth},
    )

    # THEN: The server responds with a 401 Unauthorized response.
    assert response.status_code == 401
    assert response.json() == {"detail": expected_messsage}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users/me": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read Current User",
                    "operationId": "read_current_user_users_me_get",
                    "security": [{"HTTPDigest": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {"HTTPDigest": {"type": "http", "scheme": "digest"}}
        },
    }

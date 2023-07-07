import binascii
import hashlib
import os
import re
from typing import Optional

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPDigest, HTTPDigestCredentials
from fastapi.security.utils import digest_access_response
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPDigest(realm="somewhere@host.com", userhash=True)


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
    userhash: bool = True,
) -> str:
    nonce = re.search(r'nonce="([^"]+)"', digest).group(1)
    opaque = re.search(r'opaque="([^"]+)"', digest).group(1)

    cnonce = binascii.b2a_hex(os.urandom(15))

    # Hash username
    if userhash:
        username = hashlib.new(algo, f"{username}:{realm}".encode()).hexdigest()

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
        "userhash": "true",
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
    assert 'userhash="true"' in www_authenticate


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


def test_security_http_digest_fails_unhashed_user():
    # GIVEN: The initial challenge from the server
    challenge = client.get(
        "/users/me",
    )
    assert challenge.status_code == 401
    www_authenticate = challenge.headers["WWW-Authenticate"]

    # WHEN: The client sends the response with an unhashed user.
    response = client.get(
        "/users/me",
        headers={
            "Authorization": _get_authorization_header(
                digest=www_authenticate,
                method="GET",
                uri="/users/me",
                username="johndoe",
                password="password1",
                userhash=False,
            )
        },
    )

    # THEN: The server responds with a 401 OK response.
    assert response.status_code == 401

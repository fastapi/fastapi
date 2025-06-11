from typing import Union

import pytest
from fastapi import FastAPI, Security
from fastapi.security.api_key import APIKeyBase, APIKeyCookie, APIKeyHeader, APIKeyQuery
from fastapi.security.http import HTTPBase, HTTPBearer, HTTPDigest
from fastapi.security.oauth2 import OAuth2
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "auth",
    [
        APIKeyQuery(name="key", not_authenticated_status_code=403),
        APIKeyHeader(name="key", not_authenticated_status_code=403),
        APIKeyCookie(name="key", not_authenticated_status_code=403),
    ],
)
def test_apikey_status_code_403_on_auth_error(auth: APIKeyBase):
    """
    Test temporary `not_authenticated_status_code` parameter for APIKey** classes.
    """

    app = FastAPI()

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "auth",
    [
        APIKeyQuery(name="key", not_authenticated_status_code=403, auto_error=False),
        APIKeyHeader(name="key", not_authenticated_status_code=403, auto_error=False),
        APIKeyCookie(name="key", not_authenticated_status_code=403, auto_error=False),
    ],
)
def test_apikey_status_code_403_on_auth_error_no_auto_error(auth: APIKeyBase):
    """
    Test temporary `not_authenticated_status_code` parameter for APIKey** classes with
    `auto_error=False`.
    """

    app = FastAPI()

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "auth",
    [
        HTTPBearer(not_authenticated_status_code=403),
        OpenIdConnect(not_authenticated_status_code=403, openIdConnectUrl="/openid"),
        OAuth2(
            not_authenticated_status_code=403,
            flows={"password": {"tokenUrl": "token", "scopes": {}}},
        ),
    ],
)
def test_oauth2_status_code_403_on_auth_error(auth: Union[HTTPBase, OpenIdConnect]):
    """
    Test temporary `not_authenticated_status_code` parameter for security classes that
    follow rfc6750.
    """

    app = FastAPI()

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "auth",
    [
        HTTPBearer(not_authenticated_status_code=403, auto_error=False),
        OpenIdConnect(
            not_authenticated_status_code=403,
            openIdConnectUrl="/openid",
            auto_error=False,
        ),
        OAuth2(
            not_authenticated_status_code=403,
            flows={"password": {"tokenUrl": "token", "scopes": {}}},
            auto_error=False,
        ),
    ],
)
def test_oauth2_status_code_403_on_auth_error_no_auto_error(
    auth: Union[HTTPBase, OpenIdConnect],
):
    """
    Test temporary `not_authenticated_status_code` parameter for security classes that
    follow rfc6750.
    With `auto_error=False`. Response code should be 200
    """

    app = FastAPI()

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200


def test_digest_status_code_403_on_auth_error():
    """
    Test temporary `not_authenticated_status_code` parameter for `Digest` scheme.
    """

    app = FastAPI()

    auth = HTTPDigest(not_authenticated_status_code=403)

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_digest_status_code_403_on_auth_error_no_auto_error():
    """
    Test temporary `not_authenticated_status_code` parameter for `Digest` scheme with
    `auto_error=False`.
    """

    app = FastAPI()

    auth = HTTPDigest(not_authenticated_status_code=403, auto_error=False)

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200


def test_httpbase_status_code_403_on_auth_error():
    """
    Test temporary `not_authenticated_status_code` parameter for `HTTPBase` class.
    """

    app = FastAPI()

    auth = HTTPBase(scheme="Other", not_authenticated_status_code=403)

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_httpbase_status_code_403_on_auth_error_no_auto_error():
    """
    Test temporary `not_authenticated_status_code` parameter for `HTTPBase` class with
    `auto_error=False`.
    """

    app = FastAPI()

    auth = HTTPBase(scheme="Other", not_authenticated_status_code=403, auto_error=False)

    @app.get("/")
    async def protected(_: str = Security(auth)):
        pass  # pragma: no cover

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200

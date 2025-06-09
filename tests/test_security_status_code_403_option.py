import pytest
from fastapi import FastAPI, Security
from fastapi.security.api_key import APIKeyBase, APIKeyCookie, APIKeyHeader, APIKeyQuery
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

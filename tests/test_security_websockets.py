from functools import partial

import pytest
from fastapi import FastAPI, Security, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.security import (
    APIKeyCookie,
    APIKeyHeader,
    APIKeyQuery,
    HTTPBasic,
    HTTPBearer,
    HTTPDigest,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OpenIdConnect,
)
from fastapi.security.http import HTTPBase
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse


@pytest.mark.parametrize(
    "security_factory, path, headers, expected, challenge",
    [
        pytest.param(
            partial(HTTPBase, scheme="Other"),
            "/",
            {"Authorization": "Other secret"},
            {"scheme": "Other", "credentials": "secret"},
            "Other",
            id="http-base",
        ),
        pytest.param(
            HTTPBasic,
            "/",
            {"Authorization": "Basic am9objpzZWNyZXQ="},
            {"username": "john", "password": "secret"},
            "Basic",
            id="http-basic",
        ),
        pytest.param(
            HTTPBearer,
            "/",
            {"Authorization": "Bearer secret"},
            {"scheme": "Bearer", "credentials": "secret"},
            "Bearer",
            id="http-bearer",
        ),
        pytest.param(
            HTTPDigest,
            "/",
            {"Authorization": "Digest secret"},
            {"scheme": "Digest", "credentials": "secret"},
            "Digest",
            id="http-digest",
        ),
        pytest.param(
            partial(APIKeyQuery, name="key"),
            "/?key=secret",
            {},
            "secret",
            "APIKey",
            id="api-key-query",
        ),
        pytest.param(
            partial(APIKeyHeader, name="key"),
            "/",
            {"key": "secret"},
            "secret",
            "APIKey",
            id="api-key-header",
        ),
        pytest.param(
            partial(APIKeyCookie, name="key"),
            "/",
            {"Cookie": "key=secret"},
            "secret",
            "APIKey",
            id="api-key-cookie",
        ),
        pytest.param(
            OAuth2,
            "/",
            {"Authorization": "Bearer secret"},
            "Bearer secret",
            "Bearer",
            id="oauth2",
        ),
        pytest.param(
            partial(OAuth2PasswordBearer, tokenUrl="/token"),
            "/",
            {"Authorization": "Bearer secret"},
            "secret",
            "Bearer",
            id="oauth2-password-bearer",
        ),
        pytest.param(
            partial(
                OAuth2AuthorizationCodeBearer,
                authorizationUrl="/authorize",
                tokenUrl="/token",
            ),
            "/",
            {"Authorization": "Bearer secret"},
            "secret",
            "Bearer",
            id="oauth2-authorization-code-bearer",
        ),
        pytest.param(
            partial(OpenIdConnect, openIdConnectUrl="/openid"),
            "/",
            {"Authorization": "Bearer secret"},
            "Bearer secret",
            "Bearer",
            id="openid-connect",
        ),
    ],
)
@pytest.mark.parametrize(
    "auto_error, has_credentials",
    [
        pytest.param(True, True, id="valid-credentials"),
        pytest.param(True, False, id="missing-required-credentials"),
        pytest.param(False, False, id="missing-optional-credentials"),
    ],
)
def test_security_websocket(
    security_factory,
    path: str,
    headers: dict[str, str],
    expected: dict[str, str] | str,
    challenge: str,
    auto_error: bool,
    has_credentials: bool,
):
    security = security_factory(auto_error=auto_error)
    app = FastAPI()

    @app.websocket("/")
    async def endpoint(websocket: WebSocket, credentials=Security(security)):
        await websocket.accept()
        await websocket.send_json(jsonable_encoder(credentials))
        await websocket.close()

    with TestClient(app) as client:
        if auto_error and not has_credentials:
            with pytest.raises(WebSocketDenialResponse) as exc_info:
                with client.websocket_connect("/"):
                    pass  # pragma: no cover
            assert exc_info.value.status_code == 401
            assert exc_info.value.json() == {"detail": "Not authenticated"}
            assert exc_info.value.headers["WWW-Authenticate"] == challenge
        else:
            with client.websocket_connect(
                path if has_credentials else "/",
                headers=headers if has_credentials else {},
            ) as websocket:
                assert websocket.receive_json() == (
                    expected if has_credentials else None
                )

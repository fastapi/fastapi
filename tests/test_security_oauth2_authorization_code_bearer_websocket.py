import pytest
from fastapi import FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/api/oauth/authorize",
    tokenUrl="/api/oauth/token",
    scopes={"read": "Read access", "write": "Write access"},
)


@app.websocket("/ws/admin")
async def read_admin(websocket: WebSocket, token: str = Security(oauth2_scheme)):
    await websocket.accept()
    await websocket.send_text(token)


client = TestClient(app)


def test_security_oauth2_authorization_code_bearer_ws():
    with client.websocket_connect(
        "/ws/admin", headers={"Authorization": "Bearer faketoken"}
    ) as websocket:
        data = websocket.receive_text()
        assert data == "faketoken"


def test_security_oauth2_authorization_code_bearer_no_header_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/admin"):
            pass


def test_security_oauth2_authorization_code_bearer_wrong_scheme_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect(
            "/ws/admin", headers={"Authorization": "Basic nope"}
        ):
            pass

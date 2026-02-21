from fastapi import FastAPI, Security, WebSocket
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()

security = HTTPBase(scheme="Other", auto_error=False)


@app.get("/users/me")
def read_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
):
    if credentials is None:
        return {"msg": "Create an account first"}
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


@app.websocket("/users/timeline")
async def read_user_timeline(
    websocket: WebSocket,
    credentials: HTTPAuthorizationCredentials | None = Security(security),
):
    await websocket.accept()
    await websocket.send_json(
        {"scheme": credentials.scheme, "credentials": credentials.credentials}
        if credentials
        else {"msg": "Create an account first"}
    )


client = TestClient(app)


def test_security_http_base():
    response = client.get("/users/me", headers={"Authorization": "Other foobar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"scheme": "Other", "credentials": "foobar"}


def test_security_http_base_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Create an account first"}


def test_security_http_base_with_ws():
    with client.websocket_connect(
        "/users/timeline", headers={"Authorization": "Other foobar"}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"scheme": "Other", "credentials": "foobar"}


def test_security_http_base_with_ws_no_credentials():
    with client.websocket_connect("/users/timeline") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Create an account first"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
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
                        "security": [{"HTTPBase": []}],
                    }
                }
            },
            "components": {
                "securitySchemes": {"HTTPBase": {"type": "http", "scheme": "Other"}}
            },
        }
    )

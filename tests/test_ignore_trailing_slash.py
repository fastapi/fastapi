from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.testclient import TestClient

app = FastAPI(ignore_trailing_slash=True)
router = APIRouter()

@app.get("/example")
async def example_endpoint():
    return {"msg": "Example"}

@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket")
    await websocket.close()

@router.get("/example")
def route_endpoint():
    return {"msg": "Routing Example"}

app.include_router(router, prefix="/router")

client = TestClient(app)

def test_ignoring_trailing_slash():
    response = client.get("/example", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Example"
    response = client.get("/example/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Example"

def test_ignoring_trailing_shlash_ws():
    with client.websocket_connect("/websocket") as websocket:
        assert websocket.receive_text() == "Websocket"
    with client.websocket_connect("/websocket/") as websocket:
        assert websocket.receive_text() == "Websocket"

def test_ignoring_trailing_routing():
    response = client.get("router/example", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Routing Example"
    response = client.get("router/example/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Routing Example"

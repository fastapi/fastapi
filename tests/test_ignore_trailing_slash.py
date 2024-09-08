from fastapi import APIRouter, FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI(ignore_trailing_slash=True)
router = APIRouter()


@app.get("/example")
async def example_endpoint():
    return {"msg": "Example"}


@app.get("/example2/")
async def example_endpoint_with_slash():
    return {"msg": "Example 2"}


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket")
    await websocket.close()


@app.websocket("/websocket2/")
async def websocket_endpoint_with_slash(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket 2")
    await websocket.close()


@app.websocket_route("/websocket_route")
async def websocket_route_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket route")
    await websocket.close()


@app.websocket_route("/websocket_route_2/")
async def websocket_route_endpoint_with_slash(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket route 2")
    await websocket.close()


@router.get("/example")
def route_endpoint():
    return {"msg": "Routing Example"}


@router.get("/example2/")
def route_endpoint_with_slash():
    return {"msg": "Routing Example 2"}


@router.websocket("/websocket")
async def router_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket")
    await websocket.close()


@router.websocket("/websocket2/")
async def router_websocket_endpoint_with_slash(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket 2")
    await websocket.close()


@router.websocket_route("/websocket_route")
async def router_websocket_route_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket route")
    await websocket.close()


@router.websocket_route("/websocket_route_2/")
async def router_websocket_route_endpoint_with_slash(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Websocket route 2")
    await websocket.close()


@router.route("/starlette_route", ["get"])
async def starlette_route_endpoint(request: Request):
    return JSONResponse({"msg": "Starlette Route"})


@router.route("/starlette_route_2/", ["get"])
async def starlette_route_endpoint_with_slash(request: Request):
    return JSONResponse({"msg": "Starlette Route 2"})


app.include_router(router, prefix="/router")

client = TestClient(app)


def test_ignoring_trailing_slash():
    response = client.get("/example/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Example"
    response = client.get("/example2", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Example 2"


def test_ignoring_trailing_shlash_ws():
    with client.websocket_connect("/websocket/") as websocket:
        assert websocket.receive_text() == "Websocket"
    with client.websocket_connect("/websocket2") as websocket:
        assert websocket.receive_text() == "Websocket 2"
    with client.websocket_connect("/websocket_route/") as websocket:
        assert websocket.receive_text() == "Websocket route"
    with client.websocket_connect("/websocket_route_2/") as websocket:
        assert websocket.receive_text() == "Websocket route 2"


def test_ignoring_trailing_routing():
    response = client.get("router/example/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Routing Example"
    response = client.get("router/example2", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Routing Example 2"
    response = client.get("router/starlette_route/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Starlette Route"
    response = client.get("router/starlette_route_2", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Starlette Route 2"
    with client.websocket_connect("router/websocket/") as websocket:
        assert websocket.receive_text() == "Websocket"
    with client.websocket_connect("router/websocket2") as websocket:
        assert websocket.receive_text() == "Websocket 2"
    with client.websocket_connect("router/websocket_route/") as websocket:
        assert websocket.receive_text() == "Websocket route"
    with client.websocket_connect("router/websocket_route_2/") as websocket:
        assert websocket.receive_text() == "Websocket route 2"

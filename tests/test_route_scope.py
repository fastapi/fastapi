import pytest
from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRoute, APIWebSocketRoute, RouteContext
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    route: APIRoute = request.scope["route"]
    return {"user_id": user_id, "path": route.path}


@app.websocket("/items/{item_id}")
async def websocket_item(item_id: str, websocket: WebSocket):
    route: APIWebSocketRoute = websocket.scope["route"]
    await websocket.accept()
    await websocket.send_json({"item_id": item_id, "path": route.path})


client = TestClient(app)


def test_get():
    response = client.get("/users/rick")
    assert response.status_code == 200, response.text
    assert response.json() == {"user_id": "rick", "path": "/users/{user_id}"}


def test_invalid_method_doesnt_match():
    response = client.post("/users/rick")
    assert response.status_code == 405, response.text


def test_invalid_path_doesnt_match():
    response = client.post("/usersx/rick")
    assert response.status_code == 404, response.text


def test_websocket():
    with client.websocket_connect("/items/portal-gun") as websocket:
        data = websocket.receive_json()
        assert data == {"item_id": "portal-gun", "path": "/items/{item_id}"}


def test_websocket_invalid_path_doesnt_match():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/itemsx/portal-gun"):
            pass  # pragma: no cover


# --- Regression: scope["route"].path/.path_format must include prefixes
# added by include_router(), for both single-level and nested routers.
# https://github.com/fastapi/fastapi/discussions/16051

included_app = FastAPI()
included_router = APIRouter()


@included_router.get("/users/{user_id}")
async def get_included_user(user_id: str, request: Request):
    route: RouteContext = request.scope["route"]
    return {
        "user_id": user_id,
        "path": route.path,
        "path_format": route.path_format,
        "original_path": getattr(route.original_route, "path", None),
    }


@included_router.websocket("/items/{item_id}")
async def websocket_included_item(item_id: str, websocket: WebSocket):
    route: APIWebSocketRoute = websocket.scope["route"]
    await websocket.accept()
    await websocket.send_json({"item_id": item_id, "path": route.path})


included_app.include_router(included_router, prefix="/api")

included_client = TestClient(included_app)


def test_included_router_route_path_has_prefix():
    response = included_client.get("/api/users/rick")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "user_id": "rick",
        "path": "/api/users/{user_id}",
        "path_format": "/api/users/{user_id}",
        "original_path": "/users/{user_id}",
    }


def test_included_router_websocket_route_path_has_prefix():
    with included_client.websocket_connect("/api/items/portal-gun") as websocket:
        data = websocket.receive_json()
        assert data == {"item_id": "portal-gun", "path": "/api/items/{item_id}"}


nested_app = FastAPI()
nested_inner_router = APIRouter(prefix="/level2")


@nested_inner_router.get("/endpoint")
async def nested_endpoint(request: Request):
    route: RouteContext = request.scope["route"]
    return {
        "path": route.path,
        "original_path": getattr(route.original_route, "path", None),
    }


nested_outer_router = APIRouter(prefix="/level1")
nested_outer_router.include_router(nested_inner_router)
nested_app.include_router(nested_outer_router, prefix="/api")

nested_client = TestClient(nested_app)


def test_nested_included_router_route_path_has_all_prefixes():
    response = nested_client.get("/api/level1/level2/endpoint")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "path": "/api/level1/level2/endpoint",
        "original_path": "/level2/endpoint",
    }


middleware_app = FastAPI()
middleware_router = APIRouter()
observed_middleware_paths = []


@middleware_router.get("/observed")
async def observed_endpoint():
    return {"ok": True}


@middleware_app.middleware("http")
async def record_route_path(request: Request, call_next):
    response = await call_next(request)
    route = request.scope.get("route")
    observed_middleware_paths.append(getattr(route, "path", None))
    return response


middleware_app.include_router(middleware_router, prefix="/mw")

middleware_client = TestClient(middleware_app)


def test_middleware_observed_route_path_has_prefix():
    observed_middleware_paths.clear()
    response = middleware_client.get("/mw/observed")
    assert response.status_code == 200, response.text
    assert observed_middleware_paths == ["/mw/observed"]

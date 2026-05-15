from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from starlette.requests import Request


class CustomExcA(Exception):
    pass


class CustomExcB(Exception):
    pass


def exc_a_handler(request: Request, exc: CustomExcA) -> JSONResponse:
    return JSONResponse({"error": "handled_a"}, status_code=400)


def exc_b_handler(request: Request, exc: CustomExcB) -> JSONResponse:
    return JSONResponse({"error": "handled_b"}, status_code=400)


def test_basic_router_exception_handler():
    app = FastAPI()
    router = APIRouter(exception_handlers={CustomExcA: exc_a_handler})

    @router.get("/fail")
    def fail():
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app)
    resp = client.get("/fail")
    assert resp.status_code == 400
    assert resp.json() == {"error": "handled_a"}


def test_isolation_between_routers():
    app = FastAPI()
    router1 = APIRouter(prefix="/r1", exception_handlers={CustomExcA: exc_a_handler})
    router2 = APIRouter(prefix="/r2")

    @router1.get("/fail")
    def fail1():
        raise CustomExcA()

    @router2.get("/fail")
    def fail2():
        raise CustomExcA()

    app.include_router(router1)
    app.include_router(router2)
    client = TestClient(app, raise_server_exceptions=False)

    resp1 = client.get("/r1/fail")
    assert resp1.status_code == 400
    assert resp1.json() == {"error": "handled_a"}

    resp2 = client.get("/r2/fail")
    assert resp2.status_code == 500


def test_router_overrides_app():
    def app_handler(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "app_handled"}, status_code=400)

    def router_handler(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "router_handled"}, status_code=400)

    app = FastAPI(exception_handlers={CustomExcA: app_handler})
    router = APIRouter(prefix="/r", exception_handlers={CustomExcA: router_handler})

    @router.get("/fail")
    def fail():
        raise CustomExcA()

    @app.get("/app-fail")
    def app_fail():
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app)

    resp = client.get("/r/fail")
    assert resp.status_code == 400
    assert resp.json() == {"error": "router_handled"}

    resp_app = client.get("/app-fail")
    assert resp_app.status_code == 400
    assert resp_app.json() == {"error": "app_handled"}


def test_app_fallback():
    def app_handler(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "app_handled"}, status_code=400)

    app = FastAPI(exception_handlers={CustomExcA: app_handler})
    router = APIRouter(prefix="/r")

    @router.get("/fail")
    def fail():
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app)

    resp = client.get("/r/fail")
    assert resp.status_code == 400
    assert resp.json() == {"error": "app_handled"}


def test_nested_router_precedence():
    def handler_a(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "A"}, status_code=400)

    def handler_b(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "B"}, status_code=400)

    router_a = APIRouter(prefix="/a", exception_handlers={CustomExcA: handler_a})
    router_b = APIRouter(prefix="/b", exception_handlers={CustomExcA: handler_b})

    @router_a.get("/fail")
    def fail_a():
        raise CustomExcA()

    @router_b.get("/fail")
    def fail_b():
        raise CustomExcA()

    router_a.include_router(router_b)
    app = FastAPI()
    app.include_router(router_a)
    client = TestClient(app)

    resp_b = client.get("/a/b/fail")
    assert resp_b.status_code == 400
    assert resp_b.json() == {"error": "B"}

    resp_a = client.get("/a/fail")
    assert resp_a.status_code == 400
    assert resp_a.json() == {"error": "A"}


def test_deep_nesting():
    def handler_a(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "A"}, status_code=400)

    def handler_b(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "B"}, status_code=400)

    def handler_c(request: Request, exc: CustomExcA) -> JSONResponse:
        return JSONResponse({"error": "C"}, status_code=400)

    router_a = APIRouter(prefix="/a", exception_handlers={CustomExcA: handler_a})
    router_b = APIRouter(prefix="/b", exception_handlers={CustomExcA: handler_b})
    router_c = APIRouter(prefix="/c", exception_handlers={CustomExcA: handler_c})

    @router_a.get("/fail")
    def fail_a():
        raise CustomExcA()

    @router_b.get("/fail")
    def fail_b():
        raise CustomExcA()

    @router_c.get("/fail")
    def fail_c():
        raise CustomExcA()

    router_b.include_router(router_c)
    router_a.include_router(router_b)
    app = FastAPI()
    app.include_router(router_a)
    client = TestClient(app)

    resp_c = client.get("/a/b/c/fail")
    assert resp_c.status_code == 400
    assert resp_c.json() == {"error": "C"}

    resp_b = client.get("/a/b/fail")
    assert resp_b.status_code == 400
    assert resp_b.json() == {"error": "B"}

    resp_a = client.get("/a/fail")
    assert resp_a.status_code == 400
    assert resp_a.json() == {"error": "A"}


def test_add_exception_handler_method():
    app = FastAPI()
    router = APIRouter()
    router.add_exception_handler(CustomExcA, exc_a_handler)

    @router.get("/fail")
    def fail():
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app)

    resp = client.get("/fail")
    assert resp.status_code == 400
    assert resp.json() == {"error": "handled_a"}


def test_status_code_handler():
    from starlette.exceptions import HTTPException

    def not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse({"error": "custom_404"}, status_code=404)

    app = FastAPI()
    router = APIRouter(prefix="/r", exception_handlers={404: not_found_handler})

    @router.get("/fail")
    def fail():
        raise HTTPException(status_code=404, detail="not found")

    app.include_router(router)
    client = TestClient(app)

    resp = client.get("/r/fail")
    assert resp.status_code == 404
    assert resp.json() == {"error": "custom_404"}


def test_app_routes_unaffected():
    app = FastAPI()
    router = APIRouter(prefix="/r", exception_handlers={CustomExcA: exc_a_handler})

    @router.get("/fail")
    def router_fail():
        raise CustomExcA()

    @app.get("/fail")
    def app_fail():
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app, raise_server_exceptions=False)

    resp_router = client.get("/r/fail")
    assert resp_router.status_code == 400
    assert resp_router.json() == {"error": "handled_a"}

    resp_app = client.get("/fail")
    assert resp_app.status_code == 500


def test_multiple_exception_types():
    app = FastAPI()
    router = APIRouter(
        exception_handlers={
            CustomExcA: exc_a_handler,
            CustomExcB: exc_b_handler,
        }
    )

    @router.get("/fail-a")
    def fail_a():
        raise CustomExcA()

    @router.get("/fail-b")
    def fail_b():
        raise CustomExcB()

    app.include_router(router)
    client = TestClient(app)

    resp_a = client.get("/fail-a")
    assert resp_a.status_code == 400
    assert resp_a.json() == {"error": "handled_a"}

    resp_b = client.get("/fail-b")
    assert resp_b.status_code == 400
    assert resp_b.json() == {"error": "handled_b"}


def test_websocket_router_exception_handler():
    app = FastAPI()
    router = APIRouter(
        exception_handlers={CustomExcA: exc_a_handler, 404: exc_a_handler}
    )

    @router.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket):
        await websocket.accept()
        raise CustomExcA()

    app.include_router(router)
    client = TestClient(app)

    with client.websocket_connect("/ws") as ws:
        # The exception handler returns a JSON response, but for websockets
        # the connection should close with an error
        try:
            ws.receive_text()
        except Exception:
            pass


def test_websocket_nested_router_exception_handler():
    app = FastAPI()
    router_a = APIRouter(prefix="/a", exception_handlers={CustomExcA: exc_a_handler})
    router_b = APIRouter(prefix="/b", exception_handlers={CustomExcA: exc_a_handler})

    @router_b.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket):
        await websocket.accept()
        raise CustomExcA()

    router_a.include_router(router_b)
    app.include_router(router_a)
    client = TestClient(app)

    with client.websocket_connect("/a/b/ws") as ws:
        try:
            ws.receive_text()
        except Exception:
            pass

from itertools import chain

from fastapi import APIRouter, Depends, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.routing import BaseRoute

deferred_keys = [
    "app",
    "response_fields",
    "body_field",
    "response_field",
    "dependant",
    "_flat_dependant",
    "_embed_body_fields",
]


def check_if_initialized(route: APIRoute, should_not: bool = False):
    for key in deferred_keys:
        if should_not:
            assert key not in route.__dict__
        else:
            assert key in route.__dict__


def create_test_router(routes: list[BaseRoute] | None = None, defer_init: bool = True):
    router = APIRouter(routes=routes or [], defer_init=defer_init)

    class UserIdBody(BaseModel):
        user_id: int

    @router.get("/user_id", dependencies=[Depends(lambda: True)])
    async def get_user_id(user_id: int = Depends(lambda: 1)) -> UserIdBody:
        return {"user_id": user_id}

    return router


def test_route_defers():
    app = FastAPI()
    router = create_test_router(routes=app.router.routes)

    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
        check_if_initialized(route, should_not=True)

    app.router = router
    client = TestClient(app)
    response = client.get("/user_id")
    assert response.status_code == 200
    response = client.get("/openapi.json")
    assert response.status_code == 200

    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
        check_if_initialized(route)


def test_route_manual_init():
    router = create_test_router()
    for route in router.routes:
        check_if_initialized(route, should_not=True)
        route.init_attributes()
        check_if_initialized(route)

    router = create_test_router()
    router.init_routes()
    for route in router.routes:
        check_if_initialized(route)


def test_router_defer_init_flag():
    route = APIRoute("/test", lambda: {"test": True}, defer_init=False)
    check_if_initialized(route)

    deferring_router = create_test_router()
    router = create_test_router(routes=deferring_router.routes, defer_init=False)

    for route in router.routes:
        check_if_initialized(route)


def test_root_router_always_initialized():
    app = FastAPI()

    @app.get("/test")
    async def test_get():
        return {"test": 1}

    router = create_test_router()
    app.include_router(router)
    for route in app.router.routes:
        if not isinstance(route, APIRoute):
            continue
        check_if_initialized(route)

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200


def test_include_router_no_init():
    router1 = create_test_router()

    router2 = create_test_router()
    router2.include_router(router1)

    for route in chain(router1.routes, router2.routes):
        check_if_initialized(route, should_not=True)

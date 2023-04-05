from functools import wraps

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.testclient import TestClient

DECORATOR_ARG = "arg"

app = FastAPI()


def decorator_1(endpoint):
    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
        response = await endpoint(*args, **kwargs)
        response.update({"decorator_1": True})
        return response

    return wrapper


def decorator_2(endpoint, arg_1: str):
    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
        response = await endpoint(*args, **kwargs)
        response.update({"decorator_2": True, "arg": arg_1})
        return response

    return wrapper


router_decorated = APIRouter(decorators=[(decorator_1,), (decorator_2, DECORATOR_ARG)])
router_non_decorated = APIRouter()
router_non_decorated_route = APIRouter()


@router_decorated.get("/decorated_1")
async def decorated_1_route():
    return {"return": "/decorated_1 response"}


@router_non_decorated.get("/no_decorators_in_router")
async def no_decorators_in_router():
    return {"return": "/no_decorators_in_router response"}


async def non_router_decorated_endpoint():
    return {"return": "non decorated route"}


router_non_decorated_route.add_api_route(
    "/non_router_decorated_endpoint",
    non_router_decorated_endpoint,
    decorators=[(decorator_1,), (decorator_2, DECORATOR_ARG)],
)


app.include_router(router_decorated)
app.include_router(
    router_non_decorated, decorators=[(decorator_1,), (decorator_2, DECORATOR_ARG)]
)
app.include_router(router_non_decorated_route)


client = TestClient(app)


def test_decorated_router():
    response = client.get("/decorated_1")
    assert response.status_code == 200
    assert response.json()["decorator_1"]
    assert response.json()["decorator_2"]
    assert response.json()["arg"] == DECORATOR_ARG


def test_non_decorated_router():
    response = client.get("/no_decorators_in_router")
    assert response.status_code == 200
    assert response.json()["decorator_1"]
    assert response.json()["decorator_2"]
    assert response.json()["arg"] == DECORATOR_ARG


def test_non_router_decorated_endpoint():
    response = client.get("/non_router_decorated_endpoint")
    assert response.status_code == 200
    assert response.json()["decorator_1"]
    assert response.json()["decorator_2"]
    assert response.json()["arg"] == DECORATOR_ARG

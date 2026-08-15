import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()


class APIRouteA(APIRoute):
    x_type = "A"


class APIRouteB(APIRoute):
    x_type = "B"


class APIRouteC(APIRoute):
    x_type = "C"


router_a = APIRouter(route_class=APIRouteA)
router_b = APIRouter(route_class=APIRouteB)
router_c = APIRouter(route_class=APIRouteC)


@router_a.get("/")
def get_a():
    return {"msg": "A"}


@router_b.get("/")
def get_b():
    return {"msg": "B"}


@router_c.get("/")
def get_c():
    return {"msg": "C"}


router_b.include_router(router=router_c, prefix="/c")
router_a.include_router(router=router_b, prefix="/b")
app.include_router(router=router_a, prefix="/a")


client = TestClient(app)


def test_apiroute_tags_annotation():
    # Verify APIRoute.tags class annotation presence (#15764)
    route = APIRoute("/test", endpoint=get_a, tags=["test_tag"])
    assert hasattr(route, "tags")
    assert route.tags == ["test_tag"]

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


def test_direct_append_to_child_routes_is_visible():
    app = FastAPI()
    child = APIRouter()

    @child.get("/child")
    def read_child():
        return {"msg": "v1-original"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    response = client.get("/api/child")
    assert response.status_code == 200, response.text

    def read_child2():
        return {"msg": "v2-added-directly"}

    new_route = APIRoute("/child2", read_child2, methods=["GET"])
    child.routes.append(new_route)

    response = client.get("/api/child2")
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "v2-added-directly"}


def test_direct_remove_from_child_routes_is_not_a_ghost():
    app = FastAPI()
    child = APIRouter()

    @child.get("/child")
    def read_child():
        return {"msg": "v1-original"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    response = client.get("/api/child")
    assert response.status_code == 200, response.text

    original = [rt for rt in child.routes if getattr(rt, "path", None) == "/child"][0]
    child.routes.remove(original)

    response = client.get("/api/child")
    assert response.status_code == 404, response.text


def test_full_routes_reassignment_invalidates_cache():
    app = FastAPI()
    child = APIRouter()

    @child.get("/a")
    def read_a():
        return {"msg": "a"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    response = client.get("/api/a")
    assert response.status_code == 200, response.text

    child.routes = [rt for rt in child.routes if getattr(rt, "path", None) != "/a"]

    response = client.get("/api/a")
    assert response.status_code == 404, response.text
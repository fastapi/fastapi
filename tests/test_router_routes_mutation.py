from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.testclient import TestClient


def test_direct_routes_append_invalidates_cache() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/child")
    def read_child() -> dict[str, str]:
        return {"msg": "v1-original"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    # Initial request caches effective route candidates
    response = client.get("/api/child")
    assert response.status_code == 200
    assert response.json() == {"msg": "v1-original"}

    # Direct append
    def read_child2() -> dict[str, str]:
        return {"msg": "v2-added-directly"}

    new_route = APIRoute("/child2", read_child2, methods=["GET"])
    child.routes.append(new_route)

    r1 = client.get("/api/child2")
    assert r1.status_code == 200
    assert r1.json() == {"msg": "v2-added-directly"}


def test_direct_routes_remove_invalidates_cache() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/child")
    def read_child() -> dict[str, str]:
        return {"msg": "v1-original"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    # Cache effective candidates
    assert client.get("/api/child").status_code == 200

    # Direct remove
    original = [rt for rt in child.routes if getattr(rt, "path", None) == "/child"][0]
    child.routes.remove(original)

    # Removed route should return 404, not 200 ghost route
    assert client.get("/api/child").status_code == 404


def test_direct_routes_extend_and_pop() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/item1")
    def item1() -> dict[str, int]:
        return {"item": 1}

    app.include_router(child, prefix="/api")
    client = TestClient(app)
    assert client.get("/api/item1").status_code == 200

    def item2() -> dict[str, int]:
        return {"item": 2}

    def item3() -> dict[str, int]:
        return {"item": 3}

    child.routes.extend(
        [
            APIRoute("/item2", item2, methods=["GET"]),
            APIRoute("/item3", item3, methods=["GET"]),
        ]
    )

    assert client.get("/api/item2").status_code == 200
    assert client.get("/api/item3").status_code == 200

    popped = child.routes.pop()
    assert getattr(popped, "path", None) == "/item3"
    assert client.get("/api/item3").status_code == 404
    assert client.get("/api/item2").status_code == 200


def test_direct_routes_reassignment() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/old")
    def old() -> dict[str, str]:
        return {"msg": "old"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)
    assert client.get("/api/old").status_code == 200

    def new_handler() -> dict[str, str]:
        return {"msg": "new"}

    child.routes = [APIRoute("/new", new_handler, methods=["GET"])]
    assert client.get("/api/old").status_code == 404
    assert client.get("/api/new").status_code == 200
    assert client.get("/api/new").json() == {"msg": "new"}


def test_direct_routes_clear() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/item")
    def item() -> dict[str, str]:
        return {"msg": "item"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)
    assert client.get("/api/item").status_code == 200

    child.routes.clear()
    assert client.get("/api/item").status_code == 404


def test_direct_routes_mutation_refreshes_openapi_schema() -> None:
    app = FastAPI()
    child = APIRouter()

    @child.get("/item1")
    def item1() -> dict[str, int]:
        return {"item": 1}

    app.include_router(child, prefix="/api")
    client = TestClient(app)
    assert client.get("/api/item1").status_code == 200

    schema1: dict[str, Any] = app.openapi()
    assert "/api/item1" in schema1["paths"]
    assert "/api/item2" not in schema1["paths"]

    def item2() -> dict[str, int]:
        return {"item": 2}

    child.routes.append(APIRoute("/item2", item2, methods=["GET"]))
    assert client.get("/api/item2").status_code == 200

    schema2: dict[str, Any] = app.openapi()
    assert "/api/item1" in schema2["paths"]
    assert "/api/item2" in schema2["paths"]


def test_direct_routes_insert_and_indexing() -> None:
    app = FastAPI()
    child = APIRouter()

    def r1() -> dict[str, int]:
        return {"r": 1}

    def r2() -> dict[str, int]:
        return {"r": 2}

    def r3() -> dict[str, int]:
        return {"r": 3}

    child.routes.append(APIRoute("/first", r1, methods=["GET"]))
    app.include_router(child, prefix="/api")
    client = TestClient(app)
    assert client.get("/api/first").status_code == 200

    # insert
    child.routes.insert(0, APIRoute("/second", r2, methods=["GET"]))
    assert client.get("/api/second").status_code == 200

    # __setitem__
    child.routes[0] = APIRoute("/third", r3, methods=["GET"])
    assert client.get("/api/second").status_code == 404
    assert client.get("/api/third").status_code == 200

    # __delitem__
    del child.routes[0]
    assert client.get("/api/third").status_code == 404
    assert client.get("/api/first").status_code == 200


def test_direct_routes_iadd_reverse_sort_and_self_reassignment() -> None:
    app = FastAPI()
    child = APIRouter()

    def handler_a() -> dict[str, str]:
        return {"a": "ok"}

    def handler_b() -> dict[str, str]:
        return {"b": "ok"}

    app.include_router(child, prefix="/api")
    client = TestClient(app)

    # __iadd__
    child.routes += [
        APIRoute("/b", handler_b, methods=["GET"]),
        APIRoute("/a", handler_a, methods=["GET"]),
    ]
    assert client.get("/api/a").status_code == 200
    assert client.get("/api/b").status_code == 200

    # reverse
    child.routes.reverse()
    assert client.get("/api/a").status_code == 200

    # sort
    child.routes.sort(key=lambda r: getattr(r, "path", ""))
    assert client.get("/api/a").status_code == 200

    # setter with already wrapped _ObservableRouteList on same router
    child.routes = child.routes
    assert client.get("/api/a").status_code == 200


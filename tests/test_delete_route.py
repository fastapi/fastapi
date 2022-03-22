from fastapi import APIRouter


def test_delete_api_route_method_1():
    # normal flow
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    res = router.delete_api_route("/foo")
    assert res is True
    assert len(router.routes) == 1

    assert router.routes[0].path == "/bar"


def test_delete_api_route_method_2():
    # a router with no route
    router = APIRouter()

    res = router.delete_api_route("/foo")

    assert res is False
    assert len(router.routes) == 0


def test_delete_api_route_method_3():
    # deleting a path which does not exist
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    res = router.delete_api_route("/path-not-exists")
    assert res is False
    assert len(router.routes) == 2

    path1, path2 = router.routes[0].path, router.routes[1].path

    assert "/bar" in (path1, path2)
    assert "/foo" in (path1, path2)

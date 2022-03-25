from fastapi import APIRouter


def test_exclude_routes_method_1():
    # normal flow
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes(["/foo"])

    assert len(router.routes) == 1
    assert router.routes[0].path == "/bar"


def test_exclude_routes_method_2():
    # a router with no route
    router = APIRouter()

    router.exclude_routes(["/foo"])

    assert len(router.routes) == 0


def test_exclude_routes_method_3():
    # deleting a path which does not exist
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes(["/path-not-exists_1", "/path-not-exists_2"])
    assert len(router.routes) == 2

    path1, path2 = router.routes[0].path, router.routes[1].path

    assert "/bar" in (path1, path2)
    assert "/foo" in (path1, path2)


def test_exclude_routes_method_4():
    # two paths, one of them does not exist
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes(["/foo", "/path-not-exists"])
    assert len(router.routes) == 1

    assert "/bar" == router.routes[0].path


def test_exclude_routes_method_5():
    # deleting two existing paths
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes(["/foo", "/bar"])
    assert len(router.routes) == 0


def test_exclude_routes_method_6():
    # no path to exclude
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes([])
    assert len(router.routes) == 2


def test_exclude_routes_method_7():
    # the same path multiple times
    router = APIRouter()

    @router.get("/foo")
    async def foo():
        return {"msg": "Hello from foo"}

    @router.post("/bar")
    async def bar():
        return {"msg": "Hello from bar"}

    assert len(router.routes) == 2

    router.exclude_routes(["/foo", "/foo", "/foo"])
    assert len(router.routes) == 1
    assert router.routes[0].path == "/bar"

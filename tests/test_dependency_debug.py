"""Tests for the dependency-graph debug endpoint (Task 1)."""

import functools
from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Helpers reused across tests
# ---------------------------------------------------------------------------

_DEBUG_PATH = "/_debug/deps"


def _app(**kwargs) -> FastAPI:  # type: ignore[no-untyped-def]
    return FastAPI(dependency_debug_url=_DEBUG_PATH, **kwargs)


def _find_route(payload: dict, path: str) -> dict:  # type: ignore[no-untyped-def]
    for r in payload["routes"]:
        if r["path"] == path:
            return r
    raise AssertionError(f"Route {path!r} not found in debug payload")  # pragma: no cover


# ---------------------------------------------------------------------------
# test_debug_disabled_by_default
# ---------------------------------------------------------------------------


def test_debug_disabled_by_default() -> None:
    app = FastAPI()  # dependency_debug_url not set → None

    @app.get("/hello")
    def hello() -> dict:
        return {"hi": True}

    client = TestClient(app)
    # The default path and a few guesses must all 404
    assert client.get("/_debug/deps").status_code == 404
    assert client.get("/_debug/dependencies").status_code == 404
    assert client.get("/debug").status_code == 404


# ---------------------------------------------------------------------------
# test_debug_enabled_returns_200
# ---------------------------------------------------------------------------


def test_debug_enabled_returns_200() -> None:
    app = _app()

    @app.get("/hello")
    def hello() -> dict:
        return {"hi": True}

    client = TestClient(app)
    resp = client.get(_DEBUG_PATH)
    assert resp.status_code == 200

    payload = resp.json()
    assert "routes" in payload
    route = _find_route(payload, "/hello")
    assert "GET" in route["methods"]
    assert route["dependency_graph"]["callable_name"] == "hello"


# ---------------------------------------------------------------------------
# test_debug_nested_three_levels
# ---------------------------------------------------------------------------


def test_debug_nested_three_levels() -> None:
    def dep_c() -> str:
        return "c"

    def dep_b(c: Annotated[str, Depends(dep_c)]) -> str:
        return "b"

    def dep_a(b: Annotated[str, Depends(dep_b)]) -> str:
        return "a"

    app = _app()

    @app.get("/nested")
    def nested(a: Annotated[str, Depends(dep_a)]) -> dict:
        return {"a": a}

    client = TestClient(app)
    route = _find_route(client.get(_DEBUG_PATH).json(), "/nested")
    graph = route["dependency_graph"]

    # Root is the endpoint itself
    assert graph["callable_name"] == "nested"

    # Level 1: dep_a
    assert len(graph["sub_dependencies"]) == 1
    a_node = graph["sub_dependencies"][0]
    assert a_node["callable_name"] == "dep_a"

    # Level 2: dep_b
    assert len(a_node["sub_dependencies"]) == 1
    b_node = a_node["sub_dependencies"][0]
    assert b_node["callable_name"] == "dep_b"

    # Level 3: dep_c — leaf
    assert len(b_node["sub_dependencies"]) == 1
    c_node = b_node["sub_dependencies"][0]
    assert c_node["callable_name"] == "dep_c"
    assert c_node["sub_dependencies"] == []


# ---------------------------------------------------------------------------
# test_debug_yield_dep_flagged
# ---------------------------------------------------------------------------


def test_debug_yield_dep_flagged() -> None:
    def plain_dep() -> str:
        return "plain"

    def yield_dep():  # type: ignore[no-untyped-def]
        yield "yielded"

    app = _app()

    @app.get("/mix")
    def mix(
        p: Annotated[str, Depends(plain_dep)],
        y: Annotated[str, Depends(yield_dep)],
    ) -> dict:
        return {}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/mix")
    subs = route["dependency_graph"]["sub_dependencies"]

    # Order matches signature order: plain first, yield second
    plain_node = subs[0]
    yield_node = subs[1]

    assert plain_node["callable_name"] == "plain_dep"
    assert plain_node["is_yield"] is False

    assert yield_node["callable_name"] == "yield_dep"
    assert yield_node["is_yield"] is True


# ---------------------------------------------------------------------------
# test_debug_async_generator_flagged
# ---------------------------------------------------------------------------


def test_debug_async_generator_flagged() -> None:
    async def async_gen_dep():  # type: ignore[no-untyped-def]
        yield "async"

    app = _app()

    @app.get("/agen")
    def agen(v: Annotated[str, Depends(async_gen_dep)]) -> dict:
        return {}

    node = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/agen")["dependency_graph"]
    sub = node["sub_dependencies"][0]

    assert sub["callable_name"] == "async_gen_dep"
    assert sub["is_yield"] is True
    assert sub["is_async"] is True


# ---------------------------------------------------------------------------
# test_debug_security_scopes
# ---------------------------------------------------------------------------


def test_debug_security_scopes() -> None:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
        return {"user": "me"}

    app = _app()

    @app.get("/protected")
    def protected(
        user: Annotated[dict, Security(get_current_user, scopes=["read", "admin"])],
    ) -> dict:
        return user

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/protected")
    # The Security node is a direct sub of the endpoint root
    sec_node = route["dependency_graph"]["sub_dependencies"][0]
    assert sec_node["callable_name"] == "get_current_user"
    assert "read" in sec_node["security_scopes"]
    assert "admin" in sec_node["security_scopes"]


# ---------------------------------------------------------------------------
# test_debug_security_and_depends_siblings
# ---------------------------------------------------------------------------


def test_debug_security_and_depends_siblings() -> None:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def plain_dep() -> str:
        return "plain"

    app = _app()

    @app.get("/siblings")
    def siblings(
        token: Annotated[str, Security(oauth2_scheme, scopes=["x"])],
        plain: Annotated[str, Depends(plain_dep)],
    ) -> dict:
        return {}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/siblings")
    subs = route["dependency_graph"]["sub_dependencies"]

    # First sub is the Security dep (oauth2_scheme instance)
    sec_sub = subs[0]
    assert sec_sub["is_security_scheme"] is True

    # Second sub is the plain Depends
    plain_sub = subs[1]
    assert plain_sub["callable_name"] == "plain_dep"
    assert plain_sub["is_security_scheme"] is False


# ---------------------------------------------------------------------------
# test_debug_route_level_deps_appear
# ---------------------------------------------------------------------------


def test_debug_route_level_deps_appear() -> None:
    def route_dep() -> None:
        pass

    app = _app()

    @app.get("/with-route-dep", dependencies=[Depends(route_dep)])
    def with_route_dep() -> dict:
        return {}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/with-route-dep")
    subs = route["dependency_graph"]["sub_dependencies"]

    # route_dep is prepended, so it is the first child
    assert subs[0]["callable_name"] == "route_dep"


# ---------------------------------------------------------------------------
# test_debug_partial_callable_unwrapped
# ---------------------------------------------------------------------------


def test_debug_partial_callable_unwrapped() -> None:
    def real_function(x: int = 1) -> int:
        return x

    partial_dep = functools.partial(real_function, x=42)

    app = _app()

    @app.get("/partial")
    def partial_endpoint(v: Annotated[int, Depends(partial_dep)]) -> dict:
        return {"v": v}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/partial")
    sub = route["dependency_graph"]["sub_dependencies"][0]

    # Must resolve through the partial to the underlying function name
    assert sub["callable_name"] == "real_function"


# ---------------------------------------------------------------------------
# test_debug_class_based_dep
# ---------------------------------------------------------------------------


def test_debug_class_based_dep() -> None:
    class MyDep:
        def __call__(self) -> str:
            return "class-dep"

    app = _app()

    @app.get("/classdep")
    def classdep(v: Annotated[str, Depends(MyDep)]) -> dict:
        return {"v": v}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/classdep")
    sub = route["dependency_graph"]["sub_dependencies"][0]

    assert sub["callable_name"] == "MyDep"


# ---------------------------------------------------------------------------
# test_debug_cached_repeat_detection
# ---------------------------------------------------------------------------


def test_debug_cached_repeat_detection() -> None:
    """A shared dep used by two sibling branches must appear fully in both
    (it is NOT on the same root→leaf path).  This test verifies no spurious
    ``cached_repeat`` flag is set in that scenario."""

    def shared() -> str:
        return "shared"

    def branch_a(s: Annotated[str, Depends(shared)]) -> str:
        return "a"

    def branch_b(s: Annotated[str, Depends(shared)]) -> str:
        return "b"

    app = _app()

    @app.get("/shared")
    def endpoint(
        a: Annotated[str, Depends(branch_a)],
        b: Annotated[str, Depends(branch_b)],
    ) -> dict:
        return {}

    route = _find_route(TestClient(app).get(_DEBUG_PATH).json(), "/shared")
    subs = route["dependency_graph"]["sub_dependencies"]

    # branch_a's child "shared" should be fully expanded (no cached_repeat)
    shared_under_a = subs[0]["sub_dependencies"][0]
    assert shared_under_a["callable_name"] == "shared"
    assert "cached_repeat" not in shared_under_a

    # branch_b's child "shared" should also be fully expanded
    shared_under_b = subs[1]["sub_dependencies"][0]
    assert shared_under_b["callable_name"] == "shared"
    assert "cached_repeat" not in shared_under_b

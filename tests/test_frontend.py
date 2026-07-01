import errno
import os
import runpy
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Literal

import anyio
import pytest
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, WebSocket
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse, Response
from starlette.routing import BaseRoute, Match, NoMatchFound, Route


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def record_dependency(calls: list[str], name: str):
    def dependency() -> None:
        calls.append(name)

    return dependency


def test_frontend_exact_prefix_path_serves_index(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/app")

    assert response.status_code == 200
    assert response.text == "app"


def test_apirouter_frontend_with_router_prefix_and_frontend_subpath(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "asset.txt", "asset")
    router = APIRouter(prefix="/internal")
    router.frontend("/ui", directory=dist)
    app = FastAPI()
    app.include_router(router, prefix="/prefix")

    response = TestClient(app).get("/prefix/internal/ui/asset.txt")

    assert response.status_code == 200
    assert response.text == "asset"


def test_frontend_fallback_rejects_invalid_fallback(tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    app = FastAPI()

    with pytest.raises(AssertionError, match="fallback"):
        app.frontend("/", directory=dist, fallback="invalid")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_index_fallback_ignores_invalid_q_value(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings", headers={"accept": "text/html; q=wat"}
    )

    assert response.status_code == 200
    assert response.text == "app shell"


def test_frontend_static_files_lookup_errors(monkeypatch, tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/", directory=dist)
    frontend_routes = app.router._frontend_routes
    assert frontend_routes is not None
    static_files = frontend_routes.routes[0].app

    def raise_permission_error(path: str):
        raise PermissionError

    monkeypatch.setattr(static_files, "lookup_path", raise_permission_error)
    response = TestClient(app).get("/asset.txt")
    assert response.status_code == 401

    def raise_value_error(path: str):
        raise ValueError

    monkeypatch.setattr(static_files, "lookup_path", raise_value_error)
    response = TestClient(app).get("/asset.txt")
    assert response.status_code == 404

    def raise_name_too_long(path: str):
        raise OSError(errno.ENAMETOOLONG, "name too long")

    monkeypatch.setattr(static_files, "lookup_path", raise_name_too_long)
    response = TestClient(app).get("/asset.txt")
    assert response.status_code == 404

    def raise_os_error(path: str):
        raise OSError(5, "other")

    monkeypatch.setattr(static_files, "lookup_path", raise_os_error)
    with pytest.raises(OSError):
        TestClient(app).get("/asset.txt")


def test_frontend_route_group_helpers(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/app", directory=dist)
    route_group = app.router._frontend_routes
    assert route_group is not None

    match, child_scope = route_group.matches({"type": "websocket", "path": "/"})
    assert match == Match.NONE
    assert child_scope == {}

    match, child_scope = route_group.matches_with_prefix(
        {"type": "http", "path": "/prefix/app", "method": "GET"},
        "/prefix",
    )
    assert match == Match.FULL
    assert child_scope["fastapi"]["frontend_path"] == ""

    match, child_scope = route_group.routes[0].matches(
        {"type": "http", "path": "/app", "method": "GET"}
    )
    assert match == Match.FULL
    assert child_scope["fastapi"]["frontend_path"] == ""

    with pytest.raises(StarletteHTTPException) as exc_info:
        anyio.run(
            route_group.handle,
            {"type": "http", "path": "/missing", "method": "GET"},
            None,
            None,
        )
    assert exc_info.value.status_code == 404

    with pytest.raises(NoMatchFound):
        route_group.url_path_for("frontend")
    with pytest.raises(NoMatchFound):
        route_group.routes[0].url_path_for("frontend")


def test_included_low_priority_routes_cache_is_reused():
    async def low_priority_endpoint(request: Request):
        return PlainTextResponse("low")

    router = APIRouter()
    router._low_priority_routes.append(Route("/low", low_priority_endpoint))
    router._mark_routes_changed()
    app = FastAPI()
    app.include_router(router, prefix="/prefix")
    included_router = next(
        route
        for route in app.router.routes
        if hasattr(route, "effective_low_priority_routes")
    )

    first = included_router.effective_low_priority_routes()  # ty: ignore[call-non-callable]
    second = included_router.effective_low_priority_routes()  # ty: ignore[call-non-callable]
    response = TestClient(app).get("/prefix/low")

    assert first is second
    assert response.status_code == 200
    assert response.text == "low"


def test_low_priority_api_route_handles_with_context():
    app = FastAPI()

    async def endpoint(request: Request) -> Response:
        return PlainTextResponse(request.scope["path_params"]["item_id"])

    route = app.router.route_class("/low/{item_id}", endpoint=endpoint, methods=["GET"])
    app.router._low_priority_routes.append(route)
    app.router._mark_routes_changed()

    response = TestClient(app).get("/low/abc")

    assert response.status_code == 200
    assert response.text == "abc"


def test_included_low_priority_api_route_handles_with_context():
    router = APIRouter()

    async def endpoint(request: Request) -> Response:
        return PlainTextResponse(request.scope["path_params"]["item_id"])

    route = router.route_class("/low/{item_id}", endpoint=endpoint, methods=["GET"])
    router._low_priority_routes.append(route)
    router._mark_routes_changed()
    app = FastAPI()
    app.include_router(router, prefix="/prefix")

    response = TestClient(app).get("/prefix/low/abc")

    assert response.status_code == 200
    assert response.text == "abc"


def test_normal_route_partial_match_returns_before_frontend(tmp_path: Path):
    class PartialRoute(BaseRoute):
        def matches(self, scope):
            return Match.PARTIAL, {}

        async def handle(self, scope, receive, send):
            response = PlainTextResponse("partial", status_code=405)
            await response(scope, receive, send)

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "frontend")
    app = FastAPI()
    app.router.routes.append(PartialRoute())
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/anything")

    assert response.status_code == 405
    assert response.text == "partial"


def test_normal_route_partial_match_wins_before_frontend(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "api", "frontend")
    app = FastAPI()

    @app.get("/api")
    def read_api():
        return {"source": "api"}

    app.frontend("/", directory=dist)

    client = TestClient(app)

    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"source": "api"}

    response = client.post("/api")
    assert response.status_code == 405


def test_basic_file_serving(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "assets" / "app.js", "console.log('ok')")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/assets/app.js")

    assert response.status_code == 200
    assert response.text == "console.log('ok')"
    assert "etag" in response.headers
    assert "last-modified" in response.headers


def test_app_frontend_dependencies_protect_root_asset_and_fallback(tmp_path: Path):
    calls: list[str] = []

    def require_cookie(request: Request) -> None:
        calls.append(request.url.path)
        if request.cookies.get("session") != "ok":
            raise HTTPException(status_code=401)

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    write_file(dist / "assets" / "app.js", "console.log('ok')")
    app = FastAPI(dependencies=[Depends(require_cookie)])
    app.frontend("/", directory=dist, fallback="index.html")
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 401

    response = client.get("/", headers={"cookie": "session=ok"})
    assert response.status_code == 200
    assert response.text == "app"

    response = client.get("/assets/app.js", headers={"cookie": "session=ok"})
    assert response.status_code == 200
    assert response.text == "console.log('ok')"

    response = client.get(
        "/dashboard",
        headers={"accept": "text/html", "cookie": "session=ok"},
    )
    assert response.status_code == 200
    assert response.text == "app"
    assert calls == ["/", "/", "/assets/app.js", "/dashboard"]


def test_apirouter_frontend_dependencies_protect_prefixed_frontend(tmp_path: Path):
    def require_cookie(request: Request) -> None:
        if request.cookies.get("session") != "ok":
            raise HTTPException(status_code=401)

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    write_file(dist / "assets" / "app.js", "console.log('ok')")
    router = APIRouter(dependencies=[Depends(require_cookie)])
    router.frontend("/", directory=dist, fallback="index.html")
    app = FastAPI()
    app.include_router(router, prefix="/app")
    client = TestClient(app)

    response = client.get("/app/")
    assert response.status_code == 401

    response = client.get("/app/", headers={"cookie": "session=ok"})
    assert response.status_code == 200
    assert response.text == "app"

    response = client.get("/app/assets/app.js", headers={"cookie": "session=ok"})
    assert response.status_code == 200
    assert response.text == "console.log('ok')"

    response = client.get(
        "/app/dashboard",
        headers={"accept": "text/html", "cookie": "session=ok"},
    )
    assert response.status_code == 200
    assert response.text == "app"


def test_included_frontend_does_not_block_url_path_for(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    frontend_router = APIRouter()
    frontend_router.frontend("/", directory=dist)
    api_router = APIRouter()

    @api_router.get("/api", name="read_api")
    def read_api():
        return {"ok": True}

    app = FastAPI()
    app.include_router(frontend_router, prefix="/app")
    app.include_router(api_router)
    included_frontend = next(
        route
        for route in app.router.routes
        if hasattr(route, "effective_low_priority_routes")
    )

    with pytest.raises(NoMatchFound):
        included_frontend.url_path_for("missing")
    assert app.url_path_for("read_api") == "/api"
    response = TestClient(app).get("/api")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_include_router_frontend_dependencies_apply_in_nested_order(tmp_path: Path):
    calls: list[str] = []

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    child = APIRouter(dependencies=[Depends(record_dependency(calls, "child"))])
    child.frontend("/ui", directory=dist)
    parent = APIRouter(dependencies=[Depends(record_dependency(calls, "parent"))])
    parent.include_router(
        child,
        prefix="/child",
        dependencies=[Depends(record_dependency(calls, "parent-include"))],
    )
    app = FastAPI(dependencies=[Depends(record_dependency(calls, "app"))])
    app.include_router(
        parent,
        prefix="/parent",
        dependencies=[Depends(record_dependency(calls, "app-include"))],
    )

    response = TestClient(app).get("/parent/child/ui/")

    assert response.status_code == 200
    assert response.text == "app"
    assert calls == ["app", "app-include", "parent", "parent-include", "child"]


def test_frontend_dependency_overrides_apply(tmp_path: Path):
    calls: list[str] = []

    def require_cookie() -> None:
        raise HTTPException(status_code=401)  # pragma: no cover

    def allow_cookie() -> None:
        calls.append("override")

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI(dependencies=[Depends(require_cookie)])
    app.dependency_overrides[require_cookie] = allow_cookie
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert response.text == "app"
    assert calls == ["override"]


def test_frontend_dependencies_do_not_run_when_api_route_wins(tmp_path: Path):
    calls: list[str] = []

    def frontend_dependency() -> None:
        calls.append("frontend")  # pragma: no cover

    dist = tmp_path / "dist"
    write_file(dist / "api", "frontend")
    router = APIRouter(dependencies=[Depends(frontend_dependency)])
    router.frontend("/", directory=dist)
    app = FastAPI()

    @app.get("/api")
    def read_api():
        return {"source": "api"}

    app.include_router(router)

    response = TestClient(app).get("/api")

    assert response.status_code == 200
    assert response.json() == {"source": "api"}
    assert calls == []


def test_only_selected_frontend_mount_dependencies_run(tmp_path: Path):
    calls: list[str] = []

    site = tmp_path / "site"
    admin = tmp_path / "admin"
    write_file(site / "index.html", "site")
    write_file(admin / "index.html", "admin")
    site_router = APIRouter()
    site_router.frontend("/", directory=site)
    admin_router = APIRouter()
    admin_router.frontend("/", directory=admin)
    app = FastAPI()
    app.include_router(
        site_router, dependencies=[Depends(record_dependency(calls, "site"))]
    )
    app.include_router(
        admin_router,
        prefix="/admin",
        dependencies=[Depends(record_dependency(calls, "admin"))],
    )

    response = TestClient(app).get("/admin/")

    assert response.status_code == 200
    assert response.text == "admin"
    assert calls == ["admin"]


def test_app_middleware_still_runs_for_frontend_dependencies(tmp_path: Path):
    calls: list[str] = []

    def frontend_dependency() -> None:
        calls.append("dependency")

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI(dependencies=[Depends(frontend_dependency)])

    @app.middleware("http")
    async def record_middleware(request: Request, call_next):
        calls.append("middleware-before")
        response = await call_next(request)
        calls.append("middleware-after")
        return response

    app.frontend("/", directory=dist)

    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert response.text == "app"
    assert calls == ["middleware-before", "dependency", "middleware-after"]


def test_frontend_dependency_validation_errors_return_422(tmp_path: Path):
    def require_token(token: str) -> None:
        pass  # pragma: no cover

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI(dependencies=[Depends(require_token)])
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "token"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


@pytest.mark.anyio
async def test_frontend_dependency_restores_existing_dependency_stacks(
    tmp_path: Path,
):
    def frontend_dependency() -> None:
        pass

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI(dependencies=[Depends(frontend_dependency)])
    app.frontend("/", directory=dist)
    assert app.router._frontend_routes is not None
    inner_stack = AsyncExitStack()
    function_stack = AsyncExitStack()
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "root_path": "",
        "query_string": b"",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "fastapi_inner_astack": inner_stack,
        "fastapi_function_astack": function_stack,
    }
    messages = []

    async def receive():
        return {  # pragma: no cover
            "type": "http.request",
            "body": b"",
            "more_body": False,
        }

    async def send(message):
        messages.append(message)

    async with inner_stack, function_stack:
        await app.router._frontend_routes.handle(scope, receive, send)

    assert scope["fastapi_inner_astack"] is inner_stack
    assert scope["fastapi_function_astack"] is function_stack
    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 200


def test_non_frontend_low_priority_route_keeps_order_before_frontend(
    tmp_path: Path,
):
    async def low_priority_endpoint(request: Request):
        return PlainTextResponse("low")

    dist = tmp_path / "dist"
    write_file(dist / "index.html", "frontend")
    app = FastAPI()
    app.router._low_priority_routes.append(Route("/admin", low_priority_endpoint))
    app.router._mark_routes_changed()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/admin")

    assert response.status_code == 200
    assert response.text == "low"


def test_existing_api_route_wins_over_frontend(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "api" / "users", "frontend")
    app = FastAPI()

    @app.get("/api/users")
    def read_users():
        return {"source": "api"}

    app.frontend("/", directory=dist)

    response = TestClient(app).get("/api/users")

    assert response.status_code == 200
    assert response.json() == {"source": "api"}


def test_api_route_404_is_not_replaced_by_frontend_fallback(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "frontend")
    app = FastAPI()

    @app.get("/api/users")
    def read_users():
        raise HTTPException(status_code=404, detail="api missing")

    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get("/api/users", headers={"accept": "text/html"})

    assert response.status_code == 404
    assert response.json() == {"detail": "api missing"}


def test_index_fallback_for_navigation_request(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings", headers={"accept": "text/html"}
    )

    assert response.status_code == 200
    assert response.text == "app shell"


def test_index_fallback_parses_accept_parameters(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings", headers={"accept": "text/html; q=0.8"}
    )

    assert response.status_code == 200
    assert response.text == "app shell"


def test_index_fallback_ignores_q_zero_accept(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings", headers={"accept": "text/html; q=0.0"}
    )

    assert response.status_code == 404


def test_index_fallback_respects_explicit_html_rejection_with_wildcard(
    tmp_path: Path,
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings",
        headers={"accept": "text/html; q=0, */*; q=1"},
    )

    assert response.status_code == 404


def test_index_fallback_respects_explicit_xhtml_rejection_with_wildcard(
    tmp_path: Path,
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(
        "/dashboard/settings",
        headers={"accept": "application/xhtml+xml; q=0, */*; q=1"},
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ("path", "accept"),
    [
        ("/assets/missing.js", "*/*"),
        ("/assets/missing.css", "text/css"),
        ("/assets/missing.png", "image/png"),
        ("/api/missing", "application/json"),
        ("/users/jane.doe", "text/html"),
    ],
)
def test_index_fallback_does_not_handle_asset_like_or_non_html_requests(
    tmp_path: Path, path: str, accept: str
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).get(path, headers={"accept": accept})

    assert response.status_code == 404
    assert response.text != "app shell"


def test_404_fallback_handles_missing_assets(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "404.html", "missing")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="404.html")

    response = TestClient(app).get("/assets/missing.js")

    assert response.status_code == 404
    assert response.text == "missing"


def test_auto_fallback_prefers_404_over_index(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    write_file(dist / "404.html", "missing")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/dashboard", headers={"accept": "text/html"})

    assert response.status_code == 404
    assert response.text == "missing"


def test_auto_fallback_uses_index_when_404_is_missing(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/dashboard", headers={"accept": "text/html"})

    assert response.status_code == 200
    assert response.text == "app shell"


def test_auto_fallback_returns_normal_404_without_fallback_files(tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/dashboard", headers={"accept": "text/html"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_no_fallback_returns_normal_404(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback=None)

    response = TestClient(app).get("/dashboard", headers={"accept": "text/html"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_directory_index_and_redirect(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "about" / "index.html", "about")
    app = FastAPI()
    app.frontend("/", directory=dist)
    client = TestClient(app)

    redirect = client.get("/about", follow_redirects=False)
    response = client.get("/about/")

    assert redirect.status_code == 307
    assert redirect.headers["location"] == "http://testserver/about/"
    assert response.status_code == 200
    assert response.text == "about"


def test_path_validation_and_trailing_slash_normalization(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "asset.txt", "ok")
    app = FastAPI()

    with pytest.raises(AssertionError):
        app.frontend("", directory=dist)
    with pytest.raises(AssertionError):
        app.frontend("app", directory=dist)

    app.frontend("/app/", directory=dist)
    response = TestClient(app).get("/app/asset.txt")

    assert response.status_code == 200
    assert response.text == "ok"


def test_frontend_path_matching_uses_segment_boundaries(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/app", directory=dist, fallback="index.html")

    response = TestClient(app).get("/application", headers={"accept": "text/html"})

    assert response.status_code == 404


def test_multiple_frontends_use_longest_matching_prefix(tmp_path: Path):
    site = tmp_path / "site"
    admin = tmp_path / "admin"
    write_file(site / "index.html", "site")
    write_file(admin / "index.html", "admin")
    app = FastAPI()
    app.frontend("/", directory=site, fallback="index.html")
    app.frontend("/admin", directory=admin, fallback="index.html")

    response = TestClient(app).get("/admin/settings", headers={"accept": "text/html"})

    assert response.status_code == 200
    assert response.text == "admin"


def test_apirouter_frontend_uses_include_prefix(tmp_path: Path):
    dist = tmp_path / "admin"
    write_file(dist / "index.html", "admin")
    router = APIRouter()
    router.frontend("/", directory=dist, fallback="index.html")
    app = FastAPI()
    app.include_router(router, prefix="/admin")

    response = TestClient(app).get("/admin/settings", headers={"accept": "text/html"})

    assert response.status_code == 200
    assert response.text == "admin"


def test_global_priority_across_included_routers(tmp_path: Path):
    dist = tmp_path / "site"
    write_file(dist / "index.html", "site")
    site_router = APIRouter()
    site_router.frontend("/", directory=dist, fallback="index.html")
    api_router = APIRouter()

    @api_router.get("/api/users")
    def read_users():
        return {"source": "api"}

    app = FastAPI()
    app.include_router(site_router)
    app.include_router(api_router)

    response = TestClient(app).get("/api/users", headers={"accept": "text/html"})

    assert response.status_code == 200
    assert response.json() == {"source": "api"}


def test_nested_apirouter_frontend_uses_all_include_prefixes(tmp_path: Path):
    dist = tmp_path / "admin"
    write_file(dist / "index.html", "admin")
    child_router = APIRouter()
    child_router.frontend("/", directory=dist, fallback="index.html")
    parent_router = APIRouter()
    parent_router.include_router(child_router, prefix="/child")
    app = FastAPI()
    app.include_router(parent_router, prefix="/parent")

    response = TestClient(app).get(
        "/parent/child/settings", headers={"accept": "text/html"}
    )

    assert response.status_code == 200
    assert response.text == "admin"


def test_low_priority_cache_updates_after_route_added_to_included_router(
    tmp_path: Path,
):
    dist = tmp_path / "site"
    write_file(dist / "index.html", "site")
    router = APIRouter()
    router.frontend("/", directory=dist, fallback="index.html")
    app = FastAPI()
    app.include_router(router, prefix="/app")
    client = TestClient(app)

    frontend_response = client.get("/app/dashboard", headers={"accept": "text/html"})

    @router.get("/dashboard")
    def read_dashboard():
        return {"source": "api"}

    api_response = client.get("/app/dashboard", headers={"accept": "text/html"})

    assert frontend_response.status_code == 200
    assert frontend_response.text == "site"
    assert api_response.status_code == 200
    assert api_response.json() == {"source": "api"}


def test_normal_route_slash_redirect_wins_before_frontend_redirect(tmp_path: Path):
    dist = tmp_path / "site"
    write_file(dist / "api" / "index.html", "frontend")
    app = FastAPI()

    @app.get("/api/")
    def read_api():
        return {"source": "api"}

    app.frontend("/", directory=dist)

    response = TestClient(app).get("/api", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "http://testserver/api/"

    followed = TestClient(app).get("/api/")
    assert followed.status_code == 200
    assert followed.json() == {"source": "api"}


def test_frontend_respects_root_path(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "assets" / "app.js", "console.log('ok')")
    app = FastAPI()
    app.frontend("/app", directory=dist)

    response = TestClient(app, root_path="/proxy").get("/app/assets/app.js")

    assert response.status_code == 200
    assert response.text == "console.log('ok')"


def test_websocket_route_wins_over_frontend(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "ws", "frontend")
    app = FastAPI()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text("websocket")
        await websocket.close()

    app.frontend("/", directory=dist)

    with TestClient(app).websocket_connect("/ws") as websocket:
        data = websocket.receive_text()

    assert data == "websocket"


def test_head_requests_work(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "asset.txt", "ok")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).head("/asset.txt")

    assert response.status_code == 200
    assert response.text == ""
    assert response.headers["content-length"] == "2"


def test_head_fallback_request_works(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).head(
        "/dashboard/settings", headers={"accept": "text/html"}
    )

    assert response.status_code == 200
    assert response.text == ""
    assert response.headers["content-length"] == "9"


def test_unsupported_methods_return_405(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "asset.txt", "ok")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).post("/asset.txt")

    assert response.status_code == 405


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
def test_unsupported_methods_to_fallback_only_routes_return_404(
    tmp_path: Path, method: str
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).request(
        method, "/dashboard/settings", headers={"accept": "text/html"}
    )

    assert response.status_code == 404


def test_unsupported_methods_to_frontend_root_and_directory_index_return_405(
    tmp_path: Path,
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    write_file(dist / "about" / "index.html", "about")
    app = FastAPI()
    app.frontend("/", directory=dist)
    client = TestClient(app)

    root_response = client.post("/")
    directory_response = client.post("/about/")

    assert root_response.status_code == 405
    assert directory_response.status_code == 405


def test_unsupported_method_to_directory_without_index_returns_404(tmp_path: Path):
    dist = tmp_path / "dist"
    (dist / "empty").mkdir(parents=True)
    write_file(dist / "index.html", "app")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).post("/empty/")

    assert response.status_code == 404


def test_unsupported_methods_to_fallback_only_routes_ignore_accept(
    tmp_path: Path,
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app shell")
    app = FastAPI()
    app.frontend("/", directory=dist, fallback="index.html")

    response = TestClient(app).post(
        "/dashboard/settings", headers={"accept": "application/json"}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    ("fallback", "files"),
    [
        ("404.html", {"404.html": "missing"}),
        ("auto", {"index.html": "app shell"}),
        (None, {"index.html": "app shell"}),
    ],
)
def test_unsupported_methods_to_fallback_only_routes_return_404_for_fallback_modes(
    tmp_path: Path,
    fallback: Literal["auto", "index.html", "404.html"] | None,
    files: dict[str, str],
):
    dist = tmp_path / "dist"
    for file, content in files.items():
        write_file(dist / file, content)
    app = FastAPI()
    app.frontend("/", directory=dist, fallback=fallback)

    response = TestClient(app).post(
        "/dashboard/settings", headers={"accept": "text/html"}
    )

    assert response.status_code == 404


def test_apirouter_frontend_unsupported_method_to_fallback_only_route_returns_404(
    tmp_path: Path,
):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "admin")
    router = APIRouter()
    router.frontend("/", directory=dist, fallback="index.html")
    app = FastAPI()
    app.include_router(router, prefix="/admin")

    response = TestClient(app).post(
        "/admin/client-route", headers={"accept": "text/html"}
    )

    assert response.status_code == 404


def test_unsupported_method_uses_longest_matching_frontend_prefix(tmp_path: Path):
    site = tmp_path / "site"
    admin = tmp_path / "admin"
    write_file(site / "admin" / "client-route", "site asset")
    write_file(admin / "index.html", "admin")
    app = FastAPI()
    app.frontend("/", directory=site)
    app.frontend("/admin", directory=admin, fallback="index.html")

    response = TestClient(app).post(
        "/admin/client-route", headers={"accept": "text/html"}
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "path",
    [
        "/../secret.txt",
        "/%2e%2e/secret.txt",
        "/..%2fsecret.txt",
        "/%5c..%5csecret.txt",
        "/..%5csecret.txt",
    ],
)
def test_path_traversal_cannot_escape_directory(tmp_path: Path, path: str):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    write_file(tmp_path / "secret.txt", "secret")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get(path)

    assert response.status_code == 404
    assert response.text != "secret"


def test_symlink_outside_directory_is_not_served(tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("secret")
    link = dist / "secret.txt"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError):  # pragma: no cover
        pytest.skip("symlinks are not supported")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).get("/secret.txt")

    assert response.status_code == 404
    assert response.text != "secret"


def test_check_dir_true_fails_early_for_missing_directory(monkeypatch, tmp_path: Path):
    app = FastAPI()
    monkeypatch.chdir(tmp_path)

    with pytest.raises(RuntimeError, match="does not exist") as exc_info:
        app.frontend("/", directory="missing")

    message = str(exc_info.value)
    assert "'missing'" in message
    assert str(tmp_path / "missing") in message


def test_check_dir_false_allows_missing_directory_and_fails_on_request(tmp_path: Path):
    app = FastAPI()
    app.frontend("/", directory=tmp_path / "missing", check_dir=False)

    with pytest.raises(RuntimeError, match="does not exist"):
        TestClient(app).get("/asset.txt")


def test_explicit_fallback_files_fail_clearly_when_missing(monkeypatch, tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    monkeypatch.chdir(tmp_path)
    app = FastAPI()

    with pytest.raises(RuntimeError, match="index.html") as exc_info:
        app.frontend("/", directory="dist", fallback="index.html")

    message = str(exc_info.value)
    assert "directory 'dist'" in message
    assert str(dist) in message

    app = FastAPI()
    app.frontend("/", directory="dist", fallback="404.html", check_dir=False)

    with pytest.raises(RuntimeError, match="404.html") as exc_info:
        TestClient(app).get("/missing.js")

    message = str(exc_info.value)
    assert "directory 'dist'" in message
    assert str(dist) in message


def test_frontend_routes_are_not_in_openapi(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "index.html", "app")
    app = FastAPI()

    @app.get("/api")
    def read_api():
        return {"ok": True}

    app.frontend("/", directory=dist, fallback="index.html")

    schema = TestClient(app).get("/openapi.json").json()

    assert set(schema["paths"]) == {"/api"}

    response = TestClient(app).get("/api")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


@pytest.mark.parametrize(
    ("example", "files", "path", "status_code", "body"),
    [
        (
            "tutorial001_py310.py",
            {"asset.txt": "asset"},
            "/asset.txt",
            200,
            "asset",
        ),
        (
            "tutorial002_py310.py",
            {"index.html": "index"},
            "/dashboard",
            200,
            "index",
        ),
        (
            "tutorial003_py310.py",
            {"404.html": "missing"},
            "/missing",
            404,
            "missing",
        ),
        (
            "tutorial004_py310.py",
            {"index.html": "index"},
            "/app/dashboard",
            200,
            "index",
        ),
        (
            "tutorial005_py310.py",
            {"index.html": "index"},
            "/dashboard",
            404,
            '{"detail":"Not Found"}',
        ),
        (
            "tutorial006_py310.py",
            {"asset.txt": "asset"},
            "/asset.txt",
            200,
            "asset",
        ),
    ],
)
def test_docs_frontend_examples(
    tmp_path: Path,
    monkeypatch,
    example: str,
    files: dict[str, str],
    path: str,
    status_code: int,
    body: str,
):
    dist = tmp_path / "dist"
    for file, content in files.items():
        write_file(dist / file, content)
    monkeypatch.chdir(tmp_path)

    namespace = runpy.run_path(
        str(Path(__file__).parents[1] / "docs_src" / "frontend" / example)
    )

    app = namespace["app"]
    assert isinstance(app, FastAPI)
    response = TestClient(app).get(path, headers={"accept": "text/html"})
    assert response.status_code == status_code
    assert response.text == body


def test_low_priority_routes_can_store_non_frontend_routes():
    async def low_priority_endpoint(request):
        return PlainTextResponse("low")

    app = FastAPI()
    app.router._low_priority_routes.append(Route("/low", low_priority_endpoint))
    app.router._mark_routes_changed()

    response = TestClient(app).get("/low")

    assert response.status_code == 200
    assert response.text == "low"


def test_included_low_priority_routes_can_store_non_frontend_routes():
    async def low_priority_endpoint(request):
        return PlainTextResponse("low")

    router = APIRouter()
    router._low_priority_routes.append(Route("/low", low_priority_endpoint))
    router._mark_routes_changed()
    app = FastAPI()
    app.include_router(router, prefix="/prefix")

    response = TestClient(app).get("/prefix/low")

    assert response.status_code == 200
    assert response.text == "low"

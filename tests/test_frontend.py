import os
import runpy
from pathlib import Path

import pytest
from fastapi import APIRouter, FastAPI, HTTPException, WebSocket
from fastapi.testclient import TestClient
from starlette.responses import PlainTextResponse
from starlette.routing import Route


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


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


def test_unsupported_methods_return_405(tmp_path: Path):
    dist = tmp_path / "dist"
    write_file(dist / "asset.txt", "ok")
    app = FastAPI()
    app.frontend("/", directory=dist)

    response = TestClient(app).post("/asset.txt")

    assert response.status_code == 405


@pytest.mark.parametrize(
    "path",
    ["/../secret.txt", "/%2e%2e/secret.txt", "/..%2fsecret.txt"],
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


def test_check_dir_true_fails_early_for_missing_directory(tmp_path: Path):
    app = FastAPI()

    with pytest.raises(RuntimeError, match="does not exist"):
        app.frontend("/", directory=tmp_path / "missing")


def test_check_dir_false_allows_missing_directory_and_fails_on_request(tmp_path: Path):
    app = FastAPI()
    app.frontend("/", directory=tmp_path / "missing", check_dir=False)

    with pytest.raises(RuntimeError, match="does not exist"):
        TestClient(app).get("/asset.txt")


def test_explicit_fallback_files_fail_clearly_when_missing(tmp_path: Path):
    dist = tmp_path / "dist"
    dist.mkdir()
    app = FastAPI()

    with pytest.raises(RuntimeError, match="index.html"):
        app.frontend("/", directory=dist, fallback="index.html")

    app = FastAPI()
    app.frontend("/", directory=dist, fallback="404.html", check_dir=False)

    with pytest.raises(RuntimeError, match="404.html"):
        TestClient(app).get("/missing.js")


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

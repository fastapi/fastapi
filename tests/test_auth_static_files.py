import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import AuthStaticFiles
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse, Response


@pytest.fixture(scope="module")
def static_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("static")
    (d / "public.txt").write_text("public content")
    (d / "secret.txt").write_text("secret content")
    return d


async def verify_token(request: Request) -> None:
    """Simple token-based auth for testing."""
    token = request.headers.get("Authorization")
    if token != "Bearer valid-token":
        raise HTTPException(status_code=401, detail="Not authenticated")


async def _allow_all(request: Request) -> None:
    """Auth function that allows all requests."""
    pass


@pytest.fixture(scope="module")
def app(static_dir):
    app = FastAPI()

    # Public static files (no auth)
    app.mount(
        "/public",
        AuthStaticFiles(
            directory=str(static_dir),
            auth=_allow_all,
        ),
        name="public",
    )

    # Private static files (requires auth)
    app.mount(
        "/private",
        AuthStaticFiles(
            directory=str(static_dir),
            auth=verify_token,
        ),
        name="private",
    )

    return app


@pytest.fixture(scope="module")
def client(app):
    with TestClient(app) as c:
        yield c


def test_private_file_without_auth(client: TestClient):
    """Requesting a private file without auth should return 401."""
    response = client.get("/private/secret.txt")
    assert response.status_code == 401
    assert response.text == "Not authenticated"


def test_private_file_with_wrong_token(client: TestClient):
    """Requesting a private file with wrong token should return 401."""
    response = client.get(
        "/private/secret.txt",
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401
    assert response.text == "Not authenticated"


def test_private_file_with_valid_token(client: TestClient):
    """Requesting a private file with valid token should return the file."""
    response = client.get(
        "/private/secret.txt",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 200
    assert response.text == "secret content"


def test_private_file_not_found_with_valid_token(client: TestClient):
    """Requesting a non-existent private file with valid auth should return 404."""
    response = client.get(
        "/private/nonexistent.txt",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 404


def test_public_files_accessible(client: TestClient):
    """Public mount with allow-all auth should serve files without auth."""
    response = client.get("/public/public.txt")
    assert response.status_code == 200
    assert response.text == "public content"


def test_auth_headers_forwarded(static_dir):
    """Auth errors with custom headers should forward them in the response."""

    async def auth_with_headers(request: Request) -> None:
        raise HTTPException(
            status_code=401,
            detail="Login required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    app = FastAPI()
    app.mount(
        "/protected",
        AuthStaticFiles(directory=str(static_dir), auth=auth_with_headers),
        name="protected",
    )

    with TestClient(app) as client:
        response = client.get("/protected/public.txt")
        assert response.status_code == 401
        assert response.headers["WWW-Authenticate"] == "Bearer"
        assert response.text == "Login required"


def test_cookie_based_auth(static_dir):
    """AuthStaticFiles should work with cookie-based authentication."""

    async def verify_cookie(request: Request) -> None:
        session = request.cookies.get("session_id")
        if session != "valid-session":
            raise HTTPException(status_code=403, detail="Forbidden")

    app = FastAPI()
    app.mount(
        "/dashboard",
        AuthStaticFiles(directory=str(static_dir), auth=verify_cookie),
        name="dashboard",
    )

    with TestClient(app) as client:
        # Without cookie
        response = client.get("/dashboard/public.txt")
        assert response.status_code == 403

        # With valid cookie
        client.cookies.set("session_id", "valid-session")
        response = client.get("/dashboard/public.txt")
        assert response.status_code == 200
        assert response.text == "public content"


def test_custom_on_error_redirect(static_dir):
    """on_error can redirect to a login page."""

    async def deny_all(request: Request) -> None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    async def redirect_to_login(request: Request, exc: HTTPException) -> Response:
        return RedirectResponse(url="/login", status_code=302)

    app = FastAPI()
    app.mount(
        "/protected",
        AuthStaticFiles(
            directory=str(static_dir),
            auth=deny_all,
            on_error=redirect_to_login,
        ),
        name="protected",
    )

    with TestClient(app, follow_redirects=False) as client:
        response = client.get("/protected/public.txt")
        assert response.status_code == 302
        assert response.headers["location"] == "/login"


def test_sync_auth_callable(static_dir):
    """A sync auth callable should be supported via run_in_threadpool."""

    def sync_verify(request: Request) -> None:
        token = request.headers.get("X-Token")
        if token != "valid":
            raise HTTPException(status_code=401, detail="Bad token")

    app = FastAPI()
    app.mount(
        "/sync",
        AuthStaticFiles(directory=str(static_dir), auth=sync_verify),
        name="sync",
    )

    with TestClient(app) as client:
        response = client.get("/sync/public.txt")
        assert response.status_code == 401

        response = client.get("/sync/public.txt", headers={"X-Token": "valid"})
        assert response.status_code == 200
        assert response.text == "public content"


def test_starlette_httpexception_caught(static_dir):
    """Starlette's HTTPException (used by FastAPI security modules) should be caught."""
    from starlette.exceptions import HTTPException as StarletteHTTPException

    async def deny_with_starlette(request: Request) -> None:
        raise StarletteHTTPException(status_code=401, detail="Starlette error")

    app = FastAPI()
    app.mount(
        "/starlette",
        AuthStaticFiles(directory=str(static_dir), auth=deny_with_starlette),
        name="starlette",
    )

    with TestClient(app) as client:
        response = client.get("/starlette/public.txt")
        assert response.status_code == 401
        assert response.text == "Starlette error"


def test_custom_on_error_html(static_dir):
    """on_error can return a custom HTML error page."""

    async def deny_all(request: Request) -> None:
        raise HTTPException(status_code=403, detail="Forbidden")

    async def html_error(request: Request, exc: HTTPException) -> Response:
        return HTMLResponse(
            f"<h1>{exc.status_code} {exc.detail}</h1>",
            status_code=exc.status_code,
        )

    app = FastAPI()
    app.mount(
        "/protected",
        AuthStaticFiles(
            directory=str(static_dir),
            auth=deny_all,
            on_error=html_error,
        ),
        name="protected",
    )

    with TestClient(app) as client:
        response = client.get("/protected/public.txt")
        assert response.status_code == 403
        assert "<h1>403 Forbidden</h1>" in response.text

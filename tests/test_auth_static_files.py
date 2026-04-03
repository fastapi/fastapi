import os
from pathlib import Path

import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import AuthStaticFiles
from fastapi.testclient import TestClient


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


async def _allow_all(request: Request) -> None:
    """Auth function that allows all requests."""
    pass


@pytest.fixture(scope="module")
def client(app):
    with TestClient(app) as c:
        yield c


def test_private_file_without_auth(client: TestClient):
    """Requesting a private file without auth should return 401."""
    response = client.get("/private/secret.txt")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_private_file_with_wrong_token(client: TestClient):
    """Requesting a private file with wrong token should return 401."""
    response = client.get(
        "/private/secret.txt",
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


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
        assert response.json() == {"detail": "Login required"}


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

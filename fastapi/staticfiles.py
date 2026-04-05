from collections.abc import Awaitable, Callable
from typing import Any

from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.staticfiles import StaticFiles as StaticFiles  # noqa
from starlette.types import Receive, Scope, Send


class AuthStaticFiles(StaticFiles):
    """
    A static files handler that requires authentication before serving files.

    This solves the problem where `app.mount("/static", StaticFiles(...))` serves
    files without any authentication, making it impossible to protect private files.

    `AuthStaticFiles` accepts an `auth` callable that receives a `Request` and
    should either return successfully (authenticated) or raise an `HTTPException`
    (not authenticated).

    ## Usage

    ```python
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.staticfiles import AuthStaticFiles

    app = FastAPI()


    async def verify_token(request: Request) -> None:
        token = request.headers.get("Authorization")
        if token != "Bearer mysecrettoken":
            raise HTTPException(status_code=401, detail="Unauthorized")


    app.mount(
        "/private",
        AuthStaticFiles(directory="private_files", auth=verify_token),
        name="private",
    )
    ```

    ## Parameters

    * `auth`: An async callable that takes a `Request` object and performs
      authentication. It should raise an `HTTPException` if authentication
      fails, or return `None` if authentication succeeds.
    * `on_error`: An optional callable that takes a `Request` and an
      `HTTPException` and returns a `Response`. Use this to customize
      error responses (e.g., redirect to login, return HTML instead of
      plain text). If not provided, a plain text error response is returned.
    * `directory`: The directory to serve files from.
    * `packages`: A list of Python packages to serve files from.
    * `html`: If `True`, serves `index.html` files for directories.
    * `check_dir`: If `True`, checks that the directory exists on startup.
    * `follow_symlink`: If `True`, follows symbolic links.

    ## Performance Note

    The `auth` callable runs on **every static file request** (CSS, JS,
    images, etc.). Prefer lightweight checks (header presence, JWT signature
    verification) over expensive operations (database lookups) to avoid
    slowing down page loads.

    Ref: https://github.com/fastapi/fastapi/issues/858
    """

    def __init__(
        self,
        *,
        directory: str | None = None,
        packages: list[str | tuple[str, str]] | None = None,
        html: bool = False,
        check_dir: bool = True,
        follow_symlink: bool = False,
        auth: Callable[[Request], Awaitable[Any]],
        on_error: Callable[[Request, Any], Awaitable[Response]] | None = None,
    ) -> None:
        super().__init__(
            directory=directory,
            packages=packages,
            html=html,
            check_dir=check_dir,
            follow_symlink=follow_symlink,
        )
        self.auth = auth
        self.on_error = on_error

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive)
            try:
                await self.auth(request)
            except Exception as exc:
                from fastapi.exceptions import HTTPException

                if isinstance(exc, HTTPException):
                    if self.on_error is not None:
                        response = await self.on_error(request, exc)
                    else:
                        response = PlainTextResponse(
                            str(exc.detail),
                            status_code=exc.status_code,
                            headers=getattr(exc, "headers", None),
                        )
                    await response(scope, receive, send)
                    return
                raise
        await super().__call__(scope, receive, send)

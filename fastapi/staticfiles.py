from collections.abc import Awaitable, Callable
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse
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
    * `directory`: The directory to serve files from.
    * `packages`: A list of Python packages to serve files from.
    * `html`: If `True`, serves `index.html` files for directories.
    * `check_dir`: If `True`, checks that the directory exists on startup.
    * `follow_symlink`: If `True`, follows symbolic links.

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
    ) -> None:
        super().__init__(
            directory=directory,
            packages=packages,
            html=html,
            check_dir=check_dir,
            follow_symlink=follow_symlink,
        )
        self.auth = auth

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive)
            try:
                await self.auth(request)
            except Exception as exc:
                from fastapi.exceptions import HTTPException

                if isinstance(exc, HTTPException):
                    response = JSONResponse(
                        {"detail": exc.detail},
                        status_code=exc.status_code,
                        headers=getattr(exc, "headers", None),
                    )
                    await response(scope, receive, send)
                    return
                raise
        await super().__call__(scope, receive, send)

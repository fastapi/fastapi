import typing

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


async def catch_exceptions_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    import pdb
    import sys

    try:
        return await call_next(request)
    except Exception as e:
        sys.last_traceback = e.__traceback__
        pdb.pm()
        raise


async def webpdb_catch_exceptions_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    """
    Requires web-pdb package.

    ```bash
    pip install web-pdb
    ```
    """
    import web_pdb  # type: ignore

    with web_pdb.catch_post_mortem():
        return await call_next(request)


class DebuggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to intercept exceptions and start a debugger in that stack frame.

    The default configured debugger is PDB since it comes packaged with Python.

    Additionally web UI can be added by add web-pdb a dep., or a custom callable
    be passed through the `start_debugger_func` middleware parameter to run
    a debugger of choice.

    Example:

    ```python
    # Add default (PDB) debugger
    impost os

    from fastapi import FastAPI
    from fastapi.middleware.debugger import DebuggerMiddleware

    app = FastAPI()

    if os.getenv("ENV") == "LOCAL": # Or something along those lines to check and only run in locally
        app.add_middleware(DebuggerMiddleware)
    ```

    ```python
    # Add web_PDB debugger
    impost os

    from fastapi import FastAPI
    from fastapi.middleware.debugger import DebuggerMiddleware, webpdb_catch_exceptions_middleware

    app = FastAPI()

    if os.getenv("ENV") == "LOCAL": # Or something along those lines to check and only run in locally
        app.add_middleware(DebuggerMiddleware, start_debugger_func=webpdb_catch_exceptions_middleware)
    ```

    Additional notes:
    A good practice would be to add rules to your linter or use a tool like Pre-commit to remove/ check
    for forgotten breakpoints left in prod. code.

    Also set `PYTHONBREAKPOINT=0` environment in your prod configs to prevent a python debugger running in
    prod.
    """

    def __init__(
        self,
        app: ASGIApp,
        start_debugger_func: typing.Optional[
            typing.Callable[
                [Request, RequestResponseEndpoint],
                typing.Coroutine[typing.Any, typing.Any, Response],
            ]
        ] = None,
    ) -> None:
        if start_debugger_func:
            self.start_debug = start_debugger_func
        else:
            self.start_debug = catch_exceptions_middleware
        super().__init__(app, dispatch=None)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        return await self.start_debug(request, call_next)

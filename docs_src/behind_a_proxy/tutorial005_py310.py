from fastapi import FastAPI, Request
from starlette.types import ASGIApp, Receive, Scope, Send


class ForwardedPrefixMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            scope_headers: list[tuple[bytes, bytes]] = scope.get("headers", [])
            headers = {
                k.decode("latin-1"): v.decode("latin-1") for k, v in scope_headers
            }
            prefix = headers.get("x-forwarded-prefix", "").rstrip("/")
            if prefix:
                scope["root_path"] = prefix
        await self.app(scope, receive, send)


app = FastAPI()
app.add_middleware(ForwardedPrefixMiddleware)


@app.get("/app")
def read_main(request: Request):
    return {
        "message": "Hello World",
        "path": request.scope.get("path"),
        "root_path": request.scope.get("root_path"),
    }

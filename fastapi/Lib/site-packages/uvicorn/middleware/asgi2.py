import typing

if typing.TYPE_CHECKING:
    from asgiref.typing import (
        ASGI2Application,
        ASGIReceiveCallable,
        ASGISendCallable,
        Scope,
    )


class ASGI2Middleware:
    def __init__(self, app: "ASGI2Application"):
        self.app = app

    async def __call__(
        self, scope: "Scope", receive: "ASGIReceiveCallable", send: "ASGISendCallable"
    ) -> None:
        instance = self.app(scope)
        await instance(receive, send)

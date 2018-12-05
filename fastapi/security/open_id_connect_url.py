from starlette.requests import Request

from .base import SecurityBase, Types

class OpenIdConnect(SecurityBase):
    type_ = Types.openIdConnect
    openIdConnectUrl: str

    async def __call__(self, request: Request):
        return request.headers.get("Authorization")

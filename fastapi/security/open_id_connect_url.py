from fastapi.openapi.models import OpenIdConnect as OpenIdConnectModel
from fastapi.security.base import SecurityBase
from starlette.requests import Request


class OpenIdConnect(SecurityBase):
    def __init__(self, *, openIdConnectUrl: str, scheme_name: str = None):
        self.model = OpenIdConnectModel(openIdConnectUrl=openIdConnectUrl)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")

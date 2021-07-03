from typing import Optional

from fastapi.openapi.models import OpenIdConnect as OpenIdConnectModel
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class OpenIdConnect(SecurityBase):
    def __init__(
        self,
        *,
        openIdConnectUrl: str,
        scheme_name: Optional[str] = None,
        auto_error: bool = True
    ):
        self.model = OpenIdConnectModel(openIdConnectUrl=openIdConnectUrl)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return authorization

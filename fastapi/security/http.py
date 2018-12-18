from starlette.requests import Request

from fastapi.openapi.models import (
    HTTPBase as HTTPBaseModel,
    HTTPBearer as HTTPBearerModel,
)
from fastapi.security.base import SecurityBase


class HTTPBase(SecurityBase):
    def __init__(self, *, scheme: str, scheme_name: str = None):
        self.model = HTTPBaseModel(scheme=scheme)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")


class HTTPBasic(HTTPBase):
    def __init__(self, *, scheme_name: str = None):
        self.model = HTTPBaseModel(scheme="basic")
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")


class HTTPBearer(HTTPBase):
    def __init__(self, *, bearerFormat: str = None, scheme_name: str = None):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")


class HTTPDigest(HTTPBase):
    def __init__(self, *, scheme_name: str = None):
        self.model = HTTPBaseModel(scheme="digest")
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")

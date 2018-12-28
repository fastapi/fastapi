from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class APIKeyBase(SecurityBase):
    pass


class APIKeyQuery(APIKeyBase):
    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(**{"in": APIKeyIn.query}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        api_key: str = request.query_params.get(self.model.name)
        if not api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return api_key


class APIKeyHeader(APIKeyBase):
    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(**{"in": APIKeyIn.header}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        api_key: str = request.headers.get(self.model.name)
        if not api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return api_key


class APIKeyCookie(APIKeyBase):
    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(**{"in": APIKeyIn.cookie}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        api_key: str = request.cookies.get(self.model.name)
        if not api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return api_key

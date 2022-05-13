from typing import Optional

from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class APIKeyBase(SecurityBase):
    @staticmethod
    def check_api_key(api_key: Optional[str], auto_error: bool) -> Optional[str]:
        if not api_key:
            if auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            return None
        return api_key


class APIKeyQuery(APIKeyBase):
    def __init__(
        self, *, name: str, scheme_name: Optional[str] = None, auto_error: bool = True
    ):
        self.model: APIKey = APIKey(**{"in": APIKeyIn.query}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        api_key: str = request.query_params.get(self.model.name)
        return self.check_api_key(api_key, self.auto_error)


class APIKeyHeader(APIKeyBase):
    def __init__(
        self, *, name: str, scheme_name: Optional[str] = None, auto_error: bool = True
    ):
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        api_key: str = request.headers.get(self.model.name)
        return self.check_api_key(api_key, self.auto_error)


class APIKeyCookie(APIKeyBase):
    def __init__(
        self, *, name: str, scheme_name: Optional[str] = None, auto_error: bool = True
    ):
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.cookies.get(self.model.name)
        return self.check_api_key(api_key, self.auto_error)

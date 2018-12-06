from starlette.requests import Request

from .base import SecurityBase
from fastapi.openapi.models import APIKeyIn, APIKey

class APIKeyBase(SecurityBase):
    pass

class APIKeyQuery(APIKeyBase):

    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(in_=APIKeyIn.query, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, requests: Request):
        return requests.query_params.get(self.model.name)


class APIKeyHeader(APIKeyBase):
    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(in_=APIKeyIn.header, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, requests: Request):
        return requests.headers.get(self.model.name)


class APIKeyCookie(APIKeyBase):
    def __init__(self, *, name: str, scheme_name: str = None):
        self.model = APIKey(in_=APIKeyIn.cookie, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, requests: Request):
        return requests.cookies.get(self.model.name)

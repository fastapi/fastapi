from enum import Enum

from pydantic import Schema

from starlette.requests import Request

from .base import SecurityBase, Types

class APIKeyIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


class APIKeyBase(SecurityBase):
    type_ = Schema(Types.apiKey, alias="type")
    in_: str = Schema(..., alias="in")
    name: str


class APIKeyQuery(APIKeyBase):
    in_ = Schema(APIKeyIn.query, alias="in")

    async def __call__(self, requests: Request):
        return requests.query_params.get(self.name)


class APIKeyHeader(APIKeyBase):
    in_ = Schema(APIKeyIn.header, alias="in")

    async def __call__(self, requests: Request):
        return requests.headers.get(self.name)


class APIKeyCookie(APIKeyBase):
    in_ = Schema(APIKeyIn.cookie, alias="in")

    async def __call__(self, requests: Request):
        return requests.cookies.get(self.name)

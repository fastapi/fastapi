from typing import Dict

from pydantic import BaseModel, Schema

from starlette.requests import Request
from .base import SecurityBase, Types

# __all__ = ["HTTPBase", "HTTPBasic", "HTTPBearer", "HTTPDigest"]


class OAuthFlow(BaseModel):
    refreshUrl: str = None
    scopes: Dict[str, str] = {}


class OAuthFlowImplicit(OAuthFlow):
    authorizationUrl: str


class OAuthFlowPassword(OAuthFlow):
    tokenUrl: str


class OAuthFlowClientCredentials(OAuthFlow):
    tokenUrl: str


class OAuthFlowAuthorizationCode(OAuthFlow):
    authorizationUrl: str
    tokenUrl: str


class OAuthFlows(BaseModel):
    implicit: OAuthFlowImplicit = None
    password: OAuthFlowPassword = None
    clientCredentials: OAuthFlowClientCredentials = None
    authorizationCode: OAuthFlowAuthorizationCode = None


class OAuth2(SecurityBase):
    type_ = Schema(Types.oauth2, alias="type")
    flows: OAuthFlows

    async def __call__(self, request: Request):
        return request.headers.get("Authorization")

from typing import List, Optional

from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.security.base import SecurityBase
from pydantic import BaseModel, Schema
from starlette.requests import Request


class OAuth2PasswordRequestData(BaseModel):
    grant_type: str = "password"
    username: str
    password: str
    scope: Optional[List[str]] = None
    # Client ID and secret might come from headers
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class OAuth2PasswordRequestForm(BaseModel):
    grant_type: str = Schema(..., regex="password")  # it must have the value "password"
    username: str
    password: str
    scope: str = ""
    # Client ID and secret might come from headers
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    def parse(self) -> OAuth2PasswordRequestData:
        return OAuth2PasswordRequestData(
            grant_type=self.grant_type,
            username=self.username,
            password=self.password,
            scope=self.scope.split(),
            client_id=self.client_id,
            client_secret=self.client_secret,
        )


class OAuth2(SecurityBase):
    def __init__(
        self, *, flows: OAuthFlowsModel = OAuthFlowsModel(), scheme_name: str = None
    ):
        self.model = OAuth2Model(flows=flows)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")

from starlette.requests import Request

from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.security.base import SecurityBase


class OAuth2(SecurityBase):
    def __init__(
        self, *, flows: OAuthFlowsModel = OAuthFlowsModel(), scheme_name: str = None
    ):
        self.model = OAuth2Model(flows=flows)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")

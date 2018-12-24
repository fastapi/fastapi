from typing import List, Optional

from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.params import Form
from fastapi.security.base import SecurityBase
from pydantic import BaseModel, Schema
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class OAuth2PasswordRequestData(BaseModel):
    grant_type: str = "password"
    username: str
    password: str
    scope: Optional[List[str]] = None
    # Client ID and secret might come from headers
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class OAuth2PasswordRequestForm:
    """
    This is a dependency class, use it like:

        @app.post("/login")
        def login(form_data: Oauth2PasswordRequestForm = Depends()):
            data = form_data.parse()
            print(data.username)
            print(data.password)
            for scope in data.scope:
                print(scope)
            if data.client_id:
                print(data.client_id)
            if data.client_secret:
                print(data.client_secret)
            return data

    
    It creates the following Form request parameters in your endpoint:

    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "password".
        Nevertheless, this model is permissive and allows not passing it. If you want to enforce it,
        use instead the OAuth2PasswordRequestFormStrict model.
    username: username string. The OAuth2 spec requires the exact field name "username".
    password: password string. The OAuth2 spec requires the exact field name "password".
    scope: Optional string. Several scopes (each one a string) separated by spaces. E.g.
        "items:read items:write users:read profile openid"
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    

    It has the method parse() that returns a model with all the same data and the scopes extracted as a list of strings.
    """

    def __init__(
        self,
        grant_type: str = Form(None, regex="password"),
        username: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret

    def parse(self) -> OAuth2PasswordRequestData:
        return OAuth2PasswordRequestData(
            grant_type=self.grant_type,
            username=self.username,
            password=self.password,
            scope=self.scope.split(),
            client_id=self.client_id,
            client_secret=self.client_secret,
        )


class OAuth2PasswordRequestFormStrict(OAuth2PasswordRequestForm):
    # The OAuth2 spec says it MUST have the value "password"
    grant_type: str = Schema(..., regex="password")


class OAuth2(SecurityBase):
    def __init__(
        self, *, flows: OAuthFlowsModel = OAuthFlowsModel(), scheme_name: str = None
    ):
        self.model = OAuth2Model(flows=flows)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        return request.headers.get("Authorization")


class OAuth2PasswordBearer(OAuth2):
    def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name)

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if not authorization or "Bearer " not in authorization:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        token = authorization.replace("Bearer ", "")
        return token

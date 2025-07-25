from typing import Annotated, Any, Dict, Optional

import httpx
from cachetools import TTLCache
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OpenIdConnect,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import Field
from pydantic_settings import BaseSettings
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class AccessTokenCredentials(HTTPAuthorizationCredentials):
    token: Dict[str, Any]


class AccessTokenValidator(HTTPBearer):
    """Generic HTTPBearer Validator that validates JWT tokens given the JWKS provided at jwks_url."""

    def __init__(
        self,
        *,
        jwks_url: str,
        audience: str,
        issuer: str,
        expire_seconds: int = 3600,
        roles_claim: str = "groups",
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(scheme_name=scheme_name, description=description)
        self.uri = jwks_url
        self.audience = audience
        self.issuer = issuer
        self.roles_claim = roles_claim
        self.keyset_cache: TTLCache[str, str] = TTLCache(16, expire_seconds)

    async def get_jwt_keyset(self) -> str:
        """Retrieves keyset when expired/not cached yet."""
        result: Optional[str] = self.keyset_cache.get(self.uri)
        if result is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.uri)
                result = self.keyset_cache[self.uri] = response.text
        return result

    async def __call__(
        self, request: Request, security_scopes: SecurityScopes
    ) -> AccessTokenCredentials:  # type: ignore
        """Validates the JWT Access Token. If security_scopes are given, they are validated against the roles_claim in the Access Token."""
        # 1. Unpack bearer token
        unverified_token = await super().__call__(request)
        if not unverified_token:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid Access Token")
        access_token = unverified_token.credentials
        try:
            # 2. Get keyset from authorization server so that we can validate the JWT Access Token
            keyset = await self.get_jwt_keyset()
            # 3. Perform validation
            verified_token = jwt.decode(
                token=access_token,
                key=keyset,
                audience=self.audience,
                issuer=self.issuer,
            )
        except JWTError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Unsupported authorization code",
            ) from None

        # 4. if security scopes are present, validate them
        if security_scopes and security_scopes.scopes:
            # 4.1 the roles_claim must be present in the access token
            scopes = verified_token.get(self.roles_claim)
            if scopes is None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Unsupported Access Token"
                )
            # 4.2 all required roles in the roles_claim must be present
            if not set(security_scopes.scopes).issubset(set(scopes)):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not Authorized"
                )

        return AccessTokenCredentials(
            scheme=self.scheme_name, credentials=access_token, token=verified_token
        )


class Settings(BaseSettings):
    """Settings wil be read from an .env file"""

    issuer: str = Field(default=...)
    audience: str = Field(default=...)
    client_id: str = Field(default=...)

    class Config:
        env_file = ".env"


settings = Settings()

# Standard OIDC URLs
oidc_url = f"{settings.issuer}/.well-known/openid-configuration"
jwks_url = f"{settings.issuer}/v1/keys"

openid_connect = OpenIdConnect(openIdConnectUrl=oidc_url)

swagger_ui_init_oauth = {
    "clientId": settings.client_id,
    "scopes": ["openid"],  # fill in additional scopes when necessary
    "appName": "Test Application",
    "usePkceWithAuthorizationCodeGrant": True,
}

# The openid_connect security scheme is given as a dependency so that you can authenticate using the swagger UI
app = FastAPI(
    swagger_ui_init_oauth=swagger_ui_init_oauth, dependencies=[Depends(openid_connect)]
)

# the tokenvalidator is used for all endpoints that need to be authorized
oauth2 = AccessTokenValidator(
    jwks_url=jwks_url, audience=settings.audience, issuer=settings.issuer
)


@app.get("/hello")
async def hello(
    token: Annotated[AccessTokenCredentials, Security(oauth2, scopes=["Foo"])],
) -> str:
    return "Hi!"

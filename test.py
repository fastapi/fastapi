from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseSettings


class Config(BaseSettings):
    oauth2_authorization_url: str
    oauth2_token_url: str


def get_config() -> Config:
    return Config()


def oauth2_scheme(config: Config = Depends(get_config)) -> OAuth2AuthorizationCodeBearer:
    return OAuth2AuthorizationCodeBearer(
        tokenUrl=config.oauth2_token_url,
        authorizationUrl=config.oauth2_authorization_url
    )


app = FastAPI()


@app.get("/private-route", dependencies=[Security(oauth2_scheme, scopes=["admin"])])
async def private_route():
    pass


import uvicorn
import os
from unittest.mock import patch

with patch.dict(os.environ, dict(OAUTH2_AUTHORIZATION_URL="http://test.com", OAUTH2_TOKEN_URL="http://test.com/token")):
    uvicorn.run(app)

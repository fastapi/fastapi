# Ref: https://github.com/fastapi/fastapi/issues/14454

from fastapi import APIRouter, Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from typing_extensions import Annotated

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="api/oauth/authorize",
    tokenUrl="/api/oauth/token",
    refreshUrl="/api/oauth/token",
    auto_error=False,
    scopes={"read": "Read access", "write": "Write access"},
)


async def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


AccessToken = Annotated[str, Depends(get_token)]


async def require_oauth_scopes(
    security_scopes: SecurityScopes, token: AccessToken
) -> None:
    pass


async def check_limit(token: AccessToken) -> None:
    pass


router = APIRouter(prefix="/v1", dependencies=[Depends(check_limit)])

channels_router = APIRouter(prefix="/channels", tags=["Channels"])


@channels_router.get(
    "/", dependencies=[Security(require_oauth_scopes, scopes=["read"])]
)
def read_items():
    return {"msg": "You have READ access"}


router.include_router(channels_router)

app.include_router(router)

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/v1/channels/": {
                    "get": {
                        "tags": ["Channels"],
                        "summary": "Read Items",
                        "operationId": "read_items_v1_channels__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [{"OAuth2AuthorizationCodeBearer": ["read"]}],
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "OAuth2AuthorizationCodeBearer": {
                        "type": "oauth2",
                        "flows": {
                            "authorizationCode": {
                                "refreshUrl": "/api/oauth/token",
                                "scopes": {
                                    "read": "Read access",
                                    "write": "Write access",
                                },
                                "authorizationUrl": "api/oauth/authorize",
                                "tokenUrl": "/api/oauth/token",
                            }
                        },
                    }
                }
            },
        }
    )

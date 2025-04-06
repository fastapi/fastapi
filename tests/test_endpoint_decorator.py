from functools import update_wrapper
from typing import Any, Callable

from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException


class EndpointWrapper(Callable[..., Any]):
    def __init__(self, endpoint: Callable[..., Any]):
        self.endpoint = endpoint
        self.protected = False
        update_wrapper(self, endpoint)

    async def __call__(self, *args, **kwargs):
        return await self.endpoint(*args, **kwargs)


def dummy_secruity_check(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if token.credentials != "fake-token":
        raise HTTPException(status_code=401, detail="Unauthorized")


def protect(endpoint: Callable[..., Any]):
    if not isinstance(endpoint, EndpointWrapper):
        endpoint = EndpointWrapper(endpoint)
    endpoint.protected = True
    return endpoint


class CustomAPIRoute(APIRoute):
    def __init__(
        self, path: str, endpoint: Callable[..., Any], dependencies, **kwargs
    ) -> None:
        if isinstance(endpoint, EndpointWrapper) and endpoint.protected:
            dependencies.append(Depends(dummy_secruity_check))
        super().__init__(path, endpoint, dependencies=dependencies, **kwargs)


app = FastAPI()

app.router.route_class = CustomAPIRoute


@app.get("/protected")
@protect
async def protected_route():
    return {"message": "This is a protected route"}


client = TestClient(app)


def test_protected_route():
    response = client.get("/protected")
    assert response.status_code == 403

    response = client.get("/protected", headers={"Authorization": "Bearer some-token"})
    assert response.status_code == 401

    response = client.get("/protected", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected route"}

from typing import List

from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


async def verify_scopes(required_scopes: SecurityScopes):
    return required_scopes.scopes


def no_scopes(_=Security(verify_scopes)):
    pass


app = FastAPI()


@app.get("/scopes", dependencies=[Depends(no_scopes)])
def get_scopes(
    verified_scopes: List[str] = Security(verify_scopes, scopes=["foo", "bar"]),
):
    return {"verified_scopes": verified_scopes}


def test_scopes_in_app_with_dependency():
    response = TestClient(app).get("/scopes")
    assert response.json() == {"verified_scopes": ["foo", "bar"]}

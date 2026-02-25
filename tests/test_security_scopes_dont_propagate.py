# Ref: https://github.com/tiangolo/fastapi/issues/5623

from typing import Annotated, Any

from fastapi import FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


async def security1(scopes: SecurityScopes):
    return scopes.scopes


async def security2(scopes: SecurityScopes):
    return scopes.scopes


async def dep3(
    dep1: Annotated[list[str], Security(security1, scopes=["scope1"])],
    dep2: Annotated[list[str], Security(security2, scopes=["scope2"])],
):
    return {"dep1": dep1, "dep2": dep2}


app = FastAPI()


@app.get("/scopes")
def get_scopes(
    dep3: Annotated[dict[str, Any], Security(dep3, scopes=["scope3"])],
):
    return dep3


client = TestClient(app)


def test_security_scopes_dont_propagate():
    response = client.get("/scopes")
    assert response.status_code == 200
    assert response.json() == {
        "dep1": ["scope3", "scope1"],
        "dep2": ["scope3", "scope2"],
    }

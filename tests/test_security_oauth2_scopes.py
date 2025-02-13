from fastapi import FastAPI, Security
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import SecurityScopes
from fastapi.testclient import TestClient

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


def get_security_scopes(security_scopes: SecurityScopes, token=Depends(oauth2_scheme)):
    return security_scopes.scopes


@app.get("/me")
async def read_single_scope(
    current_scope=Security(get_security_scopes, scopes="me"),
):
    return {"scopes": current_scope}


@app.get("/me-and-items")
async def read_single_scope(
    current_scope=Security(get_security_scopes, scopes=["me", "items"]),
):
    return {"scopes": current_scope}


client = TestClient(app)


def test_single_scope_string():
    response = client.get("/me", headers={"Authorization": "Bearer sometoken"})

    assert response.status_code == 200
    assert response.json() == {"scopes": ["me"]}


def test_list_scopes():
    response = client.get(
        "/me-and-items", headers={"Authorization": "Bearer sometoken"}
    )

    assert response.status_code == 200
    assert response.json() == {"scopes": ["me", "items"]}

from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

app = FastAPI()

custom_authorization_header = 'x-authorization'
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    auto_error=True,
    authorization_header=custom_authorization_header
)


@app.get("/items/")
async def read_items(token: Optional[str] = Security(oauth2_scheme)):
    if token is None:
        return {"msg": "Create an account first"}
    return {"token": token}


client = TestClient(app)


def test_security_oauth2_password_bearer_set_custom_authorization_header():
    expected_authorization_header = 'x-authorization'
    target = OAuth2PasswordBearer(
        tokenUrl="/token",
        auto_error=True,
        authorization_header=custom_authorization_header
    )
    assert target.authorization_header == expected_authorization_header


def test_security_oauth2_password_bearer_use_custom_authorization_header():
    response = client.get("/items", headers={custom_authorization_header: "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_security_oauth2_password_bearer_no_authorization_header():
    response = client.get("/items", headers={custom_authorization_header: None})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_security_oauth2_password_bearer_incorrect_authorization_header():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}

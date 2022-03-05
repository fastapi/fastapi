from fastapi import Depends, FastAPI, Security
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

custom_authorization_header = "x-authorization"
oid = OpenIdConnect(openIdConnectUrl="/openid", authorization_header=custom_authorization_header)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(oid)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


client = TestClient(app)


def test_security_openid_connect_set_custom_authorization_header():
    expected_authorization_header = 'x-authorization'
    target = OpenIdConnect(openIdConnectUrl="/openid", authorization_header=expected_authorization_header)
    assert target.authorization_header == expected_authorization_header


def test_security_openid_connect_use_custom_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: "Bearer footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "Bearer footokenbar"}


def test_security_openid_connect_no_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: None})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_security_openid_connect_incorrect_authorization_header():
    response = client.get("/users/me", headers={"Authorization": None})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}

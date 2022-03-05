from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

app = FastAPI()

custom_authorization_header = 'x-authorization'
security = HTTPBearer(authorization_header=custom_authorization_header)


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


def test_security_http_bearer_set_custom_authorization_header():
    expected_authorization_header = 'x-authorization'
    target = HTTPBearer(authorization_header=expected_authorization_header)
    assert target.authorization_header == expected_authorization_header


def test_security_http_bearer_use_custom_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: "Bearer foobar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"scheme": "Bearer", "credentials": "foobar"}


def test_security_http_bearer_no_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: None})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_security_http_bearer_incorrect_authorization_header():
    response = client.get("/users/me", headers={"Authorization": "Bearer foobar"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}

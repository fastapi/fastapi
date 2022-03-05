from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest
from fastapi.testclient import TestClient

app = FastAPI()

custom_authorization_header = "x-authorization"
security = HTTPDigest(authorization_header=custom_authorization_header)


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


def test_security_http_bearer_set_custom_authorization_header():
    expected_authorization_header = 'x-authorization'
    target = HTTPDigest(authorization_header=expected_authorization_header)
    assert target.authorization_header == expected_authorization_header


def test_security_http_digest_use_custom_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: "Digest foobar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"scheme": "Digest", "credentials": "foobar"}


def test_security_http_digest_no_authorization_header():
    response = client.get("/users/me", headers={custom_authorization_header: None})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_security_http_digest_incorrect_authorization_header():
    response = client.get("/users/me", headers={"Authorization": "Bearer foobar"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}

from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

app = FastAPI()

error_message = "not a 20 minute adventure"
security = HTTPBearer(auto_error=True, auto_error_detail=error_message)


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


def test_security_http_bearer():
    response = client.get("/users/me", headers={"Authorization": "Bearer foobar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"scheme": "Bearer", "credentials": "foobar"}


def test_security_http_bearer_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": error_message}

from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient

app = FastAPI()

error_message = "not a 20 minute adventure"
security = HTTPBasic(auto_error=True, auto_error_detail=error_message)


@app.get("/users/me")
def read_current_user(credentials: Optional[HTTPBasicCredentials] = Security(security)):
    return {"username": credentials.username, "password": credentials.password}


client = TestClient(app)


def test_security_http_basic():
    response = client.get("/users/me", auth=("john", "secret"))
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "john", "password": "secret"}


def test_security_http_basic_no_credentials():
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": error_message}

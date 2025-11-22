from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPBasic(realm="")

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}

client = TestClient(app)

def test_security_http_basic_empty_realm():
    response = client.get("/users/me", auth=("john", "secret"))
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "john", "password": "secret"}

def test_security_http_basic_invalid_credentials_empty_realm():
    response = client.get(
        "/users/me", headers={"Authorization": "Basic notabase64token"}
    )
    assert response.status_code == 401, response.text
    assert response.headers["WWW-Authenticate"] == "Basic"
    assert response.json() == {"detail": "Invalid authentication credentials"}

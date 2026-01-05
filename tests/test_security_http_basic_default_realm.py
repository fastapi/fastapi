from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient

app = FastAPI()
security = HTTPBasic()


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


client = TestClient(app)


def test_security_http_basic_default_realm():
    # 401 branch: should include default realm
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.headers["WWW-Authenticate"] == 'Basic realm="FastAPI"'
    assert response.json() == {"detail": "Not authenticated"}

    # 200 branch: execute the return line to satisfy 100% coverage
    ok = client.get("/users/me", auth=("john", "secret"))
    assert ok.status_code == 200, ok.text
    assert ok.json() == {"username": "john", "password": "secret"}

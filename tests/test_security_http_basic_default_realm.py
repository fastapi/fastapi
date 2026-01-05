from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.testclient import TestClient


def test_http_basic_includes_realm_by_default():
    app = FastAPI()
    security = HTTPBasic()  # no realm provided

    @app.get("/protected")
    def protected(credentials: HTTPBasicCredentials = Depends(security)):
        return {"username": credentials.username}

    client = TestClient(app)
    resp = client.get("/protected")

    assert resp.status_code == 401
    www_auth = resp.headers.get("www-authenticate")
    assert www_auth is not None
    assert www_auth.startswith('Basic realm="')

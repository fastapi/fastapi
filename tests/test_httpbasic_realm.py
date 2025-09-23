from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic
from fastapi.testclient import TestClient

def test_default_realm_is_included():
    app = FastAPI()
    security = HTTPBasic()

    @app.get("/protected")
    def protected(_: str = Depends(security)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == 'Basic realm="fastapi"'

def test_custom_realm_is_respected():
    app = FastAPI()
    security = HTTPBasic(realm="custom")

    @app.get("/protected")
    def protected(_: str = Depends(security)):
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == 'Basic realm="custom"'

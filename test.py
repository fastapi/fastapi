from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_hello_world():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"msg": "Hello"}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello"}

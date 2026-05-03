from fastapi import FastAPI, status
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {"msg": "Hello World"}

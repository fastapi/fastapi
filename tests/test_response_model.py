from fastapi import FastAPI
from fastapi.responses import ModelResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Model(BaseModel):
    name: str


app = FastAPI()


@app.get("/", response_model=Model)
async def get_pydantic() -> ModelResponse:
    return ModelResponse(Model(name="test_model"))


client = TestClient(app)


def test_pydantic_model():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "test_model"}

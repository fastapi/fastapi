import functools
import random

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

messages = ["操作成功.", "Successful operation."]


class ResponseModel(BaseModel):
    code: int = 200
    message: str = Field(default_factory=functools.partial(random.choice, messages))


@app.get(
    "/response_model_has_default_factory_return_dict",
    response_model=ResponseModel,
)
async def response_model_has_default_factory_return_dict():
    return {"code": 200}


@app.get(
    "/response_model_has_default_factory_return_model",
    response_model=ResponseModel,
)
async def response_model_has_default_factory_return_model():
    return ResponseModel()


client = TestClient(app)


def test_response_model_has_default_factory_return_dict():
    response = client.get("/response_model_has_default_factory_return_dict")

    assert response.status_code == 200, response.text

    assert response.json()["code"] == 200
    assert response.json()["message"] in messages


def test_response_model_has_default_factory_return_model():
    response = client.get("/response_model_has_default_factory_return_model")

    assert response.status_code == 200, response.text

    assert response.json()["code"] == 200
    assert response.json()["message"] in messages

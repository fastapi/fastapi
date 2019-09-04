from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class SubModel(BaseModel):
    a: Optional[str] = "foo"


class Model(BaseModel):
    x: Optional[int]
    sub: SubModel


class ModelSubclass(Model):
    y: int


@app.get("/", response_model=Model, response_model_skip_defaults=True)
def get() -> ModelSubclass:
    return ModelSubclass(sub={}, y=1)


client = TestClient(app)


def test_return_defaults():
    response = client.get("/")
    assert response.json() == {"sub": {}}

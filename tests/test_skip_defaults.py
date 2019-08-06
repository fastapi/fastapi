from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient


def test_return_defaults():
    app = FastAPI()

    class Model(BaseModel):
        x: Optional[int]

    @app.get("/", response_model=Model, response_model_skip_defaults=True)
    def get_x() -> Model:
        return Model()

    client = TestClient(app)
    response = client.get("/")
    print(response)
    assert response.content == b"{}"

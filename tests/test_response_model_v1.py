from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, v1


class Model(v1.BaseModel):
    name: str


app = FastAPI()


@app.get("/valid", response_model=Model)
def valid1():
    pass


client = TestClient(app)


def test_path_operations():
    response = client.get("/valid")
    assert response.status_code == 200, response.text

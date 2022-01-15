from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Level2(BaseModel):
    __root__: str


class Level1(BaseModel):
    __root__: Dict[str, Level2]


class Level0(BaseModel):
    __root__: Dict[str, Level1]


@app.get("/items/valid", response_model=Level0)
def get_valid():
    cat = Level2(__root__="cat")
    mammal = Level1(__root__={"mammal": cat})
    animal = Level0(__root__={"animal": mammal})
    return animal


client = TestClient(app)


def test_valid():
    response = client.get("/items/valid")
    response.raise_for_status()
    assert response.json() == {"animal": {"mammal": "cat"}}

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, root_validator

app = FastAPI()

counter_holder = {"counter": 0, "parsing_counter": 0}


class Model(BaseModel):
    @root_validator
    def __validate__(cls, _):
        counter_holder["parsing_counter"] += 1
        return {}


async def model_dep(model: Model) -> Model:
    return model


async def dep_counter():
    counter_holder["counter"] += 1
    return counter_holder["counter"]


async def super_dep(count: int = Depends(dep_counter)):
    return count


@app.get("/counter/")
async def get_counter(count: int = Depends(dep_counter)):
    return {"counter": count}


@app.get("/sub-counter/")
async def get_sub_counter(
    subcount: int = Depends(super_dep), count: int = Depends(dep_counter)
):
    return {"counter": count, "subcounter": subcount}


@app.get("/sub-counter-no-cache/")
async def get_sub_counter_no_cache(
    subcount: int = Depends(super_dep),
    count: int = Depends(dep_counter, use_cache=False),
):
    return {"counter": count, "subcounter": subcount}


@app.post("/sub-model-parsing/")
async def get_double_model_parsing(
    a: Model = Depends(model_dep),
    b: Model = Depends(model_dep),
):
    assert a is b
    return {"parsing_counter": counter_holder["parsing_counter"]}


client = TestClient(app)


def test_normal_counter():
    counter_holder["counter"] = 0
    response = client.get("/counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 1}
    response = client.get("/counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2}


def test_sub_counter():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 1, "subcounter": 1}
    response = client.get("/sub-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2, "subcounter": 2}


def test_sub_counter_no_cache():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter-no-cache/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2, "subcounter": 1}
    response = client.get("/sub-counter-no-cache/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 4, "subcounter": 3}


def test_sub_model_parsing_no_repeatable_parsing():
    counter_holder["parsing_counter"] = 0
    response = client.post("/sub-model-parsing/", json={})
    assert response.status_code == 200, response.text
    assert response.json() == {"parsing_counter": 1}

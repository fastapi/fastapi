from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

counter_holder = {"counter": 0}


class Model(BaseModel):
    name: str


@Depends
def get_user_model_data(model: Model):
    return model


@Depends
def log_new_users(data: dict = get_user_model_data):
    return data


@app.post("/cached-errors/", dependencies=[log_new_users])
def cached_errors(data: dict = get_user_model_data):
    return data


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


def test_caches_errors():
    response = client.post("/cached-errors/")
    assert response.json() == {
        "detail": [
            {
                "loc": ["body"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

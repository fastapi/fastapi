from typing import Optional

from fastapi import FastAPI, extra_parameters, exclude_parameters, Depends
from fastapi.testclient import TestClient

from pydantic import BaseModel


class Schema_1(BaseModel):
    schema_1_param_1: int
    schema_1_param_2: str


async def dependency_1(dependency_1_param_1: int = 1, dependency_1_param_2: int = 2):
    return {
        "dependency_1_param_1": dependency_1_param_1,
        "dependency_1_param_2": dependency_1_param_2
    }


app = FastAPI()


@app.get("/test_1")
@extra_parameters(b=str)
def endpoint_1(a, **kwargs):
    return {"a": a, "b": kwargs["b"]}


@app.get('/test2')
@extra_parameters(b=(str, 'bbb'))
def endpoint_2(a, **kwargs):
    return {"a": a, "b": kwargs["b"]}


@app.get("/test_3")
@extra_parameters(b=(Optional[str], None))
def endpoint_3(a, **kwargs):
    return {"a": a, "b": kwargs["b"]}


@app.get('/test_4/{b}')
@extra_parameters(b=int)
def endpoint_4(**kwargs):
    return {"b": kwargs["b"]}


@app.post('/test_5')
@extra_parameters(a=Schema_1)
def endpoint_5(**kwargs):
    return kwargs["a"]


@app.get('/test_6')
@extra_parameters(a=(dict, Depends(dependency_1)))
def endpoint_6(**kwargs):
    return kwargs["a"]


@app.get("/test_7")
@extra_parameters(a=(int, 1))
def endpoint_7(a):
    return {"a": a}


@app.get('/test_8')
@exclude_parameters('a')
def endpoint_8(a: int = 1, b: int = 2):
    return {"a": a, "b": b}


client = TestClient(app)


def test_extra_parameters():
    response = client.get("/test_1", params={"a": "foo", "b": "bar"})
    data = response.json()
    assert data == {"a": "foo", "b": "bar"}


def test_extra_parameters_default_with_no_value_passed():
    response = client.get("/test2", params={"a": "foo"})
    data = response.json()
    assert data == {"a": "foo", "b": "bbb"}


def test_extra_parameters_default_with_value_passed():
    response = client.get("/test2", params={"a": "foo", "b": "bar"})
    data = response.json()
    assert data == {"a": "foo", "b": "bar"}


def test_extra_parameters_optional_with_no_value_passed():
    response = client.get("/test_3", params={"a": "foo"})
    data = response.json()
    assert data == {"a": "foo", "b": None}


def test_extra_parameters_with_path_param():
    response = client.get("/test_4/123")
    data = response.json()
    assert data == {"b": 123}


def test_extra_parameters_with_schema():
    response = client.post("/test_5", json={"schema_1_param_1": 1, "schema_1_param_2": "2"})
    data = response.json()
    assert data == {"schema_1_param_1": 1, "schema_1_param_2": "2"}


def test_extra_parameters_with_depends():
    response = client.get("/test_6", json={"dependency_1_param_1": 1, "dependency_1_param_2": "2"})
    data = response.json()
    assert data == {"dependency_1_param_1": 1, "dependency_1_param_2": 2}


def test_extra_parameters_merging():
    response = client.get("/test_7")
    data = response.json()
    assert data == {"a": 1}


def test_exclude():
    response = client.get("/test_8")
    data = response.json()
    assert data == {"a": 1, "b": 2}

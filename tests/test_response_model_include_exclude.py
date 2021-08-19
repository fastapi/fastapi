from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Model1(BaseModel):
    foo: str
    bar: str


class Model2(BaseModel):
    ref: Model1
    baz: str


class Model3(BaseModel):
    name: str
    age: int
    ref2: Model2


app = FastAPI()


@app.get(
    "/simple_include",
    response_model=Model2,
    response_model_include={"baz": ..., "ref": {"foo"}},
)
def simple_include():
    return Model2(
        ref=Model1(foo="simple_include model foo", bar="simple_include model bar"),
        baz="simple_include model2 baz",
    )


@app.get(
    "/simple_include_dict",
    response_model=Model2,
    response_model_include={"baz": ..., "ref": {"foo"}},
)
def simple_include_dict():
    return {
        "ref": {
            "foo": "simple_include_dict model foo",
            "bar": "simple_include_dict model bar",
        },
        "baz": "simple_include_dict model2 baz",
    }


@app.get(
    "/simple_exclude",
    response_model=Model2,
    response_model_exclude={"ref": {"bar"}},
)
def simple_exclude():
    return Model2(
        ref=Model1(foo="simple_exclude model foo", bar="simple_exclude model bar"),
        baz="simple_exclude model2 baz",
    )


@app.get(
    "/simple_exclude_dict",
    response_model=Model2,
    response_model_exclude={"ref": {"bar"}},
)
def simple_exclude_dict():
    return {
        "ref": {
            "foo": "simple_exclude_dict model foo",
            "bar": "simple_exclude_dict model bar",
        },
        "baz": "simple_exclude_dict model2 baz",
    }


@app.get(
    "/mixed",
    response_model=Model3,
    response_model_include={"ref2", "name"},
    response_model_exclude={"ref2": {"baz"}},
)
def mixed():
    return Model3(
        name="mixed model3 name",
        age=3,
        ref2=Model2(
            ref=Model1(foo="mixed model foo", bar="mixed model bar"),
            baz="mixed model2 baz",
        ),
    )


@app.get(
    "/mixed_dict",
    response_model=Model3,
    response_model_include={"ref2", "name"},
    response_model_exclude={"ref2": {"baz"}},
)
def mixed_dict():
    return {
        "name": "mixed_dict model3 name",
        "age": 3,
        "ref2": {
            "ref": {"foo": "mixed_dict model foo", "bar": "mixed_dict model bar"},
            "baz": "mixed_dict model2 baz",
        },
    }


client = TestClient(app)


def test_nested_include_simple():
    response = client.get("/simple_include")

    assert response.status_code == 200, response.text

    assert response.json() == {
        "baz": "simple_include model2 baz",
        "ref": {"foo": "simple_include model foo"},
    }


def test_nested_include_simple_dict():
    response = client.get("/simple_include_dict")

    assert response.status_code == 200, response.text

    assert response.json() == {
        "baz": "simple_include_dict model2 baz",
        "ref": {"foo": "simple_include_dict model foo"},
    }


def test_nested_exclude_simple():
    response = client.get("/simple_exclude")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "baz": "simple_exclude model2 baz",
        "ref": {"foo": "simple_exclude model foo"},
    }


def test_nested_exclude_simple_dict():
    response = client.get("/simple_exclude_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "baz": "simple_exclude_dict model2 baz",
        "ref": {"foo": "simple_exclude_dict model foo"},
    }


def test_nested_include_mixed():
    response = client.get("/mixed")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "mixed model3 name",
        "ref2": {
            "ref": {"foo": "mixed model foo", "bar": "mixed model bar"},
        },
    }


def test_nested_include_mixed_dict():
    response = client.get("/mixed_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "mixed_dict model3 name",
        "ref2": {
            "ref": {"foo": "mixed_dict model foo", "bar": "mixed_dict model bar"},
        },
    }

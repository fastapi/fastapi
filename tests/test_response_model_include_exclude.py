from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Test(BaseModel):
    foo: str
    bar: str


class Test2(BaseModel):
    test: Test
    baz: str


class Test3(BaseModel):
    name: str
    age: int
    test2: Test2


app = FastAPI()


@app.get(
    "/simple_include",
    response_model=Test2,
    response_model_include={"baz": ..., "test": {"foo"}},
)
def simple_include():
    return Test2(
        test=Test(foo="simple_include test foo", bar="simple_include test bar"),
        baz="simple_include test2 baz",
    )


@app.get(
    "/simple_include_dict",
    response_model=Test2,
    response_model_include={"baz": ..., "test": {"foo"}},
)
def simple_include_dict():
    return {
        "test": {
            "foo": "simple_include_dict test foo",
            "bar": "simple_include_dict test bar",
        },
        "baz": "simple_include_dict test2 baz",
    }


@app.get(
    "/simple_exclude",
    response_model=Test2,
    response_model_exclude={"test": {"bar"}},
)
def simple_exclude():
    return Test2(
        test=Test(foo="simple_exclude test foo", bar="simple_exclude test bar"),
        baz="simple_exclude test2 baz",
    )


@app.get(
    "/simple_exclude_dict",
    response_model=Test2,
    response_model_exclude={"test": {"bar"}},
)
def simple_exclude_dict():
    return {
        "test": {
            "foo": "simple_exclude_dict test foo",
            "bar": "simple_exclude_dict test bar",
        },
        "baz": "simple_exclude_dict test2 baz",
    }


@app.get(
    "/mixed",
    response_model=Test3,
    response_model_include={"test2", "name"},
    response_model_exclude={"test2": {"baz"}},
)
def mixed():
    return Test3(
        name="mixed test3 name",
        age=3,
        test2=Test2(
            test=Test(foo="mixed test foo", bar="mixed test bar"), baz="mixed test2 baz"
        ),
    )


@app.get(
    "/mixed_dict",
    response_model=Test3,
    response_model_include={"test2", "name"},
    response_model_exclude={"test2": {"baz"}},
)
def mixed_dict():
    return {
        "name": "mixed_dict test3 name",
        "age": 3,
        "test2": {
            "test": {"foo": "mixed_dict test foo", "bar": "mixed_dict test bar"},
            "baz": "mixed_dict test2 baz",
        },
    }


client = TestClient(app)


def test_nested_include_simple():
    response = client.get("/simple_include")

    assert response.status_code == 200, response.text

    assert response.json() == {
        "baz": "simple_include test2 baz",
        "test": {"foo": "simple_include test foo"},
    }


def test_nested_include_simple_dict():
    response = client.get("/simple_include_dict")

    assert response.status_code == 200, response.text

    assert response.json() == {
        "baz": "simple_include_dict test2 baz",
        "test": {"foo": "simple_include_dict test foo"},
    }


def test_nested_exclude_simple():
    response = client.get("/simple_exclude")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "baz": "simple_exclude test2 baz",
        "test": {"foo": "simple_exclude test foo"},
    }


def test_nested_exclude_simple_dict():
    response = client.get("/simple_exclude_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "baz": "simple_exclude_dict test2 baz",
        "test": {"foo": "simple_exclude_dict test foo"},
    }


def test_nested_include_mixed():
    response = client.get("/mixed")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "mixed test3 name",
        "test2": {
            "test": {"foo": "mixed test foo", "bar": "mixed test bar"},
        },
    }


def test_nested_include_mixed_dict():
    response = client.get("/mixed_dict")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "mixed_dict test3 name",
        "test2": {
            "test": {"foo": "mixed_dict test foo", "bar": "mixed_dict test bar"},
        },
    }

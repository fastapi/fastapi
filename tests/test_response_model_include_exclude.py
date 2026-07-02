from fastapi import FastAPI
from fastapi.responses import JSONResponse
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


@app.get(
    "/list_include",
    response_model=list[Model1],
    response_model_include={"foo"},
)
def list_include():
    return [
        Model1(foo="list_include model foo", bar="list_include model bar"),
        Model1(foo="list_include model2 foo", bar="list_include model2 bar"),
    ]


@app.get(
    "/list_exclude",
    response_model=list[Model1],
    response_model_exclude={"bar"},
)
def list_exclude():
    return [
        Model1(foo="list_exclude model foo", bar="list_exclude model bar"),
        Model1(foo="list_exclude model2 foo", bar="list_exclude model2 bar"),
    ]


@app.get(
    "/list_exclude_nested",
    response_model=list[Model2],
    response_model_exclude={"ref": {"bar"}},
)
def list_exclude_nested():
    return [
        Model2(
            ref=Model1(
                foo="list_exclude_nested model foo",
                bar="list_exclude_nested model bar",
            ),
            baz="list_exclude_nested model2 baz",
        )
    ]


@app.get(
    "/list_exclude_all",
    response_model=list[Model1],
    response_model_exclude={"__all__": {"bar"}},
)
def list_exclude_all():
    return [
        Model1(foo="list_exclude_all model foo", bar="list_exclude_all model bar"),
    ]


@app.get(
    "/list_exclude_response_class",
    response_model=list[Model1],
    response_model_exclude={"bar"},
    response_class=JSONResponse,
)
def list_exclude_response_class():
    return [
        Model1(
            foo="list_exclude_response_class model foo",
            bar="list_exclude_response_class model bar",
        ),
    ]


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


def test_list_include():
    response = client.get("/list_include")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"foo": "list_include model foo"},
        {"foo": "list_include model2 foo"},
    ]


def test_list_exclude():
    response = client.get("/list_exclude")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"foo": "list_exclude model foo"},
        {"foo": "list_exclude model2 foo"},
    ]


def test_list_exclude_nested():
    response = client.get("/list_exclude_nested")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "ref": {"foo": "list_exclude_nested model foo"},
            "baz": "list_exclude_nested model2 baz",
        }
    ]


def test_list_exclude_all():
    response = client.get("/list_exclude_all")
    assert response.status_code == 200, response.text
    assert response.json() == [{"foo": "list_exclude_all model foo"}]


def test_list_exclude_response_class():
    response = client.get("/list_exclude_response_class")
    assert response.status_code == 200, response.text
    assert response.json() == [{"foo": "list_exclude_response_class model foo"}]

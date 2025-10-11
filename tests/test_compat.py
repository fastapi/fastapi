from typing import Any, Dict, List, Union

from fastapi import FastAPI, UploadFile
from fastapi._compat import (
    Undefined,
    _get_model_config,
    get_cached_model_fields,
    is_scalar_field,
    is_uploadfile_sequence_annotation,
    v1,
)
from fastapi._compat.shared import is_bytes_sequence_annotation
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo

from .utils import needs_py_lt_314, needs_pydanticv2


@needs_pydanticv2
def test_model_field_default_required():
    from fastapi._compat import v2

    # For coverage
    field_info = FieldInfo(annotation=str)
    field = v2.ModelField(name="foo", field_info=field_info)
    assert field.default is Undefined


def test_v1_plain_validator_function():
    # For coverage
    def func(v):  # pragma: no cover
        return v

    result = v1.with_info_plain_validator_function(func)
    assert result == {}


def test_is_model_field():
    # For coverage
    from fastapi._compat import _is_model_field

    assert not _is_model_field(str)


@needs_pydanticv2
def test_get_model_config():
    # For coverage in Pydantic v2
    class Foo(BaseModel):
        model_config = ConfigDict(from_attributes=True)

    foo = Foo()
    config = _get_model_config(foo)
    assert config == {"from_attributes": True}


def test_complex():
    app = FastAPI()

    @app.post("/")
    def foo(foo: Union[str, List[int]]):
        return foo

    client = TestClient(app)

    response = client.post("/", json="bar")
    assert response.status_code == 200, response.text
    assert response.json() == "bar"

    response2 = client.post("/", json=[1, 2])
    assert response2.status_code == 200, response2.text
    assert response2.json() == [1, 2]


@needs_pydanticv2
def test_propagates_pydantic2_model_config():
    app = FastAPI()

    class Missing:
        def __bool__(self):
            return False

    class EmbeddedModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        value: Union[str, Missing] = Missing()

    class Model(BaseModel):
        model_config = ConfigDict(
            arbitrary_types_allowed=True,
        )
        value: Union[str, Missing] = Missing()
        embedded_model: EmbeddedModel = EmbeddedModel()

    @app.post("/")
    def foo(req: Model) -> Dict[str, Union[str, None]]:
        return {
            "value": req.value or None,
            "embedded_value": req.embedded_model.value or None,
        }

    client = TestClient(app)

    response = client.post("/", json={})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "value": None,
        "embedded_value": None,
    }

    response2 = client.post(
        "/", json={"value": "foo", "embedded_model": {"value": "bar"}}
    )
    assert response2.status_code == 200, response2.text
    assert response2.json() == {
        "value": "foo",
        "embedded_value": "bar",
    }


def test_is_bytes_sequence_annotation_union():
    # For coverage
    # TODO: in theory this would allow declaring types that could be lists of bytes
    # to be read from files and other types, but I'm not even sure it's a good idea
    # to support it as a first class "feature"
    assert is_bytes_sequence_annotation(Union[List[str], List[bytes]])


def test_is_uploadfile_sequence_annotation():
    # For coverage
    # TODO: in theory this would allow declaring types that could be lists of UploadFile
    # and other types, but I'm not even sure it's a good idea to support it as a first
    # class "feature"
    assert is_uploadfile_sequence_annotation(Union[List[str], List[UploadFile]])


@needs_py_lt_314
def test_is_pv1_scalar_field():
    # For coverage
    class Model(v1.BaseModel):
        foo: Union[str, Dict[str, Any]]

    fields = v1.get_model_fields(Model)
    assert not is_scalar_field(fields[0])


def test_get_model_fields_cached():
    class Model(v1.BaseModel):
        foo: str

    non_cached_fields = v1.get_model_fields(Model)
    non_cached_fields2 = v1.get_model_fields(Model)
    cached_fields = get_cached_model_fields(Model)
    cached_fields2 = get_cached_model_fields(Model)
    for f1, f2 in zip(cached_fields, cached_fields2):
        assert f1 is f2

    assert non_cached_fields is not non_cached_fields2
    assert cached_fields is cached_fields2

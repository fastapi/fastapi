from typing import Any, Dict, List, Union

from fastapi import FastAPI, UploadFile
from fastapi._compat import (
    ModelField,
    Undefined,
    _get_model_config,
    get_cached_model_fields,
    get_model_fields,
    is_bytes_sequence_annotation,
    is_scalar_field,
    is_uploadfile_sequence_annotation,
)
from fastapi.testclient import TestClient
from pydantic import BaseConfig, BaseModel, ConfigDict
from pydantic.fields import FieldInfo

from .utils import needs_pydanticv1, needs_pydanticv2


@needs_pydanticv2
def test_model_field_default_required():
    # For coverage
    field_info = FieldInfo(annotation=str)
    field = ModelField(name="foo", field_info=field_info)
    assert field.default is Undefined


@needs_pydanticv1
def test_upload_file_dummy_with_info_plain_validator_function():
    # For coverage
    assert UploadFile.__get_pydantic_core_schema__(str, lambda x: None) == {}


@needs_pydanticv1
def test_union_scalar_list():
    # For coverage
    # TODO: there might not be a current valid code path that uses this, it would
    # potentially enable query parameters defined as both a scalar and a list
    # but that would require more refactors, also not sure it's really useful
    from fastapi._compat import is_pv1_scalar_field

    field_info = FieldInfo()
    field = ModelField(
        name="foo",
        field_info=field_info,
        type_=Union[str, List[int]],
        class_validators={},
        model_config=BaseConfig,
    )
    assert not is_pv1_scalar_field(field)


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


def test_is_pv1_scalar_field():
    # For coverage
    class Model(BaseModel):
        foo: Union[str, Dict[str, Any]]

    fields = get_model_fields(Model)
    assert not is_scalar_field(fields[0])


def test_get_model_fields_cached():
    class Model(BaseModel):
        foo: str

    non_cached_fields = get_model_fields(Model)
    non_cached_fields2 = get_model_fields(Model)
    cached_fields = get_cached_model_fields(Model)
    cached_fields2 = get_cached_model_fields(Model)
    for f1, f2 in zip(cached_fields, cached_fields2):
        assert f1 is f2

    assert non_cached_fields is not non_cached_fields2
    assert cached_fields is cached_fields2

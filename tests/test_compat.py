from typing import Union

from fastapi import FastAPI, UploadFile
from fastapi._compat import (
    Undefined,
    is_uploadfile_sequence_annotation,
)
from fastapi._compat.shared import is_bytes_sequence_annotation
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo

from .utils import needs_py310


def test_model_field_default_required():
    from fastapi._compat import v2

    # For coverage
    field_info = FieldInfo(annotation=str)
    field = v2.ModelField(name="foo", field_info=field_info)
    assert field.default is Undefined


def test_complex():
    app = FastAPI()

    @app.post("/")
    def foo(foo: Union[str, list[int]]):
        return foo

    client = TestClient(app)

    response = client.post("/", json="bar")
    assert response.status_code == 200, response.text
    assert response.json() == "bar"

    response2 = client.post("/", json=[1, 2])
    assert response2.status_code == 200, response2.text
    assert response2.json() == [1, 2]


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
    def foo(req: Model) -> dict[str, Union[str, None]]:
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
    assert is_bytes_sequence_annotation(Union[list[str], list[bytes]])


def test_is_uploadfile_sequence_annotation():
    # For coverage
    # TODO: in theory this would allow declaring types that could be lists of UploadFile
    # and other types, but I'm not even sure it's a good idea to support it as a first
    # class "feature"
    assert is_uploadfile_sequence_annotation(Union[list[str], list[UploadFile]])


def test_serialize_sequence_value_with_optional_list():
    """Test that serialize_sequence_value handles optional lists correctly."""
    from fastapi._compat import v2

    field_info = FieldInfo(annotation=Union[list[str], None])
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["a", "b", "c"])
    assert result == ["a", "b", "c"]
    assert isinstance(result, list)


@needs_py310
def test_serialize_sequence_value_with_optional_list_pipe_union():
    """Test that serialize_sequence_value handles optional lists correctly (with new syntax)."""
    from fastapi._compat import v2

    field_info = FieldInfo(annotation=list[str] | None)
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["a", "b", "c"])
    assert result == ["a", "b", "c"]
    assert isinstance(result, list)


def test_serialize_sequence_value_with_none_first_in_union():
    """Test that serialize_sequence_value handles Union[None, List[...]] correctly."""
    from fastapi._compat import v2

    field_info = FieldInfo(annotation=Union[None, list[str]])
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["x", "y"])
    assert result == ["x", "y"]
    assert isinstance(result, list)

from typing import Optional

import pytest
from fastapi import FastAPI, Form
from fastapi._compat import PYDANTIC_V2
from pydantic import BaseModel, Field
from starlette.testclient import TestClient
from typing_extensions import Annotated

from .utils import needs_pydanticv2

if PYDANTIC_V2:
    from pydantic import model_validator
else:
    from pydantic import root_validator


def _validate_input(value: dict) -> dict:
    """
    model validators in before mode should receive values passed
    to model instantiation before any further validation
    """
    # we should not be double-instantiating the models
    assert isinstance(value, dict)
    value["init_input"] = value.copy()

    # differentiate between explicit Nones and unpassed values
    if "true_if_unset" not in value:
        value["true_if_unset"] = True
    return value


class Parent(BaseModel):
    init_input: dict
    # importantly, no default here

    if PYDANTIC_V2:

        @model_validator(mode="before")
        def validate_inputs(cls, value: dict) -> dict:
            return _validate_input(value)
    else:

        @root_validator(pre=True)
        def validate_inputs(cls, value: dict) -> dict:
            return _validate_input(value)


class StandardModel(Parent):
    default_true: bool = True
    default_false: bool = False
    default_none: Optional[bool] = None
    default_zero: int = 0
    default_str: str = "foo"
    true_if_unset: Optional[bool] = None


class FieldModel(Parent):
    default_true: bool = Field(default=True)
    default_false: bool = Field(default=False)
    default_none: Optional[bool] = Field(default=None)
    default_zero: int = Field(default=0)
    default_str: str = Field(default="foo")
    true_if_unset: Optional[bool] = Field(default=None)


if PYDANTIC_V2:

    class AnnotatedFieldModel(Parent):
        default_true: Annotated[bool, Field(default=True)]
        default_false: Annotated[bool, Field(default=False)]
        default_none: Annotated[Optional[bool], Field(default=None)]
        default_zero: Annotated[int, Field(default=0)]
        default_str: Annotated[str, Field(default="foo")]
        true_if_unset: Annotated[Optional[bool], Field(default=None)]

    class AnnotatedFormModel(Parent):
        default_true: Annotated[bool, Form(default=True)]
        default_false: Annotated[bool, Form(default=False)]
        default_none: Annotated[Optional[bool], Form(default=None)]
        default_zero: Annotated[int, Form(default=0)]
        default_str: Annotated[str, Form(default="foo")]
        true_if_unset: Annotated[Optional[bool], Form(default=None)]

    class SimpleForm(BaseModel):
        """https://github.com/fastapi/fastapi/pull/13464#issuecomment-2708378172"""

        foo: Annotated[str, Form(default="bar")]
        alias_with: Annotated[str, Form(alias="with", default="nothing")]


class ResponseModel(BaseModel):
    fields_set: list = Field(default_factory=list)
    dumped_fields_no_exclude: dict = Field(default_factory=dict)
    dumped_fields_exclude_default: dict = Field(default_factory=dict)
    dumped_fields_exclude_unset: dict = Field(default_factory=dict)
    dumped_fields_no_meta: dict = Field(default_factory=dict)
    init_input: dict

    @classmethod
    def from_value(cls, value: Parent) -> "ResponseModel":
        if PYDANTIC_V2:
            return ResponseModel(
                init_input=value.init_input,
                fields_set=list(value.model_fields_set),
                dumped_fields_no_exclude=value.model_dump(),
                dumped_fields_exclude_default=value.model_dump(exclude_defaults=True),
                dumped_fields_exclude_unset=value.model_dump(exclude_unset=True),
                dumped_fields_no_meta=value.model_dump(
                    exclude={"init_input", "fields_set"}
                ),
            )
        else:
            return ResponseModel(
                init_input=value.init_input,
                fields_set=list(value.__fields_set__),
                dumped_fields_no_exclude=value.dict(),
                dumped_fields_exclude_default=value.dict(exclude_defaults=True),
                dumped_fields_exclude_unset=value.dict(exclude_unset=True),
                dumped_fields_no_meta=value.dict(exclude={"init_input", "fields_set"}),
            )


app = FastAPI()


@app.post("/form/standard")
async def form_standard(value: Annotated[StandardModel, Form()]) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/form/field")
async def form_field(value: Annotated[FieldModel, Form()]) -> ResponseModel:
    return ResponseModel.from_value(value)


if PYDANTIC_V2:

    @app.post("/form/annotated-field")
    async def form_annotated_field(
        value: Annotated[AnnotatedFieldModel, Form()],
    ) -> ResponseModel:
        return ResponseModel.from_value(value)

    @app.post("/form/annotated-form")
    async def form_annotated_form(
        value: Annotated[AnnotatedFormModel, Form()],
    ) -> ResponseModel:
        return ResponseModel.from_value(value)


@app.post("/form/inlined")
async def form_inlined(
    default_true: Annotated[bool, Form()] = True,
    default_false: Annotated[bool, Form()] = False,
    default_none: Annotated[Optional[bool], Form()] = None,
    default_zero: Annotated[int, Form()] = 0,
    default_str: Annotated[str, Form()] = "foo",
    true_if_unset: Annotated[Optional[bool], Form()] = None,
):
    """
    Rather than using a model, inline the fields in the endpoint.

    This doesn't use the `ResponseModel` pattern, since that is just to
    test the instantiation behavior prior to the endpoint function.
    Since we are receiving the values of the fields here (and thus,
    having the defaults is correct behavior), we just return the values.
    """
    if true_if_unset is None:
        true_if_unset = True

    return {
        "default_true": default_true,
        "default_false": default_false,
        "default_none": default_none,
        "default_zero": default_zero,
        "default_str": default_str,
        "true_if_unset": true_if_unset,
    }


@app.post("/json/standard")
async def json_standard(value: StandardModel) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/json/field")
async def json_field(value: FieldModel) -> ResponseModel:
    return ResponseModel.from_value(value)


if PYDANTIC_V2:

    @app.post("/json/annotated-field")
    async def json_annotated_field(value: AnnotatedFieldModel) -> ResponseModel:
        return ResponseModel.from_value(value)

    @app.post("/json/annotated-form")
    async def json_annotated_form(value: AnnotatedFormModel) -> ResponseModel:
        return ResponseModel.from_value(value)

    @app.post("/simple-form")
    def form_endpoint(model: Annotated[SimpleForm, Form()]) -> dict:
        """https://github.com/fastapi/fastapi/pull/13464#issuecomment-2708378172"""
        return model.model_dump()


if PYDANTIC_V2:
    MODEL_TYPES = {
        "standard": StandardModel,
        "field": FieldModel,
        "annotated-field": AnnotatedFieldModel,
        "annotated-form": AnnotatedFormModel,
    }
else:
    MODEL_TYPES = {
        "standard": StandardModel,
        "field": FieldModel,
    }
ENCODINGS = ("form", "json")


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize("encoding", ENCODINGS)
@pytest.mark.parametrize("model_type", MODEL_TYPES.keys())
def test_no_prefill_defaults_all_unset(encoding, model_type, client):
    """
    When the model is instantiated by the server, it should not have its defaults prefilled
    """

    endpoint = f"/{encoding}/{model_type}"
    if encoding == "form":
        res = client.post(endpoint, data={})
    else:
        res = client.post(endpoint, json={})

    assert res.status_code == 200
    response_model = ResponseModel(**res.json())
    assert response_model.init_input == {}
    assert len(response_model.fields_set) == 2
    assert response_model.dumped_fields_no_exclude["true_if_unset"] is True


@pytest.mark.parametrize("encoding", ENCODINGS)
@pytest.mark.parametrize("model_type", MODEL_TYPES.keys())
def test_no_prefill_defaults_partially_set(encoding, model_type, client):
    """
    When the model is instantiated by the server, it should not have its defaults prefilled,
    and pydantic should be able to differentiate between unset and default values when some are passed
    """
    endpoint = f"/{encoding}/{model_type}"
    if encoding == "form":
        data = {"true_if_unset": "False", "default_false": "True", "default_zero": "0"}
        res = client.post(endpoint, data=data)
    else:
        data = {"true_if_unset": False, "default_false": True, "default_zero": 0}
        res = client.post(endpoint, json=data)

    if PYDANTIC_V2:
        dumped_exclude_unset = MODEL_TYPES[model_type](**data).model_dump(
            exclude_unset=True
        )
        dumped_exclude_default = MODEL_TYPES[model_type](**data).model_dump(
            exclude_defaults=True
        )
    else:
        dumped_exclude_unset = MODEL_TYPES[model_type](**data).dict(exclude_unset=True)
        dumped_exclude_default = MODEL_TYPES[model_type](**data).dict(
            exclude_defaults=True
        )

    assert res.status_code == 200
    response_model = ResponseModel(**res.json())
    assert response_model.init_input == data
    assert len(response_model.fields_set) == 4
    assert response_model.dumped_fields_exclude_unset == dumped_exclude_unset
    assert response_model.dumped_fields_no_exclude["true_if_unset"] is False
    assert "default_zero" not in dumped_exclude_default
    assert "default_zero" not in response_model.dumped_fields_exclude_default


@needs_pydanticv2
def test_casted_empty_defaults(client: TestClient):
    """https://github.com/fastapi/fastapi/pull/13464#issuecomment-2708378172"""
    form_content = {"foo": "", "with": ""}
    response = client.post("/simple-form", data=form_content)
    response_content = response.json()
    assert response_content["foo"] == "bar"  # Expected :'bar' -> Actual   :''
    assert response_content["alias_with"] == "nothing"  # ok


@pytest.mark.parametrize("model_type", list(MODEL_TYPES.keys()) + ["inlined"])
def test_empty_string_inputs(model_type, client):
    """
    Form inputs with no input are empty strings,
    these should be treated as being unset.
    """
    data = {
        "default_true": "",
        "default_false": "",
        "default_none": "",
        "default_str": "",
        "default_zero": "",
        "true_if_unset": "",
    }
    response = client.post(f"/form/{model_type}", data=data)
    assert response.status_code == 200
    if model_type != "inlined":
        response_model = ResponseModel(**response.json())
        assert set(response_model.fields_set) == {"true_if_unset", "init_input"}
        response_data = response_model.dumped_fields_no_meta
    else:
        response_data = response.json()
    assert response_data == {
        "default_true": True,
        "default_false": False,
        "default_none": None,
        "default_zero": 0,
        "default_str": "foo",
        "true_if_unset": True,
    }

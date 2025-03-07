from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, model_validator
from starlette.testclient import TestClient


class Parent(BaseModel):
    init_input: dict
    # importantly, no default here

    @model_validator(mode="before")
    def validate_inputs(cls, value: dict) -> dict:
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


class StandardModel(Parent):
    default_true: bool = True
    default_false: bool = False
    default_none: Optional[bool] = None
    default_zero: int = 0
    true_if_unset: Optional[bool] = None


class FieldModel(Parent):
    default_true: bool = Field(default=True)
    default_false: bool = Field(default=False)
    default_none: Optional[bool] = Field(default=None)
    default_zero: int = Field(default=0)
    true_if_unset: Optional[bool] = Field(default=None)


class AnnotatedFieldModel(Parent):
    default_true: Annotated[bool, Field(default=True)]
    default_false: Annotated[bool, Field(default=False)]
    default_none: Annotated[Optional[bool], Field(default=None)]
    default_zero: Annotated[int, Field(default=0)]
    true_if_unset: Annotated[Optional[bool], Field(default=None)]


class AnnotatedFormModel(Parent):
    default_true: Annotated[bool, Form(default=True)]
    default_false: Annotated[bool, Form(default=False)]
    default_none: Annotated[Optional[bool], Form(default=None)]
    default_zero: Annotated[int, Form(default=0)]
    true_if_unset: Annotated[Optional[bool], Form(default=None)]


class ResponseModel(BaseModel):
    fields_set: list = Field(default_factory=list)
    dumped_fields_no_exclude: dict = Field(default_factory=dict)
    dumped_fields_exclude_default: dict = Field(default_factory=dict)
    dumped_fields_exclude_unset: dict = Field(default_factory=dict)
    init_input: dict

    @classmethod
    def from_value(cls, value: Parent) -> "ResponseModel":
        return ResponseModel(
            init_input=value.init_input,
            fields_set=list(value.model_fields_set),
            dumped_fields_no_exclude=value.model_dump(),
            dumped_fields_exclude_default=value.model_dump(exclude_defaults=True),
            dumped_fields_exclude_unset=value.model_dump(exclude_unset=True),
        )


app = FastAPI()


@app.post("/form/standard")
async def form_standard(value: Annotated[StandardModel, Form()]) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/form/field")
async def form_field(value: Annotated[FieldModel, Form()]) -> ResponseModel:
    return ResponseModel.from_value(value)


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


@app.post("/json/standard")
async def json_standard(value: StandardModel) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/json/field")
async def json_field(value: FieldModel) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/json/annotated-field")
async def json_annotated_field(value: AnnotatedFieldModel) -> ResponseModel:
    return ResponseModel.from_value(value)


@app.post("/json/annotated-form")
async def json_annotated_form(value: AnnotatedFormModel) -> ResponseModel:
    return ResponseModel.from_value(value)


MODEL_TYPES = {
    "standard": StandardModel,
    "field": FieldModel,
    "annotated-field": AnnotatedFieldModel,
    "annotated-form": AnnotatedFormModel,
}
ENCODINGS = ("form", "json")


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize("encoding", ENCODINGS)
@pytest.mark.parametrize("model_type", MODEL_TYPES.keys())
def test_no_prefill_defaults_all_unset(encoding, model_type, client, monkeypatch):
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
def test_no_prefill_defaults_partially_set(encoding, model_type, client, monkeypatch):
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

    data_with_init_input = data.copy()
    data_with_init_input["init_input"] = data.copy()

    assert res.status_code == 200
    response_model = ResponseModel(**res.json())
    assert response_model.init_input == data
    assert len(response_model.fields_set) == 4
    dumped_exclude_unset = MODEL_TYPES[model_type](**data).model_dump(
        exclude_unset=True
    )
    assert response_model.dumped_fields_exclude_unset == dumped_exclude_unset
    assert response_model.dumped_fields_no_exclude["true_if_unset"] is False
    dumped_exclude_default = MODEL_TYPES[model_type](**data).model_dump(
        exclude_defaults=True
    )
    assert "default_zero" not in dumped_exclude_default
    assert "default_zero" not in response_model.dumped_fields_exclude_default

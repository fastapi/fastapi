from datetime import datetime, timezone
from enum import Enum
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Optional

import pytest
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ValidationError, create_model


class Person:
    def __init__(self, name: str):
        self.name = name


class Pet:
    def __init__(self, owner: Person, name: str):
        self.owner = owner
        self.name = name


class DictablePerson(Person):
    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())


class DictablePet(Pet):
    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())


class Unserializable:
    def __iter__(self):
        raise NotImplementedError()

    @property
    def __dict__(self):
        raise NotImplementedError()


class ModelWithCustomEncoder(BaseModel):
    dt_field: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


class ModelWithCustomEncoderSubclass(ModelWithCustomEncoder):
    class Config:
        pass


class RoleEnum(Enum):
    admin = "admin"
    normal = "normal"


class ModelWithConfig(BaseModel):
    role: Optional[RoleEnum] = None

    class Config:
        use_enum_values = True


class ModelWithAlias(BaseModel):
    foo: str = Field(alias="Foo")


class ModelWithDefault(BaseModel):
    foo: str = ...  # type: ignore
    bar: str = "bar"
    bla: str = "bla"


class ModelWithRoot(BaseModel):
    __root__: str


@pytest.fixture(
    name="model_with_path", params=[PurePath, PurePosixPath, PureWindowsPath]
)
def fixture_model_with_path(request):
    class Config:
        arbitrary_types_allowed = True

    ModelWithPath = create_model(
        "ModelWithPath", path=(request.param, ...), __config__=Config  # type: ignore
    )
    return ModelWithPath(path=request.param("/foo", "bar"))


def test_encode_dict():
    pet = {"name": "Firulais", "owner": {"name": "Foo"}}
    assert jsonable_encoder(pet) == {"name": "Firulais", "owner": {"name": "Foo"}}
    assert jsonable_encoder(pet, include={"name"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, exclude={"owner"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, include={}) == {}
    assert jsonable_encoder(pet, exclude={}) == {
        "name": "Firulais",
        "owner": {"name": "Foo"},
    }


def test_encode_class():
    person = Person(name="Foo")
    pet = Pet(owner=person, name="Firulais")
    assert jsonable_encoder(pet) == {"name": "Firulais", "owner": {"name": "Foo"}}
    assert jsonable_encoder(pet, include={"name"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, exclude={"owner"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, include={}) == {}
    assert jsonable_encoder(pet, exclude={}) == {
        "name": "Firulais",
        "owner": {"name": "Foo"},
    }


def test_encode_dictable():
    person = DictablePerson(name="Foo")
    pet = DictablePet(owner=person, name="Firulais")
    assert jsonable_encoder(pet) == {"name": "Firulais", "owner": {"name": "Foo"}}
    assert jsonable_encoder(pet, include={"name"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, exclude={"owner"}) == {"name": "Firulais"}
    assert jsonable_encoder(pet, include={}) == {}
    assert jsonable_encoder(pet, exclude={}) == {
        "name": "Firulais",
        "owner": {"name": "Foo"},
    }


def test_encode_unsupported():
    unserializable = Unserializable()
    with pytest.raises(ValueError):
        jsonable_encoder(unserializable)


def test_encode_custom_json_encoders_model():
    model = ModelWithCustomEncoder(dt_field=datetime(2019, 1, 1, 8))
    assert jsonable_encoder(model) == {"dt_field": "2019-01-01T08:00:00+00:00"}


def test_encode_custom_json_encoders_model_subclass():
    model = ModelWithCustomEncoderSubclass(dt_field=datetime(2019, 1, 1, 8))
    assert jsonable_encoder(model) == {"dt_field": "2019-01-01T08:00:00+00:00"}


def test_encode_model_with_config():
    model = ModelWithConfig(role=RoleEnum.admin)
    assert jsonable_encoder(model) == {"role": "admin"}


def test_encode_model_with_alias_raises():
    with pytest.raises(ValidationError):
        ModelWithAlias(foo="Bar")


def test_encode_model_with_alias():
    model = ModelWithAlias(Foo="Bar")
    assert jsonable_encoder(model) == {"Foo": "Bar"}


def test_encode_model_with_default():
    model = ModelWithDefault(foo="foo", bar="bar")
    assert jsonable_encoder(model) == {"foo": "foo", "bar": "bar", "bla": "bla"}
    assert jsonable_encoder(model, exclude_unset=True) == {"foo": "foo", "bar": "bar"}
    assert jsonable_encoder(model, exclude_defaults=True) == {"foo": "foo"}
    assert jsonable_encoder(model, exclude_unset=True, exclude_defaults=True) == {
        "foo": "foo"
    }
    assert jsonable_encoder(model, include={"foo"}) == {"foo": "foo"}
    assert jsonable_encoder(model, exclude={"bla"}) == {"foo": "foo", "bar": "bar"}
    assert jsonable_encoder(model, include={}) == {}
    assert jsonable_encoder(model, exclude={}) == {
        "foo": "foo",
        "bar": "bar",
        "bla": "bla",
    }


def test_custom_encoders():
    class safe_datetime(datetime):
        pass

    class MyModel(BaseModel):
        dt_field: safe_datetime

    instance = MyModel(dt_field=safe_datetime.now())

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={safe_datetime: lambda o: o.isoformat()}
    )
    assert encoded_instance["dt_field"] == instance.dt_field.isoformat()


def test_custom_enum_encoders():
    def custom_enum_encoder(v: Enum):
        return v.value.lower()

    class MyEnum(Enum):
        ENUM_VAL_1 = "ENUM_VAL_1"

    instance = MyEnum.ENUM_VAL_1

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={MyEnum: custom_enum_encoder}
    )
    assert encoded_instance == custom_enum_encoder(instance)


def test_encode_model_with_path(model_with_path):
    if isinstance(model_with_path.path, PureWindowsPath):
        expected = "\\foo\\bar"
    else:
        expected = "/foo/bar"
    assert jsonable_encoder(model_with_path) == {"path": expected}


def test_encode_root():
    model = ModelWithRoot(__root__="Foo")
    assert jsonable_encoder(model) == "Foo"

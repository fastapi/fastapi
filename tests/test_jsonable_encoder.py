from datetime import datetime, timezone
from enum import Enum

import pytest
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Schema, ValidationError


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


class RoleEnum(Enum):
    admin = "admin"
    normal = "normal"


class ModelWithConfig(BaseModel):
    role: RoleEnum = None

    class Config:
        use_enum_values = True


class ModelWithAlias(BaseModel):
    foo: str = Schema(..., alias="Foo")


def test_encode_class():
    person = Person(name="Foo")
    pet = Pet(owner=person, name="Firulais")
    assert jsonable_encoder(pet) == {"name": "Firulais", "owner": {"name": "Foo"}}


def test_encode_dictable():
    person = DictablePerson(name="Foo")
    pet = DictablePet(owner=person, name="Firulais")
    assert jsonable_encoder(pet) == {"name": "Firulais", "owner": {"name": "Foo"}}


def test_encode_unsupported():
    unserializable = Unserializable()
    with pytest.raises(ValueError):
        jsonable_encoder(unserializable)


def test_encode_custom_json_encoders_model():
    model = ModelWithCustomEncoder(dt_field=datetime(2019, 1, 1, 8))
    assert jsonable_encoder(model) == {"dt_field": "2019-01-01T08:00:00+00:00"}


def test_encode_model_with_config():
    model = ModelWithConfig(role=RoleEnum.admin)
    assert jsonable_encoder(model) == {"role": "admin"}


def test_encode_model_with_alias_raises():
    with pytest.raises(ValidationError):
        model = ModelWithAlias(foo="Bar")


def test_encode_model_with_alias():
    model = ModelWithAlias(Foo="Bar")
    assert jsonable_encoder(model) == {"Foo": "Bar"}

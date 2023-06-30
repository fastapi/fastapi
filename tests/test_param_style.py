from typing import Literal, Optional

from pydantic import BaseModel


class Dog(BaseModel):
    pet_type: Literal["dog"]
    name: str


class Matrjoschka(BaseModel):
    size: str = 0  # without type coecerion Query parameters are limited to str
    inner: Optional["Matrjoschka"] = None


# may be required …
try:
    import pydantic._internal._fields
    from pydantic_core import PydanticUndefined

    pydantic._internal._fields.Undefined = PydanticUndefined
    pydantic._internal._fields._UndefinedType = type(PydanticUndefined)
except:
    pass

from fastapi import FastAPI, Query

app = FastAPI()


@app.post(
    "/pet",
    operation_id="createPet",
)
def createPet(pet: Dog = Query(style="deepObject")) -> Dog:
    return pet


@app.post(
    "/toy",
    operation_id="createToy",
)
def createToy(toy: Matrjoschka = Query(style="deepObject")) -> Matrjoschka:
    return toy


from fastapi.testclient import TestClient

client = TestClient(app)


def test_pet():
    response = client.post("""/pet?pet[pet_type]=dog&pet[name]=doggy""")
    dog = Dog.model_validate(response.json())
    assert response.status_code == 200
    assert dog.pet_type == "dog" and dog.name == "doggy"


def test_matrjoschka():
    response = client.post(
        """/toy?toy[size]=3&toy[inner][size]=2&toy[inner][inner][size]=1'"""
    )
    print(response)
    toy = Matrjoschka.model_validate(response.json())
    assert response.status_code == 200
    assert toy
    assert toy.inner.size == "2"

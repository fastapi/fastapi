from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    hashed_password: str


class PetDB(BaseModel):
    name: str
    owner: UserDB


class PetOut(BaseModel):
    name: str
    owner: UserBase


@app.post("/users/", response_model=UserBase)
async def create_user(user: UserCreate):
    return user


@app.get("/pets/{pet_id}", response_model=PetOut)
async def read_pet(pet_id: int):
    user = UserDB(
        email="johndoe@example.com",
        hashed_password="secrethashed",
    )
    pet = PetDB(name="Nibbler", owner=user)
    return pet


@app.get("/pets/", response_model=List[PetOut])
async def read_pets():
    user = UserDB(
        email="johndoe@example.com",
        hashed_password="secrethashed",
    )
    pet1 = PetDB(name="Nibbler", owner=user)
    pet2 = PetDB(name="Zoidberg", owner=user)
    return [pet1, pet2]


client = TestClient(app)


def test_filter_top_level_model():
    response = client.post(
        "/users", json={"email": "johndoe@example.com", "password": "secret"}
    )
    assert response.json() == {"email": "johndoe@example.com"}


def test_filter_second_level_model():
    response = client.get("/pets/1")
    assert response.json() == {
        "name": "Nibbler",
        "owner": {"email": "johndoe@example.com"},
    }


def test_list_of_models():
    response = client.get("/pets/")
    assert response.json() == [
        {"name": "Nibbler", "owner": {"email": "johndoe@example.com"}},
        {"name": "Zoidberg", "owner": {"email": "johndoe@example.com"}},
    ]

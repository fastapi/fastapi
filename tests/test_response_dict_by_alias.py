from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class MockServiceModel(BaseModel):
    full_name: str = Field(alias="F_NAME")


class MockService:
    def __init__(self):
        self.initialized = True
        self.data = {"F_NAME": "Ilyas Q."}

    def get_data(self) -> MockServiceModel:
        return MockServiceModel(**self.data)


class ResponseSchema(BaseModel):
    full_name: str = Field(alias="fullName")

    class Config:
        allow_population_by_field_name = True


def get_mock_service():
    return MockService()


@app.get("/by-alias")
def by_alias(service: MockService = Depends(get_mock_service)):
    data = service.get_data()

    return data


@app.get("/by-field-name", response_model=ResponseSchema, response_dict_by_alias=False)
def by_field_name(service: MockService = Depends(get_mock_service)):
    data = service.get_data()

    return data


client = TestClient(app)


def test_response_dict_by_alias():
    response = client.get("/by-alias")
    assert response.status_code == 200, response.text
    assert response.json() == {"F_NAME": "Ilyas Q."}


def test_response_dict_by_field_name():
    response = client.get("/by-field-name")
    assert response.status_code == 200, response.text
    assert response.json() == {"fullName": "Ilyas Q."}

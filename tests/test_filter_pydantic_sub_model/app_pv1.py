import warnings
from typing import Optional

from fastapi import Depends, FastAPI
from pydantic.v1 import BaseModel, validator

app = FastAPI()


class ModelB(BaseModel):
    username: str


class ModelC(ModelB):
    password: str


class ModelA(BaseModel):
    name: str
    description: Optional[str] = None
    model_b: ModelB
    tags: dict[str, str] = {}

    @validator("name")
    def lower_username(cls, name: str, values):
        if not name.endswith("A"):
            raise ValueError("name must end in A")
        return name


async def get_model_c() -> ModelC:
    return ModelC(username="test-user", password="test-password")


with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")

    @app.get("/model/{name}", response_model=ModelA)
    async def get_model_a(name: str, model_c=Depends(get_model_c)):
        return {
            "name": name,
            "description": "model-a-desc",
            "model_b": model_c,
            "tags": {"key1": "value1", "key2": "value2"},
        }

from fastapi import FastAPI
from pydantic import BaseModel, Field


def test_duplicate_models():
    app = FastAPI()

    class Model(BaseModel):
        pass

    class Model2(BaseModel):
        a: Model

    class Model3(BaseModel):
        c: Model
        d: Model2

    @app.get("/", response_model=Model3)
    def f():
        pass  # pragma: no cover

    openapi = app.openapi()
    assert isinstance(openapi, dict)


def test_response_model_by_alias():
    app = FastAPI()

    class Model(BaseModel):
        name: str = Field(alias="alias")

    @app.get("/", response_model=Model, response_model_by_alias=False)
    def f():
        pass  # pragma: no cover

    openapi = app.openapi()
    assert "name" in openapi["components"]["schemas"]["Model"]["properties"]
    assert ["name"] == openapi["components"]["schemas"]["Model"]["required"]

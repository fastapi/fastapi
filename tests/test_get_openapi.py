from fastapi import FastAPI
from pydantic import BaseModel


def test_get_openapi():
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

from fastapi import FastAPI
from pydantic import BaseModel, Field


def test_enum_const_jsonschema_conversion():
    app = FastAPI()

    class Model(BaseModel):
        constant = Field("a", const=True)

    @app.get("/", response_model=Model)
    def f():
        pass  # pragma: no cover

    openapi = app.openapi()
    assert isinstance(openapi, dict)
    assert openapi["components"]["schemas"]["Model"]["properties"] == {
        "constant": {"title": "Constant", "type": "string", "enum": ["a"]}
    }

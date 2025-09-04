from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class MyModel(BaseModel):
    """
    A model with a form feed character in the title.
    \f
    Text after form feed character.
    """


@app.get("/foo")
def foo(v: MyModel):  # pragma: no cover
    pass


client = TestClient(app)


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()

    assert openapi_schema["components"]["schemas"]["MyModel"]["description"] == (
        "A model with a form feed character in the title.\n"
    )

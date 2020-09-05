from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Test(BaseModel):
    foo: str
    bar: str


class Test2(BaseModel):
    test: Test
    baz: str


app = FastAPI()


@app.get(
    "/",
    response_model=Test2,
    response_model_include={'baz': ..., 'test': {'foo'}},
    response_model_exclude={'test': {'bar'}}
)
def index():
    return Test2(test=Test(foo="visible field", bar="invisible field"), baz="also visible field")


client = TestClient(app)


def test_nested_model_include_exluce():
    resp = client.get("/")

    assert resp.status_code == 200, resp.text

    assert "baz" in resp.json(), resp.json()
    assert resp.json()["baz"] == "also visible field", resp.json()

    assert "test" in resp.json(), resp.json()
    assert resp.json()["test"]["foo"] == "visible field", resp.json()
    assert "bar" not in resp.json()["test"], resp.json()

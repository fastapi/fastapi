from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Model(BaseModel):
    name: str


@Depends
def get_model_data(model: Model):
    return model


@Depends
def dep_which_should_not_run(data: dict = get_model_data):
    assert isinstance(
        data, dict
    ), "This function was executed without resolving the dependencies!"
    return True


@app.post("/cached-errors/")
def cached_errors(data: dict = get_model_data, ran: bool = dep_which_should_not_run):
    raise AssertionError(
        f"Should have not reached this function, data: {data!r}, ran: {ran}"
    )


client = TestClient(app)


def test_caches_errors():
    response = client.post("/cached-errors/")
    assert response.json() == {
        "detail": [
            {
                "loc": ["body"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

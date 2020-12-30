from datetime import datetime

import orjson
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class ModelWithDatetimeField(BaseModel):
    dt_field: datetime


app = FastAPI()
model = ModelWithDatetimeField(dt_field=datetime(2019, 1, 1, 8))


@app.get("/model", response_model=ModelWithDatetimeField)
def get_model():
    return ORJSONResponse(model.dict())


@app.get("/model_with_option", response_model=ModelWithDatetimeField)
def get_model_with_option():
    return ORJSONResponse(model.dict(), option=orjson.OPT_NAIVE_UTC)


client = TestClient(app)


def test_dt():
    with client:
        response = client.get("/model")
        response_with_option = client.get("/model_with_option")

    assert response.json() == {"dt_field": "2019-01-01T08:00:00"}
    assert response_with_option.json() == {"dt_field": "2019-01-01T08:00:00+00:00"}

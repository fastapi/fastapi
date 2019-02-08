import json
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient


class ModelWithDatetimeField(BaseModel):
    dt_field: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


app = FastAPI()
model = ModelWithDatetimeField(dt_field=datetime.utcnow())


@app.get("/model", response_model=ModelWithDatetimeField)
def get_model():
    return model


client = TestClient(app)


def test_dt():
    with client:
        response = client.get("/model")
    assert json.loads(model.json()) == response.json()

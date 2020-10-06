from fastapi import FastAPI, Form
from pydantic import BaseModel
from starlette.testclient import TestClient


class Message(BaseModel):
    msg: str


app = FastAPI()


@app.post("/new_message", status_code=201)
def new_entry(message: Message = Form(...)):
    return message


client = TestClient(app)


def test_new_entry():
    new_message = Message(msg="Fast API is the best")
    resp = client.post("/new_message", data={"message": new_message.json()})

    assert resp.status_code == 201, resp.json()
    assert resp.json() == new_message.dict()


def test_new_entry_bad_data():
    resp = client.post("/new_message", data={"message": "{"})

    assert resp.status_code == 422, resp.json()

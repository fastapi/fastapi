from typing import Annotated, Optional

from fastapi import FastAPI, File, Form
from starlette.testclient import TestClient

app = FastAPI()


@app.post("/urlencoded")
async def post_url_encoded(age: Annotated[Optional[int], Form()] = None):
    return age


@app.post("/multipart")
async def post_multi_part(
    age: Annotated[Optional[int], Form()] = None,
    file: Annotated[Optional[bytes], File()] = None,
):
    return {"file": file, "age": age}


client = TestClient(app)


def test_form_default_url_encoded():
    response = client.post("/urlencoded", data={"age": ""})
    assert response.status_code == 200
    assert response.text == "null"


def test_form_default_multi_part():
    response = client.post("/multipart", data={"age": ""})
    assert response.status_code == 200
    assert response.json() == {"file": None, "age": None}

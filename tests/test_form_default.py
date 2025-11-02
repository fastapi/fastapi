from typing import Optional

from fastapi import FastAPI, File, Form
from starlette.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()
client = TestClient(app)


@app.post("/urlencoded")
async def post_url_encoded(age: Annotated[Optional[int], Form()] = None):
    return age


def test_form_default_url_encoded():
    response = client.post("/urlencoded", data={"age": ""})
    assert response.status_code == 200
    assert response.text == "null"


@app.post("/multipart")
async def post_multi_part(
    age: Annotated[Optional[int], Form()] = None,
    file: Annotated[Optional[bytes], File()] = None,
):
    assert file is None
    assert age is None


def test_form_default_multi_part():
    response = client.post("/multipart", data={"age": ""})
    assert response.status_code == 200

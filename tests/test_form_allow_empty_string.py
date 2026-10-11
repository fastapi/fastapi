from typing import Annotated

from fastapi import FastAPI, File, Form
from starlette.testclient import TestClient

app = FastAPI()


@app.post("/urlencoded")
async def post_url_encoded(
    name: Annotated[str, Form()], bio: Annotated[str | None, Form()]
):
    return {"name": name, "bio": bio}


@app.post("/urlencoded_plain")
async def post_url_encoded_plain(name: str = Form(), bio: str | None = Form()):
    return {"name": name, "bio": bio}


@app.post("/multipart")
async def post_multi_part(
    name: Annotated[str, Form()],
    bio: Annotated[str | None, Form()],
    file: Annotated[bytes | None, File()] = None,
):
    return {"file": file, "name": name, "bio": bio}


@app.post("/multipart_plain")
async def post_multi_part_plain(
    name: str = Form(),
    bio: str | None = Form(),
    file: bytes | None = File(None),
):
    return {"file": file, "name": name, "bio": bio}


client = TestClient(app)


def test_form_urlencode_empty_strings():
    response = client.post("/urlencoded", data={"name": "", "bio": ""})
    assert response.status_code == 200
    assert response.text == '{"name":"","bio":""}'


def test_form_urlencode_empty_string_or_none_required_no_default():
    response = client.post("/urlencoded", data={"name": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","bio"],"msg":"Field required","input":null}]}'
    )
    assert "Field required" in response.text


def test_form_urlencode_string_required_no_default():
    response = client.post("/urlencoded", data={"bio": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":null}]}'
    )


def test_form_urlencode_plain_empty_strings():
    response = client.post("/urlencoded_plain", data={"name": "", "bio": ""})
    assert response.status_code == 200
    assert response.text == '{"name":"","bio":""}'


def test_form_urlencode_plain_empty_string_or_none_required_no_default():
    response = client.post("/urlencoded_plain", data={"name": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","bio"],"msg":"Field required","input":null}]}'
    )
    assert "Field required" in response.text


def test_form_urlencode_plain_string_required_no_default():
    response = client.post("/urlencoded_plain", data={"bio": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":null}]}'
    )


def test_form_multipart_empty_strings():
    response = client.post("/multipart", data={"name": "", "bio": ""})
    assert response.status_code == 200
    assert response.text == '{"file":null,"name":"","bio":""}'


def test_form_multipart_empty_string_or_none_required_no_default():
    response = client.post("/multipart", data={"name": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","bio"],"msg":"Field required","input":null}]}'
    )
    assert "Field required" in response.text


def test_form_multipart_string_required_no_default():
    response = client.post("/multipart", data={"bio": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":null}]}'
    )


def test_form_multipart_plain_empty_strings():
    response = client.post("/multipart_plain", data={"name": "", "bio": ""})
    assert response.status_code == 200
    assert response.text == '{"file":null,"name":"","bio":""}'


def test_form_multipart_plain_empty_string_or_none_required_no_default():
    response = client.post("/multipart_plain", data={"name": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","bio"],"msg":"Field required","input":null}]}'
    )
    assert "Field required" in response.text


def test_form_multipart_plain_string_required_no_default():
    response = client.post("/multipart_plain", data={"bio": ""})
    assert response.status_code == 422
    assert (
        response.text
        == '{"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":null}]}'
    )

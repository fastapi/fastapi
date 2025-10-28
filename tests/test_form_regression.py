from typing import Optional

import pytest
from fastapi import FastAPI, File, Form
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.post("/")
def root(
    file: Annotated[Optional[bytes], File()] = None,
    form: Annotated[Optional[str], Form(embed=True)] = None,
):
    return {"file": file, "form": form}


client = TestClient(app)


@pytest.mark.parametrize(
    "file_data, form_data, expected_response",
    [
        (None, None, {"file": None, "form": None}),
        ("", None, {"file": None, "form": None}),
        (None, "", {"file": None, "form": None}),
        ("", "", {"file": None, "form": None}),
        ("file", "form", {"file": "file", "form": "form"}),
    ],
)
def test_empty_string_to_none(file_data, form_data, expected_response):
    data = {}
    if file_data is not None:
        data["file"] = file_data
    if form_data is not None:
        data["form"] = form_data

    response = client.post("/", data=data)
    assert response.status_code == 200
    assert response.json() == expected_response

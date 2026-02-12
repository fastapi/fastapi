"""
Regression test, Error 422 if Form is declared before File
See https://github.com/tiangolo/fastapi/discussions/9116
"""

from pathlib import Path
from typing import Annotated

import pytest
from fastapi import FastAPI, File, Form
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/file_before_form")
def file_before_form(
    file: bytes = File(),
    city: str = Form(),
):
    return {"file_content": file, "city": city}


@app.post("/file_after_form")
def file_after_form(
    city: str = Form(),
    file: bytes = File(),
):
    return {"file_content": file, "city": city}


@app.post("/file_list_before_form")
def file_list_before_form(
    files: Annotated[list[bytes], File()],
    city: Annotated[str, Form()],
):
    return {"file_contents": files, "city": city}


@app.post("/file_list_after_form")
def file_list_after_form(
    city: Annotated[str, Form()],
    files: Annotated[list[bytes], File()],
):
    return {"file_contents": files, "city": city}


client = TestClient(app)


@pytest.fixture
def tmp_file_1(tmp_path: Path) -> Path:
    f = tmp_path / "example1.txt"
    f.write_text("foo")
    return f


@pytest.fixture
def tmp_file_2(tmp_path: Path) -> Path:
    f = tmp_path / "example2.txt"
    f.write_text("bar")
    return f


@pytest.mark.parametrize("endpoint_path", ("/file_before_form", "/file_after_form"))
def test_file_form_order(endpoint_path: str, tmp_file_1: Path):
    response = client.post(
        url=endpoint_path,
        data={"city": "Thimphou"},
        files={"file": (tmp_file_1.name, tmp_file_1.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_content": "foo", "city": "Thimphou"}


@pytest.mark.parametrize(
    "endpoint_path", ("/file_list_before_form", "/file_list_after_form")
)
def test_file_list_form_order(endpoint_path: str, tmp_file_1: Path, tmp_file_2: Path):
    response = client.post(
        url=endpoint_path,
        data={"city": "Thimphou"},
        files=(
            ("files", (tmp_file_1.name, tmp_file_1.read_bytes())),
            ("files", (tmp_file_2.name, tmp_file_2.read_bytes())),
        ),
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_contents": ["foo", "bar"], "city": "Thimphou"}

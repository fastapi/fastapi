from typing import List

from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/route-with-default-limit")
def files_low(files: List[UploadFile]):
    return files  # pragma: nocover


@app.post("/route-with-custom-limit", max_files=2000)
def files_high(files: List[UploadFile]):
    return files  # pragma: nocover


client = TestClient(app)


def test_max_files_setting_default():
    # Test Starlette default remains in place
    files = [("files", ("foo.txt", "foo"))] * 1500
    response = client.post("/route-with-default-limit", files=files)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Too many files. Maximum number of files is 1000."
    }


def test_max_files_setting_custom():
    # Test Starlette setting can be configured
    files = [("files", ("foo.txt", "foo"))] * 1500
    response = client.post("/route-with-custom-limit", files=files)
    assert response.status_code == 200

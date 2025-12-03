from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/", form_max_files=2, form_max_part_size=1024, form_max_fields=2)
async def upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


def test_form_max_files_send_one():
    client = TestClient(app)

    response = client.post(
        "/",
        files=[
            ("files", ("file1.txt", b"file1 content", "text/plain")),
        ],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"filenames": ["file1.txt"]}


def test_form_max_files_send_too_many():
    client = TestClient(app)

    response = client.post(
        "/",
        files=[
            ("files", ("file1.txt", b"file1 content", "text/plain")),
            ("files", ("file2.txt", b"file2 content", "text/plain")),
            ("files", ("file3.txt", b"file3 content", "text/plain")),
        ],
    )

    assert response.status_code == 400, response.text
    assert response.json() == {
        "detail": "Too many files. Maximum number of files is 2."
    }


def test_max_part_size_exceeds_custom_limit():
    client = TestClient(app)

    boundary = "------------------------4K1ON9fZkj9uCUmqLHRbbR"

    multipart_data = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="small"\r\n\r\n'
        "small content\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="large"\r\n\r\n'
        + ("x" * 1024 * 10 + "x")  # 1MB + 1 byte of data
        + "\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Transfer-Encoding": "chunked",
    }

    response = client.post("/", content=multipart_data, headers=headers)
    assert response.status_code == 400
    assert response.text == '{"detail":"Part exceeded maximum size of 1KB."}'


def test_form_max_fields_exceeds_limit():
    client = TestClient(app)

    response = client.post(
        "/",
        files=[("files", ("file1.txt", b"file1 content", "text/plain"))],
        data={
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
            "field4": "value4",
        },
    )

    assert response.status_code == 400, response.text
    assert response.json() == {
        "detail": "Too many fields. Maximum number of fields is 2."
    }

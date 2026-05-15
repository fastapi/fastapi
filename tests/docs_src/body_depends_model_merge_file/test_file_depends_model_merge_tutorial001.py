import pytest
from fastapi import status

from tests.docs_src._loader import docs_src_test_client


@pytest.fixture(scope="module")
def client():
    return docs_src_test_client(
        "docs_src_body_depends_model_merge_file_tutorial001",
        "body_depends_model_merge_file",
        "tutorial001_an_py310.py",
    )


@pytest.mark.parametrize(
    ("path", "form_fields", "file_name", "file_bytes", "file_ct"),
    [
        pytest.param(
            "/files/attachments/commented/",
            {"comment": "Spec"},
            "doc.pdf",
            b"%PDF-1.4\n",
            "application/pdf",
            id="commented",
        ),
        pytest.param(
            "/files/attachments/named/",
            {"name": "My text file"},
            "file.txt",
            b"hello",
            "text/plain",
            id="named",
        ),
    ],
)
def test_file_depends_model_merge(
    client,
    path,
    form_fields,
    file_name,
    file_bytes,
    file_ct,
):
    upload = (file_name, file_bytes, file_ct)
    response = client.post(path, data=form_fields, files={"file": upload})
    assert response.status_code == status.HTTP_200_OK, response.text
    expected = {
        "filename": file_name,
        "content_type": file_ct,
        "data": form_fields,
    }
    assert response.json() == expected

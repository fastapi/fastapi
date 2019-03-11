import pytest
from fastapi import UploadFile


def test_upload_file_invalid():
    with pytest.raises(ValueError):
        UploadFile.validate("not a Starlette UploadFile")
